package carbon

import (
	"sync"
	"testing"
)

func BenchmarkCarbon_StartOfCentury(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.StartOfCentury()
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
				c.StartOfCentury()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.StartOfCentury()
			}
		})
	})
}

func BenchmarkCarbon_EndOfCentury(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.EndOfCentury()
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
				c.EndOfCentury()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.EndOfCentury()
			}
		})
	})
}

func BenchmarkCarbon_StartOfDecade(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.StartOfDecade()
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
				c.StartOfDecade()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.StartOfDecade()
			}
		})
	})
}

func BenchmarkCarbon_EndOfDecade(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.EndOfDecade()
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
				c.EndOfDecade()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.EndOfDecade()
			}
		})
	})
}

func BenchmarkCarbon_StartOfYear(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.StartOfYear()
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
				c.StartOfYear()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.StartOfYear()
			}
		})
	})
}

func BenchmarkCarbon_EndOfYear(b *testing.B) {

	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.EndOfYear()
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
				c.EndOfYear()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.EndOfYear()
			}
		})
	})
}

func BenchmarkCarbon_StartOfQuarter(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.StartOfQuarter()
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
				c.StartOfQuarter()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.StartOfQuarter()
			}
		})
	})
}

func BenchmarkCarbon_EndOfQuarter(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.EndOfQuarter()
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
				c.EndOfQuarter()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.EndOfQuarter()
			}
		})
	})
}

func BenchmarkCarbon_StartOfMonth(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.StartOfMonth()
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
				c.StartOfMonth()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.StartOfMonth()
			}
		})
	})
}

func BenchmarkCarbon_EndOfMonth(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.EndOfMonth()
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
				c.EndOfMonth()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.EndOfMonth()
			}
		})
	})
}

func BenchmarkCarbon_StartOfWeek(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.StartOfWeek()
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
				c.StartOfWeek()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.StartOfWeek()
			}
		})
	})
}

func BenchmarkCarbon_EndOfWeek(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.EndOfWeek()
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
				c.EndOfWeek()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.EndOfWeek()
			}
		})
	})
}

func BenchmarkCarbon_StartOfDay(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.StartOfDay()
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
				c.StartOfDay()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.StartOfDay()
			}
		})
	})
}

func BenchmarkCarbon_EndOfDay(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.EndOfDay()
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
				c.EndOfDay()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.EndOfDay()
			}
		})
	})
}

func BenchmarkCarbon_StartOfHour(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.StartOfHour()
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
				c.StartOfHour()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.StartOfHour()
			}
		})
	})
}

func BenchmarkCarbon_EndOfHour(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.EndOfHour()
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
				c.EndOfHour()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.EndOfHour()
			}
		})
	})
}

func BenchmarkCarbon_StartOfMinute(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.StartOfMinute()
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
				c.StartOfMinute()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.StartOfMinute()
			}
		})
	})
}

func BenchmarkCarbon_EndOfMinute(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.EndOfMinute()
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
				c.EndOfMinute()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.EndOfMinute()
			}
		})
	})
}

func BenchmarkCarbon_StartOfSecond(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.StartOfSecond()
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
				c.StartOfSecond()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.StartOfSecond()
			}
		})
	})
}

func BenchmarkCarbon_EndOfSecond(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.EndOfSecond()
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
				c.EndOfSecond()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.EndOfSecond()
			}
		})
	})
}
