package gan

import (
	"reflect"
	"testing"
)

func minOrder() int64 {
	return 1
}

func maxOrder() int64 {
	return 10
}

func TestNewGan(t *testing.T) {
	type args struct {
		order int64
	}
	tests := []struct {
		name string
		args args
		want *Gan
	}{
		{"nil_min", args{minOrder() - 1}, nil},
		{"nil_max", args{maxOrder() + 1}, nil},
		{"test_min", args{minOrder()}, &Gan{minOrder()}},
		{"test_max", args{maxOrder()}, &Gan{maxOrder()}},
		{"test", args{8}, &Gan{8}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := NewGan(tt.args.order); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("NewGan() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestGan_Alias(t *testing.T) {
	tests := []struct {
		name string
		gan  *Gan
		want string
	}{
		{"test_1", NewGan(minOrder()), "甲"},
		{"test_2", NewGan(maxOrder()), "癸"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.gan.Alias(); got != tt.want {
				t.Errorf("Gan.Alias() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestGan_Order(t *testing.T) {
	tests := []struct {
		name string
		gan  *Gan
		want int64
	}{
		{"test_1", NewGan(minOrder()), 1},
		{"test_2", NewGan(maxOrder()), 10},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.gan.Order(); got != tt.want {
				t.Errorf("Gan.Order() = %v, want %v", got, tt.want)
			}
		})
	}
}
