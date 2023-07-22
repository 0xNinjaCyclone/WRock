
#include "fuzzer.h"

static PyObject *FuzzerTimeDuration_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    FuzzerTimeDuration *self;

    /* Allocate some memory for the timeduration class */
    self = (FuzzerTimeDuration *) type->tp_alloc(type, 0);

    if ( self ) {
        if (!(
            (self->plHours = PyLong_FromLong(0)) ||
            (self->plMinutes = PyLong_FromLong(0)) ||
            (self->plSeconds = PyLong_FromLong(0)) ||
            (self->plMicroseconds = PyLong_FromLong(0)) ||
            (self->plMilliseconds = PyLong_FromLong(0)) ||
            (self->plNanoseconds = PyLong_FromLong(0)) ||
            (self->puStr = PyUnicode_FromString("")) 
        )) {
            /* initialization failed */

            Py_DECREF(self);
            return NULL;
        }
    }

    return (PyObject *) self;
}

static void FuzzerTimeDuration_dealloc(FuzzerTimeDuration *self)
{
    PyObject_GC_UnTrack(self);
    FuzzerTimeDuration_clear(self);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static int FuzzerTimeDuration_traverse(FuzzerTimeDuration *self, visitproc visit, void *arg)
{
    Py_VISIT(self->plHours);
    Py_VISIT(self->plMinutes);
    Py_VISIT(self->plSeconds);
    Py_VISIT(self->plMicroseconds);
    Py_VISIT(self->plMilliseconds);
    Py_VISIT(self->plNanoseconds);
    Py_VISIT(self->puStr);
    return 0;
}

static int FuzzerTimeDuration_clear(FuzzerTimeDuration *self)
{
    Py_CLEAR(self->plHours);
    Py_CLEAR(self->plMinutes);
    Py_CLEAR(self->plSeconds);
    Py_CLEAR(self->plMicroseconds);
    Py_CLEAR(self->plMilliseconds);
    Py_CLEAR(self->plNanoseconds);
    Py_CLEAR(self->puStr);
    return 0;
}

static int FuzzerTimeDuration_SetHoursAttr(FuzzerTimeDuration *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the hours attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The hours attribute value must be an int");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->plHours);
    self->plHours = value;
    return 0;
}

static PyObject *FuzzerTimeDuration_GetHoursAttr(FuzzerTimeDuration *self, void *closure)
{
    Py_INCREF(self->plHours);
    return self->plHours;
}

static int FuzzerTimeDuration_SetMinutesAttr(FuzzerTimeDuration *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the minutes attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The minutes attribute value must be an int");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->plMinutes);
    self->plMinutes = value;
    return 0;
}

static PyObject *FuzzerTimeDuration_GetMinutesAttr(FuzzerTimeDuration *self, void *closure)
{
    Py_INCREF(self->plMinutes);
    return self->plMinutes;
}

static int FuzzerTimeDuration_SetSecondsAttr(FuzzerTimeDuration *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the seconds attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The seconds attribute value must be an int");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->plSeconds);
    self->plSeconds = value;
    return 0;
}

static PyObject *FuzzerTimeDuration_GetSecondsAttr(FuzzerTimeDuration *self, void *closure)
{
    Py_INCREF(self->plSeconds);
    return self->plSeconds;
}

static int FuzzerTimeDuration_SetMicrosecondsAttr(FuzzerTimeDuration *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the microseconds attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The microseconds attribute value must be an int");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->plMicroseconds);
    self->plMicroseconds = value;
    return 0;
}

static PyObject *FuzzerTimeDuration_GetMicrosecondsAttr(FuzzerTimeDuration *self, void *closure)
{
    Py_INCREF(self->plMicroseconds);
    return self->plMicroseconds;
}

static int FuzzerTimeDuration_SetMillisecondsAttr(FuzzerTimeDuration *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the milliseconds attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The milliseconds attribute value must be an int");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->plMilliseconds);
    self->plMilliseconds = value;
    return 0;
}

static PyObject *FuzzerTimeDuration_GetMillisecondsAttr(FuzzerTimeDuration *self, void *closure)
{
    Py_INCREF(self->plMilliseconds);
    return self->plMilliseconds;
}

static int FuzzerTimeDuration_SetNanosecondsAttr(FuzzerTimeDuration *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the nanoseconds attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The nanoseconds attribute value must be an int");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->plNanoseconds);
    self->plNanoseconds = value;
    return 0;
}

static PyObject *FuzzerTimeDuration_GetNanosecondsAttr(FuzzerTimeDuration *self, void *closure)
{
    Py_INCREF(self->plNanoseconds);
    return self->plNanoseconds;
}

static int FuzzerTimeDuration_SetStrAttr(FuzzerTimeDuration *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the str attribute");
        return -1;
    }

    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The str attribute value must be a string");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->puStr);
    self->puStr = value;
    return 0;
}

static PyObject *FuzzerTimeDuration_GetStrAttr(FuzzerTimeDuration *self, void *closure)
{
    Py_INCREF(self->puStr);
    return self->puStr;
}

static PyObject *FuzzerTimeDuration_GetHours(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->plHours);
    return self->plHours;
}

static PyObject *FuzzerTimeDuration_GetMinutes(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->plMinutes);
    return self->plMinutes;
}

static PyObject *FuzzerTimeDuration_GetSeconds(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->plSeconds);
    return self->plSeconds;
}

static PyObject *FuzzerTimeDuration_GetMicroseconds(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->plMicroseconds);
    return self->plMicroseconds;
}

static PyObject *FuzzerTimeDuration_GetMilliseconds(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->plMilliseconds);
    return self->plMilliseconds;
}

static PyObject *FuzzerTimeDuration_GetNanoseconds(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->plNanoseconds);
    return self->plNanoseconds;
}

static PyObject *FuzzerTimeDuration_GetStr(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->puStr);
    return self->puStr;
}

