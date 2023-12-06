#ifndef _GOROCK_HELPER
#define _GOROCK_HELPER

#include "gorock.h"
#include "Helper.h"

static PyObject *Xlevenshtein_distance(PyObject *self, PyObject *args);


static PyMethodDef HelperMethods[] = {
    {"levenshtein_distance", Xlevenshtein_distance, METH_VARARGS, "Levenshtein distance algorithm."},
    {NULL, NULL, 0, NULL}
};


static struct PyModuleDef helpermodule = {
    PyModuleDef_HEAD_INIT,
    "helper",
    "Python interface for the WRock Helper.",
    -1,
    HelperMethods
};

#endif