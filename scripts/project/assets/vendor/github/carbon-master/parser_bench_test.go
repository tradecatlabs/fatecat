package carbon

import (
	"sync"
	"testing"
)

func BenchmarkParse(b *testing.B) {
	datetime := "2020-08-05 01:02:03"

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			Parse(datetime)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				Parse(datetime)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				Parse(datetime)
			}
		})
	})
}

func BenchmarkParseByLayout(b *testing.B) {
	datetime := "2020-08-05 13:14:15"
	layout := DateTimeLayout

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			ParseByLayout(datetime, layout)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				ParseByLayout(datetime, layout)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				ParseByLayout(datetime, layout)
			}
		})
	})
}

func BenchmarkParseByFormat(b *testing.B) {
	datetime := "2020-08-05 13:14:15"
	format := DateTimeFormat

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for n := 0; n < b.N/10; n++ {
			ParseByFormat(datetime, format)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				ParseByFormat(datetime, format)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				ParseByFormat(datetime, format)
			}
		})
	})
}

func BenchmarkParseByLayouts(b *testing.B) {
	datetime := "2020-08-05 13:14:15"
	layouts := []string{DateLayout, DateTimeLayout}

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			ParseByLayouts(datetime, layouts)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				ParseByLayouts(datetime, layouts)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				ParseByLayouts(datetime, layouts)
			}
		})
	})
}

func BenchmarkParseByFormats(b *testing.B) {
	dateStr := "2020-08-05 13:14:15"
	formats := []string{DateFormat, DateTimeFormat}

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			ParseByFormats(dateStr, formats)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				ParseByFormats(dateStr, formats)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				ParseByFormats(dateStr, formats)
			}
		})
	})
}
