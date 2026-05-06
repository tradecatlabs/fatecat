package julian

import (
	"testing"
	"time"
)

func BenchmarkNewJulian(b *testing.B) {
	testValues := []float64{
		2460310.5, // Julian Day Number
		60310.0,   // Modified Julian Day Number
		1721423.5, // Early Julian Day
		2299159.5, // Last Julian calendar day
		2299170.5, // First Gregorian calendar day
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		value := testValues[i%len(testValues)]
		NewJulian(value)
	}
}

func BenchmarkFromStdTime(b *testing.B) {
	testDates := []time.Time{
		time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC),
		time.Date(2024, 3, 20, 0, 0, 0, 0, time.UTC),
		time.Date(2024, 6, 21, 0, 0, 0, 0, time.UTC),
		time.Date(2024, 9, 22, 0, 0, 0, 0, time.UTC),
		time.Date(2024, 12, 21, 0, 0, 0, 0, time.UTC),
		time.Date(1582, 10, 4, 0, 0, 0, 0, time.UTC),  // Last Julian day
		time.Date(1582, 10, 15, 0, 0, 0, 0, time.UTC), // First Gregorian day
		time.Date(1900, 1, 1, 0, 0, 0, 0, time.UTC),
		time.Date(2000, 1, 1, 0, 0, 0, 0, time.UTC),
		time.Date(1, 1, 1, 0, 0, 0, 0, time.UTC), // Very early date
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		date := testDates[i%len(testDates)]
		FromStdTime(date)
	}
}

func BenchmarkToGregorian(b *testing.B) {
	testJulianDates := []*Julian{
		FromStdTime(time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)),
		FromStdTime(time.Date(2024, 6, 15, 0, 0, 0, 0, time.UTC)),
		FromStdTime(time.Date(2024, 12, 31, 0, 0, 0, 0, time.UTC)),
		FromStdTime(time.Date(1582, 10, 4, 0, 0, 0, 0, time.UTC)),
		FromStdTime(time.Date(1582, 10, 15, 0, 0, 0, 0, time.UTC)),
		NewJulian(2460310.5),
		NewJulian(2299159.5),
		NewJulian(1721423.5),
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		j := testJulianDates[i%len(testJulianDates)]
		j.ToGregorian()
	}
}

func BenchmarkToGregorianWithTimezone(b *testing.B) {
	testJulianDates := []*Julian{
		FromStdTime(time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)),
		FromStdTime(time.Date(2024, 6, 15, 0, 0, 0, 0, time.UTC)),
		FromStdTime(time.Date(2024, 12, 31, 0, 0, 0, 0, time.UTC)),
	}

	timezones := []string{
		"UTC",
		"America/New_York",
		"Europe/London",
		"Asia/Tokyo",
		"Australia/Sydney",
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		j := testJulianDates[i%len(testJulianDates)]
		tz := timezones[i%len(timezones)]
		j.ToGregorian(tz)
	}
}

func BenchmarkJD(b *testing.B) {
	testJulianDates := []*Julian{
		FromStdTime(time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)),
		FromStdTime(time.Date(2024, 6, 15, 0, 0, 0, 0, time.UTC)),
		FromStdTime(time.Date(2024, 12, 31, 0, 0, 0, 0, time.UTC)),
		NewJulian(2460310.5),
		NewJulian(2299159.5),
	}

	precisions := []int{0, 2, 4, 6, 8}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		j := testJulianDates[i%len(testJulianDates)]
		precision := precisions[i%len(precisions)]
		j.JD(precision)
	}
}

func BenchmarkMJD(b *testing.B) {
	testJulianDates := []*Julian{
		FromStdTime(time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)),
		FromStdTime(time.Date(2024, 6, 15, 0, 0, 0, 0, time.UTC)),
		FromStdTime(time.Date(2024, 12, 31, 0, 0, 0, 0, time.UTC)),
		NewJulian(60310.0),
		NewJulian(60332.0),
	}

	precisions := []int{0, 2, 4, 6, 8}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		j := testJulianDates[i%len(testJulianDates)]
		precision := precisions[i%len(precisions)]
		j.MJD(precision)
	}
}

