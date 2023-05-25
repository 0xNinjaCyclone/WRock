
#include "crawler.h"

static int Crawler_traverse(Crawler *self, visitproc visit, void *arg)
{
    Py_VISIT(self->url);
    Py_VISIT(self->threads);
    Py_VISIT(self->depth);
    Py_VISIT(self->subsInScope);
    Py_VISIT(self->insecure);
    Py_VISIT(self->rawHeaders);
    Py_VISIT(self->sc);
    Py_VISIT(self->noOutOfScope);
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
    Py_CLEAR(self->sc);
    Py_CLEAR(self->noOutOfScope);
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
            (self->threads = PyLong_FromLong(5)) &&
            (self->depth = PyLong_FromLong(2)) &&
            (self->subsInScope = PyBool_FromLong(0)) &&
            (self->insecure = PyBool_FromLong(0)) &&
            (self->rawHeaders = PyUnicode_FromString("")) &&
            (self->sc = PyBool_FromLong(0)) &&
            (self->noOutOfScope = PyBool_FromLong(0))
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
    static char *kwlist[] = { "url", "threads", "depth", "subsInScope", "insecure", "rawHeaders", "sc", "noOutOfScope", NULL };
    PyObject *url, *threads, *depth, *subsInScope, *insecure, *rawHeaders, *sc, *noOutOfScope, *tmp;
    int nThreads,nDepth, nSubsInScope, nInsecure, nSc, nNoOutOfScope;

    url = rawHeaders = NULL;
    nThreads = nDepth = nSubsInScope = nInsecure = nSc = nNoOutOfScope = 0;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|UiiiiUii", 
                                    kwlist, &url, &nThreads, &nDepth, &nSubsInScope, &nInsecure, &rawHeaders, &nSc, &nNoOutOfScope))
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

    if (nSc) {
        sc = PyBool_FromLong(nSc);
        tmp = self->sc;
        Py_INCREF(sc);
        self->sc = sc;
        Py_DECREF(tmp);
    }

    if (nNoOutOfScope) {
        noOutOfScope = PyBool_FromLong(nNoOutOfScope);
        tmp = self->noOutOfScope;
        Py_INCREF(noOutOfScope);
        self->noOutOfScope = noOutOfScope;
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

static int CrawlerResult_traverse(CrawlerResult *self, visitproc visit, void *arg)
{
    Py_VISIT(self->endpoints);
    Py_VISIT(self->jsFiles);
    Py_VISIT(self->emails);
    return 0;
}

static int CrawlerResult_clear(CrawlerResult *self)
{
    Py_CLEAR(self->endpoints);
    Py_CLEAR(self->jsFiles);
    Py_CLEAR(self->emails);
    return 0;
}

static PyObject *CrawlerResult_new(PyTypeObject *type, PyObject *args, PyObject *kwds) 
{
    CrawlerResult *self;

    /* Allocate memory for our class */
    self = (CrawlerResult *) type->tp_alloc(type, 0);

    if (self) {
        /* initialize our attributes */
        if(!(
            (self->endpoints = PyList_New(0)) &&
            (self->jsFiles = PyList_New(0)) &&
            (self->emails = PyList_New(0)) 
        ))
        {
            /* initialization failed */

            Py_DECREF(self);
            return NULL;
        }

    }

    return (PyObject *) self;
}

static void CrawlerResult_dealloc(CrawlerResult *self)
{
    PyObject_GC_UnTrack(self);
    CrawlerResult_clear(self);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static int Crawler_SetUrl(Crawler *self, PyObject *value, void *closure) 
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the url attribute");
        return -1;
    }

    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The url attribute value must be a string");
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
        PyErr_SetString(PyExc_TypeError, "Cannot delete the threads attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The threads attribute value must be an int");
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
        PyErr_SetString(PyExc_TypeError, "Cannot delete the depth attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The depth attribute value must be an int");
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
        PyErr_SetString(PyExc_TypeError, "Cannot delete the subsInScope attribute");
        return -1;
    }

    if (!PyBool_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The subsInScope attribute value must be an boolean");
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
        PyErr_SetString(PyExc_TypeError, "Cannot delete the insecure attribute");
        return -1;
    }

    if (!PyBool_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The insecure attribute value must be an boolean");
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
        PyErr_SetString(PyExc_TypeError, "Cannot delete the rawHeaders attribute");
        return -1;
    }

    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The rawHeaders attribute value must be a string");
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

