package zhi

import (
	"reflect"
	"testing"
)

func minOrder() int64 {
	return 1
}

func maxOrder() int64 {
	return 12
}

func TestNewZhi(t *testing.T) {
	type args struct {
		order int64
	}
	tests := []struct {
		name string
		args args
		want *Zhi
	}{
		{"nil_min", args{minOrder() - 1}, nil},
		{"nil_max", args{maxOrder() + 1}, nil},
		{"test_min", args{minOrder()}, &Zhi{minOrder()}},
		{"test_max", args{maxOrder()}, &Zhi{maxOrder()}},
		{"test", args{8}, &Zhi{8}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := NewZhi(tt.args.order); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("NewZhi() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestZhi_Alias(t *testing.T) {
	tests := []struct {
		name string
		zhi  *Zhi
		want string
	}{
		{"test_1", NewZhi(minOrder()), "子"},
		{"test_2", NewZhi(maxOrder()), "亥"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.zhi.Alias(); got != tt.want {
				t.Errorf("Zhi.Alias() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestZhi_Order(t *testing.T) {
	tests := []struct {
		name string
		zhi  *Zhi
		want int64
	}{
		{"test_1", NewZhi(minOrder()), 1},
		{"test_2", NewZhi(maxOrder()), 12},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.zhi.Order(); got != tt.want {
				t.Errorf("Zhi.Order() = %v, want %v", got, tt.want)
			}
		})
	}
}
