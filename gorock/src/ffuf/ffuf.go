/*
	Author	=> Abdallah Mohamed
	Email	=> elsharifabdallah53@gmail.com
	Date	=> 4-7-2023/10:24PM
*/

package main

/*

typedef struct {
	void *pData;
	signed long lSize; // Py_ssize_t
} Content;

typedef struct {
	char *cpName;
	void *pData;
	signed long lSize; // Py_ssize_t
} InputData;

typedef struct {
	char *cpName;
	char **cpData;
} ScraperData;

typedef struct  {
	double dHours;
	double dMinutes;
	double dSeconds;
	long long llMicroseconds;
	long long llMilliseconds;
	long long llNanoseconds;
	char *cpStr;
} TimeDuration;

typedef struct {
	InputData **pInput;
	int nPosition;
	long long llStatusCode, llContentLength, llContentWords, llContentLines;
	char *cpContentType, *cpRedirectLocation, *cpUrl, *cpResultFile, *cpHost, *cpHTMLColor;
	ScraperData **pScraperData;
	TimeDuration *pTimeDuration;
	Content *pContent;
} FfufResult;

*/
import "C"

import (
	"context"
	"fmt"
	"io"
	"log"
	"time"
	"unsafe"

	"github.com/abdallah-elsharif/WRock/gorock/src/ffuf/pkg/ffuf"
	"github.com/abdallah-elsharif/WRock/gorock/src/ffuf/pkg/filter"
	"github.com/abdallah-elsharif/WRock/gorock/src/ffuf/pkg/input"
	"github.com/abdallah-elsharif/WRock/gorock/src/ffuf/pkg/output"
	"github.com/abdallah-elsharif/WRock/gorock/src/ffuf/pkg/runner"
	"github.com/abdallah-elsharif/WRock/gorock/src/ffuf/pkg/scraper"
)

type Matcher struct {
	Name  string
	Value string
}

type Filter struct {
	Name  string
	Value string
}

type Ffuf struct {
	opts     *ffuf.ConfigOptions
	config   *ffuf.Config
	matchers []Matcher
	filters  []Filter
}

var pFfuf Ffuf
var gErr string

func Init(
	url string,
	headers []string,
	wordlists []string,
	threads int,
	recursion bool,
	depth int,
	timeout int,
) error {

	var err error

	// Disabling logging
	log.SetOutput(io.Discard)

	// Config will be initialized when starting
	pFfuf.config = nil

	pFfuf.matchers = make([]Matcher, 0)
	pFfuf.filters = make([]Filter, 0)

	// prepare the default config options
	pFfuf.opts, err = ffuf.ReadDefaultConfig()

	// set params
	SetOpts(pFfuf.opts, url, headers, wordlists, threads, recursion, depth, timeout)

	return err
}

//export FfufInit
func FfufInit(
	url string,
	headers **C.char,
	headersSize int,
	wordlists **C.char,
	wordlistsSize int,
	threads int,
	recursion bool,
	depth int,
	timeout int,
) {
	goheaders := CStrArrToGo(headers, headersSize)
	gowordlists := CStrArrToGo(wordlists, wordlistsSize)

	// Initialize ffuf
	err := Init(url, goheaders, gowordlists, threads, recursion, depth, timeout)

	if err != nil {
		gErr = err.Error()
	} else {
		gErr = ""
	}

}

func SetOpts(
	opts *ffuf.ConfigOptions,
	url string,
	headers []string,
	wordlists []string,
	threads int,
	recursion bool,
	depth int,
	timeout int,
) {
	opts.HTTP.URL = url
	opts.HTTP.Headers = headers
	opts.General.Threads = threads
	opts.HTTP.Recursion = recursion
	opts.HTTP.RecursionDepth = depth
	opts.HTTP.Timeout = timeout
	opts.Input.Wordlists = wordlists
}

