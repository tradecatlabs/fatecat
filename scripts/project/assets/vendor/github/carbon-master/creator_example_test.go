package carbon_test

import (
	"fmt"
	"time"

	"github.com/dromara/carbon/v2"
)

func ExampleCreateFromStdTime() {
	t1, _ := time.Parse(carbon.DateTimeLayout, "2020-08-05 13:14:15")
	fmt.Println(carbon.CreateFromStdTime(t1).ToString())

	loc, _ := time.LoadLocation(carbon.PRC)
	t2, _ := time.ParseInLocation(carbon.DateTimeLayout, "2020-08-05 13:14:15", loc)
	fmt.Println(carbon.CreateFromStdTime(t2).ToString())

	// Output:
	// 2020-08-05 13:14:15 +0000 UTC
	// 2020-08-05 13:14:15 +0800 CST
}

func ExampleCreateFromTimestamp() {
	fmt.Println(carbon.CreateFromTimestamp(-1).ToString())
	fmt.Println(carbon.CreateFromTimestamp(0).ToString())
	fmt.Println(carbon.CreateFromTimestamp(1, carbon.PRC).ToString())
	fmt.Println(carbon.CreateFromTimestamp(1649735755, carbon.PRC).ToString())

	// Output:
	// 1969-12-31 23:59:59 +0000 UTC
	// 1970-01-01 00:00:00 +0000 UTC
	// 1970-01-01 08:00:01 +0800 CST
	// 2022-04-12 11:55:55 +0800 CST
}

func ExampleCreateFromTimestampMilli() {
	fmt.Println(carbon.CreateFromTimestampMilli(-1).ToString())
	fmt.Println(carbon.CreateFromTimestampMilli(0).ToString())
	fmt.Println(carbon.CreateFromTimestampMilli(1, carbon.PRC).ToString())
	fmt.Println(carbon.CreateFromTimestampMilli(1649735755981, carbon.PRC).ToString())

	// Output:
	// 1969-12-31 23:59:59.999 +0000 UTC
	// 1970-01-01 00:00:00 +0000 UTC
	// 1970-01-01 08:00:00.001 +0800 CST
	// 2022-04-12 11:55:55.981 +0800 CST
}

func ExampleCreateFromTimestampMicro() {
	fmt.Println(carbon.CreateFromTimestampMicro(-1).ToString())
	fmt.Println(carbon.CreateFromTimestampMicro(0).ToString())
	fmt.Println(carbon.CreateFromTimestampMicro(1, carbon.PRC).ToString())
	fmt.Println(carbon.CreateFromTimestampMicro(1649735755981566, carbon.PRC).ToString())

	// Output:
	// 1969-12-31 23:59:59.999999 +0000 UTC
	// 1970-01-01 00:00:00 +0000 UTC
	// 1970-01-01 08:00:00.000001 +0800 CST
	// 2022-04-12 11:55:55.981566 +0800 CST
}

func ExampleCreateFromTimestampNano() {
	fmt.Println(carbon.CreateFromTimestampNano(-1).ToString())
	fmt.Println(carbon.CreateFromTimestampNano(0).ToString())
	fmt.Println(carbon.CreateFromTimestampNano(1, carbon.PRC).ToString())
	fmt.Println(carbon.CreateFromTimestampNano(1649735755981566888, carbon.PRC).ToString())

	// Output:
	// 1969-12-31 23:59:59.999999999 +0000 UTC
	// 1970-01-01 00:00:00 +0000 UTC
	// 1970-01-01 08:00:00.000000001 +0800 CST
	// 2022-04-12 11:55:55.981566888 +0800 CST
}

func ExampleCreateFromDateTime() {
	fmt.Println(carbon.CreateFromDateTime(2020, 8, 5, 13, 14, 15).ToString())
	fmt.Println(carbon.CreateFromDateTime(2020, 8, 5, 13, 14, 15, carbon.PRC).ToString())

	// Output:
	// 2020-08-05 13:14:15 +0000 UTC
	// 2020-08-05 13:14:15 +0800 CST
}

func ExampleCreateFromDateTimeMilli() {
	fmt.Println(carbon.CreateFromDateTimeMilli(2020, 8, 5, 13, 14, 15, 999).ToString())
	fmt.Println(carbon.CreateFromDateTimeMilli(2020, 8, 5, 13, 14, 15, 999, carbon.PRC).ToString())

	// Output:
	// 2020-08-05 13:14:15.999 +0000 UTC
	// 2020-08-05 13:14:15.999 +0800 CST
}

