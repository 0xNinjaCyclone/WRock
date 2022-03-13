package main

// go mod init subfinder
// go mod tidy

import (
	"C"
	"bytes"
	"context"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"unsafe"

	"github.com/projectdiscovery/gologger"
	"github.com/projectdiscovery/gologger/levels"
	"github.com/projectdiscovery/subfinder/v2/pkg/passive"
	"github.com/projectdiscovery/subfinder/v2/pkg/resolve"
	"github.com/projectdiscovery/subfinder/v2/pkg/runner"
)

// subfinder type
type SubFinder map[string][]string

// config data structure
var subfinder = make(SubFinder)

//export SubFinderInit
func SubFinderInit() {
	// initiate configurations

	// Default Resolvers
	subfinder["Resolvers"] = resolve.DefaultResolvers

	// Default passive Sources
	subfinder["Sources"] = passive.DefaultSources

	// Default passive AllSources
	subfinder["AllSources"] = passive.DefaultAllSources

	// Default list of Recursive
	subfinder["Recursive"] = passive.DefaultRecursiveSources

}

func Version() string {
	return "subfinder " + runner.Version
}

//export SubFinderVersion
func SubFinderVersion() *C.char {
	return C.CString(Version())
}

func SetProperty(propname string, propval []string) {
	subfinder[propname] = propval
}

//export SubFinderSetProperty
func SubFinderSetProperty(propname string, propval **C.char, size int) {
	tmpslice := (*[1 << 28]*C.char)(unsafe.Pointer(propval))[:size:size]
	gostrings := make([]string, size)
	for i, s := range tmpslice {
		gostrings[i] = C.GoString(s)
	}

	SetProperty(propname, gostrings)
}

func GetProperty(propname string) []string {
	return subfinder[propname]
}

//export SubFinderGetProperty
func SubFinderGetProperty(propname string) **C.char {
	propvals := GetProperty(propname)

	size := len(propvals) + 1

	// Allocate memory space for C array
	cArray := C.malloc(C.size_t(size) * C.size_t(unsafe.Sizeof(uintptr(0))))

	// convert the C array to a Go Array so we can index it
	a := (*[1 << 28]*C.char)(unsafe.Pointer(cArray))[:size:size]

	for idx, item := range propvals {
		result := string(item)
		if result != "" {
			// Convert to C string before pushing to C array
			a[idx] = C.CString(result)
		}
	}

	// put a nul-terminator in the end of array
	a[size-1] = nil

	// return **char type to C
	return (**C.char)(cArray)
}

//export SubFinderStart
func SubFinderStart(domain string, threads int, timeout int, maxEnumerationTime int) **C.char {
	// Disable logging
	gologger.DefaultLogger.SetMaxLevel(levels.LevelSilent)

	config := runner.ConfigFile{
		// Use the default list of resolvers by marshaling it to the config
		Resolvers: GetProperty("Resolvers"),
		// Use the default list of passive sources
		Sources: GetProperty("Sources"),
		// Use the default list of all passive sources
		AllSources: GetProperty("AllSources"),
		// Use the default list of recursive sources
		Recursive: GetProperty("Recursive"),
		// ExcludeSources contains the sources to not include in the enumeration process
		ExcludeSources: GetProperty("ExcludeSources"),
		// API keys for different sources
		Binaryedge:     GetProperty("Binaryedge"),
		Censys:         GetProperty("Censys"),
		Certspotter:    GetProperty("Certspotter"),
		Chaos:          GetProperty("Chaos"),
		Chinaz:         GetProperty("Chinaz"),
		DNSDB:          GetProperty("DNSDB"),
		GitHub:         GetProperty("GitHub"),
		IntelX:         GetProperty("IntelX"),
		PassiveTotal:   GetProperty("PassiveTotal"),
		Recon:          GetProperty("Recon"),
		Robtex:         GetProperty("Robtex"),
		SecurityTrails: GetProperty("SecurityTrails"),
		Shodan:         GetProperty("Shodan"),
		Spyse:          GetProperty("Spyse"),
		ThreatBook:     GetProperty("ThreatBook"),
		URLScan:        GetProperty("URLScan"),
		Virustotal:     GetProperty("Virustotal"),
		ZoomEye:        GetProperty("ZoomEye"),
		Fofa:           GetProperty("Fofa"),
	}

	runnerInstance, _ := runner.NewRunner(&runner.Options{
		Threads:            threads,            // Thread controls the number of threads to use for active enumerations
		Timeout:            timeout,            // Timeout is the seconds to wait for sources to respond
		MaxEnumerationTime: maxEnumerationTime, // MaxEnumerationTime is the maximum amount of time in mins to wait for enumeration
		YAMLConfig:         config,
	})

	buf := bytes.Buffer{}
	err := runnerInstance.EnumerateSingleDomain(context.Background(), domain, []io.Writer{&buf})
	if err != nil {
		log.Fatal(err)
	}

	data, err := ioutil.ReadAll(&buf)
	if err != nil {
		log.Fatal(err)
	}

	// Split bytes to array by newline delimiter
	arr := bytes.Split(data, []byte("\n"))

	size := len(arr)

	// Allocate memory space for C array
	cArray := C.malloc(C.size_t(size) * C.size_t(unsafe.Sizeof(uintptr(0))))

	// Convert the C array to a Go Array so we can index it
	a := (*[1 << 28]*C.char)(unsafe.Pointer(cArray))[:size:size]

	for idx, item := range arr {
		// Convert bytes to string
		result := string(item)

		if result != "" {
			// Convert to C string before pushing to C array
			a[idx] = C.CString(result)
		}
	}

	// Put a nul-terminator in the end of array
	a[size-1] = nil

	// return **char type to C
	return (**C.char)(cArray)
}

func main() {
	SubFinderInit()

	//SetProperty("Sources", passive.DefaultAllSources)

	config := runner.ConfigFile{
		// Use the default list of resolvers by marshaling it to the config
		Resolvers: resolve.DefaultResolvers,
		// Use the default list of passive sources
		Sources: GetProperty("Sources"),
		// Use the default list of all passive sources
		AllSources: passive.DefaultAllSources,
		// Use the default list of recursive sources
		Recursive: passive.DefaultRecursiveSources,
	}

	gologger.Info().Msgf("current version is '%s'\n", Version())

	runnerInstance, _ := runner.NewRunner(&runner.Options{
		Threads:            10, // Thread controls the number of threads to use for active enumerations
		Timeout:            30, // Timeout is the seconds to wait for sources to respond
		MaxEnumerationTime: 10, // MaxEnumerationTime is the maximum amount of time in mins to wait for enumeration
		YAMLConfig:         config,
	})

	buf := bytes.Buffer{}

	err := runnerInstance.EnumerateSingleDomain(nil, "projectdiscovery.io", []io.Writer{&buf})
	if err != nil {
		log.Fatal(err)
	}

	data, err := ioutil.ReadAll(&buf)
	if err != nil {
		log.Fatal(err)
	}

	// Split bytes and Get splitted subdomains
	arr := bytes.Split(data, []byte("\n"))

	for idx, r := range arr {
		res := string(r)
		if res != "" {
			fmt.Printf("%d %s\n", idx, res)
		}
	}
}
