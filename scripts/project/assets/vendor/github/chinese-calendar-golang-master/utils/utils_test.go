package utils

import "testing"

func TestOrderMod(t *testing.T) {
	type args struct {
		a int64
		b int64
	}
	tests := []struct {
		name       string
		args       args
		wantResult int64
	}{
		{"test_1", args{0, 12}, 12},
		{"test_2", args{1, 12}, 1},
		{"test_3", args{12, 12}, 12},
		{"test_4", args{13, 12}, 1},
		{"test_5", args{2, 12}, 2},
		{"test_6", args{14, 12}, 2},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if gotResult := OrderMod(tt.args.a, tt.args.b); gotResult != tt.wantResult {
				t.Errorf("OrderMod() = %v, want %v", gotResult, tt.wantResult)
			}
		})
	}
}

func TestDD(t *testing.T) {
	type args struct {
		jd float64
	}
	tests := []struct {
		name  string
		args  args
		wantY int
		wantM int
		wantD int
		wantH int
		wantI int
		wantS int
	}{
		{"2018-02-04 05:28:29", args{2458153.72812377}, 2018, 2, 4, 5, 28, 29},
		{"50046-01-13 12:00:00", args{19999999}, 50046, 1, 13, 12, 00, 00},
		{"-4712-01-02 12:00:00", args{1}, -4712, 1, 2, 12, 00, 00},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			gotY, gotM, gotD, gotH, gotI, gotS := DD(tt.args.jd)
			if gotY != tt.wantY {
				t.Errorf("DD() gotY = %v, want %v", gotY, tt.wantY)
			}
			if gotM != tt.wantM {
				t.Errorf("DD() gotM = %v, want %v", gotM, tt.wantM)
			}
			if gotD != tt.wantD {
				t.Errorf("DD() gotD = %v, want %v", gotD, tt.wantD)
			}
			if gotH != tt.wantH {
				t.Errorf("DD() gotH = %v, want %v", gotH, tt.wantH)
			}
			if gotI != tt.wantI {
				t.Errorf("DD() gotI = %v, want %v", gotI, tt.wantI)
			}
			if gotS != tt.wantS {
				t.Errorf("DD() gotS = %v, want %v", gotS, tt.wantS)
			}
		})
	}
}