static int CrawlerResult_SetEndPointsAttr(CrawlerResult *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the endpoints attribute");
        return -1;
    }

    if (!PyList_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The endpoints attribute value must be a list");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->endpoints);
    self->endpoints = value;
    return 0;
}

static PyObject *CrawlerResult_GetEndPointsAttr(CrawlerResult *self, void *closure)
{
    Py_INCREF(self->endpoints);
    return self->endpoints;
}

static int CrawlerResult_SetJsFilesAttr(CrawlerResult *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the jsFiles attribute");
        return -1;
    }

    if (!PyList_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The jsFiles attribute value must be a list");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->jsFiles);
    self->jsFiles = value;
    return 0;
}

static PyObject *CrawlerResult_GetJsFilesAttr(CrawlerResult *self, void *closure)
{
    Py_INCREF(self->jsFiles);
    return self->jsFiles;
}

static int CrawlerResult_SetEmailsAttr(CrawlerResult *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the emails attribute");
        return -1;
    }

    if (!PyList_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The emails attribute value must be a list");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->emails);
    self->emails = value;
    return 0;
}

static PyObject *CrawlerResult_GetEmailsAttr(CrawlerResult *self, void *closure)
{
    Py_INCREF(self->emails);
    return self->emails;
}

static PyObject *CrawlerResult_GetEndPoints(CrawlerResult *self, PyObject *Py_UNUSED(ignored)) 
{
    Py_INCREF(self->endpoints);
    return self->endpoints;
}

static PyObject *CrawlerResult_GetJsFiles(CrawlerResult *self, PyObject *Py_UNUSED(ignored)) 
{
    Py_INCREF(self->jsFiles);
    return self->jsFiles;
}

static PyObject *CrawlerResult_GetEmails(CrawlerResult *self, PyObject *Py_UNUSED(ignored)) 
{
    Py_INCREF(self->emails);
    return self->emails;
}

static PyObject *StoreParameterResult(Parameter **params)
{
    /* a list of params */
    PyObject *pParamList; 

    /* a dict of param */
    PyObject *pParam;

    /* Initialize the params list */
    if (!(pParamList = PyList_New(0)))
    {
        PyErr_SetString(PyExc_Exception, "an error occured when initializing the params list");
        return NULL;
    }

    for (; *params; params++)
    {
        /* Initialize the parameter dict */
        if (!(pParam = PyDict_New()))
        {
            PyErr_SetString(PyExc_Exception, "an error occured when initializing the parameter data dict");
            return NULL;
        }

        /* Insert parameter name to the dict */
        PyDict_SetItemString(pParam, "name", PyUnicode_FromString( ( *params )->name ));

        /* Insert parameter value to the dict */
        PyDict_SetItemString(pParam, "value", PyUnicode_FromString( ( *params )->value ));

        /* Insert parameter type to the dict */
        PyDict_SetItemString(pParam, "p_type", PyUnicode_FromString( ( *params )->p_type ));

        /* Insert the parameter dict to the parameter list */
        PyList_Append(pParamList, pParam);
    }

    return pParamList;
}

