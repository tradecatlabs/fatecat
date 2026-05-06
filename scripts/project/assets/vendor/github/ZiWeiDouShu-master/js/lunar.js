//
//陰陽曆轉換
//By Einstein 1999-4-12
//
var BYEAR=1201
var Nyear=150;     /* number of years covered by the table */
var Nmonth=13      /* maximum number of months in a lunar year */
var title;
var y,m,d;
var jieAlert;
/*----------------------------------------------------------*/
function make_array() {
  var tmparg=make_array.arguments;
  for(var i=0;i<tmparg.length;i++) {
    this[i]=tmparg[i];
  }
  this.length=tmparg.length;
}

function make_n_array(num) {
  for(var i=0;i<num;i++) {
    this[i]=i;
  }
  this.length=num;
}

function MyDate(y,m,d,h,w,l){//year,month,day,hour,week,leap
  this.y=y;
  this.m=m;
  this.d=d;
  this.h=h;
  this.w=w;
  this.l=l;
}

    /* encoding:
                b bbbbbbbbbbbb bbbb
       bit#     1 111111000000 0000
                6 543210987654 3210
                . ............ ....
       month#     000000000111
                M 123456789012   L
                                
    b_j = 1 for long month, b_j = 0 for short month
    L is the leap month of the year if 1<=L<=12; NO leap month if L = 0.
    The leap month (if exists) is long one iff M = 1.
    */
