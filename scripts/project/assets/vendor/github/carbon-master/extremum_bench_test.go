package carbon

import (
	"sync"
	"testing"
)

func BenchmarkZeroValue(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			ZeroValue()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				ZeroValue()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				ZeroValue()
			}
		})
	})
}

func BenchmarkEpochValue(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			EpochValue()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				EpochValue()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				EpochValue()
			}
		})
	})
}

func BenchmarkMaxValue(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			MaxValue()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				MaxValue()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				MaxValue()
			}
		})
	})
}

func BenchmarkMinValue(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			MinValue()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				MinValue()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				MinValue()
			}
		})
	})
}

func BenchmarkMaxDuration(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			MaxDuration()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				MaxDuration()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				MaxDuration()
			}
		})
	})
}

func BenchmarkMinDuration(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			MinDuration()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				MinDuration()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				MinDuration()
			}
		})
	})
}

func BenchmarkMax(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-06")
		c2 := Parse("2021-08-05")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			Max(c1, c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-06")
		c2 := Parse("2021-08-05")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				Max(c1, c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-06")
		c2 := Parse("2021-08-05")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				Max(c1, c2)
			}
		})
	})
}

func BenchmarkMin(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-06")
		c2 := Parse("2021-08-05")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			Min(c1, c2)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-06")
		c2 := Parse("2021-08-05")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				Min(c1, c2)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-06")
		c2 := Parse("2021-08-05")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				Min(c1, c2)
			}
		})
	})
}

func BenchmarkCarbon_Closest(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-04")
		c2 := Parse("2020-08-05")
		c3 := Parse("2021-08-06")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.Closest(c2, c3)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-04")
		c2 := Parse("2020-08-05")
		c3 := Parse("2021-08-06")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.Closest(c2, c3)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-04")
		c2 := Parse("2020-08-05")
		c3 := Parse("2021-08-06")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.Closest(c2, c3)
			}
		})
	})
}

func BenchmarkCarbon_Farthest(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c1 := Parse("2020-08-04")
		c2 := Parse("2020-08-05")
		c3 := Parse("2021-08-06")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c1.Farthest(c2, c3)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c1 := Parse("2020-08-04")
		c2 := Parse("2020-08-05")
		c3 := Parse("2021-08-06")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c1.Farthest(c2, c3)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c1 := Parse("2020-08-04")
		c2 := Parse("2020-08-05")
		c3 := Parse("2021-08-06")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c1.Farthest(c2, c3)
			}
		})
	})
}
