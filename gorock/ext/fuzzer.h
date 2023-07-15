#ifndef _GOROCK_FUZZER
#define _GOROCK_FUZZER

#include "gorock.h"

typedef struct
{

    PyObject_HEAD
    
} Fuzzer;

typedef struct
{

    PyObject_HEAD

    PyObject *pInput;
    PyObject *plPosition;
    PyObject *plStatusCode;
    PyObject *plContentLength;
    PyObject *plContentWords;
    PyObject *plContentLines;
    PyObject *puContentType;
    PyObject *puRedirectLocation;
    PyObject *puUrl;
    PyObject *puResultFile;
    PyObject *puHost;
    PyObject *puHTMLColor;
    PyObject *pScraperData;
    PyObject *pTimeDuration;

} FuzzerResultItem;

/* This type inherits from the List type */
typedef struct
{

    PyListObject super;
    Py_ssize_t lNumberOfResults;

} FuzzerResult;

typedef struct
{

    PyObject_HEAD
    PyObject *plHours;
    PyObject *plMinutes;
    PyObject *plSeconds;
    PyObject *plMicroseconds;
    PyObject *plMilliseconds;
    PyObject *plNanoseconds;
    PyObject *puStr;
    
} FuzzerTimeDuration;


/* Needed by Python VM */
static PyObject *Fuzzer_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static int Fuzzer_init(Fuzzer *self, PyObject *args, PyObject* kwds);
static void Fuzzer_dealloc(Fuzzer *self);
static int Fuzzer_traverse(Fuzzer *self, visitproc visit, void *arg);
static int Fuzzer_clear(Fuzzer *self);

