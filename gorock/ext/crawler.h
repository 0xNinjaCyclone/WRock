#ifndef _GOROCK_CRAWLER
#define _GOROCK_CRAWLER

#include "gorock.h"

typedef struct 
{
    PyObject_HEAD

    PyObject *url;
    PyObject *threads;
    PyObject *depth;
    PyObject *subsInScope;
    PyObject *insecure;
    PyObject *rawHeaders;

} Crawler;

/* Needed by Python VM */
static int Crawler_traverse(Crawler *self, visitproc visit, void *arg);
static int Crawler_clear(Crawler *self);
static PyObject *Crawler_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int Crawler_init(Crawler *self, PyObject *args, PyObject* kwds);
static void Crawler_dealloc(Crawler *self);


/* Setters && Getters */
static int Crawler_SetUrl(Crawler *self, PyObject *value, void *closure);
static PyObject *Crawler_GetUrl(Crawler *self, void *closure);

static int Crawler_SetThreads(Crawler *self, PyObject *value, void *closure);
static PyObject *Crawler_GetThreads(Crawler *self, void *closure);

static int Crawler_SetDepth(Crawler *self, PyObject *value, void *closure);
static PyObject *Crawler_GetDepth(Crawler *self, void *closure);

static int Crawler_SetSubsInScope(Crawler *self, PyObject *value, void *closure);
static PyObject *Crawler_GetSubsInScope(Crawler *self, void *closure);

static int Crawler_SetInsecure(Crawler *self, PyObject *value, void *closure);
static PyObject *Crawler_GetInsecure(Crawler *self, void *closure);

static int Crawler_SetRawHeaders(Crawler *self, PyObject *value, void *closure);
static PyObject *Crawler_GetRawHeaders(Crawler *self, void *closure);

static PyObject *Crawler_Start(Crawler *self, PyObject *Py_UNUSED(ignored));
PyMODINIT_FUNC PyInit_rockrawler(void);


static PyGetSetDef Crawler_getsetters[] = {
    {"url", (getter) Crawler_GetUrl, (setter) Crawler_SetUrl,
        "The target url.", NULL},
    {"threads", (getter) Crawler_GetThreads, (setter) Crawler_SetThreads,
        "Number of threads.", NULL},
    {"depth", (getter) Crawler_GetDepth, (setter) Crawler_SetDepth,
        "Depth to crawl. (default 2)", NULL},
    {"subsInScope", (getter) Crawler_GetSubsInScope, (setter) Crawler_SetSubsInScope,
        "Include subdomains for crawling.", NULL},
    {"insecure", (getter) Crawler_GetInsecure, (setter) Crawler_SetInsecure,
        "Disable TLS verification.", NULL},
    {"rawHeaders", (getter) Crawler_GetRawHeaders, (setter) Crawler_SetRawHeaders,
        "Custom headers separated by two semi-colons.", NULL},

    {NULL}  /* Sentinel */
};

static PyMethodDef Crawler_methods[] = {
    {"Start", (PyCFunction) Crawler_Start, METH_NOARGS,
        "Return results in a list"},

    {NULL}  /* Sentinel */
};


static PyTypeObject CrawlerType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "rockrawler.Crawler",
    .tp_doc = "Crawler objects",
    .tp_basicsize = sizeof(Crawler),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_new = Crawler_new,
    .tp_init = (initproc) Crawler_init,
    .tp_dealloc = (destructor) Crawler_dealloc,
    .tp_traverse = (traverseproc) Crawler_traverse,
    .tp_clear = (inquiry) Crawler_clear,
    .tp_methods = Crawler_methods,
    .tp_getset = Crawler_getsetters,
};


static PyModuleDef rockrawlermodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "rockrawler",
    .m_doc = "rockrawler module is an extension to RockRawler project.",
    .m_size = -1
};

#endif