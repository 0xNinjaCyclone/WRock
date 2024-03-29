package runner

import (
	"github.com/0xNinjaCyclone/WRock/gorock/src/ffuf/pkg/ffuf"
)

func NewRunnerByName(name string, conf *ffuf.Config, replay bool) ffuf.RunnerProvider {
	// We have only one Runner at the moment
	return NewSimpleRunner(conf, replay)
}