static PyObject *FuzzerTimeDuration_Transform(FuzzerTimeDuration *self, PyObject *Py_UNUSED(ignored))
{
    PyObject *pTimeDict;

    /* Initialize our dictionary that hold the data */
    if ( !(pTimeDict = PyDict_New()) )
    {
        PyErr_SetString(PyExc_Exception, "an error occured when initializing the dict");
        return NULL;
    }

    /* Insert the hours to the dict */
    if ( PyDict_SetItemString(pTimeDict, "Hours", PyObject_GetAttrString((PyObject *)self, "hours")) != 0 )
    {
        PyErr_SetString(PyExc_Exception, "an error occurred when inserting the hours to the dict");
        return NULL;
    }


    /* Insert the minutes to the dict */
    if ( PyDict_SetItemString(pTimeDict, "Minutes", PyObject_GetAttrString((PyObject *)self, "minutes")) != 0 )
    {
        PyErr_SetString(PyExc_Exception, "an error occurred when inserting the minutes to the dict");
        return NULL;
    }


    /* Insert the seconds to the dict */
    if ( PyDict_SetItemString(pTimeDict, "Seconds", PyObject_GetAttrString((PyObject *)self, "seconds")) != 0 )
    {
        PyErr_SetString(PyExc_Exception, "an error occurred when inserting the seconds to the dict");
        return NULL;
    }


    /* Insert the microseconds to the dict */
    if ( PyDict_SetItemString(pTimeDict, "Microseconds", PyObject_GetAttrString((PyObject *)self, "microseconds")) != 0 )
    {
        PyErr_SetString(PyExc_Exception, "an error occurred when inserting the microseconds to the dict");
        return NULL;
    }


    /* Insert the milliseconds to the dict */
    if ( PyDict_SetItemString(pTimeDict, "Milliseconds", PyObject_GetAttrString((PyObject *)self, "milliseconds")) != 0 )
    {
        PyErr_SetString(PyExc_Exception, "an error occurred when inserting the milliseconds to the dict");
        return NULL;
    }


    /* Insert the nanoseconds to the dict */
    if ( PyDict_SetItemString(pTimeDict, "Nanoseconds", PyObject_GetAttrString((PyObject *)self, "nanoseconds")) != 0 )
    {
        PyErr_SetString(PyExc_Exception, "an error occurred when inserting the nanoseconds to the dict");
        return NULL;
    }


    /* Insert the str to the dict */
    if ( PyDict_SetItemString(pTimeDict, "Str", PyObject_GetAttrString((PyObject *)self, "str")) != 0 )
    {
        PyErr_SetString(PyExc_Exception, "an error occurred when inserting the str to the dict");
        return NULL;
    }

    return pTimeDict;
}

static int FuzzerResult_init(FuzzerResult *self, PyObject *args, PyObject* kwds)
{
    /* Initialize the parent */
    if ( PyList_Type.tp_init((PyObject *) self, args, kwds) < 0 )
        return -1;

    self->lNumberOfResults = 0;

    return 0;
}

static PyObject *FuzzerResult_GetNumberOfResults(FuzzerResult *self, PyObject *Py_UNUSED(ignored))
{
    return PyLong_FromLong( self->lNumberOfResults );
}

static PyObject *InputDataInNewDict(PyObject *pInputData)
{
    PyObject *pNewDataDict, *pKey, *pValue;
    Py_ssize_t lPos = 0;

    /* Initialize our dictionary that hold the data */
    if ( !(pNewDataDict = PyDict_New()) )
    {
        PyErr_SetString(PyExc_Exception, "an error occurred when initializing the dict");
        return NULL;
    }

    while ( PyDict_Next(pInputData, &lPos, &pKey, &pValue) )
    {
        if ( PyDict_SetItem(pNewDataDict, pKey, PyUnicode_FromEncodedObject(pValue, NULL, NULL)) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting to the dict");
            return NULL;
        }
    }

    return pNewDataDict;
}

static PyObject *FuzzerResult_Transform(FuzzerResult *self, PyObject *Py_UNUSED(ignored))
{

    PyObject *pDataDict, *pItemDict, *pResultItem, *pInputDict, *pKey, *pTime;

    /* Initialize our dictionary that hold the data */
    if ( !(pDataDict = PyDict_New()) )
    {
        PyErr_SetString(PyExc_Exception, "an error occured when initializing the data dict");
        return NULL;
    }

    for (Py_ssize_t lIdx = 0; lIdx < self->lNumberOfResults; lIdx++)
    {
        /* Initialize our dictionary that hold the item */
        if ( !(pItemDict = PyDict_New()) )
        {
            PyErr_SetString(PyExc_Exception, "an error occured when initializing the item dict");
            return NULL;
        }

        /* Get the FuzzerResultItem object */
        pResultItem = PyObject_CallMethod( (PyObject *) self, "__getitem__", "n", lIdx );

        /* Insert the position to the item dict */
        if ( PyDict_SetItemString(pItemDict, "Position", PyObject_GetAttrString(pResultItem, "position")) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting the position to the dict");
            return NULL;
        }

        /* Insert the statuscode to the item dict */
        if ( PyDict_SetItemString(pItemDict, "StatusCode", PyObject_GetAttrString(pResultItem, "statuscode")) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting the statuscode to the dict");
            return NULL;
        }

        /* Insert the contentlength to the item dict */
        if ( PyDict_SetItemString(pItemDict, "ContentLength", PyObject_GetAttrString(pResultItem, "contentlength")) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting the contentlength to the dict");
            return NULL;
        }

        /* Insert the contentwords to the item dict */
        if ( PyDict_SetItemString(pItemDict, "ContentWords", PyObject_GetAttrString(pResultItem, "contentwords")) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting the contentwords to the dict");
            return NULL;
        }

        /* Insert the contentlines to the item dict */
        if ( PyDict_SetItemString(pItemDict, "ContentLines", PyObject_GetAttrString(pResultItem, "contentlines")) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting the contentlines to the dict");
            return NULL;
        }

        /* Insert the contenttype to the item dict */
        if ( PyDict_SetItemString(pItemDict, "ContentType", PyObject_GetAttrString(pResultItem, "contenttype")) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting the contenttype to the dict");
            return NULL;
        }

        /* Insert the redirectlocation to the item dict */
        if ( PyDict_SetItemString(pItemDict, "RedirectLocation", PyObject_GetAttrString(pResultItem, "redirectlocation")) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting the redirectlocation to the dict");
            return NULL;
        }

        /* Insert the url to the item dict */
        if ( PyDict_SetItemString(pItemDict, "Url", PyObject_GetAttrString(pResultItem, "url")) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting the url to the dict");
            return NULL;
        }

        /* Insert the resultfile to the item dict */
        if ( PyDict_SetItemString(pItemDict, "ResultFile", PyObject_GetAttrString(pResultItem, "resultfile")) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting the resultfile to the dict");
            return NULL;
        }

        /* Insert the host to the item dict */
        if ( PyDict_SetItemString(pItemDict, "Host", PyObject_GetAttrString(pResultItem, "host")) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting the host to the dict");
            return NULL;
        }

        /* Insert the htmlcolor to the item dict */
        if ( PyDict_SetItemString(pItemDict, "HTMLColor", PyObject_GetAttrString(pResultItem, "htmlcolor")) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting the htmlcolor to the dict");
            return NULL;
        }

        /* Get the time duration object */
        pTime = PyObject_GetAttrString(pResultItem, "timeduration");

        /* Get the timeduration dict by calling its Transform method and insert it to the item dict */
        if ( PyDict_SetItemString(pItemDict, "TimeDuration", PyObject_CallMethod(pTime, "Transform", NULL)) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting the timeduration to the dict");
            return NULL;
        }

        /* Get InputData dict from the item object */
        pInputDict = PyObject_GetAttrString(pResultItem, "inputdata");

        /* Insert InputData to the item */
        if ( PyDict_SetItemString(pItemDict, "InputData", InputDataInNewDict(pInputDict)) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting the inputdata to the dict");
            return NULL;
        }
        
        /* Get the encoded hash from the inputdata dict and decode it to use as a dict key */
        pKey = PyUnicode_FromEncodedObject(PyDict_GetItemString(pInputDict, "FFUFHASH"), NULL, NULL);
        
        if ( pKey )
            /* Insert the item dict to the data dict */
            if ( PyDict_SetItem(pDataDict, pKey, pItemDict) != 0 )
            {
                PyErr_SetString(PyExc_Exception, "an error occurred when inserting the item to the dict");
                return NULL;
            }
    }
    
    
    return pDataDict;
}

