
#include "Subfinder.h"

static int SubFinder_traverse(SubFinder *self, visitproc visit, void *arg)
{
    Py_VISIT(self->domain);
    Py_VISIT(self->threads);
    Py_VISIT(self->timeout);
    Py_VISIT(self->maxEnumerationTime);
    return 0;
}

static int SubFinder_clear(SubFinder *self)
{
    Py_CLEAR(self->domain);
    Py_CLEAR(self->threads);
    Py_CLEAR(self->timeout);
    Py_CLEAR(self->maxEnumerationTime);
    return 0;
}

static PyObject *SubFinder_new(PyTypeObject *type, PyObject *args, PyObject *kwds) 
{
    SubFinder *self;

    /* Allocate memory for our class */
    self = (SubFinder *) type->tp_alloc(type, 0);

    if (self) {
        /* initialize our attributes */
        if(!(
            (self->domain = PyUnicode_FromString("")) && 
            (self->threads = PyLong_FromLong(5)) &&
            (self->timeout = PyLong_FromLong(30)) &&
            (self->maxEnumerationTime = PyLong_FromLong(10))
        ))
        {
            /* initialization failed */

            Py_DECREF(self);
            return NULL;
        }

    }

    return (PyObject *) self;
}

static int SubFinder_init(SubFinder *self, PyObject *args, PyObject* kwds)
{
    static char *kwlist[] = { "url", "threads", "timeout", "maxEnumerationTime", "recursive", "all", NULL };
    PyObject *domain, *threads, *timeout, *maxEnumerationTime, *tmp;
    int nThreads, nTimeout, nMaxEnumerationTime, nRecursive, nAll;

    /* Initiate attrs */
    domain = NULL;
    nThreads = nTimeout = nMaxEnumerationTime = 0;

    /* Initialize subfinder */
    SubFinderInit();

    /* Get attrs from python */
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|Uiiiii", 
                                    kwlist, &domain, &nThreads, &nTimeout, &nMaxEnumerationTime, &nRecursive, &nAll))
    {
        return -1;
    }

    if (domain) {
        tmp = self->domain;
        Py_INCREF(domain);
        self->domain = domain;
        Py_DECREF(tmp);
    }

    if (nThreads) {
        threads = PyLong_FromLong(nThreads);
        tmp = self->threads;
        Py_INCREF(threads);
        self->threads = threads;
        Py_DECREF(tmp);
    }

    if (nTimeout) {
        timeout = PyLong_FromLong(nTimeout);
        tmp = self->timeout;
        Py_INCREF(timeout);
        self->timeout = timeout;
        Py_DECREF(tmp);
    }

    if (nMaxEnumerationTime) {
        maxEnumerationTime = PyLong_FromLong(nMaxEnumerationTime);
        tmp = self->maxEnumerationTime;
        Py_INCREF(maxEnumerationTime);
        self->maxEnumerationTime = maxEnumerationTime;
        Py_DECREF(tmp);
    }

    if (nRecursive) {
        if (PyBool_FromLong(nRecursive) == Py_True)
            SubFinderUseRecursive();
    }

    if (nAll) {
        if (PyBool_FromLong(nAll) == Py_True)
            SubFinderUseAll();
    }

    return 0;
}

static void SubFinder_dealloc(SubFinder *self)
{
    PyObject_GC_UnTrack(self);
    SubFinder_clear(self);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static int SubFinder_SetDomain(SubFinder *self, PyObject *value, void *closure) 
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
    Py_CLEAR(self->domain);
    self->domain = value;
    return 0;
}


static PyObject *SubFinder_GetDomain(SubFinder *self, void *closure) 
{
    Py_INCREF(self->domain);
    return self->domain;
}

static int SubFinder_SetThreads(SubFinder *self, PyObject *value, void *closure) 
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


static PyObject *SubFinder_GetThreads(SubFinder *self, void *closure) 
{
    Py_INCREF(self->threads);
    return self->threads;
}

static int SubFinder_SetTimeout(SubFinder *self, PyObject *value, void *closure) 
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
    Py_CLEAR(self->timeout);
    self->timeout = value;
    return 0;
}


static PyObject *SubFinder_GetTimeout(SubFinder *self, void *closure) 
{
    Py_INCREF(self->timeout);
    return self->timeout;
}

static int SubFinder_SetMaxEnumerationTime(SubFinder *self, PyObject *value, void *closure) 
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
    Py_CLEAR(self->maxEnumerationTime);
    self->maxEnumerationTime = value;
    return 0;
}


static PyObject *SubFinder_GetMaxEnumerationTime(SubFinder *self, void *closure) 
{
    Py_INCREF(self->maxEnumerationTime);
    return self->maxEnumerationTime;
}

static PyObject *SubFinder_UseAll(SubFinder *self, PyObject *Py_UNUSED(ignored)) {
    SubFinderUseAll();
    Py_RETURN_NONE;
}

