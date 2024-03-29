package scraper

import (
	"fmt"
	"strings"

	"github.com/0xNinjaCyclone/WRock/gorock/src/ffuf/pkg/ffuf"
)

func headerString(headers map[string][]string) string {
	val := ""
	for k, vslice := range headers {
		for _, v := range vslice {
			val += fmt.Sprintf("%s: %s\n", k, v)
		}
	}
	return val
}

func isActive(name string, activegroups []string) bool {
	return ffuf.StrInSlice(strings.ToLower(strings.TrimSpace(name)), activegroups)
}

func parseActiveGroups(activestr string) []string {
	retslice := make([]string, 0)
	for _, v := range strings.Split(activestr, ",") {
		retslice = append(retslice, strings.ToLower(strings.TrimSpace(v)))
	}
	return retslice
}
