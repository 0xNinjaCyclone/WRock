package output

import (
	"sort"

	"github.com/abdallah-elsharif/WRock/gorock/src/ffuf/pkg/ffuf"
)

type GoRockOutput struct {
	config         *ffuf.Config
	fuzzkeywords   []string
	Results        []ffuf.Result
	CurrentResults []ffuf.Result
}

func NewGoRockOutput(conf *ffuf.Config) *GoRockOutput {
	var outp GoRockOutput
	outp.config = conf
	outp.Results = make([]ffuf.Result, 0)
	outp.CurrentResults = make([]ffuf.Result, 0)
	outp.fuzzkeywords = make([]string, 0)
	for _, ip := range conf.InputProviders {
		outp.fuzzkeywords = append(outp.fuzzkeywords, ip.Keyword)
	}
	sort.Strings(outp.fuzzkeywords)
	return &outp
}

func (s *GoRockOutput) Banner() {

}

// Reset resets the result slice
func (s *GoRockOutput) Reset() {
	s.CurrentResults = make([]ffuf.Result, 0)
}

// Cycle moves the CurrentResults to Results and resets the results slice
func (s *GoRockOutput) Cycle() {
	s.Results = append(s.Results, s.CurrentResults...)
	s.Reset()
}

// GetResults returns the result slice
func (s *GoRockOutput) GetCurrentResults() []ffuf.Result {
	return s.CurrentResults
}

// SetResults sets the result slice
func (s *GoRockOutput) SetCurrentResults(results []ffuf.Result) {
	s.CurrentResults = results
}

func (s *GoRockOutput) Progress(status ffuf.Progress) {

}

func (s *GoRockOutput) Info(infostring string) {

}

func (s *GoRockOutput) Error(errstring string) {

}

func (s *GoRockOutput) Warning(warnstring string) {

}

func (s *GoRockOutput) Raw(output string) {

}

// SaveFile saves the current results to a file of a given type
func (s *GoRockOutput) SaveFile(filename, format string) error {
	return nil
}

// Finalize gets run after all the ffuf jobs are completed
func (s *GoRockOutput) Finalize() error {
	return nil
}

func (s *GoRockOutput) Result(resp ffuf.Response) {
	inputs := make(map[string][]byte, len(resp.Request.Input))

	for k, v := range resp.Request.Input {
		inputs[k] = v
	}

	sResult := ffuf.Result{
		Input:            inputs,
		Position:         resp.Request.Position,
		StatusCode:       resp.StatusCode,
		ContentLength:    resp.ContentLength,
		ContentWords:     resp.ContentWords,
		ContentLines:     resp.ContentLines,
		ContentType:      resp.ContentType,
		RedirectLocation: resp.GetRedirectLocation(false),
		ScraperData:      resp.ScraperData,
		Url:              resp.Request.Url,
		Duration:         resp.Time,
		ResultFile:       resp.ResultFile,
		Host:             resp.Request.Host,
		Content:          resp.Body,
	}

	s.CurrentResults = append(s.CurrentResults, sResult)

}

func (s *GoRockOutput) PrintResult(res ffuf.Result) {

}
