package carbon

import (
	"sync"
	"testing"
)

func BenchmarkSetDefault(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		defer ResetDefault()

		d := Default{
			Layout:       DateTimeLayout,
			Timezone:     PRC,
			Locale:       "zh-CN",
			WeekStartsAt: Monday,
			WeekendDays: []Weekday{
				Saturday, Sunday,
			},
		}

		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			SetDefault(d)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		defer ResetDefault()

		var wg sync.WaitGroup
		d := Default{
			Layout:       DateTimeLayout,
			Timezone:     PRC,
			Locale:       "zh-CN",
			WeekStartsAt: Monday,
			WeekendDays: []Weekday{
				Saturday, Sunday,
			},
		}

		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				SetDefault(d)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		defer ResetDefault()

		d := Default{
			Layout:       DateTimeLayout,
			Timezone:     PRC,
			Locale:       "zh-CN",
			WeekStartsAt: Monday,
			WeekendDays: []Weekday{
				Saturday, Sunday,
			},
		}

		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				SetDefault(d)
			}
		})
	})
}

func BenchmarkResetDefault(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			ResetDefault()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				ResetDefault()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				ResetDefault()
			}
		})
	})
}
