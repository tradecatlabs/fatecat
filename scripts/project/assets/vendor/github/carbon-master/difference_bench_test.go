package carbon

import (
	"sync"
	"testing"
)

func BenchmarkCarbon_DiffInYears(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffInYears(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffInYears(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffInYears(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffAbsInYears(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffAbsInYears(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffAbsInYears(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffAbsInYears(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffInMonths(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffInMonths(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffInMonths(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffInMonths(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffAbsInMonths(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffAbsInMonths(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffAbsInMonths(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffAbsInMonths(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffInWeeks(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffInWeeks(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffInWeeks(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffInWeeks(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffAbsInWeeks(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffAbsInWeeks(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffAbsInWeeks(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffAbsInWeeks(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffInDays(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffInDays(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffInDays(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffInDays(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffAbsInDays(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffAbsInDays(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffAbsInDays(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffAbsInDays(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffInHours(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffInHours(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffInHours(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffInHours(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffAbsInHours(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffAbsInHours(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffAbsInHours(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffAbsInHours(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffInMinutes(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffInMinutes(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffInMinutes(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffInMinutes(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffAbsInMinutes(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffAbsInMinutes(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffAbsInMinutes(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffAbsInMinutes(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffInSeconds(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffInSeconds(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffInSeconds(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffInSeconds(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffAbsInSeconds(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffAbsInSeconds(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffAbsInSeconds(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffAbsInSeconds(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffInString(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffInString(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffInString(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffInString(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffAbsInString(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffAbsInString(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffAbsInString(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffAbsInString(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffInDuration(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.DiffInDuration()
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
				c.DiffInDuration()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.DiffInDuration()
			}
		})
	})
}

func BenchmarkCarbon_DiffAbsInDuration(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffAbsInDuration(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffAbsInDuration(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffAbsInDuration(c2)
			}
		})
	})
}

func BenchmarkCarbon_DiffForHumans(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.DiffForHumans(c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.DiffForHumans(c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-05")
		c2 := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.DiffForHumans(c2)
			}
		})
	})
}
