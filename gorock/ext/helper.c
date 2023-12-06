

#include "helper.h"

static PyObject *Xlevenshtein_distance(PyObject *self, PyObject *args)
{
    PyObject *pStr1, *pStr2;
    char *cpStr1, *cpStr2;

    pStr1 = pStr2 = NULL;

    if( !PyArg_ParseTuple(args, "UU", &pStr1, &pStr2) )
        return NULL;

    if ( !pStr1 || !pStr2 )
    {
        PyErr_SetString(PyExc_TypeError, "This method takes exactly two arguments");
        return NULL;
    }

    Py_INCREF( pStr1 );
    Py_INCREF( pStr2 );

    cpStr1 = (char *) PyUnicode_AsUTF8( pStr1 );
    cpStr2 = (char *) PyUnicode_AsUTF8( pStr2 );


    if ( !cpStr1 || !cpStr2 )
    {
        PyErr_SetString(PyExc_Exception, "PyUnicode_AsUTF8 return NULLs");
        return NULL;
    }

    return PyLong_FromLong( levenshtein_distance(cpStr1, cpStr2) );
}

PyMODINIT_FUNC PyInit_helper(void) {
    return PyModule_Create( &helpermodule );
}