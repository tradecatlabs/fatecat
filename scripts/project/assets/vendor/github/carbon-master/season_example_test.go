package carbon_test

import (
	"fmt"

	"github.com/dromara/carbon/v2"
)

func ExampleCarbon_Season() {
	fmt.Println(carbon.Parse("2020-01-05").Season())
	fmt.Println(carbon.Parse("2020-02-05").Season())
	fmt.Println(carbon.Parse("2020-03-05").Season())
	fmt.Println(carbon.Parse("2020-04-05").Season())
	fmt.Println(carbon.Parse("2020-05-05").Season())
	fmt.Println(carbon.Parse("2020-06-05").Season())
	fmt.Println(carbon.Parse("2020-07-05").Season())
	fmt.Println(carbon.Parse("2020-08-05").Season())
	fmt.Println(carbon.Parse("2020-09-05").Season())
	fmt.Println(carbon.Parse("2020-10-05").Season())
	fmt.Println(carbon.Parse("2020-11-05").Season())
	fmt.Println(carbon.Parse("2020-12-05").Season())

	// Output:
	// Winter
	// Winter
	// Spring
	// Spring
	// Spring
	// Summer
	// Summer
	// Summer
	// Autumn
	// Autumn
	// Autumn
	// Winter
}

func ExampleCarbon_StartOfSeason() {
	fmt.Println(carbon.Parse("2020-01-15").StartOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-02-15").StartOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-03-15").StartOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-04-15").StartOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-05-15").StartOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-06-15").StartOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-07-15").StartOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-08-15").StartOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-09-15").StartOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-10-15").StartOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-11-15").StartOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-12-15").StartOfSeason().ToString())

	// Output:
	// 2019-12-01 00:00:00 +0000 UTC
	// 2019-12-01 00:00:00 +0000 UTC
	// 2020-03-01 00:00:00 +0000 UTC
	// 2020-03-01 00:00:00 +0000 UTC
	// 2020-03-01 00:00:00 +0000 UTC
	// 2020-06-01 00:00:00 +0000 UTC
	// 2020-06-01 00:00:00 +0000 UTC
	// 2020-06-01 00:00:00 +0000 UTC
	// 2020-09-01 00:00:00 +0000 UTC
	// 2020-09-01 00:00:00 +0000 UTC
	// 2020-09-01 00:00:00 +0000 UTC
	// 2020-12-01 00:00:00 +0000 UTC
}

func ExampleCarbon_EndOfSeason() {
	fmt.Println(carbon.Parse("2020-01-15").EndOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-02-15").EndOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-03-15").EndOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-04-15").EndOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-05-15").EndOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-06-15").EndOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-07-15").EndOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-08-15").EndOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-09-15").EndOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-10-15").EndOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-11-15").EndOfSeason().ToString())
	fmt.Println(carbon.Parse("2020-12-15").EndOfSeason().ToString())

	// Output:
	// 2020-02-29 23:59:59.999999999 +0000 UTC
	// 2020-02-29 23:59:59.999999999 +0000 UTC
	// 2020-05-31 23:59:59.999999999 +0000 UTC
	// 2020-05-31 23:59:59.999999999 +0000 UTC
	// 2020-05-31 23:59:59.999999999 +0000 UTC
	// 2020-08-31 23:59:59.999999999 +0000 UTC
	// 2020-08-31 23:59:59.999999999 +0000 UTC
	// 2020-08-31 23:59:59.999999999 +0000 UTC
	// 2020-11-30 23:59:59.999999999 +0000 UTC
	// 2020-11-30 23:59:59.999999999 +0000 UTC
	// 2020-11-30 23:59:59.999999999 +0000 UTC
	// 2021-02-28 23:59:59.999999999 +0000 UTC
}

func ExampleCarbon_IsSpring() {
	fmt.Println(carbon.Parse("2020-01-01").IsSpring())
	fmt.Println(carbon.Parse("2020-03-01").IsSpring())

	// Output:
	// false
	// true
}

func ExampleCarbon_IsSummer() {
	fmt.Println(carbon.Parse("2020-01-01").IsSummer())
	fmt.Println(carbon.Parse("2020-06-01").IsSummer())

	// Output:
	// false
	// true
}

func ExampleCarbon_IsAutumn() {
	fmt.Println(carbon.Parse("2020-01-01").IsAutumn())
	fmt.Println(carbon.Parse("2020-09-01").IsAutumn())

	// Output:
	// false
	// true
}

func ExampleCarbon_IsWinter() {
	fmt.Println(carbon.Parse("2020-01-01").IsWinter())
	fmt.Println(carbon.Parse("2020-05-01").IsWinter())

	// Output:
	// true
	// false
}
