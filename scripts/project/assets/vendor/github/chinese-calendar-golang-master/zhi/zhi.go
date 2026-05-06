package zhi

// Zhi 地支
type Zhi struct {
	order int64
}

var zhiAlias = [...]string{
	"子", "丑", "寅", "卯", "辰", "巳",
	"午", "未", "申", "酉", "戌", "亥",
}

// NewZhi 创建地支对象
func NewZhi(order int64) *Zhi {
	if !isSupported(order) {
		return nil
	}
	return &Zhi{order: order}
}

// Alias 返回地支名称(子丑寅卯...)
func (zhi *Zhi) Alias() string {
	return zhiAlias[(zhi.order-1)%12]
}

// Order 返回地支序数(1234...)
func (zhi *Zhi) Order() int64 {
	return zhi.order
}

func isSupported(order int64) bool {
	return 1 <= order && order <= 12
}
