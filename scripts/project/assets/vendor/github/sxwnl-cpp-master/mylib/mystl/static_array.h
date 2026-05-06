#ifndef STATIC_ARRAY_H
#define STATIC_ARRAY_H
#include <initializer_list>
#include <cstddef>

namespace mystl {
// 实现一个非常简易的静态固定容量数组
template <class T,size_t N>
struct static_array {
    using t_list   = const std::initializer_list<T>&;
    using t_list_i = const std::initializer_list<int>&;
    using t_list_d = const std::initializer_list<double>&;
	
    // 定义迭代器类型
    using iterator = T*;
    
    static_array() {}
    
    static_array& operator=(const static_array<T, N>& right) {
	    for (int i = 0; i < N; ++i) {
	        data[i] = right.data[i];
	    }
	    return *this;
    }

    T& operator[](size_t i) {
        return data[i];
    }
    
    T get(size_t i) {
        return data[i];
    }
    
    
    void fill(const T& val) {
    	for (size_t i = 0; i < N; ++i) {
    		data[i] = val;
    	}
    }
    
    // 通过列表数组初始化
    static_array(t_list r) {
    	auto it = r.begin();
    	for (size_t i = 0; i < r.size(); ++i) {
    		data[i] = *it++;
    	}
    }
    
    iterator begin() {
        return _begin;
    }
    iterator end() {
        return _end;
    }
    
private: 
    // 数据实体
    T data[N]={};
	iterator _begin = data;
	iterator _end   = data + N;
};

// 容量为2的double数组
struct array2 : static_array<double, 2> {
    array2() {};
    array2(t_list_d r):static_array<double, 2>(r){}
};

// 容量为3的double数组
struct array3 : static_array<double, 3> {
    array3() {};
    array3(t_list_d r):static_array<double, 3>(r){}
    
};

// 容量为4的double数组
struct array4 : static_array<double, 4> {
    array4() {};
    array4(t_list_d r):static_array<double,4>(r){}
};

// 容量为5的double数组
struct array5 : static_array<double, 5> {
    array5() {};
    array5(t_list_d r):static_array<double, 5>(r){}
};

// 容量为7的double数组
struct array7 : static_array<double, 7> {
    array7() {};
    array7(t_list_d r):static_array<double, 7>(r){}
};

// 容量为10的double数组
struct array10 : static_array<double, 10> {
    array10() {};
    array10(t_list_d r):static_array<double, 10>(r){}
};

} // namespace mystl

#endif // STATIC_ARRAY_H