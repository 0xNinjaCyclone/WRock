#ifndef _GOROCK_FRAMEWORK
#define _GOROCK_FRAMEWORK


#include "Python.h"
#include "RockRawler.h"
#include "subfinder.h"


/* Convert Python String to Go String */
GoString BuildGoStr(PyObject *str);

/* Store results in a python list */
PyObject *StoreResults(char **results);

/* Free Allocated memory */
void FreeMemory(char **ptr);


#endif