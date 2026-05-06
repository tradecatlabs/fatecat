package carbon

import (
	"encoding/json"
	"sync"
	"testing"
)

func BenchmarkCarbonType_Scan(b *testing.B) {
	c := Now()
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_ = c.Scan(c)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_ = c.Scan(c)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_ = c.Scan(c)
			}
		})
	})
}

func BenchmarkCarbonType_Value(b *testing.B) {
	c := Now()
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_, _ = c.Value()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_, _ = c.Value()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_, _ = c.Value()
			}
		})
	})
}

func BenchmarkCarbonType_MarshalJSON(b *testing.B) {
	var model carbonTypeModel
	model.Carbon1 = *Parse("2020-08-05 13:14:15.999999999")
	model.Carbon2 = Parse("2020-08-05 13:14:15.999999999")
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_, _ = json.Marshal(&model)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_, _ = json.Marshal(&model)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_, _ = json.Marshal(&model)
			}
		})
	})
}

func BenchmarkCarbonType_UnmarshalJSON(b *testing.B) {
	var model carbonTypeModel
	value := `{"carbon1":"2020-08-05 13:14:15","carbon2":"2020-08-05 13:14:15"}`
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_ = json.Unmarshal([]byte(value), &model)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_ = json.Unmarshal([]byte(value), &model)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_ = json.Unmarshal([]byte(value), &model)
			}
		})
	})
}

func BenchmarkCarbonType_String(b *testing.B) {
	c := Now()
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_ = c.String()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_ = c.String()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_ = c.String()
			}
		})
	})
}

func BenchmarkBuiltinType_Scan(b *testing.B) {
	t := NewDateTime(Now())
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_ = t.Scan(Now())
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_ = t.Scan(Now())
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_ = t.Scan(Now())
			}
		})
	})
}

func BenchmarkBuiltinType_Value(b *testing.B) {
	t := NewDateTime(Now())
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_, _ = t.Value()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_, _ = t.Value()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_, _ = t.Value()
			}
		})
	})
}

func BenchmarkBuiltinType_MarshalJSON(b *testing.B) {
	var model builtinTypeModel
	c := Parse("2020-08-05 13:14:15.999999999")

	model.Date = *NewDate(c)
	model.DateMilli = *NewDateMilli(c)
	model.DateMicro = *NewDateMicro(c)
	model.DateNano = *NewDateNano(c)

	model.Time = *NewTime(c)
	model.TimeMilli = *NewTimeMilli(c)
	model.TimeMicro = *NewTimeMicro(c)
	model.TimeNano = *NewTimeNano(c)

	model.DateTime = *NewDateTime(c)
	model.DateTimeMilli = *NewDateTimeMilli(c)
	model.DateTimeMicro = *NewDateTimeMicro(c)
	model.DateTimeNano = *NewDateTimeNano(c)

	model.Timestamp = *NewTimestamp(c)
	model.TimestampMilli = *NewTimestampMilli(c)
	model.TimestampMicro = *NewTimestampMicro(c)
	model.TimestampNano = *NewTimestampNano(c)

	model.CreatedAt = NewDateTime(c)
	model.UpdatedAt = NewDateTime(c)
	model.DeletedAt = NewTimestamp(c)
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_, _ = json.Marshal(&model)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_, _ = json.Marshal(&model)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_, _ = json.Marshal(&model)
			}
		})
	})
}

func BenchmarkBuiltinType_UnmarshalJSON(b *testing.B) {
	var model builtinTypeModel
	value := `{"date":"2020-08-05","date_milli":"2020-08-05.999","date_micro":"2020-08-05.999999","date_nano":"2020-08-05.999999999","time":"13:14:15","time_milli":"13:14:15.999","time_micro":"13:14:15.999999","time_nano":"13:14:15.999999999","date_time":"2020-08-05 13:14:15","date_time_milli":"2020-08-05 13:14:15.999","date_time_micro":"2020-08-05 13:14:15.999999","date_time_nano":"2020-08-05 13:14:15.999999999","created_at":"2020-08-05 13:14:15","updated_at":"2020-08-05 13:14:15","timestamp":1596633255,"timestamp_milli":1596633255999,"timestamp_micro":1596633255999999,"timestamp_nano":1596633255999999999,"deleted_at":1596633255}`
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_ = json.Unmarshal([]byte(value), &model)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_ = json.Unmarshal([]byte(value), &model)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_ = json.Unmarshal([]byte(value), &model)
			}
		})
	})
}

func BenchmarkBuiltinType_String(b *testing.B) {
	t := NewDateTime(Now())
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_ = t.String()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_ = t.String()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_ = t.String()
			}
		})
	})
}

func BenchmarkCustomerType_Scan(b *testing.B) {
	t := NewFormatType[iso8601Type](Parse("2020-08-05"))
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_ = t.Scan(Now())
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_ = t.Scan(Now())
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_ = t.Scan(Now())
			}
		})
	})
}

func BenchmarkCustomerType_Value(b *testing.B) {
	t := NewFormatType[iso8601Type](Parse("2020-08-05"))
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_, _ = t.Value()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_, _ = t.Value()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_, _ = t.Value()
			}
		})
	})
}

func BenchmarkCustomerType_MarshalJSON(b *testing.B) {
	var model CustomerTypeModel
	c := Parse("2020-08-05 13:14:15.999999999")

	model.Customer1 = *NewLayoutType[rfc3339Type](c)
	model.Customer2 = *NewLayoutType[w3cType](c)
	model.Customer3 = *NewFormatType[iso8601Type](c)
	model.Customer4 = *NewFormatType[rssType](c)

	model.CreatedAt = NewFormatType[iso8601Type](c)
	model.UpdatedAt = NewLayoutType[rfc3339Type](c)
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_, _ = json.Marshal(&model)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_, _ = json.Marshal(&model)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_, _ = json.Marshal(&model)
			}
		})
	})
}

func BenchmarkCustomerType_UnmarshalJSON(b *testing.B) {
	var model CustomerTypeModel
	value := `{"customer1":"2020-08-05T13:14:15+00:00","customer2":"2020-08-05T13:14:15Z","created_at":"2020-08-05T13:14:15+00:00","updated_at":"2020-08-05T13:14:15Z"}`
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_ = json.Unmarshal([]byte(value), &model)
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_ = json.Unmarshal([]byte(value), &model)
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_ = json.Unmarshal([]byte(value), &model)
			}
		})
	})
}

func BenchmarkCustomerType_String(b *testing.B) {
	t := NewFormatType[iso8601Type](Parse("2020-08-05"))
	b.ResetTimer()

	b.Run("sequential", func(b *testing.B) {
		for i := 0; i < b.N/10; i++ {
			_ = t.String()
		}
	})

	b.Run("concurrent", func(b *testing.B) {
		var wg sync.WaitGroup
		for i := 0; i < b.N/10; i++ {
			wg.Add(1)
			go func() {
				defer wg.Done()
				_ = t.String()
			}()
		}
		wg.Wait()
	})

	b.Run("parallel", func(b *testing.B) {
		b.RunParallel(func(pb *testing.PB) {
			for pb.Next() {
				_ = t.String()
			}
		})
	})
}