static int FuzzerResultItem_traverse(FuzzerResultItem *self, visitproc visit, void *arg)
{
    Py_VISIT(self->pInput);
    Py_VISIT(self->plPosition);
    Py_VISIT(self->plStatusCode);
    Py_VISIT(self->plContentLength);
    Py_VISIT(self->plContentWords);
    Py_VISIT(self->plContentLines);
    Py_VISIT(self->puContentType);
    Py_VISIT(self->puRedirectLocation);
    Py_VISIT(self->puUrl);
    Py_VISIT(self->puResultFile);
    Py_VISIT(self->puHost);
    Py_VISIT(self->puHTMLColor);
    Py_VISIT(self->pScraperData);
    Py_VISIT(self->pTimeDuration);
    
   return 0;
}

static int FuzzerResultItem_clear(FuzzerResultItem *self)
{
    Py_CLEAR(self->pInput);
    Py_CLEAR(self->plPosition);
    Py_CLEAR(self->plStatusCode);
    Py_CLEAR(self->plContentLength);
    Py_CLEAR(self->plContentWords);
    Py_CLEAR(self->plContentLines);
    Py_CLEAR(self->puContentType);
    Py_CLEAR(self->puRedirectLocation);
    Py_CLEAR(self->puUrl);
    Py_CLEAR(self->puResultFile);
    Py_CLEAR(self->puHost);
    Py_CLEAR(self->puHTMLColor);
    Py_CLEAR(self->pScraperData);
    Py_CLEAR(self->pTimeDuration);
    
    return 0;
}

static PyObject *FuzzerResultItem_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    FuzzerResultItem *self;

    /* Allocate memory for our class */
    self = (FuzzerResultItem *) type->tp_alloc(type, 0);

    if ( self ) {
        if (!(
            (self->pInput = PyDict_New()) ||
            (self->plPosition = PyLong_FromLong(0)) ||
            (self->plStatusCode = PyLong_FromLong(0)) ||
            (self->plContentLength = PyLong_FromLong(0)) ||
            (self->plContentWords = PyLong_FromLong(0)) ||
            (self->plContentLines = PyLong_FromLong(0)) ||
            (self->puContentType = PyUnicode_FromString("")) ||
            (self->puRedirectLocation = PyUnicode_FromString("")) ||
            (self->puUrl = PyUnicode_FromString("")) ||
            (self->puResultFile = PyUnicode_FromString("")) ||
            (self->puHost = PyUnicode_FromString("")) ||
            (self->puHTMLColor = PyUnicode_FromString("")) ||
            (self->pScraperData = PyDict_New()) ||
            (self->pTimeDuration = Py_None)
        )) {
            /* initialization failed */

            Py_DECREF(self);
            return NULL;
        }
    }

    return (PyObject *) self;
}

static void FuzzerResultItem_dealloc(FuzzerResultItem *self)
{
    PyObject_GC_UnTrack(self);
    FuzzerResultItem_clear(self);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static int FuzzerResultItem_SetInputDataAttr(FuzzerResultItem *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the inputdata attribute");
        return -1;
    }

    if (!PyDict_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The inputdata attribute value must be a dict");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->pInput);
    self->pInput = value;
    return 0;
}

static PyObject *FuzzerResultItem_GetInputDataAttr(FuzzerResultItem *self, void *closure)
{
    Py_INCREF(self->pInput);
    return self->pInput;
}

static int FuzzerResultItem_SetPositionAttr(FuzzerResultItem *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the position attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The position attribute value must be an int");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->plPosition);
    self->plPosition = value;
    return 0;
}

static PyObject *FuzzerResultItem_GetPositionAttr(FuzzerResultItem *self, void *closure)
{
    Py_INCREF(self->plPosition);
    return self->plPosition;
}

static int FuzzerResultItem_SetStatusCodeAttr(FuzzerResultItem *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the statuscode attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The statuscode attribute value must be an int");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->plStatusCode);
    self->plStatusCode = value;
    return 0;
}

static PyObject *FuzzerResultItem_GetStatusCodeAttr(FuzzerResultItem *self, void *closure)
{
    Py_INCREF(self->plStatusCode);
    return self->plStatusCode;
}

static int FuzzerResultItem_SetContentLengthAttr(FuzzerResultItem *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the contentlength attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The contentlength attribute value must be an int");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->plContentLength);
    self->plContentLength = value;
    return 0;
}

static PyObject *FuzzerResultItem_GetContentLengthAttr(FuzzerResultItem *self, void *closure)
{
    Py_INCREF(self->plContentLength);
    return self->plContentLength;
}

static int FuzzerResultItem_SetContentWordsAttr(FuzzerResultItem *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the contentwords attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The contentwords attribute value must be an int");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->plContentWords);
    self->plContentWords = value;
    return 0;
}

static PyObject *FuzzerResultItem_GetContentWordsAttr(FuzzerResultItem *self, void *closure)
{
    Py_INCREF(self->plContentWords);
    return self->plContentWords;
}

static int FuzzerResultItem_SetContentLinesAttr(FuzzerResultItem *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the contentlines attribute");
        return -1;
    }

    if (!PyLong_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The contentlines attribute value must be an int");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->plContentLines);
    self->plContentLines = value;
    return 0;
}

static PyObject *FuzzerResultItem_GetContentLinesAttr(FuzzerResultItem *self, void *closure)
{
    Py_INCREF(self->plContentLines);
    return self->plContentLines;
}

static int FuzzerResultItem_SetContentTypeAttr(FuzzerResultItem *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the contenttype attribute");
        return -1;
    }

    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The contenttype attribute value must be a string");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->puContentType);
    self->puContentType = value;
    return 0;
}

