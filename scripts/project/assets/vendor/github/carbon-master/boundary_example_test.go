package carbon_test

import (
	"fmt"

	"github.com/dromara/carbon/v2"
)

func ExampleCarbon_StartOfCentury() {
	fmt.Println(carbon.NewCarbon().StartOfCentury().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").StartOfCentury().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").StartOfCentury().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").StartOfCentury().ToString())

	// Output:
	// 0000-01-01 00:00:00 +0000 UTC
	// 2000-01-01 00:00:00 +0000 UTC
	// 2000-01-01 00:00:00 +0000 UTC
	// 2000-01-01 00:00:00 +0000 UTC
}

func ExampleCarbon_EndOfCentury() {
	fmt.Println(carbon.NewCarbon().EndOfCentury().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").EndOfCentury().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").EndOfCentury().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").EndOfCentury().ToString())

	// Output:
	// 0099-12-31 23:59:59.999999999 +0000 UTC
	// 2099-12-31 23:59:59.999999999 +0000 UTC
	// 2099-12-31 23:59:59.999999999 +0000 UTC
	// 2099-12-31 23:59:59.999999999 +0000 UTC
}

func ExampleCarbon_StartOfDecade() {
	fmt.Println(carbon.NewCarbon().StartOfDecade().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").StartOfDecade().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").StartOfDecade().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").StartOfDecade().ToString())

	// Output:
	// 0000-01-01 00:00:00 +0000 UTC
	// 2020-01-01 00:00:00 +0000 UTC
	// 2020-01-01 00:00:00 +0000 UTC
	// 2020-01-01 00:00:00 +0000 UTC
}

func ExampleCarbon_EndOfDecade() {
	fmt.Println(carbon.NewCarbon().EndOfDecade().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").EndOfDecade().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").EndOfDecade().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").EndOfDecade().ToString())

	// Output:
	// 0009-12-31 23:59:59.999999999 +0000 UTC
	// 2029-12-31 23:59:59.999999999 +0000 UTC
	// 2029-12-31 23:59:59.999999999 +0000 UTC
	// 2029-12-31 23:59:59.999999999 +0000 UTC
}

func ExampleCarbon_StartOfYear() {
	fmt.Println(carbon.NewCarbon().StartOfYear().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").StartOfYear().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").StartOfYear().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").StartOfYear().ToString())

	// Output:
	// 0001-01-01 00:00:00 +0000 UTC
	// 2020-01-01 00:00:00 +0000 UTC
	// 2020-01-01 00:00:00 +0000 UTC
	// 2020-01-01 00:00:00 +0000 UTC
}

func ExampleCarbon_EndOfYear() {
	fmt.Println(carbon.NewCarbon().EndOfYear().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").EndOfYear().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").EndOfYear().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").EndOfYear().ToString())

	// Output:
	// 0001-12-31 23:59:59.999999999 +0000 UTC
	// 2020-12-31 23:59:59.999999999 +0000 UTC
	// 2020-12-31 23:59:59.999999999 +0000 UTC
	// 2020-12-31 23:59:59.999999999 +0000 UTC
}

func ExampleCarbon_StartOfQuarter() {
	fmt.Println(carbon.NewCarbon().StartOfQuarter().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").StartOfQuarter().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").StartOfQuarter().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").StartOfQuarter().ToString())

	// Output:
	// 0001-01-01 00:00:00 +0000 UTC
	// 2020-01-01 00:00:00 +0000 UTC
	// 2020-07-01 00:00:00 +0000 UTC
	// 2020-10-01 00:00:00 +0000 UTC
}

func ExampleCarbon_EndOfQuarter() {
	fmt.Println(carbon.NewCarbon().EndOfQuarter().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").EndOfQuarter().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").EndOfQuarter().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").EndOfQuarter().ToString())

	// Output:
	// 0001-03-31 23:59:59.999999999 +0000 UTC
	// 2020-03-31 23:59:59.999999999 +0000 UTC
	// 2020-09-30 23:59:59.999999999 +0000 UTC
	// 2020-12-31 23:59:59.999999999 +0000 UTC
}

func ExampleCarbon_StartOfMonth() {
	fmt.Println(carbon.NewCarbon().StartOfMonth().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").StartOfMonth().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").StartOfMonth().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").StartOfMonth().ToString())

	// Output:
	// 0001-01-01 00:00:00 +0000 UTC
	// 2020-01-01 00:00:00 +0000 UTC
	// 2020-08-01 00:00:00 +0000 UTC
	// 2020-12-01 00:00:00 +0000 UTC
}

func ExampleCarbon_EndOfMonth() {
	fmt.Println(carbon.NewCarbon().EndOfMonth().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").EndOfMonth().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").EndOfMonth().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").EndOfMonth().ToString())

	// Output:
	// 0001-01-31 23:59:59.999999999 +0000 UTC
	// 2020-01-31 23:59:59.999999999 +0000 UTC
	// 2020-08-31 23:59:59.999999999 +0000 UTC
	// 2020-12-31 23:59:59.999999999 +0000 UTC
}

