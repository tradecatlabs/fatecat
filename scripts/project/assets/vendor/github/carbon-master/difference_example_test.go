package carbon_test

import (
	"fmt"

	"github.com/dromara/carbon/v2"
)

func ExampleCarbon_DiffInYears() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInYears(carbon.Parse("2020-08-05 13:14:15")))
	fmt.Println(carbon.Parse("2020-12-31 13:14:15").DiffInYears(carbon.Parse("2021-01-01 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInYears(carbon.Parse("2021-08-28 13:14:59")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInYears(carbon.Parse("2018-08-28 13:14:59")))

	// Output:
	// 0
	// 0
	// 1
	// -1
}

func ExampleCarbon_DiffAbsInYears() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInYears(carbon.Parse("2020-08-05 13:14:15")))
	fmt.Println(carbon.Parse("2020-12-31 13:14:15").DiffAbsInYears(carbon.Parse("2021-01-01 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInYears(carbon.Parse("2021-08-28 13:14:59")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInYears(carbon.Parse("2018-08-28 13:14:59")))

	// Output:
	// 0
	// 0
	// 1
	// 1
}

func ExampleCarbon_DiffInMonths() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInMonths(carbon.Parse("2020-08-05 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInMonths(carbon.Parse("2020-07-28 13:14:00")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInMonths(carbon.Parse("2020-09-06 13:14:59")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInMonths(carbon.Parse("2018-08-28 13:14:59")))

	// Output:
	// 0
	// 0
	// 1
	// -23
}

func ExampleCarbon_DiffAbsInMonths() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInMonths(carbon.Parse("2020-08-05 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInMonths(carbon.Parse("2020-07-28 13:14:00")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInMonths(carbon.Parse("2020-09-06 13:14:59")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInMonths(carbon.Parse("2018-08-28 13:14:59")))

	// Output:
	// 0
	// 0
	// 1
	// 23
}

func ExampleCarbon_DiffInWeeks() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInWeeks(carbon.Parse("2020-08-05 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInWeeks(carbon.Parse("2020-07-28 13:14:00")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInWeeks(carbon.Parse("2020-08-12 13:14:15")))

	// Output:
	// 0
	// -1
	// 1
}

func ExampleCarbon_DiffAbsInWeeks() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInWeeks(carbon.Parse("2020-08-05 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInWeeks(carbon.Parse("2020-07-28 13:14:00")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInWeeks(carbon.Parse("2020-08-12 13:14:15")))

	// Output:
	// 0
	// 1
	// 1
}

func ExampleCarbon_DiffInDays() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInDays(carbon.Parse("2020-08-05 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInDays(carbon.Parse("2020-08-04 13:14:59")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInDays(carbon.Parse("2020-08-06 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInDays(carbon.Parse("2020-08-04 13:00:00")))

	// Output:
	// 0
	// 0
	// 1
	// -1
}

func ExampleCarbon_DiffAbsInDays() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInDays(carbon.Parse("2020-08-05 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInDays(carbon.Parse("2020-08-04 13:14:59")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInDays(carbon.Parse("2020-08-06 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInDays(carbon.Parse("2020-08-04 13:00:00")))

	// Output:
	// 0
	// 0
	// 1
	// 1
}

func ExampleCarbon_DiffInHours() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInHours(carbon.Parse("2020-08-05 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInHours(carbon.Parse("2020-08-05 14:13:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInHours(carbon.Parse("2020-08-05 12:14:00")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInHours(carbon.Parse("2020-08-05 14:14:15")))

	// Output:
	// 0
	// 0
	// -1
	// 1
}

func ExampleCarbon_DiffAbsInHours() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInHours(carbon.Parse("2020-08-05 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInHours(carbon.Parse("2020-08-05 14:13:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInHours(carbon.Parse("2020-08-05 12:14:00")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInHours(carbon.Parse("2020-08-05 14:14:15")))

	// Output:
	// 0
	// 0
	// 1
	// 1
}

func ExampleCarbon_DiffInMinutes() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInMinutes(carbon.Parse("2020-08-05 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInMinutes(carbon.Parse("2020-08-05 13:15:10")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInMinutes(carbon.Parse("2020-08-05 13:13:00")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInMinutes(carbon.Parse("2020-08-05 13:15:15")))

	// Output:
	// 0
	// 0
	// -1
	// 1
}

func ExampleCarbon_DiffAbsInMinutes() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInMinutes(carbon.Parse("2020-08-05 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInMinutes(carbon.Parse("2020-08-05 13:15:10")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInMinutes(carbon.Parse("2020-08-05 13:13:00")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInMinutes(carbon.Parse("2020-08-05 13:15:15")))

	// Output:
	// 0
	// 0
	// 1
	// 1
}

func ExampleCarbon_DiffInSeconds() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInSeconds(carbon.Parse("2020-08-05 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInSeconds(carbon.Parse("2020-08-05 13:14:15.999999")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInSeconds(carbon.Parse("2020-08-05 13:14:20")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffInSeconds(carbon.Parse("2020-08-05 13:14:10")))

	// Output:
	// 0
	// 0
	// 5
	// -5
}

func ExampleCarbon_DiffAbsInSeconds() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInSeconds(carbon.Parse("2020-08-05 13:14:15")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInSeconds(carbon.Parse("2020-08-05 13:14:15.999999")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInSeconds(carbon.Parse("2020-08-05 13:14:20")))
	fmt.Println(carbon.Parse("2020-08-05 13:14:15").DiffAbsInSeconds(carbon.Parse("2020-08-05 13:14:10")))

	// Output:
	// 0
	// 0
	// 5
	// 5
}

func ExampleCarbon_DiffInString() {
	defer carbon.ClearTestNow()
	now := carbon.Parse("2020-08-05 13:14:15")
	carbon.SetTestNow(now)

	fmt.Println(now.Copy().DiffInString(now))
	fmt.Println(now.Copy().AddYearsNoOverflow(1).DiffInString(now))
	fmt.Println(now.Copy().SubYearsNoOverflow(1).DiffInString(now))
	fmt.Println(now.Copy().AddMonthsNoOverflow(1).DiffInString(now))
	fmt.Println(now.Copy().SubMonthsNoOverflow(1).DiffInString(now))
	fmt.Println(now.Copy().AddWeeks(1).DiffInString(now))
	fmt.Println(now.Copy().SubWeeks(1).DiffInString(now))
	fmt.Println(now.Copy().AddDays(1).DiffInString(now))
	fmt.Println(now.Copy().SubDays(1).DiffInString(now))
	fmt.Println(now.Copy().AddHours(1).DiffInString(now))
	fmt.Println(now.Copy().SubHours(1).DiffInString(now))
	fmt.Println(now.Copy().AddMinutes(1).DiffInString(now))
	fmt.Println(now.Copy().SubMinutes(1).DiffInString(now))
	fmt.Println(now.Copy().AddSeconds(1).DiffInString(now))
	fmt.Println(now.Copy().SubSeconds(1).DiffInString(now))

	// Output:
	// just now
	// -1 year
	// 1 year
	// -1 month
	// 1 month
	// -1 week
	// 1 week
	// -1 day
	// 1 day
	// -1 hour
	// 1 hour
	// -1 minute
	// 1 minute
	// -1 second
	// 1 second
}

func ExampleCarbon_DiffAbsInString() {
	defer carbon.ClearTestNow()
	now := carbon.Parse("2020-08-05 13:14:15")
	carbon.SetTestNow(now)

	fmt.Println(now.Copy().DiffAbsInString(now))
	fmt.Println(now.Copy().AddYearsNoOverflow(1).DiffAbsInString(now))
	fmt.Println(now.Copy().SubYearsNoOverflow(1).DiffAbsInString(now))
	fmt.Println(now.Copy().AddMonthsNoOverflow(1).DiffAbsInString(now))
	fmt.Println(now.Copy().SubMonthsNoOverflow(1).DiffAbsInString(now))
	fmt.Println(now.Copy().AddWeeks(1).DiffAbsInString(now))
	fmt.Println(now.Copy().SubWeeks(1).DiffAbsInString(now))
	fmt.Println(now.Copy().AddDays(1).DiffAbsInString(now))
	fmt.Println(now.Copy().SubDays(1).DiffAbsInString(now))
	fmt.Println(now.Copy().AddHours(1).DiffAbsInString(now))
	fmt.Println(now.Copy().SubHours(1).DiffAbsInString(now))
	fmt.Println(now.Copy().AddMinutes(1).DiffAbsInString(now))
	fmt.Println(now.Copy().SubMinutes(1).DiffAbsInString(now))
	fmt.Println(now.Copy().AddSeconds(1).DiffAbsInString(now))
	fmt.Println(now.Copy().SubSeconds(1).DiffAbsInString(now))

	// Output:
	// just now
	// 1 year
	// 1 year
	// 1 month
	// 1 month
	// 1 week
	// 1 week
	// 1 day
	// 1 day
	// 1 hour
	// 1 hour
	// 1 minute
	// 1 minute
	// 1 second
	// 1 second
}

func ExampleCarbon_DiffInDuration() {
	defer carbon.ClearTestNow()
	now := carbon.Parse("2020-08-05 13:14:15")
	carbon.SetTestNow(now)

	fmt.Println(now.Copy().DiffInDuration(now))
	fmt.Println(now.Copy().AddYearsNoOverflow(1).DiffInDuration(now).String())
	fmt.Println(now.Copy().SubYearsNoOverflow(1).DiffInDuration(now).String())
	fmt.Println(now.Copy().AddMonthsNoOverflow(1).DiffInDuration(now).String())
	fmt.Println(now.Copy().SubMonthsNoOverflow(1).DiffInDuration(now).String())
	fmt.Println(now.Copy().AddDays(1).DiffInDuration(now).String())
	fmt.Println(now.Copy().SubDays(1).DiffInDuration(now).String())

	// Output:
	// 0s
	// -8760h0m0s
	// 8784h0m0s
	// -744h0m0s
	// 744h0m0s
	// -24h0m0s
	// 24h0m0s
}

func ExampleCarbon_DiffAbsInDuration() {
	defer carbon.ClearTestNow()
	now := carbon.Parse("2020-08-05 13:14:15")
	carbon.SetTestNow(now)

	fmt.Println(now.Copy().DiffAbsInDuration(now))
	fmt.Println(now.Copy().AddYearsNoOverflow(1).DiffAbsInDuration(now).String())
	fmt.Println(now.Copy().SubYearsNoOverflow(1).DiffAbsInDuration(now).String())
	fmt.Println(now.Copy().AddMonthsNoOverflow(1).DiffAbsInDuration(now).String())
	fmt.Println(now.Copy().SubMonthsNoOverflow(1).DiffAbsInDuration(now).String())
	fmt.Println(now.Copy().AddDays(1).DiffAbsInDuration(now).String())
	fmt.Println(now.Copy().SubDays(1).DiffAbsInDuration(now).String())

	// Output:
	// 0s
	// 8760h0m0s
	// 8784h0m0s
	// 744h0m0s
	// 744h0m0s
	// 24h0m0s
	// 24h0m0s
}

func ExampleCarbon_DiffForHumans() {
	defer carbon.ClearTestNow()
	now := carbon.Parse("2020-08-05 13:14:15")
	carbon.SetTestNow(now)

	fmt.Println(now.Copy().DiffForHumans(now))
	fmt.Println(carbon.Parse("2020-08-03 13:14:15").DiffForHumans())
	fmt.Println(carbon.Parse("2020-08-07 13:14:15").DiffForHumans())
	fmt.Println(now.Copy().AddYearsNoOverflow(1).DiffForHumans(now))
	fmt.Println(now.Copy().SubYearsNoOverflow(1).DiffForHumans(now))
	fmt.Println(now.Copy().AddMonthsNoOverflow(1).DiffForHumans(now))
	fmt.Println(now.Copy().SubMonthsNoOverflow(1).DiffForHumans(now))
	fmt.Println(now.Copy().AddDays(1).DiffForHumans(now))
	fmt.Println(now.Copy().SubDays(1).DiffForHumans(now))

	// Output:
	// just now
	// 2 days ago
	// 2 days from now
	// 1 year after
	// 1 year before
	// 1 month after
	// 1 month before
	// 1 day after
	// 1 day before
}