var yearInfo=new make_array(
                                        0x04bd8,        /* 1900 */
    0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950,        /* 1905 */
    0x16554, 0x056a0, 0x09ad0, 0x055d2, 0x04ae0,        /* 1910 */
    0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540,        /* 1915 */
    0x0d6a0, 0x0ada2, 0x095b0, 0x14977, 0x04970,        /* 1920 */
    0x0a4b0, 0x0b4b5, 0x06a50, 0x06d40, 0x1ab54,        /* 1925 */
    0x02b60, 0x09570, 0x052f2, 0x04970, 0x06566,        /* 1930 */
    0x0d4a0, 0x0ea50, 0x06e95, 0x05ad0, 0x02b60,        /* 1935 */
    0x186e3, 0x092e0, 0x1c8d7, 0x0c950, 0x0d4a0,        /* 1940 */
    0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0,        /* 1945 */
    0x092d0, 0x0d2b2, 0x0a950, 0x0b557, 0x06ca0,        /* 1950 */
    0x0b550, 0x15355, 0x04da0, 0x0a5d0, 0x14573,        /* 1955 */
    0x052d0, 0x0a9a8, 0x0e950, 0x06aa0, 0x0aea6,        /* 1960 */
    0x0ab50, 0x04b60, 0x0aae4, 0x0a570, 0x05260,        /* 1965 */
    0x0f263, 0x0d950, 0x05b57, 0x056a0, 0x096d0,        /* 1970 */
    0x04dd5, 0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250,        /* 1975 */
    0x0d558, 0x0b540, 0x0b5a0, 0x195a6, 0x095b0,        /* 1980 */
    0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50,        /* 1985 */
    0x06d40, 0x0af46, 0x0ab60, 0x09570, 0x04af5,        /* 1990 */
    0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58,        /* 1995 */
    0x055c0, 0x0ab60, 0x096d5, 0x092e0, 0x0c960,        /* 2000 */
    0x0d954, 0x0d4a0, 0x0da50, 0x07552, 0x056a0,        /* 2005 */
    0x0abb7, 0x025d0, 0x092d0, 0x0cab5, 0x0a950,        /* 2010 */
    0x0b4a0, 0x0baa4, 0x0ad50, 0x055d9, 0x04ba0,        /* 2015 */
    0x0a5b0, 0x15176, 0x052b0, 0x0a930, 0x07954,        /* 2020 */
    0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6,        /* 2025 */
    0x0a4e0, 0x0d260, 0x0ea65, 0x0d530, 0x05aa0,        /* 2030 */
    0x076a3, 0x096d0, 0x04bd7, 0x04ad0, 0x0a4d0,        /* 2035 */
    0x1d0b6, 0x0d250, 0x0d520, 0x0dd45, 0x0b5a0,        /* 2040 */
    0x056d0, 0x055b2, 0x049b0, 0x0a577, 0x0a4b0,        /* 2045 */
    0x0aa50, 0x1b255, 0x06d20, 0x0ada0                  /* 2049 */
);
var fest = new make_array(/* [Nyear][12] */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1900 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1901 */
5, 6, 6, 6, 7, 8, 8, 8, 9, 8, 8, 6,   /* 1902 */
5, 7, 6, 7, 7, 8, 9, 9, 9, 8, 8, 7,   /* 1903 */
5, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1904 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1905 */
5, 6, 6, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1906 */
5, 7, 6, 7, 7, 8, 9, 9, 9, 8, 8, 7,   /* 1907 */
5, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1908 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1909 */
5, 6, 6, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1910 */
5, 7, 6, 7, 7, 8, 9, 9, 9, 8, 8, 7,   /* 1911 */
5, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1912 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1913 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1914 */
5, 6, 6, 6, 7, 8, 8, 9, 9, 8, 8, 6,   /* 1915 */
5, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 1916 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 7, 6,   /* 1917 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1918 */
5, 6, 6, 6, 7, 8, 8, 9, 9, 8, 8, 6,   /* 1919 */
5, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 1920 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 9, 7, 6,   /* 1921 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1922 */
5, 6, 6, 6, 7, 8, 8, 9, 9, 8, 8, 6,   /* 1923 */
5, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 1924 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 7, 6,   /* 1925 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1926 */
5, 6, 6, 6, 7, 8, 8, 8, 9, 8, 8, 6,   /* 1927 */
5, 6, 5, 6, 6, 7, 8, 8, 8, 7, 7, 6,   /* 1928 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1929 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1930 */
5, 6, 6, 6, 7, 8, 8, 8, 9, 8, 8, 6,   /* 1931 */
5, 6, 5, 6, 6, 7, 8, 8, 8, 7, 7, 6,   /* 1932 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1933 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1934 */
5, 6, 6, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1935 */
5, 6, 5, 6, 6, 7, 8, 8, 8, 7, 7, 6,   /* 1936 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1937 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1938 */
5, 6, 6, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1939 */
5, 6, 5, 6, 6, 7, 8, 8, 8, 7, 7, 6,   /* 1940 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1941 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1942 */
5, 6, 6, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1943 */
5, 6, 5, 5, 6, 7, 8, 8, 8, 7, 7, 6,   /* 1944 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 1945 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1946 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1947 */
5, 5, 5, 5, 6, 7, 7, 8, 8, 7, 7, 5,   /* 1948 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 1949 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1950 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1951 */
5, 5, 5, 5, 6, 7, 7, 8, 8, 7, 7, 5,   /* 1952 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 1953 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 7, 6,   /* 1954 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1955 */
5, 5, 5, 5, 6, 7, 7, 8, 8, 7, 7, 5,   /* 1956 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 1957 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1958 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1959 */
5, 5, 5, 5, 6, 7, 7, 7, 8, 7, 7, 5,   /* 1960 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 7, 7, 6,   /* 1961 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1962 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1963 */
5, 5, 5, 5, 6, 7, 7, 7, 8, 7, 7, 5,   /* 1964 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 7, 7, 6,   /* 1965 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1966 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1967 */
5, 5, 5, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 1968 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 7, 7, 6,   /* 1969 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1970 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1971 */
5, 5, 5, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 1972 */
4, 6, 5, 5, 6, 7, 8, 8, 8, 7, 7, 6,   /* 1973 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1974 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1975 */
5, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 1976 */
4, 6, 5, 5, 6, 7, 7, 8, 8, 7, 7, 6,   /* 1977 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 1978 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1979 */
5, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 1980 */
4, 6, 5, 5, 6, 7, 7, 8, 8, 7, 7, 6,   /* 1981 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 1982 */
4, 6, 5, 6, 6, 8, 8, 8, 9, 8, 8, 6,   /* 1983 */
4, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 1984 */
5, 5, 5, 5, 5, 8, 7, 7, 8, 7, 7, 5,   /* 1985 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 1986 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1987 */
4, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 1988 */
5, 5, 5, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 1989 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 1990 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1991 */
4, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 1992 */
5, 5, 5, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 1993 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 7, 7, 6,   /* 1994 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1995 */
4, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 1996 */
5, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 1997 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 7, 7, 6,   /* 1998 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 1999 */
4, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2000 */
4, 5, 5, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2001 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 7, 7, 6,   /* 2002 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 2003 */
4, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2004 */
4, 5, 5, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2005 */
4, 6, 5, 5, 6, 7, 7, 8, 8, 7, 7, 6,   /* 2006 */
4, 6, 5, 6, 6, 7, 8, 8, 9, 8, 7, 6,   /* 2007 */
4, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2008 */
4, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2009 */
4, 6, 5, 5, 6, 7, 7, 8, 8, 7, 7, 6,   /* 2010 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 2011 */
4, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2012 */
4, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2013 */
4, 6, 5, 5, 6, 7, 7, 8, 8, 7, 7, 6,   /* 2014 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 2015 */
4, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2016 */
3, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2017 */
4, 5, 5, 5, 6, 7, 7, 8, 8, 7, 7, 5,   /* 2018 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 2019 */
4, 5, 4, 5, 5, 6, 7, 7, 8, 7, 7, 5,   /* 2020 */
3, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2021 */
4, 5, 5, 5, 6, 7, 7, 7, 8, 7, 7, 5,   /* 2022 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 8, 7, 6,   /* 2023 */
4, 5, 4, 5, 5, 6, 7, 7, 8, 7, 6, 5,   /* 2024 */
3, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2025 */
4, 5, 5, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2026 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 7, 7, 6,   /* 2027 */
4, 5, 4, 5, 5, 6, 7, 7, 8, 7, 6, 5,   /* 2028 */
3, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2029 */
4, 5, 5, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2030 */
4, 6, 5, 6, 6, 7, 8, 8, 8, 7, 7, 6,   /* 2031 */
4, 5, 4, 5, 5, 6, 7, 7, 8, 7, 6, 5,   /* 2032 */
3, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2033 */
4, 5, 5, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2034 */
4, 6, 5, 5, 6, 7, 7, 8, 8, 7, 7, 6,   /* 2035 */
4, 5, 4, 5, 5, 6, 7, 7, 8, 7, 6, 5,   /* 2036 */
3, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2037 */
4, 5, 5, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2038 */
4, 6, 5, 5, 6, 7, 7, 8, 8, 7, 7, 6,   /* 2039 */
4, 5, 4, 5, 5, 6, 7, 7, 8, 7, 6, 5,   /* 2040 */
3, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2041 */
4, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2042 */
4, 6, 5, 5, 6, 7, 7, 8, 8, 7, 7, 6,   /* 2043 */
4, 5, 4, 5, 5, 6, 7, 7, 7, 7, 6, 5,   /* 2044 */
3, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2045 */
4, 5, 4, 5, 5, 7, 7, 7, 8, 7, 7, 5,   /* 2046 */
4, 6, 5, 5, 6, 7, 7, 8, 8, 7, 7, 6,   /* 2047 */
4, 5, 4, 5, 5, 6, 7, 7, 7, 7, 6, 5,   /* 2048 */
3, 5, 4, 5, 5, 6, 7, 7, 8, 7, 7, 5    /* 2049 */
);

