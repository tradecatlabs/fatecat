package carbon_test

import (
	"fmt"

	"github.com/dromara/carbon/v2"
)

func ExampleCarbon_StdTime() {
	fmt.Println(carbon.Parse("2020-08-05").StdTime().String())
	fmt.Println(carbon.Parse("2020-08-05", carbon.PRC).StdTime().String())

	// Output:
	// 2020-08-05 00:00:00 +0000 UTC
	// 2020-08-05 00:00:00 +0800 CST
}

func ExampleCarbon_DaysInYear() {
	fmt.Println(carbon.Parse("2020-08-05").DaysInYear())
	fmt.Println(carbon.Parse("2021-08-05").DaysInYear())

	// Output:
	// 366
	// 365
}

func ExampleCarbon_DaysInMonth() {
	fmt.Println(carbon.Parse("2020-01-05").DaysInMonth())
	fmt.Println(carbon.Parse("2020-02-05").DaysInMonth())
	fmt.Println(carbon.Parse("2020-03-05").DaysInMonth())
	fmt.Println(carbon.Parse("2020-04-05").DaysInMonth())

	// Output:
	// 31
	// 29
	// 31
	// 30
}

func ExampleCarbon_MonthOfYear() {
	fmt.Println(carbon.Parse("2020-01-05").MonthOfYear())
	fmt.Println(carbon.Parse("2020-02-05").MonthOfYear())
	fmt.Println(carbon.Parse("2020-03-05").MonthOfYear())
	fmt.Println(carbon.Parse("2020-04-05").MonthOfYear())

	// Output:
	// 1
	// 2
	// 3
	// 4
}

func ExampleCarbon_DayOfYear() {
	fmt.Println(carbon.Parse("2020-01-05").DayOfYear())
	fmt.Println(carbon.Parse("2020-02-05").DayOfYear())
	fmt.Println(carbon.Parse("2020-03-05").DayOfYear())
	fmt.Println(carbon.Parse("2020-04-05").DayOfYear())

	// Output:
	// 5
	// 36
	// 65
	// 96
}

func ExampleCarbon_DayOfMonth() {
	fmt.Println(carbon.Parse("2020-01-01").DayOfMonth())
	fmt.Println(carbon.Parse("2020-01-05").DayOfMonth())
	fmt.Println(carbon.Parse("2020-01-31").DayOfMonth())

	// Output:
	// 1
	// 5
	// 31
}

func ExampleCarbon_DayOfWeek() {
	fmt.Println(carbon.Parse("2020-08-03").DayOfWeek())
	fmt.Println(carbon.Parse("2020-08-04").DayOfWeek())
	fmt.Println(carbon.Parse("2020-08-05").DayOfWeek())

	// Output:
	// 1
	// 2
	// 3
}

func ExampleCarbon_WeekOfYear() {
	fmt.Println(carbon.Parse("2021-01-01").WeekOfYear())
	fmt.Println(carbon.Parse("2021-02-01").WeekOfYear())
	fmt.Println(carbon.Parse("2021-03-01").WeekOfYear())
	fmt.Println(carbon.Parse("2021-04-01").WeekOfYear())

	// Output:
	// 53
	// 5
	// 9
	// 13
}

func ExampleCarbon_WeekOfMonth() {
	fmt.Println(carbon.Parse("2021-07-01").WeekOfMonth())
	fmt.Println(carbon.Parse("2021-07-02").WeekOfMonth())
	fmt.Println(carbon.Parse("2021-07-03").WeekOfMonth())
	fmt.Println(carbon.Parse("2021-07-04").WeekOfMonth())
	fmt.Println(carbon.Parse("2021-07-05").WeekOfMonth())
	fmt.Println(carbon.Parse("2021-07-06").WeekOfMonth())

	// Output:
	// 1
	// 1
	// 1
	// 1
	// 2
	// 2
}

func ExampleCarbon_DateTime() {
	year, month, day, hour, minute, second := carbon.Parse("2020-08-05 13:14:15.999999999").DateTime()

	fmt.Println(year)
	fmt.Println(month)
	fmt.Println(day)
	fmt.Println(hour)
	fmt.Println(minute)
	fmt.Println(second)

	// Output:
	// 2020
	// 8
	// 5
	// 13
	// 14
	// 15
}

func ExampleCarbon_DateTimeMilli() {
	year, month, day, hour, minute, second, millisecond := carbon.Parse("2020-08-05 13:14:15.999999999").DateTimeMilli()

	fmt.Println(year)
	fmt.Println(month)
	fmt.Println(day)
	fmt.Println(hour)
	fmt.Println(minute)
	fmt.Println(second)
	fmt.Println(millisecond)

	// Output:
	// 2020
	// 8
	// 5
	// 13
	// 14
	// 15
	// 999
}

func ExampleCarbon_DateTimeMicro() {
	year, month, day, hour, minute, second, microsecond := carbon.Parse("2020-08-05 13:14:15.999999999").DateTimeMicro()

	fmt.Println(year)
	fmt.Println(month)
	fmt.Println(day)
	fmt.Println(hour)
	fmt.Println(minute)
	fmt.Println(second)
	fmt.Println(microsecond)

	// Output:
	// 2020
	// 8
	// 5
	// 13
	// 14
	// 15
	// 999999
}

