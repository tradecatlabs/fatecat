package carbon

import (
	"sync"
	"testing"
)

func BenchmarkLanguage_Copy(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		lang := NewLanguage()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			lang.Copy()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		lang := NewLanguage()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				lang.Copy()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		lang := NewLanguage()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				lang.Copy()
			}
		})
	})
}

func BenchmarkLanguage_SetLocale(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		lang := NewLanguage()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			lang.SetLocale("en")
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		lang := NewLanguage()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				lang.SetLocale("en")
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		lang := NewLanguage()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				lang.SetLocale("en")
			}
		})
	})
}

func BenchmarkLanguage_SetResources(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		resources := map[string]string{
			"months":       "Ⅰ月|Ⅱ月|Ⅲ月|Ⅳ月|Ⅴ月|Ⅵ月|Ⅶ月|Ⅷ月|Ⅸ月|Ⅹ月|Ⅺ月|Ⅻ月",
			"short_months": "Ⅰ|Ⅱ|Ⅲ|Ⅳ|Ⅴ|Ⅵ|Ⅶ|Ⅷ|Ⅸ|Ⅹ|Ⅺ|Ⅻ",
		}
		lang := NewLanguage()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			lang.SetResources(resources)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		resources := map[string]string{
			"months":       "Ⅰ月|Ⅱ月|Ⅲ月|Ⅳ月|Ⅴ月|Ⅵ月|Ⅶ月|Ⅷ月|Ⅸ月|Ⅹ月|Ⅺ月|Ⅻ月",
			"short_months": "Ⅰ|Ⅱ|Ⅲ|Ⅳ|Ⅴ|Ⅵ|Ⅶ|Ⅷ|Ⅸ|Ⅹ|Ⅺ|Ⅻ",
		}
		lang := NewLanguage()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				lang.SetResources(resources)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		resources := map[string]string{
			"months":       "Ⅰ月|Ⅱ月|Ⅲ月|Ⅳ月|Ⅴ月|Ⅵ月|Ⅶ月|Ⅷ月|Ⅸ月|Ⅹ月|Ⅺ月|Ⅻ月",
			"short_months": "Ⅰ|Ⅱ|Ⅲ|Ⅳ|Ⅴ|Ⅵ|Ⅶ|Ⅷ|Ⅸ|Ⅹ|Ⅺ|Ⅻ",
		}
		lang := NewLanguage()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				lang.SetResources(resources)
			}
		})
	})
}

func BenchmarkLanguage_translate(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		lang := NewLanguage()
		lang.SetLocale("en")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			lang.translate("month", 1)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		lang := NewLanguage()
		lang.SetLocale("en")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				lang.translate("month", 1)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		lang := NewLanguage()
		lang.SetLocale("en")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				lang.translate("month", 1)
			}
		})
	})
}
