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
    PyObject *sc; // status_code -> PyBool
    PyObject *noOutOfScope;

} Crawler;

typedef struct
{
    PyObject_HEAD

    PyObject *endpoints;
    PyObject *jsFiles;
    PyObject *emails;
    
} CrawlerResult;


/* Needed by Python VM */
static int Crawler_traverse(Crawler *self, visitproc visit, void *arg);
static int Crawler_clear(Crawler *self);
static PyObject *Crawler_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int Crawler_init(Crawler *self, PyObject *args, PyObject* kwds);
static void Crawler_dealloc(Crawler *self);

static int CrawlerResult_traverse(CrawlerResult *self, visitproc visit, void *arg);
static int CrawlerResult_clear(CrawlerResult *self);
static PyObject *CrawlerResult_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static void CrawlerResult_dealloc(CrawlerResult *self);

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

static int CrawlerResult_SetEndPointsAttr(CrawlerResult *self, PyObject *value, void *closure);
static PyObject *CrawlerResult_GetEndPointsAttr(CrawlerResult *self, void *closure);

static int CrawlerResult_SetJsFilesAttr(CrawlerResult *self, PyObject *value, void *closure);
static PyObject *CrawlerResult_GetJsFilesAttr(CrawlerResult *self, void *closure);

static int CrawlerResult_SetEmailsAttr(CrawlerResult *self, PyObject *value, void *closure);
static PyObject *CrawlerResult_GetEmailsAttr(CrawlerResult *self, void *closure);

static PyObject *CrawlerResult_GetEndPoints(CrawlerResult *self, PyObject *Py_UNUSED(ignored));
static PyObject *CrawlerResult_GetJsFiles(CrawlerResult *self, PyObject *Py_UNUSED(ignored));
static PyObject *CrawlerResult_GetEmails(CrawlerResult *self, PyObject *Py_UNUSED(ignored));
static PyObject *CrawlerResult_Transform(CrawlerResult *self, PyObject *Py_UNUSED(ignored));

static PyObject *StorePyDataInNewList(PyObject *pObj);
static PyObject *StoreParameterResult(Parameter **params);
static PyObject *StoreEndPointsResult(EndPoint **endpoints);
static PyObject *StoreCrawlerResult(RockRawlerResult *result);
static void FreeCrawlerResult(RockRawlerResult *result);

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

static PyGetSetDef CrawlerResult_getsetters[] = {
    {"endpoints", (getter) CrawlerResult_GetEndPointsAttr, (setter) CrawlerResult_SetEndPointsAttr,
        "The obtained endpoints.", NULL},
    {"jsFiles", (getter) CrawlerResult_GetJsFilesAttr, (setter) CrawlerResult_SetJsFilesAttr,
        "The obtained JavaScipt files.", NULL},
    {"emails", (getter) CrawlerResult_GetEmailsAttr, (setter) CrawlerResult_SetEmailsAttr,
        "Include subdomains for crawling.", NULL},

    {NULL}  /* Sentinel */
};

static PyMethodDef Crawler_methods[] = {
    {"Start", (PyCFunction) Crawler_Start, METH_NOARGS,
        "Return an instance of CrawlerResult class"},

    {NULL}  /* Sentinel */
};

static PyMethodDef CrawlerResult_methods[] = {
    {"GetEndPoints", (PyCFunction) CrawlerResult_GetEndPoints, METH_NOARGS,
        "Return a list of endpoints"},
    {"GetJsFiles", (PyCFunction) CrawlerResult_GetJsFiles, METH_NOARGS,
        "Return a list of js files"},
    {"GetEmails", (PyCFunction) CrawlerResult_GetEmails, METH_NOARGS,
        "Return a list of emails"},
    {"Transform", (PyCFunction) CrawlerResult_Transform, METH_NOARGS,
        "Transform the result to a dictionary"},

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

static PyTypeObject CrawlerResultType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "rockrawler.CrawlerResult",
    .tp_doc = "Crawler result",
    .tp_basicsize = sizeof(CrawlerResult),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_new = CrawlerResult_new,
    .tp_dealloc = (destructor) CrawlerResult_dealloc,
    .tp_traverse = (traverseproc) CrawlerResult_traverse,
    .tp_clear = (inquiry) CrawlerResult_clear,
    .tp_methods = CrawlerResult_methods,
    .tp_getset = CrawlerResult_getsetters,
};


static PyModuleDef rockrawlermodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "rockrawler",
    .m_doc = "rockrawler module is an extension to RockRawler project.",
    .m_size = -1
};

#endif