func ConfigFromFile(opts *ffuf.ConfigOptions) (*ffuf.ConfigOptions, error) {
	var newopts *ffuf.ConfigOptions
	var err error

	newopts, err = ffuf.ReadConfig(opts.General.ConfigFile)

	if err != nil {
		return nil, err
	}

	// re-init our options
	SetOpts(
		newopts,
		opts.HTTP.URL,
		opts.HTTP.Headers,
		opts.Input.Wordlists,
		opts.General.Threads,
		opts.HTTP.Recursion,
		opts.HTTP.RecursionDepth,
		opts.HTTP.Timeout,
	)

	return newopts, nil
}

func GetVersion() string {
	return "ffuf " + ffuf.Version()
}

//export FfufGetVersion
func FfufGetVersion() *C.char {
	return C.CString(GetVersion())
}

func SetMethod(method string) {
	pFfuf.opts.HTTP.Method = method
}

//export FfufSetMethod
func FfufSetMethod(method string) {
	SetMethod(method)
}

func SetData(data string) {
	pFfuf.opts.HTTP.Data = data
}

//export FfufSetData
func FfufSetData(data string) {
	SetData(data)
}

func SetConfigFile(cfgfile string) {
	pFfuf.opts.General.ConfigFile = cfgfile
}

//export FfufSetConfigFile
func FfufSetConfigFile(cfgfile string) {
	SetConfigFile(cfgfile)
}

func SetInputMode(inpmode string) {
	pFfuf.opts.Input.InputMode = inpmode
}

//export FfufSetInputMode
func FfufSetInputMode(inpmode string) {
	SetInputMode(inpmode)
}

func SetInputCommands(inpcmds []string) {
	pFfuf.opts.Input.Inputcommands = inpcmds
}

//export FfufSetInputCommands
func FfufSetInputCommands(inpcmds **C.char, size int) {
	SetInputCommands(CStrArrToGo(inpcmds, size))
}

func SetRequestFile(reqfile string) {
	pFfuf.opts.Input.Request = reqfile
}

//export FfufSetRequestFile
func FfufSetRequestFile(reqfile string) {
	SetRequestFile(reqfile)
}

func SetAutoCalibrationStrategy(strategy string) {
	pFfuf.opts.General.AutoCalibrationStrategy = strategy
}

//export FfufSetAutoCalibrationStrategy
func FfufSetAutoCalibrationStrategy(strategy string) {
	SetAutoCalibrationStrategy(strategy)
}

func SetRecursionStrategy(strategy string) {
	pFfuf.opts.HTTP.RecursionStrategy = strategy
}

//export FfufSetRecursionStrategy
func FfufSetRecursionStrategy(strategy string) {
	SetRecursionStrategy(strategy)
}

func SetRequestProto(reqproto string) {
	pFfuf.opts.Input.RequestProto = reqproto
}

//export FfufSetRequestProto
func FfufSetRequestProto(reqproto string) {
	SetRequestProto(reqproto)
}

func SetScrapers(scrapers string) {
	pFfuf.opts.General.Scrapers = scrapers
}

//export FfufSetScrapers
func FfufSetScrapers(scrapers string) {
	SetScrapers(scrapers)
}

func SetMatcherMode(mode string) {
	pFfuf.opts.Matcher.Mode = mode
}

//export FfufSetMatcherMode
func FfufSetMatcherMode(mode string) {
	SetMatcherMode(mode)
}

func SetFilterMode(mode string) {
	pFfuf.opts.Filter.Mode = mode
}

//export FfufSetFilterMode
func FfufSetFilterMode(mode string) {
	SetFilterMode(mode)
}

func SetMatchers(matchers []Matcher) {
	pFfuf.matchers = matchers
}

func SetFilters(filters []Filter) {
	pFfuf.filters = filters
}

func AddMatcher(matcher Matcher) {
	pFfuf.matchers = append(pFfuf.matchers, matcher)
}

//export FfufAddMatcher
func FfufAddMatcher(name string, value string) {
	AddMatcher(Matcher{
		Name:  name,
		Value: value,
	})
}

func AddFilter(filter Filter) {
	pFfuf.filters = append(pFfuf.filters, filter)
}

//export FfufAddFilter
func FfufAddFilter(name string, value string) {
	AddFilter(Filter{
		Name:  name,
		Value: value,
	})
}