func ExampleCarbon_DateTimeNano() {
	year, month, day, hour, minute, second, nanosecond := carbon.Parse("2020-08-05 13:14:15.999999999").DateTimeNano()

	fmt.Println(year)
	fmt.Println(month)
	fmt.Println(day)
	fmt.Println(hour)
	fmt.Println(minute)
	fmt.Println(second)
	fmt.Println(nanosecond)

	// Output:
	// 2020
	// 8
	// 5
	// 13
	// 14
	// 15
	// 999999999
}

func ExampleCarbon_Date() {
	year, month, day := carbon.Parse("2020-08-05 13:14:15.999999999").Date()

	fmt.Println(year)
	fmt.Println(month)
	fmt.Println(day)

	// Output:
	// 2020
	// 8
	// 5
}

func ExampleCarbon_DateMilli() {
	year, month, day, millisecond := carbon.Parse("2020-08-05 13:14:15.999999999").DateMilli()

	fmt.Println(year)
	fmt.Println(month)
	fmt.Println(day)
	fmt.Println(millisecond)

	// Output:
	// 2020
	// 8
	// 5
	// 999
}

func ExampleCarbon_DateMicro() {
	year, month, day, microsecond := carbon.Parse("2020-08-05 13:14:15.999999999").DateMicro()

	fmt.Println(year)
	fmt.Println(month)
	fmt.Println(day)
	fmt.Println(microsecond)

	// Output:
	// 2020
	// 8
	// 5
	// 999999
}

func ExampleCarbon_DateNano() {
	year, month, day, nanosecond := carbon.Parse("2020-08-05 13:14:15.999999999").DateNano()

	fmt.Println(year)
	fmt.Println(month)
	fmt.Println(day)
	fmt.Println(nanosecond)

	// Output:
	// 2020
	// 8
	// 5
	// 999999999
}

func ExampleCarbon_Time() {
	hour, minute, second := carbon.Parse("2020-08-05 13:14:15.999999999").Time()

	fmt.Println(hour)
	fmt.Println(minute)
	fmt.Println(second)

	// Output:
	// 13
	// 14
	// 15
}

func ExampleCarbon_TimeMilli() {
	hour, minute, second, millisecond := carbon.Parse("2020-08-05 13:14:15.999999999").TimeMilli()

	fmt.Println(hour)
	fmt.Println(minute)
	fmt.Println(second)
	fmt.Println(millisecond)

	// Output:
	// 13
	// 14
	// 15
	// 999
}

func ExampleCarbon_TimeMicro() {
	hour, minute, second, microsecond := carbon.Parse("2020-08-05 13:14:15.999999999").TimeMicro()

	fmt.Println(hour)
	fmt.Println(minute)
	fmt.Println(second)
	fmt.Println(microsecond)

	// Output:
	// 13
	// 14
	// 15
	// 999999
}

func ExampleCarbon_TimeNano() {
	hour, minute, second, nanosecond := carbon.Parse("2020-08-05 13:14:15.999999999").TimeNano()

	fmt.Println(hour)
	fmt.Println(minute)
	fmt.Println(second)
	fmt.Println(nanosecond)

	// Output:
	// 13
	// 14
	// 15
	// 999999999
}

func ExampleCarbon_Century() {
	fmt.Println(carbon.Parse("1990-08-05").Century())
	fmt.Println(carbon.Parse("2021-08-05").Century())

	// Output:
	// 20
	// 21
}

func ExampleCarbon_Decade() {
	fmt.Println(carbon.Parse("2010-08-05").Decade())
	fmt.Println(carbon.Parse("2011-08-05").Decade())
	fmt.Println(carbon.Parse("2020-08-05").Decade())
	fmt.Println(carbon.Parse("2021-08-05").Decade())

	// Output:
	// 10
	// 10
	// 20
	// 20
}

func ExampleCarbon_Year() {
	fmt.Println(carbon.Parse("2010-08-05").Year())
	fmt.Println(carbon.Parse("2011-08-05").Year())
	fmt.Println(carbon.Parse("2020-08-05").Year())
	fmt.Println(carbon.Parse("2021-08-05").Year())

	// Output:
	// 2010
	// 2011
	// 2020
	// 2021
}

func ExampleCarbon_Quarter() {
	fmt.Println(carbon.Parse("2020-01-05").Quarter())
	fmt.Println(carbon.Parse("2020-04-05").Quarter())
	fmt.Println(carbon.Parse("2020-08-05").Quarter())
	fmt.Println(carbon.Parse("2020-11-05").Quarter())

	// Output:
	// 1
	// 2
	// 3
	// 4
}

func ExampleCarbon_Month() {
	fmt.Println(carbon.Parse("2020-01-05").Month())
	fmt.Println(carbon.Parse("2020-04-05").Month())
	fmt.Println(carbon.Parse("2020-08-05").Month())
	fmt.Println(carbon.Parse("2020-11-05").Month())

	// Output:
	// 1
	// 4
	// 8
	// 11
}

