---
title: "实现__int128的快读和快输"
date: 2026-08-10T23:28:58+08:00
draft: false
math: false
tags: ["洛谷", "学习·资料"]
categories: ["学习·资料"]
summary: ""
slug: "luogu-tf1vmcu4"
source: "https://www.luogu.com.cn/article/tf1vmcu4"
---
```cpp
#include <bits/stdc++.h>
using namespace std;

// 快读（支持负数）
inline __int128 read() {
    char c = getchar();
    __int128 x = 0, f = 1;
    while (c < '0' || c > '9') { // 跳过空白字符和负号判断
        if (c == '-') f = -1;
        c = getchar();
    }
    while (c >= '0' && c <= '9') {
        x = x * 10 + (c - '0');
        c = getchar();
    }
    return x * f;
}

// 快输（支持负数）
inline void write(__int128 x) {
    if (x < 0) {
        putchar('-');
        x = -x;
    }
    if (x > 9) write(x / 10);  // 递归到最高位
    putchar(x % 10 + '0');
}

int main() {
    __int128 a = read();
    __int128 b = read();
    write(a + b);
    return 0;
}
```
