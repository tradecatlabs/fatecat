package animal

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

func TestNewAnimal(t *testing.T) {
	type args struct {
		order int64
	}
	tests := []struct {
		name string
		args args
		want *Animal
	}{
		{"nil_min", args{minOrder() - 1}, nil},
		{"nil_max", args{maxOrder() + 1}, nil},
		{"test_min", args{minOrder()}, &Animal{minOrder()}},
		{"test_max", args{maxOrder()}, &Animal{maxOrder()}},
		{"test", args{8}, &Animal{8}},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := NewAnimal(tt.args.order); !reflect.DeepEqual(got, tt.want) {
				t.Errorf("NewAnimal() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestAnimal_Alias(t *testing.T) {
	tests := []struct {
		name   string
		animal *Animal
		want   string
	}{
		{"test_1", NewAnimal(minOrder()), "鼠"},
		{"test_2", NewAnimal(maxOrder()), "猪"},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := tt.animal.Alias(); got != tt.want {
				t.Errorf("Animal.Alias() = %v, want %v", got, tt.want)
			}
		})
	}
}
