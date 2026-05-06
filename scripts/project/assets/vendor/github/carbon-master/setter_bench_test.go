package carbon

import (
	"sync"
	"testing"
	"time"
)

func BenchmarkSetLayout(b *testing.B) {
	layout := DateTimeLayout

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			SetLayout(layout)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					SetLayout(layout)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				SetLayout(layout)
			}
		})
	})
}

func BenchmarkSetFormat(b *testing.B) {
	format := DateTimeFormat

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			SetFormat(format)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					SetFormat(format)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				SetFormat(format)
			}
		})
	})
}

func BenchmarkSetWeekStartsAt(b *testing.B) {
	weekStartsAt := Monday

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			SetWeekStartsAt(weekStartsAt)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					SetWeekStartsAt(weekStartsAt)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				SetWeekStartsAt(weekStartsAt)
			}
		})
	})
}

func BenchmarkSetTimezone(b *testing.B) {
	timezone := UTC

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			SetTimezone(timezone)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					SetTimezone(timezone)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				SetTimezone(timezone)
			}
		})
	})
}

func BenchmarkSetLocation(b *testing.B) {
	location := time.UTC

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			SetLocation(location)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					SetLocation(location)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				SetLocation(location)
			}
		})
	})
}

func BenchmarkSetLocale(b *testing.B) {
	locale := "en"

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			SetLocale(locale)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					SetLocale(locale)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				SetLocale(locale)
			}
		})
	})
}

func BenchmarkCarbon_SetLayout(b *testing.B) {
	c := Now()
	layout := DateTimeLayout

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetLayout(layout)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetLayout(layout)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetLayout(layout)
			}
		})
	})
}

func BenchmarkCarbon_SetFormat(b *testing.B) {
	c := Now()
	format := DateTimeFormat

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetFormat(format)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetFormat(format)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetFormat(format)
			}
		})
	})
}

func BenchmarkCarbon_SetWeekStartsAt(b *testing.B) {
	c := Now()
	weekStartsAt := Monday

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetWeekStartsAt(weekStartsAt)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetWeekStartsAt(weekStartsAt)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetWeekStartsAt(weekStartsAt)
			}
		})
	})
}

func BenchmarkCarbon_SetLocale(b *testing.B) {
	c := Now()
	locale := "en"

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetLocale(locale)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetLocale(locale)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetLocale(locale)
			}
		})
	})
}

func BenchmarkCarbon_SetTimezone(b *testing.B) {
	c := Now()
	timezone := UTC

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetTimezone(timezone)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetTimezone(timezone)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetTimezone(timezone)
			}
		})
	})
}

func BenchmarkCarbon_SetLocation(b *testing.B) {
	c := Now()
	location := time.UTC

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetLocation(location)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetLocation(location)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetLocation(location)
			}
		})
	})
}

func BenchmarkCarbon_SetLanguage(b *testing.B) {
	c := Now()
	lang := NewLanguage()
	lang.SetLocale("en")

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetLanguage(lang)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetLanguage(lang)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetLanguage(lang)
			}
		})
	})
}

func BenchmarkCarbon_SetDateTime(b *testing.B) {
	c := Now()
	year, month, day, hour, minute, second := 2020, 8, 5, 13, 14, 15

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetDateTime(year, month, day, hour, minute, second)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetDateTime(year, month, day, hour, minute, second)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetDateTime(year, month, day, hour, minute, second)
			}
		})
	})
}

func BenchmarkCarbon_SetDateTimeMilli(b *testing.B) {
	c := Now()
	year, month, day, hour, minute, second, milli := 2020, 8, 5, 13, 14, 15, 999

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetDateTimeMilli(year, month, day, hour, minute, second, milli)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetDateTimeMilli(year, month, day, hour, minute, second, milli)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetDateTimeMilli(year, month, day, hour, minute, second, milli)
			}
		})
	})
}

func BenchmarkCarbon_SetDateTimeMicro(b *testing.B) {
	c := Now()
	year, month, day, hour, minute, second, micro := 2020, 8, 5, 13, 14, 15, 999999

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetDateTimeMicro(year, month, day, hour, minute, second, micro)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetDateTimeMicro(year, month, day, hour, minute, second, micro)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetDateTimeMicro(year, month, day, hour, minute, second, micro)
			}
		})
	})
}

func BenchmarkCarbon_SetDateTimeNano(b *testing.B) {
	c := Now()
	year, month, day, hour, minute, second, nano := 2020, 8, 5, 13, 14, 15, 999999999

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetDateTimeNano(year, month, day, hour, minute, second, nano)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetDateTimeNano(year, month, day, hour, minute, second, nano)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetDateTimeNano(year, month, day, hour, minute, second, nano)
			}
		})
	})
}