//export FfufGetLastError
func FfufGetLastError() *C.char {
	if gErr == "" {
		return nil
	}

	return C.CString(gErr)
}

func Start() ([]ffuf.Result, error) {
	var err error
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	if pFfuf.opts.General.ConfigFile != "" {
		pFfuf.opts, err = ConfigFromFile(pFfuf.opts)

		if err != nil {
			return nil, err
		}
	}

	prepareFilters()
	prepareMatchers()

	// Set up Config struct
	pFfuf.config, err = ffuf.ConfigFromOptions(pFfuf.opts, ctx, cancel)

	if err != nil {
		return nil, err
	}

	job, err := prepareJob(pFfuf.config)

	if err != nil {
		return nil, err
	}

	if err := SetupFilters(pFfuf.opts, pFfuf.config); err != nil {
		return nil, err
	}

	// Job handles waiting for goroutines to complete itself
	job.Start()

	return job.Output.GetCurrentResults(), nil
}

//export FfufStart
func FfufStart() **C.FfufResult {
	results, err := Start()

	// return NULL to C if error occurred
	if err != nil {
		gErr = err.Error()
		return nil
	}

	// Get size of data to allocate memory for c results
	size := len(results) + 1

	// Allocate memory space for C array
	cArray := C.malloc(C.size_t(size) * C.size_t(unsafe.Sizeof(uintptr(0))))

	// Convert the C array to a Go Array so we can index it
	a := (*[1 << 28]*C.FfufResult)(unsafe.Pointer(cArray))[:size:size]

	// Iterate all results and store them in C structures
	for idx, result := range results {
		pResult := (*C.FfufResult)(C.malloc(C.size_t(unsafe.Sizeof(C.FfufResult{}))))
		pResult.pInput = GoInputDataToC(result.Input)
		pResult.nPosition = C.int(result.Position)
		pResult.llStatusCode = C.longlong(result.StatusCode)
		pResult.llContentLength = C.longlong(result.ContentLength)
		pResult.llContentWords = C.longlong(result.ContentWords)
		pResult.llContentLines = C.longlong(result.ContentLines)
		pResult.cpContentType = C.CString(result.ContentType)
		pResult.cpRedirectLocation = C.CString(result.RedirectLocation)
		pResult.cpUrl = C.CString(result.Url)
		pResult.cpResultFile = C.CString(result.ResultFile)
		pResult.cpHost = C.CString(result.Host)
		pResult.cpHTMLColor = C.CString(result.HTMLColor)
		pResult.pScraperData = GoScraperDataToC(result.ScraperData)
		pResult.pTimeDuration = GoTimeDurationToC(result.Duration)
		pResult.pContent = GoContentToC(result.Content)
		a[idx] = pResult
	}

	// Terminator
	a[size-1] = nil

	return (**C.FfufResult)(cArray)
}

func prepareFilters() {
	for _, filter := range pFfuf.filters {
		switch filter.Name {
		case "fs":
			pFfuf.opts.Filter.Size = filter.Value

		case "fl":
			pFfuf.opts.Filter.Lines = filter.Value

		case "fr":
			pFfuf.opts.Filter.Regexp = filter.Value

		case "fc":
			pFfuf.opts.Filter.Status = filter.Value

		case "ft":
			pFfuf.opts.Filter.Time = filter.Value

		case "fw":
			pFfuf.opts.Filter.Words = filter.Value
		}
	}
}

func prepareMatchers() {
	for _, matcher := range pFfuf.matchers {
		switch matcher.Name {
		case "mc":
			pFfuf.opts.Matcher.Status = matcher.Value

		case "ml":
			pFfuf.opts.Matcher.Lines = matcher.Value

		case "mr":
			pFfuf.opts.Matcher.Regexp = matcher.Value

		case "ms":
			pFfuf.opts.Matcher.Size = matcher.Value

		case "mt":
			pFfuf.opts.Matcher.Time = matcher.Value

		case "mw":
			pFfuf.opts.Matcher.Words = matcher.Value

		}
	}
}

