package carbon

import (
	"sync"
	"testing"
)

func BenchmarkCarbon_Julian(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-08-05")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Julian()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-08-05")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Julian()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-08-05")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Julian()
			}
		})
	})
}

func BenchmarkCreateFromJulian(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			CreateFromJulian(2460333.051563)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				CreateFromJulian(2460333.051563)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				CreateFromJulian(2460333.051563)
			}
		})
	})
}

func BenchmarkCarbon_Lunar(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-08-05")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Lunar()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-08-05")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Lunar()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-08-05")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Lunar()
			}
		})
	})
}

func BenchmarkCreateFromLunar(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			CreateFromLunar(2023, 12, 11, false)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				CreateFromLunar(2023, 12, 11, false)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				CreateFromLunar(2023, 12, 11, false)
			}
		})
	})
}

func BenchmarkCarbon_Persian(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-08-05")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Persian()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-08-05")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Persian()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-08-05")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Persian()
			}
		})
	})
}

func BenchmarkCreateFromPersian(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			CreateFromPersian(1178, 10, 11)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				CreateFromPersian(1178, 10, 11)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				CreateFromPersian(1178, 10, 11)
			}
		})
	})
}

func BenchmarkCarbon_Hebrew(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		c := Parse("2020-08-05")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			c.Hebrew()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		c := Parse("2020-08-05")
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				c.Hebrew()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		c := Parse("2020-08-05")
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				c.Hebrew()
			}
		})
	})
}

func BenchmarkCreateFromHebrew(b *testing.B) {
	b.Run("sequential", func(b *testing.B) {
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			CreateFromHebrew(5784, 10, 20)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		b.ResetTimer()
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				CreateFromHebrew(5784, 10, 20)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.ResetTimer()
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				CreateFromHebrew(5784, 10, 20)
			}
		})
	})
}
