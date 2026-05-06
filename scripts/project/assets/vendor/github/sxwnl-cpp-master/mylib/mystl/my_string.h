#ifndef MY_STRING_H
#define MY_STRING_H
#include <string>
#include <limits>
#include <stdexcept>
#include <cerrno>
#include "itoa.h"
#include "dtoa.h"

namespace mystl
{
    using string = std::string;
} // namespace mystl


// 萃取float类型
template <typename T> struct is_float {const static bool value = false;};
template <> struct is_float<long double> {const static bool value = true;};
template <> struct is_float<double> {const static bool value = true;};
template <> struct is_float<float> {const static bool value = true;};

inline int my_stoi(const mystl::string &str, typename mystl::string::size_type *pos = nullptr, int base = 10)
{
    typename mystl::string::value_type *end;
    int answer = ::strtol(str.data(), &end, base);
    if (end == str.data())
    {
        throw std::invalid_argument("invalid stof argument");
    }

    if (errno == ERANGE)
    {
        throw std::out_of_range("stof argument out of range");
    }

    if (pos)
    {
        *pos = end - str.data();
    }

    return answer;
}

inline long stol(const mystl::string &str, typename mystl::string::size_type *pos = nullptr, int base = 10)
{
    typename mystl::string::value_type *end;
    long answer = ::strtol(str.data(), &end, base);
    if (end == str.data())
    {
        throw std::invalid_argument("invalid stof argument");
    }

    if (errno == ERANGE)
    {
        throw std::out_of_range("stof argument out of range");
    }

    if (pos)
    {
        *pos = end - str.data();
    }

    return answer;
}

inline long long stoll(const mystl::string &str, typename mystl::string::size_type *pos = nullptr, int base = 10)
{
    typename mystl::string::value_type *end;
    long long answer = ::strtoll(str.data(), &end, base);
    if (end == str.data())
    {
        throw std::invalid_argument("invalid stof argument");
    }

    if (errno == ERANGE)
    {
        throw std::out_of_range("stof argument out of range");
    }

    if (pos)
    {
        *pos = end - str.data();
    }

    return answer;
}

inline unsigned long stoul(const mystl::string &str, typename mystl::string::size_type *pos = nullptr, int base = 10)
{
    typename mystl::string::value_type *end;
    unsigned long answer = ::strtoul(str.data(), &end, base);
    if (end == str.data())
    {
        throw std::invalid_argument("invalid stof argument");
    }

    if (errno == ERANGE)
    {
        throw std::out_of_range("stof argument out of range");
    }

    if (pos)
    {
        *pos = end - str.data();
    }

    return answer;
}

inline unsigned long long stoull(const mystl::string &str, typename mystl::string::size_type *pos = nullptr, int base = 10)
{
    typename mystl::string::value_type *end;
    unsigned long long answer = ::strtoull(str.data(), &end, base);
    if (end == str.data())
    {
        throw std::invalid_argument("invalid stof argument");
    }

    if (errno == ERANGE)
    {
        throw std::out_of_range("stof argument out of range");
    }

    if (pos)
    {
        *pos = end - str.data();
    }

    return answer;
}

inline float stof(const mystl::string &str, typename mystl::string::size_type *pos = nullptr)
{
    typename mystl::string::value_type *end;
    float answer = ::strtof(str.data(), &end);

    if (end == str.data())
    {
        throw std::invalid_argument("invalid stof argument");
    }

    if (errno == ERANGE)
    {
        throw std::out_of_range("stof argument out of range");
    }

    if (pos)
    {
        *pos = end - str.data();
    }

    return answer;
}

inline double stod(const mystl::string &str, typename mystl::string::size_type *pos = nullptr)
{
    typename mystl::string::value_type *end;
    double answer = ::strtod(str.data(), &end);
    if (end == str.data())
    {
        throw std::invalid_argument("invalid stof argument");
    }

    if (errno == ERANGE)
    {
        throw std::out_of_range("stof argument out of range");
    }

    if (pos)
    {
        *pos = end - str.data();
    }

    return answer;
}

inline long double stold(const mystl::string &str, typename mystl::string::size_type *pos = nullptr)
{
    typename mystl::string::value_type *end;
    long double answer = ::strtold(str.data(), &end);
    if (end == str.data())
    {
        throw std::invalid_argument("invalid stof argument");
    }

    if (errno == ERANGE)
    {
        throw std::out_of_range("stof argument out of range");
    }

    if (pos)
    {
        *pos = end - str.data();
    }

    return answer;
}

// length 总长度，是否右对齐
template <class T>
inline mystl::string to_str(T value, int precision = 4, int length = 0, bool right_align = false)
{
    // digits10 returns floor value, so add 1 for remainder, 1 for - and 1 for null terminator
    char str[32] = {};
    
    if ( is_float<T>::value) { // 浮点数
        dtoa_milo2(value, str, precision, true);
    } else { // 整数
        jeaiii::to_text_from_integer(str, value);
    }

    char fill[64] = "";
    size_t s_len = strlen(str);
    if (length > s_len) { 
        size_t len = length - s_len;
        for (size_t i = 0; i < len; i++) {
            fill[i] = ' ';
        }
    }
    return right_align ? 
    (mystl::string(fill) + mystl::string(str)) : (mystl::string(str) + mystl::string(fill)); 
}

#endif // !MY_STRING_H