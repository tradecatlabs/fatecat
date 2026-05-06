package carbon

import (
	"sync"
	"testing"
	"time"
)

func BenchmarkNewCarbon(b *testing.B) {
	loc, _ := time.LoadLocation(PRC)
	tt, _ := time.ParseInLocation(DateTimeLayout, "2020-08-05 13:14:15", loc)

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			NewCarbon(tt)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				NewCarbon(tt)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				NewCarbon(tt)
			}
		})
	})
}

func BenchmarkCopy(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-08-05").SetLocale("zh-CN")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Copy()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-08-05").SetLocale("zh-CN")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Copy()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-08-05").SetLocale("zh-CN")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Copy()
			}
		})
	})
}

func BenchmarkSleep(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		testNow := Parse("2020-08-05 13:14:15")
		SetTestNow(testNow)
		defer ClearTestNow()

		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			Sleep(1 * time.Hour)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		testNow := Parse("2020-08-05 13:14:15")
		SetTestNow(testNow)
		defer ClearTestNow()

		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				Sleep(1 * time.Hour)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		testNow := Parse("2020-08-05 13:14:15")
		SetTestNow(testNow)
		defer ClearTestNow()

		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				Sleep(1 * time.Hour)
			}
		})
	})
}

func BenchmarkSleep_DifferentDurations(b *testing.B) {
	durations := []time.Duration{
		1 * time.Nanosecond,
		1 * time.Microsecond,
		1 * time.Millisecond,
		1 * time.Second,
		1 * time.Minute,
		1 * time.Hour,
	}

	for _, duration := range durations {
		b.Run(duration.String(), func(b *testing.B) {
			testNow := Parse("2020-08-05 13:14:15")
			SetTestNow(testNow)
			defer ClearTestNow()

			b.ResetTimer()
			for i := 0; i < b.N/10; i++ {
				Sleep(duration)
			}
		})
	}
}
