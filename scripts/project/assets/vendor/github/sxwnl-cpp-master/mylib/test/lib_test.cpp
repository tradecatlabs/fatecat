// #include "../mystl/my_string.h"

#include <cstdio>
#include <string>
#include <cstring>
#include <iostream>

char *base91(int x, char *res)
{
    static char ss[92] = "!#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_`abcdefghijklmnopqrstuvwxyz{|}~";
    char res0[16] = {};
    int k = 91;
    int i = 0;
    while (x >= k)
    {
        res0[i++] = ss[x % k];
        x /= k;
    }
    res0[i] = ss[x];
    int size = strlen(res0);
    for (size_t i = 0; i < size; i++)
    {
        res[i] = res0[size - i - 1];
    }
    return res;
}


int main()
{
    for (size_t i = 61000000; i < 61001000; i++)
    {
        char s[16] = {};
        // std::cout<<
        base91(i, s);
        // <<"\n";
        puts(s);
    }

    return 0;
}