func ExampleCreateFromDateTimeMicro() {
	fmt.Println(carbon.CreateFromDateTimeMicro(2020, 8, 5, 13, 14, 15, 999999).ToString())
	fmt.Println(carbon.CreateFromDateTimeMicro(2020, 8, 5, 13, 14, 15, 999999, carbon.PRC).ToString())

	// Output:
	// 2020-08-05 13:14:15.999999 +0000 UTC
	// 2020-08-05 13:14:15.999999 +0800 CST
}

func ExampleCreateFromDateTimeNano() {
	fmt.Println(carbon.CreateFromDateTimeNano(2020, 8, 5, 13, 14, 15, 999999999).ToString())
	fmt.Println(carbon.CreateFromDateTimeNano(2020, 8, 5, 13, 14, 15, 999999999, carbon.PRC).ToString())

	// Output:
	// 2020-08-05 13:14:15.999999999 +0000 UTC
	// 2020-08-05 13:14:15.999999999 +0800 CST
}

func ExampleCreateFromDate() {
	fmt.Println(carbon.CreateFromDate(2020, 8, 5).ToString())
	fmt.Println(carbon.CreateFromDate(2020, 8, 5, carbon.PRC).ToString())

	// Output:
	// 2020-08-05 00:00:00 +0000 UTC
	// 2020-08-05 00:00:00 +0800 CST
}

func ExampleCreateFromDateMilli() {
	fmt.Println(carbon.CreateFromDateMilli(2020, 8, 5, 999).ToString())
	fmt.Println(carbon.CreateFromDateMilli(2020, 8, 5, 999, carbon.PRC).ToString())

	// Output:
	// 2020-08-05 00:00:00.999 +0000 UTC
	// 2020-08-05 00:00:00.999 +0800 CST
}

func ExampleCreateFromDateMicro() {
	fmt.Println(carbon.CreateFromDateMicro(2020, 8, 5, 999999).ToString())
	fmt.Println(carbon.CreateFromDateMicro(2020, 8, 5, 999999, carbon.PRC).ToString())

	// Output:
	// 2020-08-05 00:00:00.999999 +0000 UTC
	// 2020-08-05 00:00:00.999999 +0800 CST
}

func ExampleCreateFromDateNano() {
	fmt.Println(carbon.CreateFromDateNano(2020, 8, 5, 999999999).ToString())
	fmt.Println(carbon.CreateFromDateNano(2020, 8, 5, 999999999, carbon.PRC).ToString())

	// Output:
	// 2020-08-05 00:00:00.999999999 +0000 UTC
	// 2020-08-05 00:00:00.999999999 +0800 CST
}

func ExampleCreateFromTime() {
	fmt.Println(carbon.CreateFromTime(13, 14, 15).ToTimeString())
	fmt.Println(carbon.CreateFromTime(13, 14, 15, carbon.PRC).ToTimeString())

	// Output:
	// 13:14:15
	// 13:14:15
}

func ExampleCreateFromTimeMilli() {
	fmt.Println(carbon.CreateFromTimeMilli(13, 14, 15, 999).ToTimeMilliString())
	fmt.Println(carbon.CreateFromTimeMilli(13, 14, 15, 999, carbon.PRC).ToTimeMilliString())

	// Output:
	// 13:14:15.999
	// 13:14:15.999
}

func ExampleCreateFromTimeMicro() {
	fmt.Println(carbon.CreateFromTimeMicro(13, 14, 15, 999999).ToTimeMicroString())
	fmt.Println(carbon.CreateFromTimeMicro(13, 14, 15, 999999, carbon.PRC).ToTimeMicroString())

	// Output:
	// 13:14:15.999999
	// 13:14:15.999999
}

func ExampleCreateFromTimeNano() {
	fmt.Println(carbon.CreateFromTimeNano(13, 14, 15, 999999999).ToTimeNanoString())
	fmt.Println(carbon.CreateFromTimeNano(13, 14, 15, 999999999, carbon.PRC).ToTimeNanoString())

	// Output:
	// 13:14:15.999999999
	// 13:14:15.999999999
}
