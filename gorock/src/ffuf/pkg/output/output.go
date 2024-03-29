package output

import (
	"github.com/0xNinjaCyclone/WRock/gorock/src/ffuf/pkg/ffuf"
)

func NewOutputProviderByName(name string, conf *ffuf.Config) ffuf.OutputProvider {
	return NewGoRockOutput(conf)
}
