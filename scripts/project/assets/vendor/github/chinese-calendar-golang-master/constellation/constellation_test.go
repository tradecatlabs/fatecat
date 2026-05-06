package constellation

import (
	"testing"
	"time"
)

func loc() *time.Location {
	loc, _ := time.LoadLocation("PRC")
	return loc
}

func now() *time.Time {
	t := time.Now()
	return &t
}

func testTime1() *time.Time {
	t := time.Date(2018, 1, 1, 0, 0, 0, 0, loc())
	return &t
}

func testTime2() *time.Time {
	t := time.Date(2018, 2, 1, 0, 0, 0, 0, loc())
	return &t
}

func testTime3() *time.Time {
	t := time.Date(2018, 3, 1, 0, 0, 0, 0, loc())
	return &t
}

func testTime4() *time.Time {
	t := time.Date(2018, 4, 1, 0, 0, 0, 0, loc())
	return &t
}

func testTime5() *time.Time {
	t := time.Date(2018, 5, 1, 0, 0, 0, 0, loc())
	return &t
}

func testTime6() *time.Time {
	t := time.Date(2018, 6, 1, 0, 0, 0, 0, loc())
	return &t
}

func testTime7() *time.Time {
	t := time.Date(2018, 7, 1, 0, 0, 0, 0, loc())
	return &t
}

func testTime8() *time.Time {
	t := time.Date(2018, 8, 1, 0, 0, 0, 0, loc())
	return &t
}

func testTime9() *time.Time {
	t := time.Date(2018, 9, 1, 0, 0, 0, 0, loc())
	return &t
}

func testTime10() *time.Time {
	t := time.Date(2018, 10, 1, 0, 0, 0, 0, loc())
	return &t
}

func testTime11() *time.Time {
	t := time.Date(2018, 11, 1, 0, 0, 0, 0, loc())
	return &t
}

func testTime12() *time.Time {
	t := time.Date(2018, 12, 1, 0, 0, 0, 0, loc())
	return &t
}

func TestNewConstellation(t *testing.T) {
	type args struct {
		t *time.Time
	}
	tests := []struct {
		name string
		args args
		want *Constellation
	}{
		{"test", args{now()}, &Constellation{now()}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := NewConstellation(tt.args.t); got.Alias() != tt.want.Alias() {
				t.Errorf("NewConstellation() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestConstellation_Alias(t *testing.T) {
	tests := []struct {
		name          string
		constellation *Constellation
		want          string
	}{
		{"摩羯", NewConstellation(testTime1()), "摩羯"},
		{"水瓶", NewConstellation(testTime2()), "水瓶"},
		{"双鱼", NewConstellation(testTime3()), "双鱼"},
		{"白羊", NewConstellation(testTime4()), "白羊"},
		{"金牛", NewConstellation(testTime5()), "金牛"},
		{"双子", NewConstellation(testTime6()), "双子"},
		{"巨蟹", NewConstellation(testTime7()), "巨蟹"},
		{"狮子", NewConstellation(testTime8()), "狮子"},
		{"处女", NewConstellation(testTime9()), "处女"},
		{"天秤", NewConstellation(testTime10()), "天秤"},
		{"天蝎", NewConstellation(testTime11()), "天蝎"},
		{"射手", NewConstellation(testTime12()), "射手"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.constellation.Alias(); got != tt.want {
				t.Errorf("Constellation.Alias() = %v, want %v", got, tt.want)
			}
		})
	}
}
