/*
MIT License

Copyright (c) 2017 James Edward Anhalt III - https://github.com/jeaiii/itoa

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>
#include <random>
#include <type_traits>

#include "../mystl/itoa.h"

template <typename T> struct is_float {const static bool value = false;};
template <> struct is_float<long double> {const static bool value = true;};
template <> struct is_float<double> {const static bool value = true;};
template <> struct is_float<float> {const static bool value = true;};

template <class T>
void show(T n)
{
    std::cout << "is_float<int> == " << std::boolalpha << is_float<T>::value << std::endl;
    char text[32] = {};
    jeaiii::to_text_from_integer(text, n);
    std::cout << text << "\n";
}

template <class T>
void test(T n)
{
    show(n);
}

int main()
{
    test(-1.2);
    test(-1);
    test(99963555669888.9687);
    test(0x7fffffff);
    test(-0x7fffffff - 1);

    test(1000000000900000000ULL);
    test(1000000000800000001ULL);
    test(1000000000700000002ULL);
    test(1000000000600000003ULL);
    test(1000000000500000004ULL);
    test(1000000000400000005ULL);
    test(1000000000300000006ULL);
    test(1000000000200000007ULL);
    test(1000000000100000008ULL);
    test(1000000000000000009ULL);

    test(999010000000ULL);
    test(999010000001ULL);
    test(999010000009ULL);

    test(99909000000ULL);
    test(99909000001ULL);
    test(99909000009ULL);

    test(99909000009LL);
    test(-99909000009LL);

    test(17999999999999999999ULL);

    test(5999999999999999999LL);
    test(-5999999999999999999LL);

    return 0;
}