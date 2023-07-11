package output

import (
	"github.com/abdallah-elsharif/WRock/gorock/src/ffuf/pkg/ffuf"
)

func NewOutputProviderByName(name string, conf *ffuf.Config) ffuf.OutputProvider {
	return NewGoRockOutput(conf)
}