func ExampleCarbon_Week() {
	fmt.Println(carbon.Parse("2020-08-03").Week())
	fmt.Println(carbon.Parse("2020-08-04").Week())
	fmt.Println(carbon.Parse("2020-08-05").Week())
	fmt.Println(carbon.Parse("2020-08-09").Week())

	// Output:
	// 0
	// 1
	// 2
	// 6
}

func ExampleCarbon_Day() {
	fmt.Println(carbon.Parse("2020-08-05").Day())

	// Output:
	// 5
}

func ExampleCarbon_Hour() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15.999999999").Hour())

	// Output:
	// 13
}

func ExampleCarbon_Minute() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15.999999999").Minute())

	// Output:
	// 14
}

func ExampleCarbon_Second() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15.999999999").Second())

	// Output:
	// 15
}

func ExampleCarbon_Millisecond() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15.999999999").Millisecond())

	// Output:
	// 999
}

func ExampleCarbon_Microsecond() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15.999999999").Microsecond())

	// Output:
	// 999999
}

func ExampleCarbon_Nanosecond() {
	fmt.Println(carbon.Parse("2020-08-05 13:14:15.999999999").Nanosecond())

	// Output:
	// 999999999
}

func ExampleCarbon_Timestamp() {
	fmt.Println(carbon.Parse("2020-01-01 13:14:15", carbon.PRC).Timestamp())
	fmt.Println(carbon.Parse("2020-08-05 13:14:15.999999999").Timestamp())

	// Output:
	// 1577855655
	// 1596633255
}

func ExampleCarbon_TimestampMilli() {
	fmt.Println(carbon.Parse("2020-01-01 13:14:15", carbon.PRC).TimestampMilli())
	fmt.Println(carbon.Parse("2020-08-05 13:14:15.999999999").TimestampMilli())

	// Output:
	// 1577855655000
	// 1596633255999
}

func ExampleCarbon_TimestampMicro() {
	fmt.Println(carbon.Parse("2020-01-01 13:14:15", carbon.PRC).TimestampMicro())
	fmt.Println(carbon.Parse("2020-08-05 13:14:15.999999999").TimestampMicro())

	// Output:
	// 1577855655000000
	// 1596633255999999
}

func ExampleCarbon_TimestampNano() {
	fmt.Println(carbon.Parse("2020-01-01 13:14:15", carbon.PRC).TimestampNano())
	fmt.Println(carbon.Parse("2020-08-05 13:14:15.999999999").TimestampNano())

	// Output:
	// 1577855655000000000
	// 1596633255999999999
}

func ExampleCarbon_Timezone() {
	fmt.Println(carbon.Now().Timezone())
	fmt.Println(carbon.Now(carbon.Tokyo).Timezone())
	fmt.Println(carbon.Now(carbon.PRC).Timezone())

	// Output:
	// UTC
	// Asia/Tokyo
	// PRC
}

func ExampleCarbon_ZoneName() {
	fmt.Println(carbon.Now().ZoneName())
	fmt.Println(carbon.Now(carbon.Tokyo).ZoneName())
	fmt.Println(carbon.Now(carbon.PRC).ZoneName())

	// Output:
	// UTC
	// JST
	// CST
}

func ExampleCarbon_ZoneOffset() {
	fmt.Println(carbon.Parse("2020-08-05").ZoneOffset())
	fmt.Println(carbon.Parse("2020-08-05", carbon.Tokyo).ZoneOffset())
	fmt.Println(carbon.Parse("2020-08-05", carbon.PRC).ZoneOffset())

	// Output:
	// 0
	// 32400
	// 28800
}

func ExampleCarbon_Locale() {
	fmt.Println(carbon.Now().SetLocale("en").Locale())
	fmt.Println(carbon.Now().SetLocale("zh-CN").Locale())

	// Output:
	// en
	// zh-CN
}

func ExampleCarbon_WeekStartsAt() {
	fmt.Println(carbon.Now().SetWeekStartsAt(carbon.Sunday).WeekStartsAt())
	fmt.Println(carbon.Now().SetWeekStartsAt(carbon.Monday).WeekStartsAt())

	// Output:
	// Sunday
	// Monday
}

func ExampleCarbon_WeekEndsAt() {
	fmt.Println(carbon.Now().SetWeekStartsAt(carbon.Sunday).WeekEndsAt())
	fmt.Println(carbon.Now().SetWeekStartsAt(carbon.Monday).WeekEndsAt())

	// Output:
	// Saturday
	// Sunday
}

func ExampleCarbon_CurrentLayout() {
	fmt.Println(carbon.Parse("now").CurrentLayout())
	fmt.Println(carbon.ParseByLayout("13:14:15", carbon.TimeLayout).CurrentLayout())
	fmt.Println(carbon.ParseByLayout("2020-08-05", carbon.DateLayout).CurrentLayout())

	// Output:
	// 2006-01-02 15:04:05
	// 15:04:05
	// 2006-01-02
}

func ExampleCarbon_Age() {
	fmt.Println(carbon.Now().AddYears(18).Age())
	fmt.Println(carbon.Now().SubYears(18).Age())

	// Output:
	// 0
	// 18
}