func BenchmarkParseFloat64(b *testing.B) {
	testValues := []float64{
		2460310.5,
		60310.0,
		1721423.5,
		2299159.5,
		2299170.5,
		3.14159265359,
		2.71828182846,
	}

	precisions := []int{0, 2, 4, 6, 8}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		value := testValues[i%len(testValues)]
		precision := precisions[i%len(precisions)]
		parseFloat64(value, precision)
	}
}

func BenchmarkJulianDayCalculation(b *testing.B) {
	testCases := []struct {
		year  int
		month int
		day   int
	}{
		{2024, 1, 1},
		{2024, 6, 15},
		{2024, 12, 31},
		{1582, 10, 4},
		{1582, 10, 15},
		{1900, 1, 1},
		{2000, 1, 1},
		{1, 1, 1},
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		tc := testCases[i%len(testCases)]
		date := time.Date(tc.year, time.Month(tc.month), tc.day, 0, 0, 0, 0, time.UTC)
		FromStdTime(date)
	}
}

func BenchmarkGregorianReformBoundary(b *testing.B) {
	// Test dates around the Gregorian reform boundary
	testDates := []time.Time{
		time.Date(1582, 10, 4, 0, 0, 0, 0, time.UTC),  // Last Julian day
		time.Date(1582, 10, 5, 0, 0, 0, 0, time.UTC),  // First Gregorian day (Julian calendar)
		time.Date(1582, 10, 14, 0, 0, 0, 0, time.UTC), // Tenth Gregorian day (Julian calendar)
		time.Date(1582, 10, 15, 0, 0, 0, 0, time.UTC), // First Gregorian day (Gregorian calendar)
		time.Date(1582, 10, 16, 0, 0, 0, 0, time.UTC), // Second Gregorian day (Gregorian calendar)
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		date := testDates[i%len(testDates)]
		FromStdTime(date)
	}
}

func BenchmarkLeapYearDates(b *testing.B) {
	// Test leap year dates
	testDates := []time.Time{
		time.Date(2024, 2, 29, 0, 0, 0, 0, time.UTC), // Leap day 2024
		time.Date(2020, 2, 29, 0, 0, 0, 0, time.UTC), // Leap day 2020
		time.Date(2016, 2, 29, 0, 0, 0, 0, time.UTC), // Leap day 2016
		time.Date(2000, 2, 29, 0, 0, 0, 0, time.UTC), // Leap day 2000
		time.Date(1900, 2, 28, 0, 0, 0, 0, time.UTC), // Non-leap year 1900
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		date := testDates[i%len(testDates)]
		FromStdTime(date)
	}
}

func BenchmarkExtremeDates(b *testing.B) {
	// Test extreme dates
	testDates := []time.Time{
		time.Date(1, 1, 1, 0, 0, 0, 0, time.UTC),      // Very early date
		time.Date(100, 1, 1, 0, 0, 0, 0, time.UTC),    // Early date
		time.Date(1000, 6, 15, 0, 0, 0, 0, time.UTC),  // Medieval date
		time.Date(3000, 1, 1, 0, 0, 0, 0, time.UTC),   // Future date
		time.Date(5000, 12, 31, 0, 0, 0, 0, time.UTC), // Far future date
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		date := testDates[i%len(testDates)]
		FromStdTime(date)
	}
}

func BenchmarkTimeWithFractionalSeconds(b *testing.B) {
	// Test times with fractional seconds
	testDates := []time.Time{
		time.Date(2024, 1, 1, 12, 30, 45, 500000000, time.UTC),  // 12:30:45.5
		time.Date(2024, 6, 15, 23, 59, 59, 999999999, time.UTC), // 23:59:59.999999999
		time.Date(2024, 12, 31, 0, 0, 0, 123456789, time.UTC),   // 00:00:00.123456789
		time.Date(1582, 10, 15, 6, 0, 0, 0, time.UTC),           // 06:00:00
		time.Date(2000, 1, 1, 18, 30, 15, 250000000, time.UTC),  // 18:30:15.25
	}

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		date := testDates[i%len(testDates)]
		FromStdTime(date)
	}
}
