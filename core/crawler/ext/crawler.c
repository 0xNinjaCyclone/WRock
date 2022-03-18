
#include "crawler.h"

static int Crawler_traverse(Crawler *self, visitproc visit, void *arg)
{
    Py_VISIT(self->url);
    Py_VISIT(self->threads);
    Py_VISIT(self->depth);
    Py_VISIT(self->subsInScope);
    Py_VISIT(self->insecure);
    Py_VISIT(self->rawHeaders);
    return 0;
}

static int Crawler_clear(Crawler *self)
{
    Py_CLEAR(self->url);
    Py_CLEAR(self->threads);
    Py_CLEAR(self->depth);
    Py_CLEAR(self->subsInScope);
    Py_CLEAR(self->insecure);
    Py_CLEAR(self->rawHeaders);
    return 0;
}

static PyObject *Crawler_new(PyTypeObject *type, PyObject *args, PyObject *kwds) 
{
    Crawler *self;

    /* Allocate memory for our class */
    self = (Crawler *) type->tp_alloc(type, 0);

    if (self) {
        /* initialize our attributes */
        if(!(
            (self->url = PyUnicode_FromString("")) && 
            (self->threads = PyLong_FromLong(0)) &&
            (self->depth = PyLong_FromLong(0)) &&
            (self->subsInScope = Py_False) &&
            (self->insecure = Py_False) &&
            (self->rawHeaders = PyUnicode_FromString(""))
        ))
        {
            /* initialization failed */

            Py_DECREF(self);
            return NULL;
        }

    }

    return (PyObject *) self;
}

static int Crawler_init(Crawler *self, PyObject *args, PyObject* kwds)
{
    static char *kwlist[] = { "url", "threads", "depth", "subsInScope", "insecure", "rawHeaders", NULL };
    PyObject *url, *threads, *depth, *subsInScope, *insecure, *rawHeaders, *tmp;
    int nThreads,nDepth, nSubsInScope, nInsecure;

    url = rawHeaders = NULL;
    nThreads = nDepth = nSubsInScope = nInsecure = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|UiiiiU", 
                                    kwlist, &url, &nThreads, &nDepth, &nSubsInScope, &nInsecure, &rawHeaders))
    {
        return -1;
    }

    if (url) {
        tmp = self->url;
        Py_INCREF(url);
        self->url = url;
        Py_DECREF(tmp);
    }

    if (nThreads) {
        threads = PyLong_FromLong(nThreads);
        tmp = self->threads;
        Py_INCREF(threads);
        self->threads = threads;
        Py_DECREF(tmp);
    }

    if (nDepth) {
        depth = PyLong_FromLong(nDepth);
        tmp = self->depth;
        Py_INCREF(depth);
        self->depth = depth;
        Py_DECREF(tmp);
    }

    if (nSubsInScope) {
        subsInScope = PyBool_FromLong(nSubsInScope);
        tmp = self->subsInScope;
        Py_INCREF(subsInScope);
        self->subsInScope = subsInScope;
        Py_DECREF(tmp);
    }

    if (nInsecure) {
        insecure = PyBool_FromLong(nInsecure);
        tmp = self->insecure;
        Py_INCREF(insecure);
        self->insecure = insecure;
        Py_DECREF(tmp);
    }

    if (rawHeaders) {
        tmp = self->rawHeaders;
        Py_INCREF(rawHeaders);
        self->rawHeaders = rawHeaders;
        Py_DECREF(tmp);
    }

    return 0;
}

static void Crawler_dealloc(Crawler *self)
{
    PyObject_GC_UnTrack(self);
    Crawler_clear(self);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

GoString BuildGoStr(PyObject *str)
{
    GoString GoStr;
    GoStr.p = PyUnicode_AsUTF8(str);
    GoStr.n = PyUnicode_GET_LENGTH(str);
    return GoStr;
}

static int Crawler_SetUrl(Crawler *self, PyObject *value, void *closure) 
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the first attribute");
        return -1;
    }

    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The first attribute value must be a string");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->url);
    self->url = value;
    return 0;
}


