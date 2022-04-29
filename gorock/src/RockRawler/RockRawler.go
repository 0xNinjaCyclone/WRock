/*
	Author	=> Abdallah Mohamed Elsharif
	Email	=> elsharifabdallah53@gmail.com
	Date	=> 3-1-2022
*/

package main

import (
	"C"
	"crypto/tls"
	"errors"
	"fmt"
	"net/http"
	"net/url"
	"regexp"
	"strings"
	"unsafe"

	"github.com/gocolly/colly"
)

func StartCrawler(url string, threads int, depth int, subsInScope bool, insecure bool, rawHeaders string) []string {

	// Convert the headers input to a usable map (or die trying)
	headers, _ := parseHeaders(rawHeaders)

	// A container where the results are stored
	results := make([]string, 0)

	// if a url does not start with scheme (It fix hakrawler bug)
	if !strings.HasPrefix(url, "http") {
		url = "http://" + url
	}

	// Get hostname from url
	hostname, err := extractHostname(url)

	if err != nil {
		// return empty slice
		return results
	}

	// Instantiate default collector
	c := colly.NewCollector(

		// default user agent header
		colly.UserAgent("Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0"),

		// limit crawling to the domain of the specified URL
		colly.AllowedDomains(hostname),

		// set MaxDepth to the specified depth
		colly.MaxDepth(depth),

		// specify Async for threading
		colly.Async(true),
	)

	// if -subs is present, use regex to filter out subdomains in scope.
	if subsInScope {
		c.AllowedDomains = nil
		c.URLFilters = []*regexp.Regexp{regexp.MustCompile(".*(\\.|\\/\\/)" + strings.ReplaceAll(hostname, ".", "\\.") + "((#|\\/|\\?).*)?")}
	}

	// Set parallelism
	c.Limit(&colly.LimitRule{DomainGlob: "*", Parallelism: threads})

	// append every href found, and visit it
	c.OnHTML("a[href]", func(e *colly.HTMLElement) {
		link := e.Attr("href")
		appendResult(link, &results, e)
		e.Request.Visit(link)
	})

	// find all JavaScript files
	c.OnHTML("script[src]", func(e *colly.HTMLElement) {
		appendResult(e.Attr("src"), &results, e)
	})

	// find all the form action URLs
	c.OnHTML("form[action]", func(e *colly.HTMLElement) {
		appendResult(e.Attr("action"), &results, e)
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
		TLSClientConfig: &tls.Config{InsecureSkipVerify: insecure},
	})

	// Start scraping
	c.Visit(url)

	// Wait until threads are finished
	c.Wait()

	return results
}

func printResults(results []string) {
	for _, res := range results {
		fmt.Printf("%s\n", res)
	}
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

// returns whether the supplied url is unique or not
func isUnique(data *[]string, url string) bool {
	for _, item := range *data {
		if item == url {
			return false
		}
	}

	return true
}

//export CStartCrawler
func CStartCrawler(url string, threads int, depth int, subsInScope bool, insecure bool, rawHeaders string) **C.char {

	// Pass the supplied parameters from C to the crawler
	results := StartCrawler(url, threads, depth, subsInScope, insecure, rawHeaders)

	// Get size of results to allocate memory for c results
	size := len(results) + 1 // add one to put a nul terminator at the end of C strings array

	// Allocate memory space for C array
	cArray := C.malloc(C.size_t(size) * C.size_t(unsafe.Sizeof(uintptr(0))))

	// convert the C array to a Go Array so we can index it
	a := (*[1 << 28]*C.char)(unsafe.Pointer(cArray))[:size:size]

	for idx, link := range results {
		a[idx] = C.CString(link)
	}

	// put a nul-terminator in the end of array
	a[size-1] = nil

	// return **char type to C
	return (**C.char)(cArray)
}

func main() {}
