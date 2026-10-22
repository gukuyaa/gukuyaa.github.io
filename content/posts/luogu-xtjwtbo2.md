---
title: "STL库——set的用法"
date: 2026-07-28T13:39:03+08:00
draft: false
math: false
tags: ["洛谷", "学习·资料"]
categories: ["学习·资料"]
summary: "1.基本定义 底层原理 ：和 map 一样是红黑树，插入后自动按键升序排列，且元素唯一（自动去重）。 2. 核心增删查操作 3.lower bound 和 up…"
slug: "luogu-xtjwtbo2"
source: "https://www.luogu.com.cn/article/xtjwtbo2"
---
## 1.基本定义
**底层原理**：和 map 一样是红黑树，插入后自动按键升序排列，且元素唯一（自动去重）。

```cpp
#include <bits/stdc++.h>
using namespace std;

set<int> s1;                // 存整数
set<string> s2;             // 存字符串（按字典序排列）
set<pair<int,int>> s3;      // 存坐标对（先比 first，再比 second）
```
---


## 2. 核心增删查操作
```cpp
set<int> st;

// 1. 插入（自动去重，如果已存在则忽略）
st.insert(5);
st.insert(3);
st.insert(5); // 第二次插入无效，size 仍是 2

// 2. 查找（【唯一正确】判断存在）
auto it = st.find(3);
if (it != st.end()) {
    cout << "找到了，值为: " << *it << endl; // 注意取值直接解引用，不像 map 要 .first
} else {
    cout << "不存在" << endl;
}

// 3. 查找的简写（只想知道有没有）
if (st.count(3)) { // count 对于 set 只返回 0 或 1
    cout << "存在" << endl;
}

// 4. 删除（两种方式）
int n = st.erase(3);   // 方式1：直接删值，成功返回1，失败返回0（安全）
auto it2 = st.find(5);
if (it2 != st.end()) {
    st.erase(it2);     // 方式2：删迭代器（效率更高）
}

// 5. 清空
st.clear();
```
## 3.lower_bound 和 upper_bound在set中的应用

```cpp
set<int> st = {1, 3, 5, 7, 9};

// 1. 找第一个 >= x 的元素
auto it1 = st.lower_bound(5); // 指向 5
auto it2 = st.lower_bound(6); // 指向 7（因为 6 不存在，找第一个比 6 大的）

// 2. 找第一个 > x 的元素
auto it3 = st.upper_bound(5); // 指向 7
auto it4 = st.upper_bound(9); // 指向 end()（因为 9 是最大的）

// 3. 实战：打印所有在 [L, R] 区间内的元素
int L = 3, R = 7;
auto itL = st.lower_bound(L);
auto itR = st.upper_bound(R); // 注意上界用 upper_bound，取到 R 的后一位
for (auto it = itL; it != itR; ++it) {
    cout << *it << " "; // 输出 3, 5, 7
}
```
请务必写 st.lower_bound(x)，而不要写lower_bound(st.begin(), st.end(), x)。

st.lower_bound(x) 利用了红黑树结构，复杂度是 
O(logn)。

std::lower_bound 是全局函数，只能顺序遍历，复杂度是 
O(n)，用在 set 上会直接导致超时（TLE）。

## 4.遍历
set 默认升序（从小到大）。如果想降序，使用反向迭代器或自定义排序。
```cpp
set<int> st = {1, 2, 3};

// 正向遍历（升序）：1 2 3
for (auto &x : st) {
    cout << x << " ";
}

// 反向遍历（降序）：3 2 1
for (auto it = st.rbegin(); it != st.rend(); ++it) {
    cout << *it << " ";
}
```
