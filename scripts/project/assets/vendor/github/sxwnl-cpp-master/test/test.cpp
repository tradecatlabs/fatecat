/*
寿星天文历v5.05js版 C++翻译工程
API测试
2018-8-28
*/

#include <ctime>
#include <iostream>
#include <array>

#include "../mylib/tool.h"
#include "../lunar/lunar.h"
#include "../eph/eph_show.h"
#include "../eph/eph0.h"
#include "../eph/eph.h"
int main()
{
#if defined(__WIN32__) || defined(_MSC_VER)
	system("@chcp 65001");
#endif

	Date date = { 2008, 1, 1, 0, 0, 0};
    double jd1 = toJD(date) - J2000;
    mystl::string ss = xingX(1, jd1, A2R(116.383333), A2R(39.900000));
	std::cout<<ss<<std::endl;
	system("pause");
	return 0;
}