static PyObject *StoreEndPointsResult(EndPoint **endpoints)
{
    /* a list of endpoints */
    PyObject *pDataList; 

    /* a dict of endpoint */
    PyObject *pData;

    /* Initialize the endpoints list */
    if (!(pDataList = PyList_New(0)))
    {
        PyErr_SetString(PyExc_Exception, "an error occured when initializing the endpoints list");
        return NULL;
    }

    for (; *endpoints; endpoints++)
    {
        /* Initialize the endpoints dict */
        if (!(pData = PyDict_New()))
        {
            PyErr_SetString(PyExc_Exception, "an error occured when initializing the endpoint dict");
            return NULL;
        }

        /* Insert url to the endpoint dict */
        PyDict_SetItemString(pData, "url", PyUnicode_FromString( ( *endpoints )->url ));

        /* Insert status code to the endpoint dict */
        PyDict_SetItemString(pData, "status_code", PyLong_FromLong( ( *endpoints )->nStatusCode ));

        /* Insert inScope flag to the endpoint dict */
        PyDict_SetItemString(pData, "in_scope", PyBool_FromLong( ( *endpoints )->bInScope ));

        /* Insert method type to the endpoint dict */
        PyDict_SetItemString(pData, "m_type", PyUnicode_FromString( ( *endpoints )->m_type ));

        /* Insert the parameter list to the dict */
        PyDict_SetItemString(pData, "params", StoreParameterResult( ( *endpoints )->params ));

        /* Insert the endpoint dict to the endpoints list */
        PyList_Append(pDataList, pData);
    }

    return pDataList;
    
}

static PyObject *StoreCrawlerResult(RockRawlerResult *result)
{
    /* Create a python instance of CrawlerResult class */
    PyObject *pResult = PyObject_CallObject((PyObject *)&CrawlerResultType, NULL);

    PyObject_SetAttrString(pResult, "endpoints", StoreEndPointsResult(result->endpoints));
    PyObject_SetAttrString(pResult, "jsFiles", StoreResults(result->jsFiles));
    PyObject_SetAttrString(pResult, "emails", StoreResults(result->emails));

    return pResult;
}

static void FreeCrawlerResult(RockRawlerResult *result)
{
    FreeMemory(result->jsFiles);
    FreeMemory(result->emails);

    for (EndPoint **e = result->endpoints; *e; e++)
    {
        for (Parameter **p = ( *e )->params; *p; p++)
        {
            PyMem_Free( ( *p )->name );
            PyMem_Free( ( *p )->value );
            PyMem_Free( ( *p )->p_type );
            PyMem_Free( *p );
        }

        PyMem_Free( ( *e )->url );
        PyMem_Free( ( *e )->m_type );
        PyMem_Free( ( *e )->params );
        PyMem_Free( *e );
    }

    PyMem_Free(result->endpoints);
    PyMem_Free(result);
}

static PyObject *Crawler_Start(Crawler *self, PyObject *Py_UNUSED(ignored)) {

    /* RockRawler results */
    RockRawlerResult *result;

    /* CrawlerResult */
    PyObject *pResult; 

    /* Start Crawler */
    result = CStartCrawler(
            BuildGoStr(self->url), 
            (GoInt) PyLong_AsLong(self->threads), 
            (GoInt) PyLong_AsLong(self->depth), 
            (GoUint8) PyLong_AsLong(self->subsInScope), 
            (GoUint8) PyLong_AsLong(self->insecure), 
            BuildGoStr(self->rawHeaders),
            (GoUint8) PyLong_AsLong(self->sc),
            (GoUint8) PyLong_AsLong(self->noOutOfScope)
    );

    /* returns CrawlerResult object */
    pResult = StoreCrawlerResult(result);
    
    /* Free memory */
    FreeCrawlerResult(result);

    return pResult; 
}

PyMODINIT_FUNC PyInit_rockrawler(void)
{
    PyObject *m;
    
    if (PyType_Ready(&CrawlerType) < 0)
        return NULL;

    if (PyType_Ready(&CrawlerResultType) < 0)
        return NULL;

    if (!(m = PyModule_Create(&rockrawlermodule)))
        return NULL;

    Py_INCREF(&CrawlerType);
    Py_INCREF(&CrawlerResultType);

    if (
        PyModule_AddObject(m, "Crawler", (PyObject *) &CrawlerType) < 0 ||
        PyModule_AddObject(m, "CrawlerResult", (PyObject *) &CrawlerResultType) < 0
    ) {
        Py_DECREF(&CrawlerType);
        Py_DECREF(&CrawlerResultType);
        Py_DECREF(&m);
        return NULL;
    }

    return m;
}