/* Fuzzer Methods */
static PyObject *Fuzzer_GetVersion(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_SetMethod(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_SetData(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_SetConfigFile(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_SetInputMode(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_SetInputCommands(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_SetRequestFile(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_SetAutoCalibrationStrategy(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_SetRecursionStrategy(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_SetRequestProto(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_SetScrapers(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_SetMatcherMode(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_SetFilterMode(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_AddMatcher(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_AddFilter(Fuzzer *self, PyObject *args);
static PyObject *Fuzzer_Start(Fuzzer *self, PyObject *Py_UNUSED(ignored));

/* FuzzerResultItem -> functions needed by Python VM */
static int FuzzerResultItem_traverse(FuzzerResultItem *self, visitproc visit, void *arg);
static int FuzzerResultItem_clear(FuzzerResultItem *self);
static PyObject *FuzzerResultItem_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static void FuzzerResultItem_dealloc(FuzzerResultItem *self);

/* FuzzerResultItem -> Setters && Getters */
static int FuzzerResultItem_SetInputDataAttr(FuzzerResultItem *self, PyObject *value, void *closure);
static PyObject *FuzzerResultItem_GetInputDataAttr(FuzzerResultItem *self, void *closure);
static int FuzzerResultItem_SetPositionAttr(FuzzerResultItem *self, PyObject *value, void *closure);
static PyObject *FuzzerResultItem_GetPositionAttr(FuzzerResultItem *self, void *closure);
static int FuzzerResultItem_SetStatusCodeAttr(FuzzerResultItem *self, PyObject *value, void *closure);
static PyObject *FuzzerResultItem_GetStatusCodeAttr(FuzzerResultItem *self, void *closure);
static int FuzzerResultItem_SetContentLengthAttr(FuzzerResultItem *self, PyObject *value, void *closure);
static PyObject *FuzzerResultItem_GetContentLengthAttr(FuzzerResultItem *self, void *closure);
static int FuzzerResultItem_SetContentWordsAttr(FuzzerResultItem *self, PyObject *value, void *closure);
static PyObject *FuzzerResultItem_GetContentWordsAttr(FuzzerResultItem *self, void *closure);
static int FuzzerResultItem_SetContentLinesAttr(FuzzerResultItem *self, PyObject *value, void *closure);
static PyObject *FuzzerResultItem_GetContentLinesAttr(FuzzerResultItem *self, void *closure);
static int FuzzerResultItem_SetContentTypeAttr(FuzzerResultItem *self, PyObject *value, void *closure);
static PyObject *FuzzerResultItem_GetContentTypeAttr(FuzzerResultItem *self, void *closure);
static int FuzzerResultItem_SetRedirectLocationAttr(FuzzerResultItem *self, PyObject *value, void *closure);
static PyObject *FuzzerResultItem_GetRedirectLocationAttr(FuzzerResultItem *self, void *closure);
static int FuzzerResultItem_SetUrlAttr(FuzzerResultItem *self, PyObject *value, void *closure);
static PyObject *FuzzerResultItem_GetUrlAttr(FuzzerResultItem *self, void *closure);
static int FuzzerResultItem_SetResultFileAttr(FuzzerResultItem *self, PyObject *value, void *closure);
static PyObject *FuzzerResultItem_GetResultFileAttr(FuzzerResultItem *self, void *closure);
static int FuzzerResultItem_SetHostAttr(FuzzerResultItem *self, PyObject *value, void *closure);
static PyObject *FuzzerResultItem_GetHostAttr(FuzzerResultItem *self, void *closure);
static int FuzzerResultItem_SetHTMLColorAttr(FuzzerResultItem *self, PyObject *value, void *closure);
static PyObject *FuzzerResultItem_GetHTMLColorAttr(FuzzerResultItem *self, void *closure);
static int FuzzerResultItem_SetScraperDataAttr(FuzzerResultItem *self, PyObject *value, void *closure);
static PyObject *FuzzerResultItem_GetScraperDataAttr(FuzzerResultItem *self, void *closure);
static int FuzzerResultItem_SetTimeDurationAttr(FuzzerResultItem *self, PyObject *value, void *closure);
static PyObject *FuzzerResultItem_GetTimeDurationAttr(FuzzerResultItem *self, void *closure);

/* FuzzerResultItem -> Methods */
static PyObject *FuzzerResultItem_GetInputData(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResultItem_GetPosition(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResultItem_GetStatusCode(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResultItem_GetContentLength(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResultItem_GetContentWords(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResultItem_GetContentLines(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResultItem_GetContentType(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResultItem_GetRedirectLocation(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResultItem_GetUrl(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResultItem_GetResultFile(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResultItem_GetHost(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResultItem_GetHTMLColor(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResultItem_GetScraperData(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResultItem_GetTimeDuration(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResultItem_GetFuzzingWords(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored));

/* FuzzerResult -> functions needed by Python VM */
static int FuzzerResult_init(FuzzerResult *self, PyObject *args, PyObject* kwds);

/* FuzzerResult Methods */
static PyObject *FuzzerResult_GetNumberOfResults(FuzzerResult *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerResult_Transform(FuzzerResult *self, PyObject *Py_UNUSED(ignored));

/* FuzzerTimeDuration -> functions needed by Python VM*/
static PyObject *FuzzerTimeDuration_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
static void FuzzerTimeDuration_dealloc(FuzzerTimeDuration *self);
static int FuzzerTimeDuration_traverse(FuzzerTimeDuration *self, visitproc visit, void *arg);
static int FuzzerTimeDuration_clear(FuzzerTimeDuration *self);

/* FuzzerTimeDuration -> Setters && Getters */
static int FuzzerTimeDuration_SetHoursAttr(FuzzerTimeDuration *self, PyObject *value, void *closure);
static PyObject *FuzzerTimeDuration_GetHoursAttr(FuzzerTimeDuration *self, void *closure);
static int FuzzerTimeDuration_SetMinutesAttr(FuzzerTimeDuration *self, PyObject *value, void *closure);
static PyObject *FuzzerTimeDuration_GetMinutesAttr(FuzzerTimeDuration *self, void *closure);
static int FuzzerTimeDuration_SetSecondsAttr(FuzzerTimeDuration *self, PyObject *value, void *closure);
static PyObject *FuzzerTimeDuration_GetSecondsAttr(FuzzerTimeDuration *self, void *closure);
static int FuzzerTimeDuration_SetMicrosecondsAttr(FuzzerTimeDuration *self, PyObject *value, void *closure);
static PyObject *FuzzerTimeDuration_GetMicrosecondsAttr(FuzzerTimeDuration *self, void *closure);
static int FuzzerTimeDuration_SetMillisecondsAttr(FuzzerTimeDuration *self, PyObject *value, void *closure);
static PyObject *FuzzerTimeDuration_GetMillisecondsAttr(FuzzerTimeDuration *self, void *closure);
static int FuzzerTimeDuration_SetNanosecondsAttr(FuzzerTimeDuration *self, PyObject *value, void *closure);
static PyObject *FuzzerTimeDuration_GetNanosecondsAttr(FuzzerTimeDuration *self, void *closure);
static int FuzzerTimeDuration_SetStrAttr(FuzzerTimeDuration *self, PyObject *value, void *closure);
static PyObject *FuzzerTimeDuration_GetStrAttr(FuzzerTimeDuration *self, void *closure);

/* FuzzerTimeDuration -> Methods */
static PyObject *FuzzerTimeDuration_GetHours(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerTimeDuration_GetMinutes(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerTimeDuration_GetSeconds(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerTimeDuration_GetMicroseconds(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerTimeDuration_GetMilliseconds(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerTimeDuration_GetNanoseconds(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerTimeDuration_GetStr(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored));
static PyObject *FuzzerTimeDuration_Transform(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored));

PyMODINIT_FUNC PyInit_ffuf(void);


/* Fuzzer utils */
static PyObject *StoreInputData(InputData **pInputData);
static PyObject *StoreScraperData(ScraperData **pScraperData);
static PyObject *StoreTimeDuration(TimeDuration *pTimeDuration);
static PyObject *StoreFuzzerResult(FfufResult **pFfufResults);
static void FreeFuzzerMemory(FfufResult **pFfufResults);


static PyGetSetDef FuzzerResultItem_getsetters[] = {
    {"inputdata", (getter) FuzzerResultItem_GetInputDataAttr, (setter) FuzzerResultItem_SetInputDataAttr,
        "The item inputdata.", NULL},
    {"position", (getter) FuzzerResultItem_GetPositionAttr, (setter) FuzzerResultItem_SetPositionAttr,
        "The item position.", NULL},
    {"statuscode", (getter) FuzzerResultItem_GetStatusCodeAttr, (setter) FuzzerResultItem_SetStatusCodeAttr,
        "The item statuscode.", NULL},
    {"contentlength", (getter) FuzzerResultItem_GetContentLengthAttr, (setter) FuzzerResultItem_SetContentLengthAttr,
        "The item contentlength.", NULL},
    {"contentwords", (getter) FuzzerResultItem_GetContentWordsAttr, (setter) FuzzerResultItem_SetContentWordsAttr,
        "The item contentwords.", NULL},
    {"contentlines", (getter) FuzzerResultItem_GetContentLinesAttr, (setter) FuzzerResultItem_SetContentLinesAttr,
        "The item contentlines.", NULL},
    {"contenttype", (getter) FuzzerResultItem_GetContentTypeAttr, (setter) FuzzerResultItem_SetContentTypeAttr,
        "The item contenttype.", NULL},
    {"redirectlocation", (getter) FuzzerResultItem_GetRedirectLocationAttr, (setter) FuzzerResultItem_SetRedirectLocationAttr,
        "The item redirectlocation.", NULL},
    {"url", (getter) FuzzerResultItem_GetUrlAttr, (setter) FuzzerResultItem_SetUrlAttr,
        "The item url.", NULL},
    {"resultfile", (getter) FuzzerResultItem_GetResultFileAttr, (setter) FuzzerResultItem_SetResultFileAttr,
        "The item resultfile.", NULL},
    {"host", (getter) FuzzerResultItem_GetHostAttr, (setter) FuzzerResultItem_SetHostAttr,
        "The item host.", NULL},
    {"htmlcolor", (getter) FuzzerResultItem_GetHTMLColorAttr, (setter) FuzzerResultItem_SetHTMLColorAttr,
        "The item htmlcolor.", NULL},
    {"scraperdata", (getter) FuzzerResultItem_GetScraperDataAttr, (setter) FuzzerResultItem_SetScraperDataAttr,
        "The item scraperdata.", NULL},
    {"timeduration", (getter) FuzzerResultItem_GetTimeDurationAttr, (setter) FuzzerResultItem_SetTimeDurationAttr,
        "The item timeduration.", NULL},

    { NULL }  /* Sentinel */
};

static PyGetSetDef FuzzerTimeDuration_getsetters[] = {
    {"hours", (getter) FuzzerTimeDuration_GetHoursAttr, (setter) FuzzerTimeDuration_SetHoursAttr,
        "The time duration hours.", NULL},
    {"minutes", (getter) FuzzerTimeDuration_GetMinutesAttr, (setter) FuzzerTimeDuration_SetMinutesAttr,
        "The time duration minutes.", NULL},
    {"seconds", (getter) FuzzerTimeDuration_GetSecondsAttr, (setter) FuzzerTimeDuration_SetSecondsAttr,
        "The time duration seconds.", NULL},
    {"microseconds", (getter) FuzzerTimeDuration_GetMicrosecondsAttr, (setter) FuzzerTimeDuration_SetMicrosecondsAttr,
        "The time duration microseconds.", NULL},
    {"milliseconds", (getter) FuzzerTimeDuration_GetMillisecondsAttr, (setter) FuzzerTimeDuration_SetMillisecondsAttr,
        "The time duration milliseconds.", NULL},
    {"nanoseconds", (getter) FuzzerTimeDuration_GetNanosecondsAttr, (setter) FuzzerTimeDuration_SetNanosecondsAttr,
        "The time duration nanoseconds.", NULL},
    {"str", (getter) FuzzerTimeDuration_GetStrAttr, (setter) FuzzerTimeDuration_SetStrAttr,
        "The time duration str.", NULL},

    { NULL }  /* Sentinel */
};

static PyMethodDef Fuzzer_methods[] = {
    {"GetVersion", (PyCFunction) Fuzzer_GetVersion, METH_NOARGS,
        "Get used ffuf version."},
    {"SetMethod", (PyCFunction) Fuzzer_SetMethod, METH_VARARGS,
        "Set HTTP Method."},
    {"SetData", (PyCFunction) Fuzzer_SetData, METH_VARARGS,
        "Set HTTP Data."},
    {"SetConfigFile", (PyCFunction) Fuzzer_SetConfigFile, METH_VARARGS,
        "Set Config File."},
    {"SetInputMode", (PyCFunction) Fuzzer_SetInputMode, METH_VARARGS,
        "Set Input Mode."},
    {"SetInputCommands", (PyCFunction) Fuzzer_SetInputCommands, METH_VARARGS,
        "Set Input Commands."},
    {"SetRequestFile", (PyCFunction) Fuzzer_SetRequestFile, METH_VARARGS,
        "Set Request File."},
    {"SetAutoCalibrationStrategy", (PyCFunction) Fuzzer_SetAutoCalibrationStrategy, METH_VARARGS,
        "Set Auto Calibration Strategy."},
    {"SetRecursionStrategy", (PyCFunction) Fuzzer_SetRecursionStrategy, METH_VARARGS,
        "Set Recursion Strategy."},
    {"SetRequestProto", (PyCFunction) Fuzzer_SetRequestProto, METH_VARARGS,
        "Set Request Protocol."},
    {"SetScrapers", (PyCFunction) Fuzzer_SetScrapers, METH_VARARGS,
        "Set Scrapers."},
    {"SetMatcherMode", (PyCFunction) Fuzzer_SetMatcherMode, METH_VARARGS,
        "Set Matcher Mode."},
    {"SetFilterMode", (PyCFunction) Fuzzer_SetFilterMode, METH_VARARGS,
        "Set Filter Mode."},
    {"AddMatcher", (PyCFunction) Fuzzer_AddMatcher, METH_VARARGS,
        "Add Matcher."},
    {"AddFilter", (PyCFunction) Fuzzer_AddFilter, METH_VARARGS,
        "Add Filter."},
    {"Start", (PyCFunction) Fuzzer_Start, METH_NOARGS,
        "Return a FuzzerResult object."},

    { NULL }  /* Sentinel */
};

static PyMethodDef FuzzerResultItem_methods[] = {
    {"GetInputData", (PyCFunction) FuzzerResultItem_GetInputData, METH_NOARGS,
        "Return the item inputdata."},
    {"GetPosition", (PyCFunction) FuzzerResultItem_GetPosition, METH_NOARGS,
        "Return the item position."},
    {"GetStatusCode", (PyCFunction) FuzzerResultItem_GetStatusCode, METH_NOARGS,
        "Return the item statuscode."},
    {"GetContentLength", (PyCFunction) FuzzerResultItem_GetContentLength, METH_NOARGS,
        "Return the item contentlength."},
    {"GetContentWords", (PyCFunction) FuzzerResultItem_GetContentWords, METH_NOARGS,
        "Return the item contentwords."},
    {"GetContentLines", (PyCFunction) FuzzerResultItem_GetContentLines, METH_NOARGS,
        "Return the item contentlines."},
    {"GetContentType", (PyCFunction) FuzzerResultItem_GetContentType, METH_NOARGS,
        "Return the item contenttype."},
    {"GetRedirectLocation", (PyCFunction) FuzzerResultItem_GetRedirectLocation, METH_NOARGS,
        "Return the item redirectlocation."},
    {"GetUrl", (PyCFunction) FuzzerResultItem_GetUrl, METH_NOARGS,
        "Return the item url."},
    {"GetResultFile", (PyCFunction) FuzzerResultItem_GetResultFile, METH_NOARGS,
        "Return the item resultfile."},
    {"GetHost", (PyCFunction) FuzzerResultItem_GetHost, METH_NOARGS,
        "Return the item host."},
    {"GetHTMLColor", (PyCFunction) FuzzerResultItem_GetHTMLColor, METH_NOARGS,
        "Return the item htmlcolor."},
    {"GetScraperData", (PyCFunction) FuzzerResultItem_GetScraperData, METH_NOARGS,
        "Return the item scraperdata."},
    {"GetTimeDuration", (PyCFunction) FuzzerResultItem_GetTimeDuration, METH_NOARGS,
        "Return the item timeduration."},
    {"GetFuzzingWords", (PyCFunction) FuzzerResultItem_GetFuzzingWords, METH_NOARGS,
        "Return the item fuzzing words."},

    { NULL }  /* Sentinel */
};

static PyMethodDef FuzzerTimeDuration_methods[] = {
    {"GetHours", (PyCFunction) FuzzerTimeDuration_GetHours, METH_NOARGS,
        "Return the time duration hours."},
    {"GetMinutes", (PyCFunction) FuzzerTimeDuration_GetMinutes, METH_NOARGS,
        "Return the time duration minutes."},
    {"GetSeconds", (PyCFunction) FuzzerTimeDuration_GetSeconds, METH_NOARGS,
        "Return the time duration seconds."},
    {"GetMicroseconds", (PyCFunction) FuzzerTimeDuration_GetMicroseconds, METH_NOARGS,
        "Return the time duration microseconds."},
    {"GetMilliseconds", (PyCFunction) FuzzerTimeDuration_GetMilliseconds, METH_NOARGS,
        "Return the time duration milliseconds."},
    {"GetNanoseconds", (PyCFunction) FuzzerTimeDuration_GetNanoseconds, METH_NOARGS,
        "Return the time duration nanoseconds."},
    {"GetStr", (PyCFunction) FuzzerTimeDuration_GetStr, METH_NOARGS,
        "Return the time duration str."},
    {"Transform", (PyCFunction) FuzzerTimeDuration_Transform, METH_NOARGS,
        "Represent time duration as a dict."},

    { NULL }  /* Sentinel */
};

static PyMethodDef FuzzerResult_methods[] = {
    {"GetLength", (PyCFunction) FuzzerResult_GetNumberOfResults, METH_NOARGS,
        "Get Number Of Results"},
    {"Transform", (PyCFunction) FuzzerResult_Transform, METH_NOARGS,
        "Transform the result to a dictionary"},
        
    { NULL }  /* Sentinel */
};

static PyTypeObject FuzzerType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "ffuf.Fuzzer",
    .tp_doc = "Fuzzer objects",
    .tp_basicsize = sizeof(Fuzzer),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_new = Fuzzer_new,
    .tp_init = (initproc) Fuzzer_init,
    .tp_dealloc = (destructor) Fuzzer_dealloc,
    .tp_traverse = (traverseproc) Fuzzer_traverse,
    .tp_clear = (inquiry) Fuzzer_clear,
    .tp_methods = Fuzzer_methods,
};

static PyTypeObject FuzzerResultItemType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "ffuf.FuzzerResultItem",
    .tp_doc = "Fuzzer result item",
    .tp_basicsize = sizeof(FuzzerResultItem),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_new = FuzzerResultItem_new,
    .tp_dealloc = (destructor) FuzzerResultItem_dealloc,
    .tp_traverse = (traverseproc) FuzzerResultItem_traverse,
    .tp_clear = (inquiry) FuzzerResultItem_clear,
    .tp_methods = FuzzerResultItem_methods,
    .tp_getset = FuzzerResultItem_getsetters,
};

static PyTypeObject FuzzerResultType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "ffuf.FuzzerResult",
    .tp_doc = "Fuzzer Result",
    .tp_basicsize = sizeof(FuzzerResult),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_init = (initproc) FuzzerResult_init,
    .tp_methods = FuzzerResult_methods,
    .tp_base = &PyList_Type, 
};

static PyTypeObject FuzzerTimeDurationType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "ffuf.TimeDuration",
    .tp_doc = "Fuzzer Time Duration",
    .tp_basicsize = sizeof(FuzzerTimeDuration),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    .tp_new = FuzzerTimeDuration_new,
    .tp_dealloc = (destructor) FuzzerTimeDuration_dealloc,
    .tp_traverse = (traverseproc) FuzzerTimeDuration_traverse,
    .tp_clear = (inquiry) FuzzerTimeDuration_clear,
    .tp_methods = FuzzerTimeDuration_methods,
    .tp_getset = FuzzerTimeDuration_getsetters,
};

static PyModuleDef ffufmodule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "ffuf",
    .m_doc = "ffuf module is an extension to ffuf project.",
    .m_size = -1
};

#endif