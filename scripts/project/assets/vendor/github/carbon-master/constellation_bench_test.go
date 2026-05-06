package carbon

import (
	"sync"
	"testing"
)

func BenchmarkCarbon_Constellation(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Constellation()
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
				c.Constellation()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Now()
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Constellation()
			}
		})
	})
}

func BenchmarkCarbon_IsAries(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-03-21")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.IsAries()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-03-21")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.IsAries()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-03-21")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.IsAries()
			}
		})
	})
}

func BenchmarkCarbon_IsTaurus(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-04-20")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.IsTaurus()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-04-20")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.IsTaurus()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-04-20")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.IsTaurus()
			}
		})
	})
}

func BenchmarkCarbon_IsGemini(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-05-21")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.IsGemini()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-05-21")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.IsGemini()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-05-21")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.IsGemini()
			}
		})
	})
}

func BenchmarkCarbon_IsCancer(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-06-22")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.IsCancer()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-06-22")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.IsCancer()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-06-22")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.IsCancer()
			}
		})
	})
}

func BenchmarkCarbon_IsLeo(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-07-23")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.IsLeo()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-07-23")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.IsLeo()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-07-23")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.IsLeo()
			}
		})
	})
}

func BenchmarkCarbon_IsVirgo(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-08-23")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.IsVirgo()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-08-23")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.IsVirgo()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-08-23")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.IsVirgo()
			}
		})
	})
}

func BenchmarkCarbon_IsLibra(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-09-23")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.IsLibra()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-09-23")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.IsLibra()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-09-23")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.IsLibra()
			}
		})
	})
}

func BenchmarkCarbon_IsScorpio(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-10-24")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.IsScorpio()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-10-24")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.IsScorpio()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-10-24")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.IsScorpio()
			}
		})
	})
}

func BenchmarkCarbon_IsSagittarius(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-11-23")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.IsSagittarius()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-11-23")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.IsSagittarius()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-11-23")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.IsSagittarius()
			}
		})
	})
}

func BenchmarkCarbon_IsCapricorn(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-12-22")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.IsCapricorn()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-12-22")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.IsCapricorn()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-12-22")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.IsCapricorn()
			}
		})
	})
}

func BenchmarkCarbon_IsAquarius(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-01-20")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.IsAquarius()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-01-20")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.IsAquarius()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-01-20")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.IsAquarius()
			}
		})
	})
}

func BenchmarkCarbon_IsPisces(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-02-19")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.IsPisces()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-02-19")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.IsPisces()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-02-19")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.IsPisces()
			}
		})
	})
}
