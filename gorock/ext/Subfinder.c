
#include "Subfinder.h"


static int SubFinderResult_init(SubFinderResult *self, PyObject *args, PyObject* kwds)
{
    /* Initialize our parent */
    if ( PyList_Type.tp_init((PyObject *) self, args, kwds) < 0 )
        return -1;

    self->lNumberOfSubdomains = 0;

    return 0;
}

static PyObject *SubFinderResult_GetNumberOfSubdomains(SubFinderResult *self, PyObject *Py_UNUSED(ignored))
{
    return PyLong_FromLong( self->lNumberOfSubdomains );
}

static PyObject *SubFinderResult_Transform(SubFinderResult *self, PyObject *Py_UNUSED(ignored))
{
    PyObject *pDict, *pList;

    /* Initialize our dictionary that hold the data */
    if ( !(pDict = PyDict_New()) )
    {
        PyErr_SetString(PyExc_Exception, "an error occured when initializing the dict");
        return NULL;
    }

    /* Initialize the subdomains list */
    if ( !(pList = PyList_New(0)) )
    {
        PyErr_SetString(PyExc_Exception, "an error occured when initializing the subdomains list");
        return NULL;
    }

    for (Py_ssize_t lIdx = 0; lIdx < self->lNumberOfSubdomains; lIdx++)
    {
        if ( PyList_Append(pList, PyObject_CallMethod( (PyObject *) self, "__getitem__", "n", lIdx )) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when appending results to the list");
            return NULL;
        }
    }

    /* Insert the subdomains list to the dict */
    if ( PyDict_SetItemString(pDict, "subdomains", pList) != 0 )
    {
        PyErr_SetString(PyExc_Exception, "an error occurred when inserting subdomains to the dict");
        return NULL;
    }

    return pDict;
    
}


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
    nThreads = nTimeout = nMaxEnumerationTime = nRecursive = nAll = 0;

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
        PyErr_SetString(PyExc_TypeError, "Cannot delete the domain attribute");
        return -1;
    }

    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The domain attribute value must be a string");
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


static PyObject *SubFinder_GetThreads(SubFinder *self, void *closure) 
{
    Py_INCREF(self->threads);
    return self->threads;
}

static int SubFinder_SetTimeout(SubFinder *self, PyObject *value, void *closure) 
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the timeout attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The timeout attribute value must be an int");
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
        PyErr_SetString(PyExc_TypeError, "Cannot delete the maxEnumerationTime attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError,
                        "The maxEnumerationTime attribute value must be an int");
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
    PyObject *propname = NULL, *propval = NULL, *pListItem;
    char **property;
    Py_ssize_t nSize, nItemSize;

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
        goto OOM;
    }

    for (Py_ssize_t idx = 0; idx < nSize; idx++)
    {
        /* Get list item by index */
        pListItem = PyList_GetItem(propval, idx);

        /* Check if the list item not a string */
        if (!PyUnicode_Check(pListItem)) {
            PyErr_SetString(PyExc_TypeError,
                        "The properity value must be a string");
            return NULL;
        }

        /* Property name size */
        nItemSize = PyUnicode_GET_LENGTH(pListItem);

        /* Allocate memory space for the array item */
        if (!(property[idx] = (char *) PyMem_Malloc(nItemSize + 1))) { /* add one for nul */
            /* OOM CASE */

            /* Null Terminator at the end of the allocated items to free them easily */
            property[idx] = NULL;

            /* Free Allocated Memory */
            FreeMemory(property);
            
            goto OOM;
        }

        /* Copy N bytes from memory to allocated space */
        memcpy(property[idx], PyUnicode_AsUTF8(pListItem), nItemSize);

        /* Nul-terminator */
        property[idx][nItemSize] = 0x00;
    }

    /* Terminator */
    property[nSize] = NULL;
    
    /* Set Property using SubFinder API */
    SubFinderSetProperty(BuildGoStr(propname), property, (GoInt) nSize);

    /* Free memory */
    FreeMemory(property);

    Py_RETURN_NONE;

    OOM:
        PyErr_SetString(PyExc_Exception, "Out Of Memory");
        return NULL;
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

static PyObject *StoreSubFinderResult(char **results)
{
    PyObject *pObj, *pResult;

    /* Check if we can create an instance from our type or not */
    if ( !PyCallable_Check(pObj = (PyObject *)&SubFinderResultType) )
    {
        PyErr_SetString(PyExc_Exception, "SubFinderResultType isn't callable");
        return NULL;
    }
    
    /* Create a python instance of SubFinderResult class */
    pResult = PyObject_CallObject(pObj, NULL);

    if ( results && *results ) 
    {
        do
        {
            if ( !PyObject_CallMethod(pResult, "append", "s", *results) )
            {
                PyErr_SetString(PyExc_Exception, "an error occurred when appending a result to the list");
                return NULL;
            }

            /* Count the number of subdomains */
            ( (SubFinderResult *) pResult )->lNumberOfSubdomains++;

        } while ( *( ++results ) );
        
    }

    return pResult;
}

static PyObject *SubFinder_Start(SubFinder *self, PyObject *Py_UNUSED(ignored)) {

    /* subdomains container */
    char **results;

    /* SubFinderResult object */
    PyObject *pResult = NULL; 

    /* Start Enumeration */
    if(!(results = SubFinderStart(
        BuildGoStr(self->domain), (GoInt) PyLong_AsLong(self->threads),
        (GoInt) PyLong_AsLong(self->timeout), (GoInt) PyLong_AsLong(self->maxEnumerationTime)
    ))) {
        PyErr_SetString(PyExc_Exception, "Subfinder failed");
        return NULL;
    }


    /* Store data in a python list */
    pResult = StoreSubFinderResult(results);
    
    /* free allocation of results */
    FreeMemory(results);

    return pResult; 
}


PyMODINIT_FUNC PyInit_subfinder(void)
{
    PyObject *m;
    
    if (PyType_Ready(&SubFinderType) < 0)
        return NULL;

    if (PyType_Ready(&SubFinderResultType) < 0)
        return NULL;

    m = PyModule_Create(&subfindermodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&SubFinderType);
    Py_INCREF(&SubFinderResultType);

    if (
        PyModule_AddObject(m, "SubFinder", (PyObject *) &SubFinderType) <0 ||
        PyModule_AddObject(m, "SubFinderResult", (PyObject *) &SubFinderResultType) < 0
    )
    {
        Py_DECREF(&SubFinderType);
        Py_DECREF(&SubFinderResultType);
        Py_DECREF(m);
    }
    
    
    return m;
}
