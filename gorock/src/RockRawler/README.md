# RockRawler

A modified version of hakrawler, it's fast web crawler .

## Why
i developed it to improve hakrawler and make it better, and make it extendable to C language\
You can now embed RockRawler with existing C projects and therefore you can use RockRawler with more languages like python and ruby if developed your own extension using C API of that languages.

## Notes
- Extendable to C language (Take a look at usage below)
- RockRawler removes non-unique results automatically (more Faster and better)
- Fix hakrawler bug (fail when scheme not supplied)

## Installation

First, you'll need to [install go](https://golang.org/doc/install).

Then run this command to download + compile RockRawler:
```
go install github.com/abdallah-elsharif/RockRawler@latest
```

You can now run `~/go/bin/RockRawler`. If you'd like to just run `RockRawler` without the full path, you'll need to `export PATH="/go/bin/:$PATH"`. You can also add this line to your `~/.bashrc` file if you'd like this to persist.

## Example usages

Single URL:

```
echo https://google.com | RockRawler
```

Multiple URLs:

```
cat urls.txt | RockRawler
```

Include subdomains:

```
echo https://google.com | RockRawler -subs
```

> Note: a common issue is that the tool returns no URLs. This usually happens when a domain is specified (https://example.com), but it redirects to a subdomain (https://www.example.com). The subdomain is not included in the scope, so the no URLs are printed. In order to overcome this, either specify the final URL in the redirect chain or use the `-subs` option to include subdomains.

## Example tool chain

Get all subdomains of google, find the ones that respond to http(s), crawl them all.

```
echo google.com | haktrails subdomains | httpx | RockRawler
```

## Command-line options
```
  -d int
    	Depth to crawl. (default 2)
  -h string
    	Custom headers separated by two semi-colons. E.g. -h "Cookie: foo=bar;;Referer: http://example.com/"
  -insecure
    	Disable TLS verification.
  -subs
    	Include subdomains for crawling.
  -t int
    	Number of threads to utilise. (default 5)
```

## C Usage
First you must build RockRawler via this command `go build -buildmode=c-archive RockRawler.go`\
Then you will get two files that you use in your project named `RockRawler.a` and `RockRawler.h`

### RockRawler API
```
extern char** CStartCrawler(GoString url, GoInt threads, GoInt depth, GoUint8 subsInScope, GoUint8 insecure, GoString rawHeaders);
```

### Simple example
This is an example of usage RockRawler from C

```
#include "RockRawler.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

GoString BuildGoStr(char *str) { /* Convert C String to Go String */
    GoString GoStr;
    GoStr.p = str;
    GoStr.n = strlen(str);
    return GoStr;
}

void printResults(char **results) { /* Print RockRawler results */
    for (; *results; results++)
    {
        printf("Link obtained by RockRawler -> %s\n",*results);
    }
}

void main(void) {
    char **results; 
    /* Start RockRawler and pass (URL, Threads, Depth, subsInScope, insecure, Headers) */
    results = CStartCrawler(BuildGoStr("https://www.example.com"), 5, 2, 0, 0, BuildGoStr("Cookie: foo=bar;;Referer: http://example.com/"));
    printResults(results); /* print results */
    free(results); /* We must free memory allocation when finished */
}
```

compile via `gcc -pthread yourprogram.c RockRawler.a -o yourprogram` note The -pthread option is needed because the Go runtime makes use of threads

## Finally
Thank you to the original developers of hakrawler.