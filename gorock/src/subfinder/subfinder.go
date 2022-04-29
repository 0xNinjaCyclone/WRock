package main

// go mod init subfinder
// go mod tidy

import (
	"C"
	"bytes"
	"context"
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

type SubFinder struct {
	Threads            int
	Timeout            int
	MaxEnumerationTime int
	All                bool
	Recursive          bool
	Property           Property
}

type Property map[string][]string

// config data structure
var subfinder = SubFinder{}

//export SubFinderInit
func SubFinderInit() {
	// Disable logging
	gologger.DefaultLogger.SetMaxLevel(levels.LevelSilent)

	// initiate configurations
	subfinder.All = false
	subfinder.Recursive = false

	// Initiate property
	subfinder.Property = make(Property)

	// Default Resolvers
	subfinder.Property["Resolvers"] = resolve.DefaultResolvers

	// Default passive Sources
	subfinder.Property["Sources"] = passive.DefaultSources

	// Default passive AllSources
	subfinder.Property["AllSources"] = passive.DefaultAllSources

	// Default list of Recursive
	subfinder.Property["Recursive"] = passive.DefaultRecursiveSources

}

func Version() string {
	return "subfinder " + runner.Version
}

//export SubFinderVersion
func SubFinderVersion() *C.char {
	return C.CString(Version())
}

func UseAll() {
	subfinder.All = true
}

//export SubFinderUseAll
func SubFinderUseAll() {
	UseAll()
}

func UseRecursive() {
	subfinder.Recursive = true
}

//export SubFinderUseRecursive
func SubFinderUseRecursive() {
	UseRecursive()
}

func SetProperty(propname string, propval []string) {
	subfinder.Property[propname] = propval
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
	return subfinder.Property[propname]
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

	runnerInstance, _ := runner.NewRunner(&runner.Options{
		Threads:            threads,                       // Thread controls the number of threads to use for active enumerations
		Timeout:            timeout,                       // Timeout is the seconds to wait for sources to respond
		MaxEnumerationTime: maxEnumerationTime,            // MaxEnumerationTime is the maximum amount of time in mins to wait for enumeration
		All:                subfinder.All,                 // Use all Sources
		OnlyRecursive:      subfinder.Recursive,           // Enumerate Recursively
		Resolvers:          GetProperty("Resolvers"),      // Use the default list of resolvers by marshaling it to the config
		Sources:            GetProperty("Sources"),        // Use the default list of passive sources
		AllSources:         GetProperty("AllSources"),     // Use the default list of all passive sources
		Recursive:          GetProperty("Recursive"),      // Use the default list of recursive sources
		ExcludeSources:     GetProperty("ExcludeSources"), // ExcludeSources contains the sources to not include in the enumeration process

		// API keys for different sources
		Providers: &runner.Providers{
			Bufferover:     GetProperty("Bufferover"),
			Binaryedge:     GetProperty("Binaryedge"),
			C99:            GetProperty("C99"),
			Censys:         GetProperty("Censys"),
			Certspotter:    GetProperty("Certspotter"),
			Chaos:          GetProperty("Chaos"),
			Chinaz:         GetProperty("Chinaz"),
			DNSDB:          GetProperty("Dnsdb"),
			GitHub:         GetProperty("Github"),
			IntelX:         GetProperty("Intelx"),
			PassiveTotal:   GetProperty("Passivetotal"),
			Robtex:         GetProperty("Robtex"),
			SecurityTrails: GetProperty("Securitytrails"),
			Shodan:         GetProperty("Shodan"),
			Spyse:          GetProperty("Spyse"),
			ThreatBook:     GetProperty("Threatbook"),
			URLScan:        GetProperty("Urlscan"),
			Virustotal:     GetProperty("Virustotal"),
			ZoomEye:        GetProperty("Zoomeye"),
			ZoomEyeApi:     GetProperty("Zoomeyeapi"),
			Fofa:           GetProperty("Fofa"),
			FullHunt:       GetProperty("Fullhunt"),
		},
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

	// Array size
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

func main() {}
