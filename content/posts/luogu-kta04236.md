---
title: "c++高频函数"
date: 2026-08-14T11:03:52+08:00
draft: false
math: false
tags: ["洛谷", "学习·资料"]
categories: ["学习·资料"]
summary: "一、浮点数取整与格式化输出 1. 格式化输出（保留小数点后 n 位） 2. 取整函数 floor(x) 向下取整（往小取） floor(3.9) = 3，flo…"
slug: "luogu-kta04236"
source: "https://www.luogu.com.cn/article/kta04236"
---
## 一、浮点数取整与格式化输出
### 1. 格式化输出（保留小数点后 n 位）
```cpp
#include <iomanip>
double x = 3.1415926;
cout << fixed << setprecision(2) << x; // 输出 3.14
// fixed 表示固定小数位数，不加 fixed 则输出有效数字位数
```
## 2. 取整函数

floor(x)	向下取整（往小取）	floor(3.9) = 3，floor(-3.1) = -4
ceil(x)	向上取整（往大取）	ceil(3.1) = 4，ceil(-3.9) = -3   
     round(x)	四舍五入	round(3.5) = 4，round(3.4) = 3     
trunc(x)	向零取整（截断小数）	trunc(3.9) = 3，trunc(-3.9) = -3

## 二、字符串常用操作
### 1. 取子串 substr
```cpp
string s = "Hello World";
string sub1 = s.substr(0, 5);      // "Hello"（从0开始取5个）
string sub2 = s.substr(6);         // "World"（从6取到末尾）
// ⚠️ 若 pos + len 超出长度，会抛异常，建议先判断 if (pos < s.size())
```
### 2. 查找子串 find
```cpp
string s = "Hello World";
int pos = s.find("World");         // 返回 6，没找到返回 string::npos（即 -1）
if (pos != string::npos) { ... }
```
### 3. 替换与删除
```cpp
s.replace(pos, len, "new");        // 从 pos 开始替换 len 个字符为 "new"
s.erase(pos, len);                 // 从 pos 开始删除 len 个字符
s.erase(pos);                      // 从 pos 删到末尾
```
### 4. 字符串 ↔ 字符数组
```cpp
string s = "abc";
const char* cstr = s.c_str();      // 转为 const char*（只读）
char buf[100];
strcpy(buf, s.c_str());            // 复制到 char 数组（需头文件 <cstring>）
```
## 三、类型转换（int / string / char 互转）
### 1. string → int / long long / double
```cpp
#include <string>
string s = "123";
int a = stoi(s);                   // string to int
long long b = stoll(s);            // string to long long
double c = stod(s);                // string to double
// ⚠️ 如果 s 不是纯数字，会抛异常；可用 try-catch 或先判断 s[0] 是否为数字
```
### 2. int / long long → string
```cpp
int a = 123;
string s = to_string(a);           // "123"
// ⚠️ 需要 C++11 支持（现在所有 OJ 都支持）
```
### 3. char ↔ int（ASCII 转换）
```cpp
char c = '5';
int digit = c - '0';               // 5（字符转数字）
char ch = digit + '0';             // '5'（数字转字符）
// ⚠️ 不能写成 (int)c，那样得到的是 ASCII 码 53
```
### 4.大小写转换
```cpp
tolower(c)	//转小写（返回转换后的字符）
toupper(c)	//转大写（返回转换后的字符）
```
