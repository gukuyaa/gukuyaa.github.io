---
title: "二分汇总（手写+stl库）"
date: 2026-07-23T23:22:29+08:00
draft: false
math: false
tags: ["洛谷", "学习·资料"]
categories: ["学习·资料"]
summary: "一.手写二分 统一格式 ：区间采用 左闭右开 [l, r)，这是 STL 的习惯 1.查找是否存在某个值（标准find） 2.手写lower bound（找第一…"
slug: "luogu-fyl3vbwh"
source: "https://www.luogu.com.cn/article/fyl3vbwh"
---
# 一.手写二分
**统一格式**：区间采用 左闭右开 [l, r)，这是 STL 的习惯

## 1.查找是否存在某个值（标准find）
```cpp
bool find(int a[], int n, int x) {
    int l = 0, r = n;
    while (l < r) {
        int mid = (l + r) >> 1;
        if (a[mid] == x) return true;
        else if (a[mid] < x) l = mid + 1;
        else r = mid;
    }
    return false;
}
```

## 2.手写lower_bound（找第一个 >= x 的下标）

```cpp
int lower_bound(int a[], int n, int x) {
    int l = 0, r = n;
    while (l < r) {
        int mid = (l + r) >> 1;
        if (a[mid] >= x) r = mid;
        else l = mid + 1;
    }
    return l;
}
```
## 3.手写 upper_bound（找第一个 > x 的下标）

```cpp
int upper_bound(int a[], int n, int x) {
    int l = 0, r = n;
    while (l < r) {
        int mid = (l + r) >> 1;
        if (a[mid] > x) r = mid;
        else l = mid + 1;
    }
    return l;
}
```
# 二.针对数组的 STL 使用方法
```cpp
int a[100005], n, x;

// 1. 判断是否存在
if (binary_search(a, a + n, x)) { ... }

// 2. 找第一个 >= x 的下标
int pos1 = lower_bound(a, a + n, x) - a;

// 3. 找第一个 > x 的下标
int pos2 = upper_bound(a, a + n, x) - a;

// 统计 x 出现的个数
int cnt = upper_bound(a, a + n, x) - lower_bound(a, a + n, x);
```
