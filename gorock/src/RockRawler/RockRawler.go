/*
	Author	=> Abdallah Mohamed Elsharif
	Email	=> elsharifabdallah53@gmail.com
	Date	=> 3-1-2022
*/

package main

/*
typedef struct {
	char *name;
	char *value;
	char *p_type; // parameter type
} Parameter;

typedef struct {
	char      *url;
	char	  *m_type;
	Parameter **params;
} EndPoint;

typedef struct {
	EndPoint **endpoints;
	char     **jsFiles;
	char     **emails;
} RockRawlerResult;
*/
import "C"

import (
	"crypto/tls"
	"errors"
	"net/http"
	"net/url"
	"regexp"
	"strings"
	"unsafe"

	"github.com/gocolly/colly"
)

type RockRawlerConfig struct {
	url         string
	threads     int
	depth       int
	insecure    bool
	subsInScope bool
	rawHeaders  string
}

type Parameter struct {
	name   string
	value  string
	p_type string // parameter type
}

type EndPoint struct {
	url    string
	m_type string // method type -> Get or Post ?
	params []Parameter
}

type RockRawlerResult struct {
	endpoints []EndPoint
	jsFiles   []string
	emails    []string
}

func initRockRawlerResult() RockRawlerResult {
	return RockRawlerResult{
		endpoints: make([]EndPoint, 0),
		jsFiles:   make([]string, 0),
		emails:    make([]string, 0),
	}
}

func FindEmails(text string) []string {
	var EMAILS_REGEX = regexp.MustCompile(`(?i)([A-Za-z0-9!#$%&'*+\/=?^_{|.}~-]+@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)`)
	return EMAILS_REGEX.FindAllString(text, -1)
}

func StartCrawler(config RockRawlerConfig) RockRawlerResult {
	// Target url
	url := config.url

	// Convert the headers input to a usable map (or die trying)
	headers, _ := parseHeaders(config.rawHeaders)

	// A container where the results are stored
	result := initRockRawlerResult()

	// if a url does not start with scheme (It fix hakrawler bug)
	if !strings.HasPrefix(url, "http") {
		url = "http://" + url
	}

	// Get hostname from url
	hostname, err := extractHostname(url)

	if err != nil {
		// return empty
		return result
	}

	// Instantiate default collector
	c := colly.NewCollector(

		// default user agent header
		colly.UserAgent("Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"),

		// limit crawling to the domain of the specified URL
		colly.AllowedDomains(hostname),

		// set MaxDepth to the specified depth
		colly.MaxDepth(config.depth),

		// specify Async for threading
		colly.Async(true),
	)

	// if -subs is present, use regex to filter out subdomains in scope.
	if config.subsInScope {
		c.AllowedDomains = nil
		c.URLFilters = []*regexp.Regexp{regexp.MustCompile(".*(\\.|\\/\\/)" + strings.ReplaceAll(hostname, ".", "\\.") + "((#|\\/|\\?).*)?")}
	}

	// Set parallelism
	c.Limit(&colly.LimitRule{DomainGlob: "*", Parallelism: config.threads})

	// Search about emails in html content
	c.OnHTML("html", func(e *colly.HTMLElement) {
		appendEmails(&result.emails, e)
	})

	// append every href found, and visit it
	c.OnHTML("a[href]", func(e *colly.HTMLElement) {
		appendEndPoint(e.Attr("href"), &result, e)
		e.Request.Visit(e.Attr("href"))
	})

	// find all JavaScript files
	c.OnHTML("script[src]", func(e *colly.HTMLElement) {
		appendResult(e.Attr("src"), &result.jsFiles, e)
	})

	// find all the form action URLs
	c.OnHTML("form[action]", func(e *colly.HTMLElement) {
		appendEndPoint(e.Attr("action"), &result, e)
	})

	// add the custom headers
	if headers != nil {
		c.OnRequest(func(r *colly.Request) {
			for header, value := range headers {
				r.Headers.Set(header, value)
			}
		})
	}

	// Skip TLS verification if -insecure flag is present
	c.WithTransport(&http.Transport{
		TLSClientConfig: &tls.Config{InsecureSkipVerify: config.insecure},
	})

	// Start scraping
	c.Visit(url)

	// Wait until threads are finished
	c.Wait()

	return result
}

// parseHeaders does validation of headers input and saves it to a formatted map.
func parseHeaders(rawHeaders string) (map[string]string, error) {
	headers := make(map[string]string)

	if rawHeaders != "" {
		// if headers is not valid
		if !strings.Contains(rawHeaders, ":") {
			return nil, errors.New("headers flag not formatted properly (no colon to separate header and value)")
		}

		// Split headers by two semi-colons to avoid splitting values
		rawHeaders := strings.Split(rawHeaders, ";;")

		for _, header := range rawHeaders {
			var parts []string

			if strings.Contains(header, ": ") {
				// To avoid a space before its value
				parts = strings.SplitN(header, ": ", 2)
			} else if strings.Contains(header, ":") {
				parts = strings.SplitN(header, ":", 2)
			} else {
				// Bad header
				continue
			}

			// append processed header to headers
			headers[strings.TrimSpace(parts[0])] = strings.TrimSpace(parts[1])
		}
	}

	return headers, nil
}

// extractHostname() extracts the hostname from a URL and returns it
func extractHostname(urlString string) (string, error) {
	u, err := url.Parse(urlString)

	if err != nil {
		// if error occured
		return "", err
	}

	return u.Hostname(), nil
}