func ExampleCarbon_StartOfWeek() {
	fmt.Println(carbon.NewCarbon().StartOfWeek().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").StartOfWeek().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").StartOfWeek().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").StartOfWeek().ToString())

	// Output:
	// 0001-01-01 00:00:00 +0000 UTC
	// 2019-12-30 00:00:00 +0000 UTC
	// 2020-08-10 00:00:00 +0000 UTC
	// 2020-12-28 00:00:00 +0000 UTC
}

func ExampleCarbon_EndOfWeek() {
	fmt.Println(carbon.NewCarbon().EndOfWeek().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").EndOfWeek().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").EndOfWeek().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").EndOfWeek().ToString())

	// Output:
	// 0001-01-07 23:59:59.999999999 +0000 UTC
	// 2020-01-05 23:59:59.999999999 +0000 UTC
	// 2020-08-16 23:59:59.999999999 +0000 UTC
	// 2021-01-03 23:59:59.999999999 +0000 UTC
}

func ExampleCarbon_StartOfDay() {
	fmt.Println(carbon.NewCarbon().StartOfDay().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").StartOfDay().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").StartOfDay().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").StartOfDay().ToString())

	// Output:
	// 0001-01-01 00:00:00 +0000 UTC
	// 2020-01-01 00:00:00 +0000 UTC
	// 2020-08-15 00:00:00 +0000 UTC
	// 2020-12-31 00:00:00 +0000 UTC
}

func ExampleCarbon_EndOfDay() {
	fmt.Println(carbon.NewCarbon().EndOfDay().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").EndOfDay().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").EndOfDay().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").EndOfDay().ToString())

	// Output:
	// 0001-01-01 23:59:59.999999999 +0000 UTC
	// 2020-01-01 23:59:59.999999999 +0000 UTC
	// 2020-08-15 23:59:59.999999999 +0000 UTC
	// 2020-12-31 23:59:59.999999999 +0000 UTC
}

func ExampleCarbon_StartOfHour() {
	fmt.Println(carbon.NewCarbon().StartOfHour().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").StartOfHour().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").StartOfHour().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").StartOfHour().ToString())

	// Output:
	// 0001-01-01 00:00:00 +0000 UTC
	// 2020-01-01 00:00:00 +0000 UTC
	// 2020-08-15 12:00:00 +0000 UTC
	// 2020-12-31 23:00:00 +0000 UTC
}

func ExampleCarbon_EndOfHour() {
	fmt.Println(carbon.NewCarbon().EndOfHour().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").EndOfHour().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").EndOfHour().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").EndOfHour().ToString())

	// Output:
	// 0001-01-01 00:59:59.999999999 +0000 UTC
	// 2020-01-01 00:59:59.999999999 +0000 UTC
	// 2020-08-15 12:59:59.999999999 +0000 UTC
	// 2020-12-31 23:59:59.999999999 +0000 UTC
}

func ExampleCarbon_StartOfMinute() {
	fmt.Println(carbon.NewCarbon().StartOfMinute().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").StartOfMinute().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").StartOfMinute().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").StartOfMinute().ToString())

	// Output:
	// 0001-01-01 00:00:00 +0000 UTC
	// 2020-01-01 00:00:00 +0000 UTC
	// 2020-08-15 12:30:00 +0000 UTC
	// 2020-12-31 23:59:00 +0000 UTC
}

func ExampleCarbon_EndOfMinute() {
	fmt.Println(carbon.NewCarbon().EndOfMinute().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").EndOfMinute().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").EndOfMinute().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").EndOfMinute().ToString())

	// Output:
	// 0001-01-01 00:00:59.999999999 +0000 UTC
	// 2020-01-01 00:00:59.999999999 +0000 UTC
	// 2020-08-15 12:30:59.999999999 +0000 UTC
	// 2020-12-31 23:59:59.999999999 +0000 UTC
}

func ExampleCarbon_StartOfSecond() {
	fmt.Println(carbon.NewCarbon().StartOfSecond().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").StartOfSecond().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").StartOfSecond().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").StartOfSecond().ToString())

	// Output:
	// 0001-01-01 00:00:00 +0000 UTC
	// 2020-01-01 00:00:00 +0000 UTC
	// 2020-08-15 12:30:30 +0000 UTC
	// 2020-12-31 23:59:59 +0000 UTC
}

func ExampleCarbon_EndOfSecond() {
	fmt.Println(carbon.NewCarbon().EndOfSecond().ToString())
	fmt.Println(carbon.Parse("2020-01-01 00:00:00").EndOfSecond().ToString())
	fmt.Println(carbon.Parse("2020-08-15 12:30:30").EndOfSecond().ToString())
	fmt.Println(carbon.Parse("2020-12-31 23:59:59").EndOfSecond().ToString())

	// Output:
	// 0001-01-01 00:00:00.999999999 +0000 UTC
	// 2020-01-01 00:00:00.999999999 +0000 UTC
	// 2020-08-15 12:30:30.999999999 +0000 UTC
	// 2020-12-31 23:59:59.999999999 +0000 UTC
}
