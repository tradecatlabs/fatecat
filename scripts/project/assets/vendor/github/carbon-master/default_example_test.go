package carbon_test

import (
	"fmt"

	"github.com/dromara/carbon/v2"
)

func ExampleSetDefault() {
	defer carbon.ResetDefault()

	carbon.SetDefault(carbon.Default{
		Layout:       carbon.DateTimeLayout,
		Timezone:     carbon.PRC,
		Locale:       "zh-CN",
		WeekStartsAt: carbon.Monday,
		WeekendDays: []carbon.Weekday{
			carbon.Saturday, carbon.Sunday,
		},
	})

	fmt.Println("default layout:", carbon.DefaultLayout)
	fmt.Println("default timezone:", carbon.DefaultTimezone)
	fmt.Println("default week starts at:", carbon.DefaultWeekStartsAt)
	fmt.Println("default weekend days:", carbon.DefaultWeekendDays)
	fmt.Println("default locale:", carbon.DefaultLocale)

	// Output:
	// default layout: 2006-01-02 15:04:05
	// default timezone: PRC
	// default week starts at: Monday
	// default weekend days: [Saturday Sunday]
	// default locale: zh-CN
}
