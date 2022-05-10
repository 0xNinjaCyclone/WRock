
#include "gorock.h"


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