func prepareJob(conf *ffuf.Config) (*ffuf.Job, error) {
	var err error
	job := ffuf.NewJob(conf)
	var errs ffuf.Multierror
	job.Input, errs = input.NewInputProvider(conf)
	// TODO: implement error handling for runnerprovider and outputprovider
	// We only have http runner right now
	job.Runner = runner.NewRunnerByName("http", conf, false)
	if len(conf.ReplayProxyURL) > 0 {
		job.ReplayRunner = runner.NewRunnerByName("http", conf, true)
	}

	// We only have gorock outputprovider right now
	job.Output = output.NewOutputProviderByName("gorock", conf)

	// Initialize scraper
	newscraper, scraper_err := scraper.FromDir(ffuf.SCRAPERDIR, conf.Scrapers)
	if scraper_err.ErrorOrNil() != nil {
		errs.Add(scraper_err.ErrorOrNil())
	}
	job.Scraper = newscraper
	if conf.ScraperFile != "" {
		err = job.Scraper.AppendFromFile(conf.ScraperFile)
		if err != nil {
			errs.Add(err)
		}
	}
	return job, errs.ErrorOrNil()
}

func SetupFilters(parseOpts *ffuf.ConfigOptions, conf *ffuf.Config) error {
	errs := ffuf.NewMultierror()
	conf.MatcherManager = filter.NewMatcherManager()
	// If any other matcher is set, ignore -mc default value
	matcherSet := false
	statusSet := false
	warningIgnoreBody := false
	for _, f := range pFfuf.matchers {
		if f.Name == "mc" {
			statusSet = true
		}
		if f.Name == "ms" {
			matcherSet = true
			warningIgnoreBody = true
		}
		if f.Name == "ml" {
			matcherSet = true
			warningIgnoreBody = true
		}
		if f.Name == "mr" {
			matcherSet = true
		}
		if f.Name == "mt" {
			matcherSet = true
		}
		if f.Name == "mw" {
			matcherSet = true
			warningIgnoreBody = true
		}
	}
	// Only set default matchers if no
	if statusSet || !matcherSet {
		if err := conf.MatcherManager.AddMatcher("status", parseOpts.Matcher.Status); err != nil {
			errs.Add(err)
		}
	}

	if parseOpts.Filter.Status != "" {
		if err := conf.MatcherManager.AddFilter("status", parseOpts.Filter.Status, false); err != nil {
			errs.Add(err)
		}
	}
	if parseOpts.Filter.Size != "" {
		warningIgnoreBody = true
		if err := conf.MatcherManager.AddFilter("size", parseOpts.Filter.Size, false); err != nil {
			errs.Add(err)
		}
	}
	if parseOpts.Filter.Regexp != "" {
		if err := conf.MatcherManager.AddFilter("regexp", parseOpts.Filter.Regexp, false); err != nil {
			errs.Add(err)
		}
	}
	if parseOpts.Filter.Words != "" {
		warningIgnoreBody = true
		if err := conf.MatcherManager.AddFilter("word", parseOpts.Filter.Words, false); err != nil {
			errs.Add(err)
		}
	}
	if parseOpts.Filter.Lines != "" {
		warningIgnoreBody = true
		if err := conf.MatcherManager.AddFilter("line", parseOpts.Filter.Lines, false); err != nil {
			errs.Add(err)
		}
	}
	if parseOpts.Filter.Time != "" {
		if err := conf.MatcherManager.AddFilter("time", parseOpts.Filter.Time, false); err != nil {
			errs.Add(err)
		}
	}
	if parseOpts.Matcher.Size != "" {
		if err := conf.MatcherManager.AddMatcher("size", parseOpts.Matcher.Size); err != nil {
			errs.Add(err)
		}
	}
	if parseOpts.Matcher.Regexp != "" {
		if err := conf.MatcherManager.AddMatcher("regexp", parseOpts.Matcher.Regexp); err != nil {
			errs.Add(err)
		}
	}
	if parseOpts.Matcher.Words != "" {
		if err := conf.MatcherManager.AddMatcher("word", parseOpts.Matcher.Words); err != nil {
			errs.Add(err)
		}
	}
	if parseOpts.Matcher.Lines != "" {
		if err := conf.MatcherManager.AddMatcher("line", parseOpts.Matcher.Lines); err != nil {
			errs.Add(err)
		}
	}
	if parseOpts.Matcher.Time != "" {
		if err := conf.MatcherManager.AddMatcher("time", parseOpts.Matcher.Time); err != nil {
			errs.Add(err)
		}
	}
	if conf.IgnoreBody && warningIgnoreBody {
		fmt.Printf("*** Warning: possible undesired combination of -ignore-body and the response options: fl,fs,fw,ml,ms and mw.\n")
	}
	return errs.ErrorOrNil()
}

