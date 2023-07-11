#ifndef _GOROCK_FRAMEWORK
#define _GOROCK_FRAMEWORK


#include "Python.h"
#include "RockRawler.h"
#include "subfinder.h"
#include "ffuf.h"


/* Convert Python List to C array */
char **PyListToArray(PyObject *pList);

/* Convert headers dict to => { "header: valua\r\n", .... } */
char **ParseHeaders(PyObject *pHeadersDict);

/* Convert Python String to Go String */
GoString BuildGoStr(PyObject *str);

/* Store results in a python list */
PyObject *StoreResults(char **results);

/* Free Allocated memory */
void FreeMemory(char **ptr);


#endif