static PyObject *FuzzerResultItem_GetContentTypeAttr(FuzzerResultItem *self, void *closure)
{
    Py_INCREF(self->puContentType);
    return self->puContentType;
}

static int FuzzerResultItem_SetRedirectLocationAttr(FuzzerResultItem *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the redirectlocation attribute");
        return -1;
    }

    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The redirectlocation attribute value must be a string");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->puRedirectLocation);
    self->puRedirectLocation = value;
    return 0;
}

static PyObject *FuzzerResultItem_GetRedirectLocationAttr(FuzzerResultItem *self, void *closure)
{
    Py_INCREF(self->puRedirectLocation);
    return self->puRedirectLocation;
}

static int FuzzerResultItem_SetUrlAttr(FuzzerResultItem *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the url attribute");
        return -1;
    }

    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The url attribute value must be a string");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->puUrl);
    self->puUrl = value;
    return 0;
}

static PyObject *FuzzerResultItem_GetUrlAttr(FuzzerResultItem *self, void *closure)
{
    Py_INCREF(self->puUrl);
    return self->puUrl;
}

static int FuzzerResultItem_SetResultFileAttr(FuzzerResultItem *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the resultfile attribute");
        return -1;
    }

    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The resultfile attribute value must be a string");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->puResultFile);
    self->puResultFile = value;
    return 0;
}

static PyObject *FuzzerResultItem_GetResultFileAttr(FuzzerResultItem *self, void *closure)
{
    Py_INCREF(self->puResultFile);
    return self->puResultFile;
}

static int FuzzerResultItem_SetHostAttr(FuzzerResultItem *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the host attribute");
        return -1;
    }

    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The host attribute value must be a string");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->puHost);
    self->puHost = value;
    return 0;
}

static PyObject *FuzzerResultItem_GetHostAttr(FuzzerResultItem *self, void *closure)
{
    Py_INCREF(self->puHost);
    return self->puHost;
}

static int FuzzerResultItem_SetHTMLColorAttr(FuzzerResultItem *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the htmlcolor attribute");
        return -1;
    }

    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The htmlcolor attribute value must be a string");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->puHTMLColor);
    self->puHTMLColor = value;
    return 0;
}

static PyObject *FuzzerResultItem_GetHTMLColorAttr(FuzzerResultItem *self, void *closure)
{
    Py_INCREF(self->puHTMLColor);
    return self->puHTMLColor;
}

static int FuzzerResultItem_SetScraperDataAttr(FuzzerResultItem *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the scraperdata attribute");
        return -1;
    }

    if (!PyDict_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The scraper attribute value must be a dict");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->pScraperData);
    self->pScraperData = value;
    return 0;
}

static PyObject *FuzzerResultItem_GetScraperDataAttr(FuzzerResultItem *self, void *closure)
{
    Py_INCREF(self->pScraperData);
    return self->pScraperData;
}

static int FuzzerResultItem_SetTimeDurationAttr(FuzzerResultItem *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the timeduration attribute");
        return -1;
    }

    Py_INCREF(value);
    Py_CLEAR(self->pTimeDuration);
    self->pTimeDuration = value;
    return 0;
}

static PyObject *FuzzerResultItem_GetTimeDurationAttr(FuzzerResultItem *self, void *closure)
{
    Py_INCREF(self->pTimeDuration);
    return self->pTimeDuration;
}

static PyObject *FuzzerResultItem_GetInputData(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->pInput);
    return self->pInput;
}

static PyObject *FuzzerResultItem_GetPosition(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->plPosition);
    return self->plPosition;
}

static PyObject *FuzzerResultItem_GetStatusCode(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->plStatusCode);
    return self->plStatusCode;
}

static PyObject *FuzzerResultItem_GetContentLength(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->plContentLength);
    return self->plContentLength;
}

static PyObject *FuzzerResultItem_GetContentWords(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->plContentWords);
    return self->plContentWords;
}

static PyObject *FuzzerResultItem_GetContentLines(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->plContentLines);
    return self->plContentLines;
}

static PyObject *FuzzerResultItem_GetContentType(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->puContentType);
    return self->puContentType;
}

static PyObject *FuzzerResultItem_GetRedirectLocation(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->puRedirectLocation);
    return self->puRedirectLocation;
}

static PyObject *FuzzerResultItem_GetUrl(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->puUrl);
    return self->puUrl;
}

static PyObject *FuzzerResultItem_GetResultFile(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->puResultFile);
    return self->puResultFile;
}

static PyObject *FuzzerResultItem_GetHost(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->puHost);
    return self->puHost;
}

static PyObject *FuzzerResultItem_GetHTMLColor(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->puHTMLColor);
    return self->puHTMLColor;
}

static PyObject *FuzzerResultItem_GetScraperData(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->pScraperData);
    return self->pScraperData;
}

