package carbon

import (
	"sync"
	"testing"
)

func BenchmarkCarbon_StdTime(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.StdTime()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.StdTime()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.StdTime()
			}
		})
	})
}

func BenchmarkCarbon_DaysInYear(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.DaysInYear()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.DaysInYear()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.DaysInYear()
			}
		})
	})
}

func BenchmarkCarbon_DaysInMonth(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.DaysInMonth()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.DaysInMonth()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.DaysInMonth()
			}
		})
	})
}

func BenchmarkCarbon_MonthOfYear(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.MonthOfYear()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.MonthOfYear()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.MonthOfYear()
			}
		})
	})
}

func BenchmarkCarbon_DayOfYear(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.DayOfYear()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.DayOfYear()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.DayOfYear()
			}
		})
	})
}

func BenchmarkCarbon_DayOfMonth(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.DayOfMonth()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.DayOfMonth()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.DayOfMonth()
			}
		})
	})
}

func BenchmarkCarbon_DayOfWeek(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.DayOfWeek()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.DayOfWeek()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.DayOfWeek()
			}
		})
	})
}

func BenchmarkCarbon_WeekOfYear(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.WeekOfYear()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.WeekOfYear()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.WeekOfYear()
			}
		})
	})
}

func BenchmarkCarbon_WeekOfMonth(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.WeekOfMonth()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.WeekOfMonth()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.WeekOfMonth()
			}
		})
	})
}

func BenchmarkCarbon_DateTime(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.DateTime()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.DateTime()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.DateTime()
			}
		})
	})
}

func BenchmarkCarbon_DateTimeMilli(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.DateTimeMilli()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.DateTimeMilli()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.DateTimeMilli()
			}
		})
	})
}

func BenchmarkCarbon_DateTimeMicro(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.DateTimeMicro()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.DateTimeMicro()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.DateTimeMicro()
			}
		})
	})
}

func BenchmarkCarbon_DateTimeNano(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.DateTimeNano()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.DateTimeNano()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.DateTimeNano()
			}
		})
	})
}

func BenchmarkCarbon_Date(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Date()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Date()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Date()
			}
		})
	})
}

func BenchmarkCarbon_DateMilli(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.DateMilli()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.DateMilli()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.DateMilli()
			}
		})
	})
}

func BenchmarkCarbon_DateMicro(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.DateMicro()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.DateMicro()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.DateMicro()
			}
		})
	})
}

func BenchmarkCarbon_DateNano(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.DateNano()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.DateNano()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.DateNano()
			}
		})
	})
}

func BenchmarkCarbon_Time(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Time()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Time()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Time()
			}
		})
	})
}

func BenchmarkCarbon_TimeMilli(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.TimeMilli()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.TimeMilli()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.TimeMilli()
			}
		})
	})
}

func BenchmarkCarbon_TimeMicro(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.TimeMicro()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.TimeMicro()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.TimeMicro()
			}
		})
	})
}

func BenchmarkCarbon_TimeNano(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.TimeNano()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.TimeNano()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.TimeNano()
			}
		})
	})
}

func BenchmarkCarbon_Century(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Century()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Century()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Century()
			}
		})
	})
}

func BenchmarkCarbon_Decade(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Decade()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Decade()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Decade()
			}
		})
	})
}

func BenchmarkCarbon_Year(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Year()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Year()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Year()
			}
		})
	})
}

func BenchmarkCarbon_Quarter(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Quarter()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Quarter()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Quarter()
			}
		})
	})
}

func BenchmarkCarbon_Month(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Month()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Month()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Month()
			}
		})
	})
}

func BenchmarkCarbon_Week(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Week()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Week()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Week()
			}
		})
	})
}

func BenchmarkCarbon_Day(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Day()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Day()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Day()
			}
		})
	})
}

func BenchmarkCarbon_Hour(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Hour()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Hour()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Hour()
			}
		})
	})
}

func BenchmarkCarbon_Minute(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Minute()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Minute()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Minute()
			}
		})
	})
}

func BenchmarkCarbon_Second(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Second()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Second()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Second()
			}
		})
	})
}

func BenchmarkCarbon_Millisecond(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Millisecond()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Millisecond()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Millisecond()
			}
		})
	})
}

func BenchmarkCarbon_Microsecond(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Microsecond()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Microsecond()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Microsecond()
			}
		})
	})
}

func BenchmarkCarbon_Nanosecond(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Nanosecond()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Nanosecond()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Nanosecond()
			}
		})
	})
}

func BenchmarkCarbon_Timestamp(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Timestamp()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Timestamp()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Timestamp()
			}
		})
	})
}

func BenchmarkCarbon_TimestampMilli(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.TimestampMilli()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.TimestampMilli()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.TimestampMilli()
			}
		})
	})
}

func BenchmarkCarbon_TimestampMicro(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.TimestampMicro()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.TimestampMicro()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.TimestampMicro()
			}
		})
	})
}

func BenchmarkCarbon_TimestampNano(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.TimestampNano()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.TimestampNano()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.TimestampNano()
			}
		})
	})
}

func BenchmarkCarbon_Timezone(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Timezone()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Timezone()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Timezone()
			}
		})
	})
}

func BenchmarkCarbon_ZoneName(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.ZoneName()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.ZoneName()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.ZoneName()
			}
		})
	})
}

func BenchmarkCarbon_ZoneOffset(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.ZoneOffset()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.ZoneOffset()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.ZoneOffset()
			}
		})
	})
}

func BenchmarkCarbon_Locale(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Locale()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Locale()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Locale()
			}
		})
	})
}

func BenchmarkCarbon_WeekStartsAt(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.WeekStartsAt()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.WeekStartsAt()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.WeekStartsAt()
			}
		})
	})
}

func BenchmarkCarbon_WeekEndsAt(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.WeekEndsAt()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.WeekEndsAt()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.WeekEndsAt()
			}
		})
	})
}

func BenchmarkCarbon_CurrentLayout(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.CurrentLayout()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.CurrentLayout()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.CurrentLayout()
			}
		})
	})
}

func BenchmarkCarbon_Age(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Age()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Age()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Age()
			}
		})
	})
}
