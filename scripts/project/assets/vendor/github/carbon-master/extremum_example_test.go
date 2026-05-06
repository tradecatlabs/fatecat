package carbon_test

import (
	"fmt"

	"github.com/dromara/carbon/v2"
)

func ExampleZeroValue() {
	fmt.Println(carbon.ZeroValue().ToString())

	// Output:
	// 0001-01-01 00:00:00 +0000 UTC
}

func ExampleEpochValue() {
	fmt.Println(carbon.EpochValue().ToString())

	// Output:
	// 1970-01-01 00:00:00 +0000 UTC
}

func ExampleMaxValue() {
	fmt.Println(carbon.MaxValue().ToString())

	// Output:
	// 9999-12-31 23:59:59.999999999 +0000 UTC
}

func ExampleMinValue() {
	fmt.Println(carbon.MinValue().ToString())

	// Output:
	// 0001-01-01 00:00:00 +0000 UTC
}

func ExampleMaxDuration() {
	fmt.Println(carbon.MaxDuration().Seconds())

	// Output:
	// 9.223372036854776e+09
}

func ExampleMinDuration() {
	fmt.Println(carbon.MinDuration().Seconds())

	// Output:
	// -9.223372036854776e+09
}

func ExampleMax() {
	c1 := carbon.Parse("2020-08-01")
	c2 := carbon.Parse("2020-08-05")
	c3 := carbon.Parse("2020-08-06")
	fmt.Println(carbon.Max(c1, c2, c3).ToString())

	// Output:
	// 2020-08-06 00:00:00 +0000 UTC
}

func ExampleMin() {
	c1 := carbon.Parse("2020-08-01")
	c2 := carbon.Parse("2020-08-05")
	c3 := carbon.Parse("2020-08-06")
	fmt.Println(carbon.Min(c1, c2, c3).ToString())

	// Output:
	// 2020-08-01 00:00:00 +0000 UTC
}

func ExampleCarbon_Closest() {
	c1 := carbon.Parse("2020-08-01")
	c2 := carbon.Parse("2020-08-05")
	c3 := carbon.Parse("2020-08-06")
	fmt.Println(c1.Closest(c2, c3).ToString())
	fmt.Println(c2.Closest(c1, c3).ToString())
	fmt.Println(c3.Closest(c2, c1).ToString())

	// Output:
	// 2020-08-05 00:00:00 +0000 UTC
	// 2020-08-06 00:00:00 +0000 UTC
	// 2020-08-05 00:00:00 +0000 UTC
}

func ExampleCarbon_Farthest() {
	c1 := carbon.Parse("2020-08-01")
	c2 := carbon.Parse("2020-08-05")
	c3 := carbon.Parse("2020-08-06")
	fmt.Println(c1.Farthest(c2, c3).ToString())
	fmt.Println(c2.Farthest(c1, c3).ToString())
	fmt.Println(c3.Farthest(c1, c2).ToString())

	// Output:
	// 2020-08-06 00:00:00 +0000 UTC
	// 2020-08-01 00:00:00 +0000 UTC
	// 2020-08-01 00:00:00 +0000 UTC
}
