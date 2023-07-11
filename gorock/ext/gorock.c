
#include "gorock.h"

char **PyListToArray(PyObject *pList)
{
    PyObject *pListItem;
    char **pArr;
    Py_ssize_t lSize, lItemSize;

    if ( !PyList_Check(pList) )
    {
        PyErr_SetString(PyExc_TypeError, "[PyListToArray] parameter should be a list");
        return NULL;
    }

    /* Get Size of the list */
    lSize = PyList_Size(pList);

    /* Allocate memory for the C Array */
    if (!(pArr = (char **) PyMem_Malloc(sizeof(*pArr) * (lSize + 1)))) 
        goto OOM;
    

    for (Py_ssize_t lIdx = 0; lIdx < lSize; lIdx++)
    {
        /* Get list item by index */
        pListItem = PyList_GetItem(pList, lIdx);

        /* Check if the list item not a string */
        if ( !PyUnicode_Check(pListItem) ) {
            PyErr_SetString(PyExc_TypeError, "[PyListToArray] The list item value must be a string");
            return NULL;
        }

        /* Property name size */
        lItemSize = PyUnicode_GET_LENGTH(pListItem);

        /* Allocate memory space for the array item */
        if ( !(pArr[lIdx] = (char *) PyMem_Malloc(lItemSize + 1)) ) 
        { 
            /* OOM CASE */

            /* Null Terminator at the end of the allocated items to free them easily */
            pArr[lIdx] = NULL;

            /* Free Allocated Memory */
            FreeMemory(pArr);
            
            goto OOM;
        }

        /* Copy N bytes from memory to the allocated space */
        memcpy(pArr[lIdx], PyUnicode_AsUTF8(pListItem), lItemSize);

        /* Nul-terminator */
        pArr[lIdx][lItemSize] = 0x00;
    }

    /* Terminator */
    pArr[lSize] = NULL;

    return pArr;
    
    OOM:
        PyErr_SetString(PyExc_Exception, "[PyListToArray] Out Of Memory");
        return NULL;
}

char **ParseHeaders(PyObject *pHeadersDict)
{
    char **pHeaders;
    PyObject *pKey, *pValue;
    Py_ssize_t lPos = 0, lCtr = 0, lSize, lItemSize;

    if ( !PyDict_Check(pHeadersDict) )
    {
        PyErr_SetString(PyExc_TypeError, "[ParseHeaders] parameter should be a dict");
        return NULL;
    }

    lSize = PyDict_Size(pHeadersDict);

    /* Allocate memory for the C Array */
    if (!(pHeaders = (char **) PyMem_Malloc(sizeof(*pHeaders) * (lSize + 1)))) 
        goto OOM;


    while ( PyDict_Next(pHeadersDict, &lPos, &pKey, &pValue) )
    {
        /* Check if the key or value not a string */
        if ( !PyUnicode_Check(pKey) || !PyUnicode_Check(pValue) ) {
            PyErr_SetString(PyExc_TypeError, "[ParseHeaders] The key and value must be a string");
            return NULL;
        }

        /* Size of the key and the value and ': ' and also '\r\n' */
        lItemSize = PyUnicode_GET_LENGTH(pKey) + PyUnicode_GET_LENGTH(pValue) + 5;

        /* Allocate memory for the header (+1 for NUL) */
        if ( !(pHeaders[lCtr] = (char *) PyMem_Malloc(lItemSize + 1)) ) 
        {
            /* OOM CASE */

            /* Null Terminator at the end of the allocated items to free them easily */
            pHeaders[lCtr] = NULL;

            /* Free Allocated Memory */
            FreeMemory(pHeaders);
            
            goto OOM;
        }

        /* Header format */
        snprintf(pHeaders[lCtr], lItemSize, "%s: %s\r\n", PyUnicode_AsUTF8(pKey), PyUnicode_AsUTF8(pValue));

        /* Nul-terminator */
        pHeaders[lCtr][lItemSize] = 0x00;

        lCtr++;
    }

    /* Terminator */
    pHeaders[lSize] = NULL;

    return pHeaders;

    OOM:
        PyErr_SetString(PyExc_Exception, "[ParseHeaders] Out Of Memory");
        return NULL;
}

GoString BuildGoStr(PyObject *str)
{
    return (GoString) { .p = PyUnicode_AsUTF8(str), .n = PyUnicode_GET_LENGTH(str) };
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
            PyErr_SetString(PyExc_Exception, "an error occured when append results to the list");
            return NULL;
        }
    }

    return pyresult;
}

void FreeMemory(char **ptr)
{
    for (char **temp = ptr; *temp; temp++)
        /* Free each item of the array */
        PyMem_Free(*temp);
    

    PyMem_Free(ptr);
}