static PyObject *Crawler_GetUrl(Crawler *self, void *closure) 
{
    Py_INCREF(self->url);
    return self->url;
}

static int Crawler_SetThreads(Crawler *self, PyObject *value, void *closure) 
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the first attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The first attribute value must be an int");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->threads);
    self->threads = value;
    return 0;
}


static PyObject *Crawler_GetThreads(Crawler *self, void *closure) 
{
    Py_INCREF(self->threads);
    return self->threads;
}

static int Crawler_SetDepth(Crawler *self, PyObject *value, void *closure) 
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the first attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The first attribute value must be an int");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->depth);
    self->depth = value;
    return 0;
}


static PyObject *Crawler_GetDepth(Crawler *self, void *closure) 
{
    Py_INCREF(self->depth);
    return self->depth;
}

static int Crawler_SetSubsInScope(Crawler *self, PyObject *value, void *closure) 
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the first attribute");
        return -1;
    }

    if (!PyBool_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The first attribute value must be an boolean");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->subsInScope);
    self->subsInScope = value;
    return 0;
}


static PyObject *Crawler_GetSubsInScope(Crawler *self, void *closure) 
{
    Py_INCREF(self->subsInScope);
    return self->subsInScope;
}

static int Crawler_SetInsecure(Crawler *self, PyObject *value, void *closure) 
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the first attribute");
        return -1;
    }

    if (!PyBool_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The first attribute value must be an boolean");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->insecure);
    self->insecure = value;
    return 0;
}

static PyObject *Crawler_GetInsecure(Crawler *self, void *closure) 
{
    Py_INCREF(self->insecure);
    return self->insecure;
}


static int Crawler_SetRawHeaders(Crawler *self, PyObject *value, void *closure) 
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the first attribute");
        return -1;
    }

    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The first attribute value must be a string");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->rawHeaders);
    self->rawHeaders = value;
    return 0;
}


static PyObject *Crawler_GetRawHeaders(Crawler *self, void *closure) 
{
    Py_INCREF(self->rawHeaders);
    return self->rawHeaders;
}

void freeAllocatedMemory(char **ptr) {
    for (char **temp = ptr; *temp; temp++)
    {
        /* Free each item of the array */
        PyMem_Free(*temp);
    }

    PyMem_Free(ptr);
}

PyObject *StoreResults(char **results) 
{
    /* declare a python list */
    PyObject *pyresult; 

    /* initialize the list and except error if init failed */
    if (!(pyresult = PyList_New(0))) {
        PyErr_SetString(PyExc_Exception, "an error occured when initializing the list");
        return NULL;
    } 

    /* put all results in python list */
    for (; *results; results++)
    {
        if(PyList_Append(pyresult, PyUnicode_FromString(*results)) != 0)
        {
            PyErr_SetString(PyExc_Exception, "Error occured when append results to the list");
            return NULL;
        }
    }

    return pyresult;
}

static PyObject *Crawler_Start(Crawler *self, PyObject *Py_UNUSED(ignored)) {

    /* RockRawler results */
    char **results;

    /* declare a python list */
    PyObject *pyresult = NULL; 

    /* Start Crawler */
    results = CStartCrawler(
            BuildGoStr(self->url), 
            (GoInt) PyLong_AsLong(self->threads), 
            (GoInt) PyLong_AsLong(self->depth), 
            (GoUint8) PyLong_AsLong(self->subsInScope), 
            (GoUint8) PyLong_AsLong(self->insecure), 
            BuildGoStr(self->rawHeaders)
    );

    /* Store data in a python list */
    pyresult = StoreResults(results);
    
    /* Free memory */
    freeAllocatedMemory(results);

    return pyresult; 
}

PyMODINIT_FUNC PyInit_rockrawler(void)
{
    PyObject *m;
    
    if (PyType_Ready(&CrawlerType) < 0)
        return NULL;

    m = PyModule_Create(&rockrawlermodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&CrawlerType);
    PyModule_AddObject(m, "Crawler", (PyObject *) &CrawlerType);
    return m;
}