static PyObject *FuzzerResultItem_GetTimeDuration(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    Py_INCREF(self->pTimeDuration);
    return self->pTimeDuration;
}

static PyObject *FuzzerResultItem_GetFuzzingWords(FuzzerResultItem *self, PyObject *Py_UNUSED(ignored))
{
    PyObject *pInputDict, *pWordsList, *pKey, *pValue;
    Py_ssize_t lPos = 0;

    /* Initialize the list and except error if init failed */
    if ( !(pWordsList = PyList_New(0)) ) {
        PyErr_SetString(PyExc_Exception, "an error occurred when initializing the list");
        return NULL;
    }

    /* Get the InputData dict */
    pInputDict = PyObject_GetAttrString((PyObject *) self, "inputdata");

    while ( PyDict_Next(pInputDict, &lPos, &pKey, &pValue) )
    {
        /* Skip FFUFHASH key */
        if ( PyUnicode_CompareWithASCIIString(pKey, "FFUFHASH") == 0 )
            continue;

        /* Insert decoded fuzzing word */
        if( PyList_Append(pWordsList, PyUnicode_FromEncodedObject(pValue, NULL, NULL)) != 0 )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when inserting fuzzing word to the list");
            return NULL;
        }
    }

    return pWordsList;
}

static PyObject *Fuzzer_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    Fuzzer *self;

    /* Allocate memory for the fuzzer */
    self = (Fuzzer *) type->tp_alloc(type, 0);

    if ( self ) {
        /*
            Fuzzer doesn't have composed objects right now.
        */
    }

    return (PyObject *) self;
}

static int Fuzzer_init(Fuzzer *self, PyObject *args, PyObject* kwds)
{
    PyObject *pUrl, *pHeaders, *pWordlists;
    int nThreads, nRecursion, nDepth, nTimeout;

    char **cpHeaders, **cpWordlists;

    static char *kwlist[] = {
        "url",
        "headers",
        "wordlists",
        "threads",
        "recursion",
        "depth",
        "timeout",
        NULL
    };

    pUrl = pHeaders = pWordlists = NULL;
    nThreads = nRecursion = nDepth = nTimeout = 0;

    if (
        !PyArg_ParseTupleAndKeywords(
            args,
            kwds,
            "UOO|iiii",
            kwlist,
            &pUrl,
            &pHeaders,
            &pWordlists,
            &nThreads,
            &nRecursion,
            &nDepth,
            &nTimeout
        )
    ) {
        return -1;
    }

    if ( !pUrl || !pWordlists || !pHeaders )
        return -1;

    if ( !PyDict_Check(pHeaders) || !PyList_Check(pWordlists) )
        return -1;

    if ( !nThreads )
        nThreads = 40;

    if ( nRecursion && !nDepth )
        nDepth = 2;

    if ( !nTimeout )
        nTimeout = 10;

    
    Py_INCREF(pUrl);
    Py_INCREF(pHeaders);
    Py_INCREF(pWordlists);

    cpWordlists = PyListToArray(pWordlists);
    cpHeaders = ParseHeaders(pHeaders);

    FfufInit(
        BuildGoStr(pUrl),
        cpHeaders,
        (GoInt) PyDict_Size(pHeaders),
        cpWordlists,
        (GoInt) PyList_Size(pWordlists),
        (GoInt) nThreads,
        (GoUint8) nRecursion,
        (GoInt) nDepth,
        (GoInt) nTimeout
    );

    FreeMemory(cpWordlists);
    FreeMemory(cpHeaders);

    return 0;
}

