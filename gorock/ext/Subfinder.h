#ifndef _ROCK_SUBFINDER
#define _ROCK_SUBFINDER

#include "gorock.h"

typedef struct 
{
    PyObject_HEAD

    PyObject *domain;
    PyObject *threads;
    PyObject *timeout;
    PyObject *maxEnumerationTime;

} SubFinder;

/* Needed by Python VM */
static int SubFinder_traverse(SubFinder *self, visitproc visit, void *arg);
static int SubFinder_clear(SubFinder *self);
static PyObject *SubFinder_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int SubFinder_init(SubFinder *self, PyObject *args, PyObject* kwds);
static void SubFinder_dealloc(SubFinder *self);


/* Setters && Getters */
static int SubFinder_SetDomain(SubFinder *self, PyObject *value, void *closure);
static PyObject *SubFinder_GetDomin(SubFinder *self, void *closure);

static int SubFinder_SetThreads(SubFinder *self, PyObject *value, void *closure);
static PyObject *SubFinder_GetThreads(SubFinder *self, void *closure);

static int SubFinder_SetTimeout(SubFinder *self, PyObject *value, void *closure);
static PyObject *SubFinder_GetTimeout(SubFinder *self, void *closure);

static int SubFinder_SetMaxEnumerationTime(SubFinder *self, PyObject *value, void *closure);
static PyObject *SubFinder_GetMaxEnumerationTime(SubFinder *self, void *closure);

/* Methods */
static PyObject *SubFinder_UseAll(SubFinder *self, PyObject *Py_UNUSED(ignored));
static PyObject *SubFinder_UseRecursive(SubFinder *self, PyObject *Py_UNUSED(ignored));
static PyObject *SubFinder_SetProperty(SubFinder *self, PyObject *args);
static PyObject *SubFinder_GetProperty(SubFinder *self, PyObject *args);
static PyObject *SubFinder_Version(SubFinder *self, PyObject *Py_UNUSED(ignored));
static PyObject *SubFinder_Start(SubFinder *self, PyObject *Py_UNUSED(ignored));

/* Initiate the module */
PyMODINIT_FUNC PyInit_subfinder(void);


static PyGetSetDef SubFinder_getsetters[] = {
    {"domain", (getter) SubFinder_GetDomin, (setter) SubFinder_SetDomain,
        "Domain to find subdomains for.", NULL},
    {"threads", (getter) SubFinder_GetThreads, (setter) SubFinder_SetThreads,
        "Number of threads.", NULL},
    {"timeout", (getter) SubFinder_GetTimeout, (setter) SubFinder_SetTimeout,
        "Seconds to wait before timing out (default 30)", NULL},
    {"maxEnumerationTime", (getter) SubFinder_GetMaxEnumerationTime, (setter) SubFinder_SetMaxEnumerationTime,
        "Minutes to wait for enumeration results (default 10).", NULL},

    {NULL}  /* Sentinel */
};

static PyMethodDef SubFinder_methods[] = {
    {"Start", (PyCFunction) SubFinder_Start, METH_NOARGS,
        "Return results in a list"},
    {"Version", (PyCFunction) SubFinder_Version, METH_NOARGS,
        "Return subfinder version"},
    {"UseAll", (PyCFunction) SubFinder_UseAll, METH_NOARGS,
        "Use all sources"},
    {"UseRecursive", (PyCFunction) SubFinder_UseRecursive, METH_NOARGS,
        "Enumerate Recursively"},
    {"SetProperty", (PyCFunction) SubFinder_SetProperty, METH_VARARGS,
        "Set subfinder configurations"},
    {"GetProperty", (PyCFunction) SubFinder_GetProperty, METH_VARARGS,
        "Return property in a list"},

    {NULL}  /* Sentinel */
};


static PyTypeObject SubFinderType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "subfinder.SubFinder",
    .tp_doc = "SubFinder objects",
    .tp_basicsize = sizeof(SubFinder),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_new = SubFinder_new,
    .tp_init = (initproc) SubFinder_init,
    .tp_dealloc = (destructor) SubFinder_dealloc,
    .tp_traverse = (traverseproc) SubFinder_traverse,
    .tp_clear = (inquiry) SubFinder_clear,
    .tp_methods = SubFinder_methods,
    .tp_getset = SubFinder_getsetters,
};


static PyModuleDef subfindermodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "subfinder",
    .m_doc = "subfinder module is an extension to subfinder project.",
    .m_size = -1
};

#endif