// append valid unique result to results
func appendResult(link string, results *[]string, e *colly.HTMLElement) {
	result := e.Request.AbsoluteURL(link)

	if result != "" {
		// Append only unique links
		if isUnique(results, result) {
			*results = append(*results, result)
		}
	}
}

func appendEmails(result *[]string, e *colly.HTMLElement) {
	for _, email := range FindEmails(string(e.Response.Body)) {
		if isUnique(result, email) {
			*result = append(*result, email)
		}
	}
}

// append endpoints
func appendEndPoint(link string, result *RockRawlerResult, e *colly.HTMLElement) {
	endpoint := EndPoint{
		url: e.Request.AbsoluteURL(func() string {
			if link == "#" {
				return ""
			} else {
				return link
			}
		}()),
		m_type: func() string {
			if e.Attr("method") != "" {
				return e.Attr("method")
			} else {
				return "get"
			}
		}(),
		params: make([]Parameter, 0),
	}

	e.ForEach("input", func(_ int, i *colly.HTMLElement) {
		param := Parameter{
			name:   i.Attr("name"),
			value:  i.Attr("value"),
			p_type: i.Attr("type"),
		}

		endpoint.params = append(endpoint.params, param)
	})

	if isUniqueEndPoint(result.endpoints, endpoint) {
		result.endpoints = append(result.endpoints, endpoint)
	}
}

// returns whether the supplied element is unique or not
func isUnique(data *[]string, element string) bool {
	for _, item := range *data {
		if item == element {
			return false
		}
	}

	return true
}

func isUniqueParameter(p1 []Parameter, p2 []Parameter) bool {
	unique := false

	for _, item := range p1 {
		for _, item2 := range p2 {
			if item.name != item2.name {
				unique = true
			}
		}
	}

	return unique
}

func isUniqueEndPoint(endpoints []EndPoint, endpoint EndPoint) bool {
	for _, item := range endpoints {
		if item.url == endpoint.url && item.m_type == endpoint.m_type && !isUniqueParameter(item.params, endpoint.params) {
			return false
		}
	}

	return true
}

func GoStringsToC(gostrings []string) **C.char {
	// Get size of results to allocate memory for c results
	size := len(gostrings) + 1 // add one to put a nul terminator at the end of C strings array

	// Allocate memory space for C array
	cArray := C.malloc(C.size_t(size) * C.size_t(unsafe.Sizeof(uintptr(0))))

	// convert the C array to a Go Array so we can index it
	a := (*[1 << 28]*C.char)(unsafe.Pointer(cArray))[:size:size]

	for idx, link := range gostrings {
		a[idx] = C.CString(link)
	}

	// put a nul-terminator in the end of array
	a[size-1] = nil

	return (**C.char)(cArray)
}

func GoParameterToC(params []Parameter) **C.Parameter {
	// Get size of params to allocate memory for c results
	size := len(params) + 1

	// Allocate memory space for C array
	cArray := C.malloc(C.size_t(size) * C.size_t(unsafe.Sizeof(uintptr(0))))

	// Convert the C array to a Go Array so we can index it
	a := (*[1 << 28]*C.Parameter)(unsafe.Pointer(cArray))[:size:size]

	for idx, p := range params {
		pParam := (*C.Parameter)(C.malloc(C.size_t(unsafe.Sizeof(C.Parameter{}))))
		pParam.name = C.CString(p.name)
		pParam.value = C.CString(p.value)
		pParam.p_type = C.CString(p.p_type)
		a[idx] = pParam
	}

	// Put a nul-terminator in the end of array
	a[size-1] = nil

	return (**C.Parameter)(cArray)
}

func GoEndpointsToC(endpoint []EndPoint) **C.EndPoint {
	// Get size of data to allocate memory for c results
	size := len(endpoint) + 1

	// Allocate memory space for C array
	cArray := C.malloc(C.size_t(size) * C.size_t(unsafe.Sizeof(uintptr(0))))

	// Convert the C array to a Go Array so we can index it
	a := (*[1 << 28]*C.EndPoint)(unsafe.Pointer(cArray))[:size:size]

	for idx, data := range endpoint {
		pData := (*C.EndPoint)(C.malloc(C.size_t(unsafe.Sizeof(C.EndPoint{}))))
		pData.url = C.CString(data.url)
		pData.m_type = C.CString(data.m_type)
		pData.params = GoParameterToC(data.params)
		a[idx] = pData
	}

	// Put a nul-terminator in the end of array
	a[size-1] = nil

	return (**C.EndPoint)(cArray)
}

func GoResultToC(result RockRawlerResult) *C.RockRawlerResult {
	pResult := (*C.RockRawlerResult)(C.malloc(C.size_t(unsafe.Sizeof(C.RockRawlerResult{}))))
	pResult.endpoints = GoEndpointsToC(result.endpoints)
	pResult.jsFiles = GoStringsToC(result.jsFiles)
	pResult.emails = GoStringsToC(result.emails)
	return pResult
}

//export CStartCrawler
func CStartCrawler(
	url string,
	threads int,
	depth int,
	subsInScope bool,
	insecure bool,
	rawHeaders string,
) *C.RockRawlerResult {

	// Config
	config := RockRawlerConfig{
		url:         url,
		threads:     threads,
		depth:       depth,
		subsInScope: subsInScope,
		insecure:    insecure,
		rawHeaders:  rawHeaders,
	}

	// Pass the supplied parameters from C to the crawler
	result := StartCrawler(config)

	// Return *C.RockRawlerResult
	return GoResultToC(result)
}

func main() {}