static void Fuzzer_dealloc(Fuzzer *self)
{
    PyObject_GC_UnTrack(self);
    Fuzzer_clear(self);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static int Fuzzer_traverse(Fuzzer *self, visitproc visit, void *arg)
{
    /*
        Fuzzer doesn't have composed objects to visit.
    */

    return 0;
}

static int Fuzzer_clear(Fuzzer *self)
{
    /*
        Fuzzer doesn't have composed objects to clear.
    */

    return 0;
}

static PyObject *Fuzzer_GetVersion(Fuzzer *self, PyObject *args)
{
    PyObject *pVersion;
    char *cpVersion;

    cpVersion = FfufGetVersion();
    pVersion = PyUnicode_FromString(cpVersion);
    PyMem_Free(cpVersion);

    return pVersion;
}

static PyObject *Fuzzer_SetMethod(Fuzzer *self, PyObject *args)
{
    PyObject *pMethod = NULL;

    /* Parse arguments */
    if( !PyArg_ParseTuple(args, "U", &pMethod) ) 
        return NULL;

    if ( !pMethod )
    {
        PyErr_SetString(PyExc_Exception, "this method takes exactly one argument");
        return NULL;
    }

    if ( !PyUnicode_Check(pMethod) )
    {
        PyErr_SetString(PyExc_TypeError, "The method must be a string");
        return NULL;
    }
    
    Py_INCREF(pMethod);
    FfufSetMethod( BuildGoStr(pMethod) );

    Py_RETURN_NONE;
}

static PyObject *Fuzzer_SetData(Fuzzer *self, PyObject *args)
{
    PyObject *pData = NULL;

    /* Parse arguments */
    if( !PyArg_ParseTuple(args, "U", &pData) ) 
        return NULL;

    if ( !pData )
    {
        PyErr_SetString(PyExc_Exception, "this method takes exactly one argument");
        return NULL;
    }

    if ( !PyUnicode_Check(pData) )
    {
        PyErr_SetString(PyExc_TypeError, "The data must be a string");
        return NULL;
    }
    
    Py_INCREF(pData);
    FfufSetData( BuildGoStr(pData) );

    Py_RETURN_NONE;
}

static PyObject *Fuzzer_SetConfigFile(Fuzzer *self, PyObject *args)
{
    PyObject *pConfigFile = NULL;

    /* Parse arguments */
    if( !PyArg_ParseTuple(args, "U", &pConfigFile) ) 
        return NULL;

    if ( !pConfigFile )
    {
        PyErr_SetString(PyExc_Exception, "this method takes exactly one argument");
        return NULL;
    }

    if ( !PyUnicode_Check(pConfigFile) )
    {
        PyErr_SetString(PyExc_TypeError, "The configfile must be a string");
        return NULL;
    }
    
    Py_INCREF(pConfigFile);
    FfufSetConfigFile( BuildGoStr(pConfigFile) );

    Py_RETURN_NONE;
}

static PyObject *Fuzzer_SetInputMode(Fuzzer *self, PyObject *args)
{
    PyObject *pInputMode = NULL;

    /* Parse arguments */
    if( !PyArg_ParseTuple(args, "U", &pInputMode) ) 
        return NULL;

    if ( !pInputMode )
    {
        PyErr_SetString(PyExc_Exception, "this method takes exactly one argument");
        return NULL;
    }

    if ( !PyUnicode_Check(pInputMode) )
    {
        PyErr_SetString(PyExc_TypeError, "The inputmode must be a string");
        return NULL;
    }
    
    Py_INCREF(pInputMode);
    FfufSetInputMode( BuildGoStr(pInputMode) );

    Py_RETURN_NONE;
}

static PyObject *Fuzzer_SetInputCommands(Fuzzer *self, PyObject *args)
{
    PyObject *pInputCommands = NULL;
    char **cpInputCommands;

    /* Parse arguments */
    if( !PyArg_ParseTuple(args, "O", &pInputCommands) ) 
        return NULL;

    if ( !pInputCommands )
    {
        PyErr_SetString(PyExc_Exception, "this method takes exactly one argument");
        return NULL;
    }

    if ( !PyList_Check(pInputCommands) )
    {
        PyErr_SetString(PyExc_TypeError, "The inputcommands must be a list");
        return NULL;
    }
    
    if ( !(cpInputCommands = PyListToArray(pInputCommands)) )
        return NULL;

    Py_INCREF(pInputCommands);
    FfufSetInputCommands(cpInputCommands, (GoInt)PyList_Size(pInputCommands));
    FreeMemory( cpInputCommands );

    Py_RETURN_NONE;
}

static PyObject *Fuzzer_SetRequestFile(Fuzzer *self, PyObject *args)
{
    PyObject *pRequestFile = NULL;

    /* Parse arguments */
    if( !PyArg_ParseTuple(args, "U", &pRequestFile) ) 
        return NULL;

    if ( !pRequestFile )
    {
        PyErr_SetString(PyExc_Exception, "this method takes exactly one argument");
        return NULL;
    }

    if ( !PyUnicode_Check(pRequestFile) )
    {
        PyErr_SetString(PyExc_TypeError, "The requestfile must be a string");
        return NULL;
    }

    Py_INCREF(pRequestFile);
    FfufSetRequestFile( BuildGoStr(pRequestFile) );

    Py_RETURN_NONE;
}

static PyObject *Fuzzer_SetAutoCalibrationStrategy(Fuzzer *self, PyObject *args)
{
    PyObject *pAutoCalibrationStrategy = NULL;

    /* Parse arguments */
    if( !PyArg_ParseTuple(args, "U", &pAutoCalibrationStrategy) ) 
        return NULL;

    if ( !pAutoCalibrationStrategy )
    {
        PyErr_SetString(PyExc_Exception, "this method takes exactly one argument");
        return NULL;
    }

    if ( !PyUnicode_Check(pAutoCalibrationStrategy) )
    {
        PyErr_SetString(PyExc_TypeError, "The autocalibrationstrategy must be a string");
        return NULL;
    }

    Py_INCREF(pAutoCalibrationStrategy);
    
    FfufSetAutoCalibrationStrategy( BuildGoStr(pAutoCalibrationStrategy) );

    Py_RETURN_NONE;
}

static PyObject *Fuzzer_SetRecursionStrategy(Fuzzer *self, PyObject *args)
{
    PyObject *pRecursionStrategy = NULL;

    /* Parse arguments */
    if( !PyArg_ParseTuple(args, "U", &pRecursionStrategy) ) 
        return NULL;

    if ( !pRecursionStrategy )
    {
        PyErr_SetString(PyExc_Exception, "this method takes exactly one argument");
        return NULL;
    }

    if ( !PyUnicode_Check(pRecursionStrategy) )
    {
        PyErr_SetString(PyExc_TypeError, "The recursionstrategy must be a string");
        return NULL;
    }

    Py_INCREF(pRecursionStrategy);
    FfufSetRecursionStrategy( BuildGoStr(pRecursionStrategy) );

    Py_RETURN_NONE;
}

static PyObject *Fuzzer_SetRequestProto(Fuzzer *self, PyObject *args)
{
    PyObject *pRequestProto = NULL;

    /* Parse arguments */
    if( !PyArg_ParseTuple(args, "U", &pRequestProto) ) 
        return NULL;

    if ( !pRequestProto )
    {
        PyErr_SetString(PyExc_Exception, "this method takes exactly one argument");
        return NULL;
    }

    if ( !PyUnicode_Check(pRequestProto) )
    {
        PyErr_SetString(PyExc_TypeError, "The requestproto must be a string");
        return NULL;
    }

    Py_INCREF(pRequestProto);
    FfufSetRequestProto( BuildGoStr(pRequestProto) );

    Py_RETURN_NONE;
}

static PyObject *Fuzzer_SetScrapers(Fuzzer *self, PyObject *args)
{
    PyObject *pScrapers = NULL;

    /* Parse arguments */
    if( !PyArg_ParseTuple(args, "U", &pScrapers) ) 
        return NULL;

    if ( !pScrapers )
    {
        PyErr_SetString(PyExc_Exception, "this method takes exactly one argument");
        return NULL;
    }

    if ( !PyUnicode_Check(pScrapers) )
    {
        PyErr_SetString(PyExc_TypeError, "The scrapers must be a string");
        return NULL;
    }

    Py_INCREF(pScrapers);
    FfufSetScrapers( BuildGoStr(pScrapers) );

    Py_RETURN_NONE;
}

static PyObject *Fuzzer_SetMatcherMode(Fuzzer *self, PyObject *args)
{
    PyObject *pMatcherMode = NULL;

    /* Parse arguments */
    if( !PyArg_ParseTuple(args, "U", &pMatcherMode) ) 
        return NULL;

    if ( !pMatcherMode )
    {
        PyErr_SetString(PyExc_Exception, "this method takes exactly one argument");
        return NULL;
    }

    if ( !PyUnicode_Check(pMatcherMode) )
    {
        PyErr_SetString(PyExc_TypeError, "The matchermode must be a string");
        return NULL;
    }

    Py_INCREF(pMatcherMode);
    FfufSetMatcherMode( BuildGoStr(pMatcherMode) );

    Py_RETURN_NONE;
}

static PyObject *Fuzzer_SetFilterMode(Fuzzer *self, PyObject *args)
{
    PyObject *pFilterMode = NULL;

    /* Parse arguments */
    if( !PyArg_ParseTuple(args, "U", &pFilterMode) ) 
        return NULL;

    if ( !pFilterMode )
    {
        PyErr_SetString(PyExc_Exception, "this method takes exactly one argument");
        return NULL;
    }

    if ( !PyUnicode_Check(pFilterMode) )
    {
        PyErr_SetString(PyExc_TypeError, "The filtermode must be a string");
        return NULL;
    }

    Py_INCREF(pFilterMode);
    FfufSetFilterMode( BuildGoStr(pFilterMode) );

    Py_RETURN_NONE;
}

static PyObject *Fuzzer_AddMatcher(Fuzzer *self, PyObject *args)
{
    PyObject *pMatcherName, *pMatcherVal;
    
    pMatcherName = pMatcherVal = NULL;

    /* Parse arguments */
    if( !PyArg_ParseTuple(args, "UU", &pMatcherName, &pMatcherVal) ) 
        return NULL;

    if ( !pMatcherName || !pMatcherVal )
    {
        PyErr_SetString(PyExc_Exception, "this method takes exactly two arguments");
        return NULL;
    }

    if ( !PyUnicode_Check(pMatcherName) || !PyUnicode_Check(pMatcherVal) )
    {
        PyErr_SetString(PyExc_TypeError, "The matchername and matchervalue must be a string");
        return NULL;
    }

    Py_INCREF(pMatcherName);
    Py_INCREF(pMatcherVal);
    
    FfufAddMatcher( BuildGoStr(pMatcherName), BuildGoStr(pMatcherVal) );

    Py_RETURN_NONE;
}

static PyObject *Fuzzer_AddFilter(Fuzzer *self, PyObject *args)
{
    PyObject *pFilterName, *pFilterVal;
    
    pFilterName = pFilterVal = NULL;

    /* Parse arguments */
    if( !PyArg_ParseTuple(args, "UU", &pFilterName, &pFilterVal) ) 
        return NULL;

    if ( !pFilterName || !pFilterVal )
    {
        PyErr_SetString(PyExc_Exception, "this method takes exactly two arguments");
        return NULL;
    }

    if ( !PyUnicode_Check(pFilterName) || !PyUnicode_Check(pFilterVal) )
    {
        PyErr_SetString(PyExc_TypeError, "The filtername and filtervalue must be a string");
        return NULL;
    }

    Py_INCREF(pFilterName);
    Py_INCREF(pFilterVal);
    
    FfufAddFilter( BuildGoStr(pFilterName), BuildGoStr(pFilterVal) );

    Py_RETURN_NONE;
}

static PyObject *StoreInputData(InputData **pInputData)
{
    PyObject *pInputDataDict;

    /* Initialize our dictionary that hold the input data */
    if ( !(pInputDataDict = PyDict_New()) )
    {
        PyErr_SetString(PyExc_Exception, "an error occured when initializing the data dict");
        return NULL;
    }

    if ( pInputData && *pInputData )
        do {

            /* Insert the input data to the dict */
            if ( PyDict_SetItemString(pInputDataDict, (*pInputData)->cpName, PyBytes_FromStringAndSize((const char *)(*pInputData)->pData, (Py_ssize_t)(*pInputData)->lSize)) != 0 )
            {
                PyErr_SetString(PyExc_Exception, "an error occurred when inserting the input data to the dict");
                return NULL;
            }

        } while( *(++pInputData) );
    
    
    return pInputDataDict;
}

static PyObject *StoreScraperData(ScraperData **pScraperData)
{
    PyObject *pScraperDataDict;

    /* Initialize our dictionary that hold the scraper data */
    if ( !(pScraperDataDict = PyDict_New()) )
    {
        PyErr_SetString(PyExc_Exception, "an error occured when initializing the data dict");
        return NULL;
    }

    if ( pScraperData && *pScraperData )
        do {

            /* Insert the scraper data to the dict */
            if ( PyDict_SetItemString(pScraperDataDict, (*pScraperData)->cpName, StoreResults( (*pScraperData)->cpData )) != 0 )
            {
                PyErr_SetString(PyExc_Exception, "an error occurred when inserting the scraper data to the dict");
                return NULL;
            }
            
        } while( *(++pScraperData) );
    

    return pScraperDataDict;
}

static PyObject *StoreTimeDuration(TimeDuration *pTimeDuration)
{
    /* Create a python instance of TimeDuration class */
    PyObject *pObj = PyObject_CallObject((PyObject *)&FuzzerTimeDurationType, NULL);

    PyObject_SetAttrString(pObj, "hours", PyLong_FromDouble(pTimeDuration->dHours));
    PyObject_SetAttrString(pObj, "minutes", PyLong_FromDouble(pTimeDuration->dMinutes));
    PyObject_SetAttrString(pObj, "seconds", PyLong_FromDouble(pTimeDuration->dSeconds));
    PyObject_SetAttrString(pObj, "microseconds", PyLong_FromLongLong(pTimeDuration->llMicroseconds));
    PyObject_SetAttrString(pObj, "milliseconds", PyLong_FromLongLong(pTimeDuration->llMilliseconds));
    PyObject_SetAttrString(pObj, "nanoseconds", PyLong_FromLongLong(pTimeDuration->llNanoseconds));
    PyObject_SetAttrString(pObj, "str", PyUnicode_FromString(pTimeDuration->cpStr));

    return pObj;
}

static PyObject *StoreFuzzerResult(FfufResult **pFfufResults)
{
    PyObject *pResult, *pResultItem;
    FfufResult *pFfufResult;

    /* Create a python instance of FuzzerResult class */
    pResult = PyObject_CallObject((PyObject *)&FuzzerResultType, NULL);

    while ( pFfufResult = *pFfufResults++ )
    {
        /* Create a python instance of FuzzerResultItem class */
        pResultItem = PyObject_CallObject((PyObject *)&FuzzerResultItemType, NULL);

        /* Store results in the item object via its attributes */
        PyObject_SetAttrString(pResultItem, "inputdata", StoreInputData(pFfufResult->pInput));
        PyObject_SetAttrString(pResultItem, "position", PyLong_FromLong(pFfufResult->nPosition));
        PyObject_SetAttrString(pResultItem, "statuscode", PyLong_FromLong(pFfufResult->llStatusCode));
        PyObject_SetAttrString(pResultItem, "contentlength", PyLong_FromLong(pFfufResult->llContentLength));
        PyObject_SetAttrString(pResultItem, "contentwords", PyLong_FromLong(pFfufResult->llContentWords));
        PyObject_SetAttrString(pResultItem, "contentlines", PyLong_FromLong(pFfufResult->llContentLines));
        PyObject_SetAttrString(pResultItem, "contenttype", PyUnicode_FromString(pFfufResult->cpContentType));
        PyObject_SetAttrString(pResultItem, "redirectlocation", PyUnicode_FromString(pFfufResult->cpRedirectLocation));
        PyObject_SetAttrString(pResultItem, "url", PyUnicode_FromString(pFfufResult->cpUrl));
        PyObject_SetAttrString(pResultItem, "resultfile", PyUnicode_FromString(pFfufResult->cpResultFile));
        PyObject_SetAttrString(pResultItem, "host", PyUnicode_FromString(pFfufResult->cpHost));
        PyObject_SetAttrString(pResultItem, "htmlcolor", PyUnicode_FromString(pFfufResult->cpHTMLColor));
        PyObject_SetAttrString(pResultItem, "scraperdata", StoreScraperData(pFfufResult->pScraperData));
        PyObject_SetAttrString(pResultItem, "timeduration", StoreTimeDuration(pFfufResult->pTimeDuration));

        /* Append item to the main result object */
        if ( !PyObject_CallMethod(pResult, "append", "O", pResultItem) )
        {
            PyErr_SetString(PyExc_Exception, "an error occurred when appending a result to the list");
            return NULL;
        }

        /* Count the number of result items */
        ( (FuzzerResult *) pResult )->lNumberOfResults++;
    }

    return pResult;
    
}

static void FreeFuzzerMemory(FfufResult **pFfufResults)
{
    for (FfufResult **pTempResults = pFfufResults; *pTempResults; pTempResults++)
    {
        if ( ( *pTempResults )->pInput )
        {
            for (InputData **pTempInput = ( *pTempResults )->pInput; *pTempInput; pTempInput++)
            {
                PyMem_Free( ( *pTempInput )->cpName );
                PyMem_Free( ( *pTempInput )->pData );
                PyMem_Free( *pTempInput );
            }
            
            PyMem_Free( ( *pTempResults )->pInput );
        }

        if ( ( *pTempResults )->pScraperData )
        {
            for (ScraperData **pTempScraperData = ( *pTempResults )->pScraperData; *pTempScraperData; pTempScraperData++)
            {
                PyMem_Free( ( *pTempScraperData )->cpName );
                FreeMemory( ( *pTempScraperData )->cpData );
                PyMem_Free( *pTempScraperData );
            }
            
            PyMem_Free( ( *pTempResults )->pScraperData );
        }

        if ( ( *pTempResults )->pTimeDuration )
        {
            PyMem_Free( ( *pTempResults )->pTimeDuration->cpStr );
            PyMem_Free( ( *pTempResults )->pTimeDuration );
        }

        PyMem_Free( ( *pTempResults )->cpContentType );
        PyMem_Free( ( *pTempResults )->cpHost );
        PyMem_Free( ( *pTempResults )->cpHTMLColor );
        PyMem_Free( ( *pTempResults )->cpRedirectLocation );
        PyMem_Free( ( *pTempResults )->cpResultFile );
        PyMem_Free( ( *pTempResults )->cpUrl );
        PyMem_Free( *pTempResults );
    }
    
    PyMem_Free(pFfufResults);
}

static PyObject *Fuzzer_Start(Fuzzer *self, PyObject *Py_UNUSED(ignored))
{
    FfufResult **pFfufResult;
    PyObject *pResult;
    char*cpError;
    
    /* Start fuzzing */
    if ( !(pFfufResult = FfufStart()) )
    {
        if ( cpError = FfufGetLastError() )
        {
            PyErr_SetString(PyExc_Exception, cpError);
            PyMem_Free(cpError);
        }

        else
            PyErr_SetString(PyExc_Exception, "Fuzzer failed");
            
        return NULL;
    }

    /* Store results in a prepared python object */
    pResult = StoreFuzzerResult(pFfufResult);

    /* Free Memory */
    FreeFuzzerMemory(pFfufResult);

    return pResult;
}

PyMODINIT_FUNC PyInit_ffuf(void)
{
    PyObject *m;

    if (PyType_Ready(&FuzzerType) < 0)
        return NULL;

    if (PyType_Ready(&FuzzerResultItemType) < 0)
        return NULL;

    if (PyType_Ready(&FuzzerResultType) < 0)
        return NULL;

    if (PyType_Ready(&FuzzerTimeDurationType) < 0)
        return NULL;

    if ( !(m = PyModule_Create(&ffufmodule)) )
        return NULL;

    Py_INCREF(&FuzzerType);
    Py_INCREF(&FuzzerResultItemType);
    Py_INCREF(&FuzzerResultType);
    Py_INCREF(&FuzzerTimeDurationType);

    if (
        PyModule_AddObject(m, "Fuzzer", (PyObject *) &FuzzerType) < 0 ||
        PyModule_AddObject(m, "FuzzerResultItem", (PyObject *) &FuzzerResultItemType) < 0 ||
        PyModule_AddObject(m, "FuzzerResult", (PyObject *) &FuzzerResultType) < 0 ||
        PyModule_AddObject(m, "TimeDuration", (PyObject *) &FuzzerTimeDurationType) < 0
    ) {
        Py_DECREF(&FuzzerType);
        Py_DECREF(&FuzzerResultItemType);
        Py_DECREF(&FuzzerResultType);
        Py_DECREF(&FuzzerTimeDurationType);
        Py_DECREF(&m);
        return NULL;
    }

    return m;
}