/**
 *	conio.h
 *	Author: Jakash3 QAIU
 */

// Update.2021-11-01 兼容Cygwin 修改getch实现方式
// Update.2021-11-03 添加windows下MinGW-GCC编译支持
// Update.2023-03-15 修改getch和kbhit的实现
// Update.2025-07-28 添加MACOS下__llvm__宏定义

#ifndef CONIO_H
#define CONIO_H

#if defined (__unix__) || defined(__llvm__)
#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>

//读取单字符 https://my.oschina.net/yougui/blog/111345
static char getch() 
{
    struct termios oldt, newt;
    tcgetattr(STDIN_FILENO, &oldt);
    memcpy(&newt, &oldt, sizeof(newt));
    newt.c_lflag &= ~(ICANON | ECHO | ECHOE | ECHOK | ECHONL | ECHOKE | ICRNL);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    char c=getchar();
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    return c;
}

//判断输入 https://www.cnblogs.com/xiayong123/archive/2011/07/19/3717262.html
static int kbhit(void)
{
    struct termios oldt, newt;
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    int oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);
    int ch = getchar();
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    fcntl(STDIN_FILENO, F_SETFL, oldf);
    return (ch != EOF)? ungetc(ch, stdin),1:0;
}

static void gotoxy(int x, int y) { printf("\033[%d;%df", y, x); }

static void _gotoxy(int x,int y) {gotoxy(x,y);}
	 
static void clrscr() { printf("\033[2J\033[0;0f"); }

static void _clrscr() {clrscr();}

static int _getch() {return getch();}

static int _kbhit() {return kbhit();}

#elif defined (__WIN32__) || defined (__GNUC__) || defined (_MSC_VER) // __unix__
#include <windows.h>
#include <conio.h>
#include <stdio.h>

static void clrscr() {system("cls");}

static void _clrscr() {clrscr();}

static void gotoxy(int x, int y) {
  COORD c;
  c.X = x;
  c.Y = y;
  SetConsoleCursorPosition (GetStdHandle(STD_OUTPUT_HANDLE), c);
}
static void _gotoxy(int x,int y) {gotoxy(x,y);}
#endif // __WIN32__

#endif // CONIO_H