static PyObject *SubFinder_UseRecursive(SubFinder *self, PyObject *Py_UNUSED(ignored)) {
    SubFinderUseRecursive();
    Py_RETURN_NONE;
}

static PyObject *SubFinder_SetProperty(SubFinder *self, PyObject *args) {

    /* Property name and its value */
    PyObject *propname = NULL, *propval = NULL, *listItemVal = NULL;
    char **property;
    size_t nSize, nStrSize;

    /* Parse arguments */
    if(!PyArg_ParseTuple(args, "|UO", &propname, &propval)) {
        return NULL;
    }

    /* Check if required params passed or not */
    if (!(propname && propval)) {
        PyErr_SetString(PyExc_TypeError,
                        "this method takes exactly two arguments");
        return NULL;
    }

    /* Check if the object passed is a List */
    if(!PyList_Check(propval)) {
        PyErr_SetString(PyExc_TypeError,
                        "The properity must be a list");
        return NULL;
    }

    /* Size of the property list */
    nSize = PyList_Size(propval);

    /* Allocate memory for property values that will pass to SubFinder API */
    if (!(property = (char **) PyMem_Malloc(sizeof(*property) * (nSize + 1)))) { /* add one for terminator */
        PyErr_SetString(PyExc_Exception, "Out Of Memory");
        return NULL;
    }

    for (size_t i = 0; i < nSize; i++)
    {
        /* Get list item by index */
        listItemVal = PyList_GetItem(propval, i);

        /* Check if the list item not a string */
        if (!PyUnicode_Check(listItemVal)) {
            PyErr_SetString(PyExc_TypeError,
                        "The properity value must be a string");
            return NULL;
        }

        /* Property name size */
        nStrSize = PyUnicode_GET_LENGTH(listItemVal);

        /* Allocate memory space for the array item */
        if (!(property[i] = (char *) PyMem_Malloc(nStrSize + 1))) { /* add one for nul */
            PyErr_SetString(PyExc_Exception, "Out Of Memory");
            return NULL;
        }

        /* Copy N bytes from memory to allocated space */
        memcpy(property[i], PyUnicode_AsUTF8(listItemVal), nStrSize);

        /* Nul-terminator */
        property[i][nStrSize] = 0;
    }

    /* Terminator */
    property[nSize] = NULL;
    
    /* Set Property using SubFinder API */
    SubFinderSetProperty(BuildGoStr(propname), property, (GoInt) nSize);

    /* Free memory */
    FreeMemory(property);

    Py_RETURN_NONE;
}

static PyObject *SubFinder_GetProperty(SubFinder *self, PyObject *args) {

    PyObject *result, *propname = NULL;
    char **property;

    /* Parse arguments */
    if(!PyArg_ParseTuple(args, "|U", &propname)) {
        return NULL;
    }

    /* Check if property name supplied or not */
    if (!propname) {
        PyErr_SetString(PyExc_TypeError,
                        "this method takes exactly one argument");
        return NULL;
    }

    /* Get all properity of the passed param using SubFinder API */
    property = SubFinderGetProperty(BuildGoStr(propname));

    /* Store all results in a python list */
    result = StoreResults(property);

    /* Free memory */
    FreeMemory(property);

    return result;
}

static PyObject *SubFinder_Version(SubFinder *self, PyObject *Py_UNUSED(ignored)) {
    char *version;
    PyObject *py_version;

    /* Get SubFinder Version Using API */
    version = SubFinderVersion();

    /* Convert to a python object */
    py_version = PyUnicode_FromString(version);

    /* Free memory */
    PyMem_Free(version);

    return py_version;
}

static PyObject *SubFinder_Start(SubFinder *self, PyObject *Py_UNUSED(ignored)) {

    /* subdomains container */
    char **results;

    /* declare a python list */
    PyObject *pyresult = NULL; 

    /* Start Enumeration */
    if(!(results = SubFinderStart(
        BuildGoStr(self->domain), (GoInt) PyLong_AsLong(self->threads),
        (GoInt) PyLong_AsLong(self->timeout), (GoInt) PyLong_AsLong(self->maxEnumerationTime)
    ))) {
        PyErr_SetString(PyExc_Exception, "Subfinder failed");
        return NULL;
    }


    /* Store data in a python list */
    pyresult = StoreResults(results);
    
    /* free allocation of results */
    FreeMemory(results);

    return pyresult; 
}


PyMODINIT_FUNC PyInit_subfinder(void)
{
    PyObject *m;
    
    if (PyType_Ready(&SubFinderType) < 0)
        return NULL;

    m = PyModule_Create(&subfindermodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&SubFinderType);
    PyModule_AddObject(m, "SubFinder", (PyObject *) &SubFinderType);
    return m;
}