var ymonth=new make_n_array(Nyear);// number of lunar months in the years
var yday=new make_n_array(Nyear);  // number of lunar days in the years
var mday=new make_n_array(Nmonth+1);// number of days in the months of the lunar year
var moon=new make_array(29,30);// a short (long) lunar month has 29 (30) days 
var weekdayGB=new make_array("日", "一", "二", "三","四", "五", "六");
var ShengXiaoGB=new make_array("鼠", "牛", "虎", "兔", "龍", "蛇",
    "馬", "羊", "猴", "雞", "狗", "豬");
var GanGB=new make_array("甲", "乙", "丙", "丁", "戊",
    "己", "庚", "辛", "壬", "癸");

var ZhiGB=new make_array("子", "丑", "寅", "卯", "辰", "巳",
    "午", "未", "申", "酉", "戌", "亥");
var daysInSolarMonth=new
    make_array(0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
var solarFirstDate=new MyDate(1900,1,31,0,3,0);

/* Wednesday, 12 a.m., First day, First month, 1900 */
var LunarFirstDate=new MyDate(1900, 1, 1, 0, 3, 0);

    /* geng1-nian2 wu4-yue4 jia3-ri4 jia3-shi2 */
var GanFirstDate=new MyDate(6,4,0,0,3,0);

    /* zi3-nian2 yin2-yue4 chen2-ri4 zi3-shi2 */
var ZhiFirstDate=new MyDate(0,2,4,0,3,0);

var solar=new MyDate(0,0,0,0,0,0);
var lunar=new MyDate(0,0,0,0,0,0);
var gan=new MyDate(0,0,0,0,0,0);
var zhi=new MyDate(0,0,0,0,0,0);
var gan2=new MyDate(0,0,0,0,0,0);
var zhi2=new MyDate(0,0,0,0,0,0);
var lunar2=new MyDate(0,0,0,0,0,0);
/*----------------------------------------------------------
function report(type,ans) {
  var answer,answer2;
//  alert("type"+type+"ans="+ans);
//  answer=title+solar.y+"年"+solar.m+"月"+solar.d+"日,星期"+solar.w;
  if(type==0) { //陽->陰
    answer="陰曆"+lunar.y+"("+GanGB[gan.y]+ZhiGB[zhi.y]+")年"+(lunar.l?"閏":"")+lunar.m+"月"+lunar.d+"日,生肖屬"+ShengXiaoGB[zhi.y]; 
//    answer2="干支:"+GanGB[gan.y]+ZhiGB[zhi.y]+"年"+
//        GanGB[gan.m]+ZhiGB[zhi.m]+"月"+GanGB[gan.d]+ZhiGB[zhi.d]+"日"; 
  }
  else {
    answer="陽曆"+solar.y+"年"+solar.m+"月"+solar.d+"日,星期"+weekdayGB[solar.w]; 
//    answer2="干支:"+GanGB[gan.y]+ZhiGB[zhi.y]+"年"+
//        GanGB[gan.m]+ZhiGB[zhi.m]+"月"+GanGB[gan.d]+ZhiGB[zhi.d]+"日"; 
  }
//  answer2=title+lunar.y+"年"+lunar.m+"月"+lunar.d+"日,星期"+lunar.w;
//  alert(answer);
  ans.value=answer;
//  ans2.value=answer2;
}
----------------------------------------------------------*/
function LeapYear(y) {
  return ( ((y%4)==0) && ((y%100)!=0) || ((y%400)==0) );
}
function solar2Day1(d) {//d:MyDate type
  var offset,delta;
  var i;
  delta=d.y-BYEAR;//BYEAR
  if(delta<0) {
    alert("internal error:pick a larger constant for BYEAR");
    return -1;
  }
  offset=Math.floor(delta*365)+Math.floor(delta/4)-Math.floor(delta/100)+
    Math.floor(delta/400);
  for(i=1;i<d.m;i++) {
    offset+=daysInSolarMonth[i];
  }
  if((d.m>2) && (LeapYear(d.y))) offset++;
  offset+=d.d-1;
  if((d.m==2) && LeapYear(d.y)) {
    if(d.d>29) {
      alert("day1 out of range");
      return -1;
    }
  }
  else if(d.d>daysInSolarMonth[d.m]) {
    alert("day2 out of range");
    return -1;
  }
  return offset;
}
/*----------------------------------------------------------*/
function solar2Day(d) {//MyDate type
//  alert("d="+d);
//  alert("1:"+solar2Day1(d)+"\n2:"+solar2Day1(solarFirstDate));
  return (solar2Day1(d)-solar2Day1(solarFirstDate));
}
/*----------------------------------------------------------*/
/* Compute the number of days in each lunar year in the table */
function make_yday()
{
  var year, i, leap;
  var code;
    
  for (year = 0; year < Nyear; year++) {
    code = yearInfo[year];
    leap = code & 0xf;
    yday[year] = 0;
    if (leap != 0) {
      i = (code >> 16) & 0x1;
      yday[year] += moon[i];
    }
    code >>= 4;
    for (i = 0; i < Nmonth-1; i++) {
      yday[year] += moon[code&0x1];
      code >>= 1;
    }
    ymonth[year] = 12;
    if (leap != 0) ymonth[year]++;
  }
  return Nyear;
}
/*----------------------------------------------------------*/
/* Compute the days of each month in the given lunar year */
function make_mday(year)
{
    var i, leapMonth,code;
    
    code = yearInfo[year];
    leapMonth = code & 0xf;
    /* leapMonth == 0 means no leap month */
    code >>= 4;
    if (leapMonth == 0)
    {
        mday[Nmonth] = 0;
        for (i = Nmonth-1; i >= 1; i--)
        {
            mday[i] = moon[code&0x1];
            code >>= 1;
        }
    }
    else
    {
        /* 
          There is a leap month (run4 yue4) L in this year.
          mday[1] contains the number of days in the 1-st month;
          mday[L] contains the number of days in the L-th month;
          mday[L+1] contains the number of days in the L-th leap month;
          mday[L+2] contains the number of days in the L+1 month, etc.

          cf. yearInfo[]: info about the leap month is encoded differently.
        */
        i = (yearInfo[year] >> 16) & 0x1;
        mday[leapMonth+1] = moon[i];
        for (i = Nmonth; i >= 1; i--)
        {
            if (i == leapMonth+1) i--;
            mday[i] = moon[code&0x1];
            code >>= 1;
        }
    }
    return leapMonth;
}
/*----------------------------------------------------------*/
function day2Lunar(offset,d) {
  var i,m,nYear,leapMonth;

  nYear = make_yday();
  for (i=0; i<nYear && offset > 0; i++)  offset -= yday[i];

  if (offset<0)  offset += yday[--i];

  if (i==Nyear) {
    alert("Year out of range.");
    return ;
  }

  d.y = i + LunarFirstDate.y;

  leapMonth = make_mday(i);
  for (m=1; m<=Nmonth && offset>0; m++)  offset -= mday[m];

  if (offset<0) offset += mday[--m];

  d.l= 0;        /* don't know leap or not yet */

  if (leapMonth>0)  {  /* has leap month */
// if preceeding month number is the leap month, this month is the actual extra leap month 
    d.l = (leapMonth == (m - 1));
    /* month > leapMonth is off by 1, so adjust it */
    if (m > leapMonth) --m;
  }

  d.m = m;
  d.d = offset + 1;
}
/*----------------------------------------------------------*/
function CalGZ(offset, d, g, z)
{
  var year, month;
        
  year = d.y - LunarFirstDate.y;
  month = year * 12 + d.m - 1;   /* leap months do not count */

//  alert("year="+year+"month="+month);
  g.y = (GanFirstDate.y + year) % 10;
  z.y = (ZhiFirstDate.y + year) % 12;
  g.m = (GanFirstDate.m + month) % 10;
  z.m = (ZhiFirstDate.m + month) % 12;
  g.d = (GanFirstDate.d + offset) % 10;
  z.d = (ZhiFirstDate.d + offset) % 12;
  z.h = Math.floor((d.h + 1) / 2) % 12;
  g.h = (g.d * 12 + z.h) % 10;
}
/*----------------------------------------------------------*/
/* Compare two dates and return <,=,> 0 if the 1st is <,=,> the 2nd */
function CmpDate(month1, day1, month2, day2)
{
    if (month1!=month2) return(month1-month2);
    if (day1!=day2) return(day1-day2);
    return(0);
}
/*----------------------------------------------------------*/
/* Given a solar date, find the "lunar" date for the purpose of
   calculating the "4-columns" by taking jie into consideration.
*/
function JieDate(ds, dl)//MyDate type
{
    var m, flag;

    if (ds.m==1) {
        flag = CmpDate(ds.m, ds.d,
                       1, fest[(ds.y - solarFirstDate.y - 1)*12+11]);
        if (flag<0) dl.m = 11;
        else if (flag>0) dl.m = 12;
        dl.y = ds.y - 1;
        return(flag==0);
    }
    for (m=2; m<=12; m++) {
        flag = CmpDate(ds.m, ds.d,
                       m, fest[(ds.y - solarFirstDate.y)*12+m-2]);
        if (flag==0) m++;
        if (flag<=0) break;
    }
    dl.m = (m-2) % 12;
    dl.y = ds.y;
    if ((dl.m)==0){
        dl.y = ds.y - 1;
        dl.m = 12;
    }
    return(flag==0);
}
/*----------------------------------------------------------*/
function solar2Lunar() {
  var offset;
  offset=solar2Day(solar);

  solar.w=(offset+solarFirstDate.w)%7;
//alert("offset="+offset+",w="+solar.w);
//a lunar day begins at 11pm
  if(solar.h==23) offset++;

  day2Lunar(offset,lunar);
 lunar.h=solar.h;
  CalGZ(offset,lunar,gan,zhi);

  jieAlert = JieDate(solar, lunar2);
  lunar2.d = lunar.d;
  lunar2.hour = lunar.hour;
  CalGZ(offset, lunar2, gan2, zhi2);
}
/*----------------------------------------------------------*/
/* Compute offset days of a lunar date from the beginning of the table */
function Lunar2Day(d)
{
    var offset = 0;
    var year, i, m, nYear, leapMonth;

    nYear = make_yday();
    year = d.y - LunarFirstDate.y;
    for (i=0; i<year; i++)  offset += yday[i];

    leapMonth = make_mday(year);
    if ((d.l) && (leapMonth!=d.m)) {
      alert(d.m +"is not a leap month in year "+d.y);
      return -1;
//        printf("%d is not a leap month in year %d.\n", d->month, d->year);
//        exit(1);
    }
    for (m=1; m<d.m; m++) offset += mday[m];
    if (leapMonth && ((d.m>leapMonth) || (d.l && (d.m==leapMonth))))
        offset += mday[m++];
    offset += d.d- 1;

    if (d.d > mday[m]) Error("Day out of range.");

    return offset;
}
/*----------------------------------------------------------*/
function Solar2Day(d)
{
    return (Solar2Day1(d) - Solar2Day1(solarFirstDate));
}
/*----------------------------------------------------------*/
/* Compute the number of days from the Solar date BYEAR.1.1 */
function Solar2Day1(d)
{
    var offset, delta;
    var i;

    delta = d.y - BYEAR;
    if (delta<0) {
//Error("Internal error: pick a larger constant for BYEAR.");
      alert("Internal error: pick a larger constant for BYEAR.");
      return -1;
    }
    offset = delta * 365 + Math.floor(delta / 4) - Math.floor(delta / 100) + 
        Math.floor(delta / 400);
    for (i=1; i< d.m; i++)
        offset += daysInSolarMonth[i];
    if ((d.m > 2) && LeapYear(d.y))  offset++;
    offset += d.d - 1;

    if ((d.m == 2) && LeapYear(d.y)) {
        if (d.d > 29){
// Error("Day out of range.");
           alert("Day out of range.");
           return -1;
        }
    }
    else if (d.d > daysInSolarMonth[d.m]) {
//       Error("Day out of range.");
      alert("Day out of range.");
      return -1;
    }
    return offset;
}
/*----------------------------------------------------------*/
function Day2Solar(offset, d)
{
    var i, m, days;

    /* offset is the number of days from SolarFirstDate */
    offset -= Solar2Day(LunarFirstDate);  /* the argument is negative */
    /* offset is now the number of days from SolarFirstDate.year.1.1 */

    for (i=solarFirstDate.y;(i<solarFirstDate.y+Nyear) && (offset > 0);  i++) 
        offset -= 365 + LeapYear(i);
    if (offset<0) {
        --i;    /* LeapYear is a macro */
        offset += 365 + LeapYear(i);
    }
    if (i==(solarFirstDate.y + Nyear)) {
//Error("Year out of range.");
      alert("Year out of range.");
      return ;
    }
    d.y = i;
    
    /* assert(offset<(365+LeapYear(i))); */
    for (m=1; m<=12; m++) {
        days = daysInSolarMonth[m];
        if ((m==2) && LeapYear(i))      /* leap February */
            days++;
        if (offset<days) {
            d.m = m;
            d.d = offset + 1;
            return;
        }
        offset -= days;
    }
}
/*----------------------------------------------------------*/
function Lunar2Solar()
{
    var offset;
    var adj;
    var d;

    /* A solar day begins at 12 a.m. */
    adj = (lunar.h == 23)? -1 : 0;
    offset = Lunar2Day(lunar);
//    alert("offset:"+offset);
    solar.w = (offset+ adj + solarFirstDate.w) % 7;
    Day2Solar(offset + adj, solar);
    solar.h = lunar.h;
    CalGZ(offset, lunar, gan, zhi);

    jieAlert = JieDate(solar, lunar2);
    lunar2.d = lunar.d;
    lunar2.h = lunar.h;
    CalGZ(offset, lunar2, gan2, zhi2);
}
/*----------------------------------------------------------*/
//type=0,default,陽->陰
//type=1,陰->陽
function Lunar(type,my_y,my_m,my_d) 
{
  if(type==0) {//陽->陰
    solar.y=my_y;
    solar.m=my_m;
    solar.d=my_d;
    title="陰曆:";
    solar2Lunar();
  }
  else {//陰->陽
    lunar.y=my_y;
    lunar.m=my_m;
    lunar.d=my_d;
    title="陽曆:";
    Lunar2Solar();
  }
}