func BenchmarkCarbon_SetDate(b *testing.B) {
	c := Now()
	year, month, day := 2020, 8, 5

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetDate(year, month, day)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetDate(year, month, day)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetDate(year, month, day)
			}
		})
	})
}

func BenchmarkCarbon_SetDateMilli(b *testing.B) {
	c := Now()
	year, month, day, milli := 2020, 8, 5, 999

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetDateMilli(year, month, day, milli)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetDateMilli(year, month, day, milli)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetDateMilli(year, month, day, milli)
			}
		})
	})
}

func BenchmarkCarbon_SetDateMicro(b *testing.B) {
	c := Now()
	year, month, day, micro := 2020, 8, 5, 999999

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetDateMicro(year, month, day, micro)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetDateMicro(year, month, day, micro)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetDateMicro(year, month, day, micro)
			}
		})
	})
}

func BenchmarkCarbon_SetDateNano(b *testing.B) {
	c := Now()
	year, month, day, nano := 2020, 8, 5, 999999999

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetDateNano(year, month, day, nano)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetDateNano(year, month, day, nano)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetDateNano(year, month, day, nano)
			}
		})
	})
}

func BenchmarkCarbon_SetTime(b *testing.B) {
	c := Now()
	hour, minute, second := 13, 14, 15

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetTime(hour, minute, second)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetTime(hour, minute, second)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetTime(hour, minute, second)
			}
		})
	})
}

func BenchmarkCarbon_SetTimeMilli(b *testing.B) {
	c := Now()
	hour, minute, second, milli := 13, 14, 15, 999

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetTimeMilli(hour, minute, second, milli)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetTimeMilli(hour, minute, second, milli)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetTimeMilli(hour, minute, second, milli)
			}
		})
	})
}

func BenchmarkCarbon_SetTimeMicro(b *testing.B) {
	c := Now()
	hour, minute, second, micro := 13, 14, 15, 999999

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetTimeMicro(hour, minute, second, micro)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetTimeMicro(hour, minute, second, micro)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetTimeMicro(hour, minute, second, micro)
			}
		})
	})
}

func BenchmarkCarbon_SetTimeNano(b *testing.B) {
	c := Now()
	hour, minute, second, nano := 13, 14, 15, 999999999

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetTimeNano(hour, minute, second, nano)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetTimeNano(hour, minute, second, nano)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetTimeNano(hour, minute, second, nano)
			}
		})
	})
}

func BenchmarkCarbon_SetYear(b *testing.B) {
	c := Now()
	year := 2020

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetYear(year)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetYear(year)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetYear(year)
			}
		})
	})
}

func BenchmarkCarbon_SetYearNoOverflow(b *testing.B) {
	c := Now()
	year := 2020

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetYearNoOverflow(year)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetYearNoOverflow(year)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetYearNoOverflow(year)
			}
		})
	})
}

func BenchmarkCarbon_SetMonth(b *testing.B) {
	c := Now()
	month := 2

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetMonth(month)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetMonth(month)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetMonth(month)
			}
		})
	})
}

func BenchmarkCarbon_SetMonthNoOverflow(b *testing.B) {
	c := Now()
	month := 2

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetMonthNoOverflow(month)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetMonthNoOverflow(month)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetMonthNoOverflow(month)
			}
		})
	})
}

func BenchmarkCarbon_SetDay(b *testing.B) {
	c := Now()
	day := 31

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetDay(day)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetDay(day)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetDay(day)
			}
		})
	})
}

func BenchmarkCarbon_SetHour(b *testing.B) {
	c := Now()
	hour := 10

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetHour(hour)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetHour(hour)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetHour(hour)
			}
		})
	})
}

func BenchmarkCarbon_SetMinute(b *testing.B) {
	c := Now()
	minute := 10

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetMinute(minute)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetMinute(minute)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetMinute(minute)
			}
		})
	})
}

func BenchmarkCarbon_SetSecond(b *testing.B) {
	c := Now()
	second := 10

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetSecond(second)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetSecond(second)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetSecond(second)
			}
		})
	})
}

func BenchmarkCarbon_SetMillisecond(b *testing.B) {
	c := Now()
	millisecond := 999

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetMillisecond(millisecond)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetMillisecond(millisecond)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetMillisecond(millisecond)
			}
		})
	})
}

func BenchmarkCarbon_SetMicrosecond(b *testing.B) {
	c := Now()
	microsecond := 999999

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetMicrosecond(microsecond)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetMicrosecond(microsecond)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetMicrosecond(microsecond)
			}
		})
	})
}

func BenchmarkCarbon_SetNanosecond(b *testing.B) {
	c := Now()
	nanosecond := 999999999

	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.SetNanosecond(nanosecond)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		b.ResetTimer()
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				for n := 0; n < b.N/10; n++ {
					c.SetNanosecond(nanosecond)
				}
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.SetNanosecond(nanosecond)
			}
		})
	})
}
