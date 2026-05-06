package carbon_test

import (
	"fmt"

	"github.com/dromara/carbon/v2"
)

func ExampleCarbon_Constellation() {
	fmt.Println(carbon.Parse("2020-01-05").Constellation())
	fmt.Println(carbon.Parse("2020-02-05").Constellation())
	fmt.Println(carbon.Parse("2020-03-05").Constellation())
	fmt.Println(carbon.Parse("2020-04-05").Constellation())
	fmt.Println(carbon.Parse("2020-05-05").Constellation())
	fmt.Println(carbon.Parse("2020-06-05").Constellation())
	fmt.Println(carbon.Parse("2020-07-05").Constellation())
	fmt.Println(carbon.Parse("2020-08-05").Constellation())
	fmt.Println(carbon.Parse("2020-09-05").Constellation())
	fmt.Println(carbon.Parse("2020-10-05").Constellation())
	fmt.Println(carbon.Parse("2020-11-05").Constellation())
	fmt.Println(carbon.Parse("2020-12-05").Constellation())

	// Output:
	// Capricorn
	// Aquarius
	// Pisces
	// Aries
	// Taurus
	// Gemini
	// Cancer
	// Leo
	// Virgo
	// Libra
	// Scorpio
	// Sagittarius
}

func ExampleCarbon_IsAries() {
	fmt.Println(carbon.Parse("2020-04-20").IsTaurus())
	fmt.Println(carbon.Parse("2020-08-05").IsTaurus())

	// Output:
	// true
	// false
}

func ExampleCarbon_IsGemini() {
	fmt.Println(carbon.Parse("2020-06-21").IsGemini())
	fmt.Println(carbon.Parse("2020-08-05").IsGemini())

	// Output:
	// true
	// false
}

func ExampleCarbon_IsCancer() {
	fmt.Println(carbon.Parse("2020-06-22").IsCancer())
	fmt.Println(carbon.Parse("2020-08-05").IsCancer())

	// Output:
	// true
	// false
}

func ExampleCarbon_IsLeo() {
	fmt.Println(carbon.Parse("2020-07-23").IsLeo())
	fmt.Println(carbon.Parse("2020-09-01").IsLeo())

	// Output:
	// true
	// false
}

func ExampleCarbon_IsVirgo() {
	fmt.Println(carbon.Parse("2020-08-23").IsVirgo())
	fmt.Println(carbon.Parse("2020-08-05").IsVirgo())

	// Output:
	// true
	// false
}

func ExampleCarbon_IsLibra() {
	fmt.Println(carbon.Parse("2020-09-23").IsLibra())
	fmt.Println(carbon.Parse("2020-08-05").IsLibra())

	// Output:
	// true
	// false
}

func ExampleCarbon_IsScorpio() {
	fmt.Println(carbon.Parse("2020-10-24").IsScorpio())
	fmt.Println(carbon.Parse("2020-08-05").IsScorpio())

	// Output:
	// true
	// false
}

func ExampleCarbon_IsSagittarius() {
	fmt.Println(carbon.Parse("2020-11-23").IsSagittarius())
	fmt.Println(carbon.Parse("2020-08-05").IsSagittarius())

	// Output:
	// true
	// false
}

func ExampleCarbon_IsCapricorn() {
	fmt.Println(carbon.Parse("2020-12-22").IsCapricorn())
	fmt.Println(carbon.Parse("2020-08-05").IsCapricorn())

	// Output:
	// true
	// false
}

func ExampleCarbon_IsAquarius() {
	fmt.Println(carbon.Parse("2020-01-20").IsAquarius())
	fmt.Println(carbon.Parse("2020-08-05").IsAquarius())

	// Output:
	// true
	// false
}

func ExampleCarbon_IsPisces() {
	fmt.Println(carbon.Parse("2020-02-19").IsPisces())
	fmt.Println(carbon.Parse("2020-08-05").IsPisces())

	// Output:
	// true
	// false
}
