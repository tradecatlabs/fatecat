package carbon

import (
	"testing"

	"github.com/stretchr/testify/suite"
)

type DefaultSuite struct {
	suite.Suite
}

func TestDefaultSuite(t *testing.T) {
	suite.Run(t, new(DefaultSuite))
}

func (s *DefaultSuite) TearDownTest() {
	ResetDefault()
}

func (s *DefaultSuite) TestSetDefault() {
	SetDefault(Default{
		Layout:       DateTimeLayout,
		Timezone:     PRC,
		Locale:       "zh-CN",
		WeekStartsAt: Monday,
		WeekendDays: []Weekday{
			Saturday, Sunday,
		},
	})

	s.Equal(DateTimeLayout, DefaultLayout)
	s.Equal(PRC, DefaultTimezone)
	s.Equal("zh-CN", DefaultLocale)
	s.Equal(Monday, DefaultWeekStartsAt)
	s.Equal([]Weekday{
		Saturday, Sunday,
	}, DefaultWeekendDays)
}