func GoStringsToC(gostrings []string) **C.char {
	// Get size of results to allocate memory for c results
	size := len(gostrings) + 1 // add one to put a nul terminator at the end of C strings array

	// Allocate memory space for C array
	cArray := C.malloc(C.size_t(size) * C.size_t(unsafe.Sizeof(uintptr(0))))

	// convert the C array to a Go Array so we can index it
	a := (*[1 << 28]*C.char)(unsafe.Pointer(cArray))[:size:size]

	for idx, str := range gostrings {
		a[idx] = C.CString(str)
	}

	// put a nul-terminator in the end of array
	a[size-1] = nil

	return (**C.char)(cArray)
}

func CStrArrToGo(arr **C.char, size int) []string {
	tmpslice := (*[1 << 28]*C.char)(unsafe.Pointer(arr))[:size:size]
	gostrings := make([]string, size)
	for i, s := range tmpslice {
		gostrings[i] = C.GoString(s)
	}

	return gostrings
}

func GoInputDataToC(inpdata map[string][]byte) **C.InputData {
	idx := 0
	size := len(inpdata) + 1
	cArray := C.malloc(C.size_t(size) * C.size_t(unsafe.Sizeof(uintptr(0))))
	a := (*[1 << 28]*C.InputData)(unsafe.Pointer(cArray))[:size:size]

	for key, data := range inpdata {
		pData := (*C.InputData)(C.malloc(C.size_t(unsafe.Sizeof(C.InputData{}))))
		pData.cpName = C.CString(key)
		pData.pData = C.CBytes(data)
		pData.lSize = C.long(len(data))
		a[idx] = pData
		idx++
	}

	a[size-1] = nil

	return (**C.InputData)(cArray)
}

func GoContentToC(content []byte) *C.Content {
	pContent := (*C.Content)(C.malloc(C.size_t(unsafe.Sizeof(C.Content{}))))
	pContent.pData = C.CBytes(content)
	pContent.lSize = C.long(len(content))
	return pContent
}

func GoScraperDataToC(scdata map[string][]string) **C.ScraperData {
	idx := 0
	size := len(scdata) + 1
	cArray := C.malloc(C.size_t(size) * C.size_t(unsafe.Sizeof(uintptr(0))))
	a := (*[1 << 28]*C.ScraperData)(unsafe.Pointer(cArray))[:size:size]

	for key, data := range scdata {
		pData := (*C.ScraperData)(C.malloc(C.size_t(unsafe.Sizeof(C.ScraperData{}))))
		pData.cpName = C.CString(key)
		pData.cpData = GoStringsToC(data)
		a[idx] = pData
		idx++
	}

	a[size-1] = nil

	return (**C.ScraperData)(cArray)
}

func GoTimeDurationToC(d time.Duration) *C.TimeDuration {
	pTime := (*C.TimeDuration)(C.malloc(C.size_t(unsafe.Sizeof(C.TimeDuration{}))))
	pTime.dHours = C.double(d.Hours())
	pTime.dMinutes = C.double(d.Minutes())
	pTime.dSeconds = C.double(d.Seconds())
	pTime.llMicroseconds = C.longlong(d.Microseconds())
	pTime.llMilliseconds = C.longlong(d.Milliseconds())
	pTime.llNanoseconds = C.longlong(d.Nanoseconds())
	pTime.cpStr = C.CString(d.String())
	return pTime
}

func main() {

}
