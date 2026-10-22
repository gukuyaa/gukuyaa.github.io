---
title: "STL库——map的用法"
date: 2026-07-28T10:25:40+08:00
draft: false
math: false
tags: ["洛谷", "学习·资料"]
categories: ["学习·资料"]
summary: "1.基本定义 map 是 C++ STL 中基于红黑树的有序键值对容器。在算法竞赛中，它主要用于建立下标非连续或类型特殊（如 string 映射到 int）的查…"
slug: "luogu-j0tjrw6h"
source: "https://www.luogu.com.cn/article/j0tjrw6h"
---
## 1.基本定义
map 是 C++ STL 中基于红黑树的有序键值对容器。在算法竞赛中，它主要用于建立下标非连续或类型特殊（如 string 映射到 int）的查找表。
```cpp
#include <bits/stdc++.h>
using namespace std;

map<int, string> mp1;          // 键是 int，值是 string
map<string, int> mp2;          // 键是 string，值是 int (最常用)
map<int, int> mp3;             // 离散化常用
map<pair<int,int>, int> mp4;   // 坐标映射到值
```

---


## 2. 插入数据（三种方式）
```cpp
map<string, int> mp;

// 方式一：数组下标赋值（最常用，但如果键不存在，会自动创建）
mp["apple"] = 5; 

// 方式二：insert 插入（如果键已存在，不会覆盖原值）
mp.insert({"banana", 3});      // C++11 初始化列表写法
mp.insert(make_pair("orange", 7)); // 传统写法

// 方式三：C++11 emplace（直接构造，效率高）
mp.emplace("grape", 9);
```
**区别记忆**：用 [] 会覆盖旧值；用 insert 或 emplace 在键已存在时不会覆盖，适合“有就保留，没有才插入”的场景。

---

## 3. 访问与查找

### **查找：正确且标准的姿势（用 find）**
```cpp
auto it = mp.find("apple");
if (it != mp.end()) {
    cout << "找到了，值为: " << it->second << endl;
} else {
    cout << "不存在" << endl;
}
```
find 返回迭代器，若没找到则返回 mp.end()。

**取值**：键用 it->first，值用 it->second。


### 危险操作：用 [] 判断是否存在（必看！）
```cpp
// ❌ 极其错误的做法！
if (mp["apple"] == 0) { ... }
```
**为什么错？** 因为 map 的 operator[] 具有自动插入特性：如果键 "apple" 不存在，这行代码会强行插入一个 {"apple", 0}，然后才返回这个 0。这会污染你的数据，导致遍历时多出一个垃圾元素。

---

## 4.删除元素
```cpp
// 1. 根据键删除（最常用，安全）
int n = mp.erase("apple"); // 删除成功返回 1，失败返回 0（不崩溃）

// 2. 根据迭代器删除（效率更高，适合已知位置）
auto it = mp.find("banana");
if (it != mp.end()) {
    mp.erase(it);
}

// 3. 清空全部
mp.clear();
```
**在循环中删除的正确写法**（防止迭代器失效）：
```cpp
for (auto it = mp.begin(); it != mp.end(); ) {
    if (it->second == 0) {          // 假设删除值为 0 的元素
        it = mp.erase(it);          // C++11 起 erase 返回下一个迭代器
    } else {
        it++;
    }
}
```

## 5. 遍历（三种写法）
map 默认按键的升序（字典序或数值顺序）遍历。
```cpp
// 写法一：传统迭代器（C++98 兼容）
for (map<string, int>::iterator it = mp.begin(); it != mp.end(); it++) {
    cout << it->first << " " << it->second << endl;
}

// 写法二：范围 for（C++11 起，竞赛最推荐，打字少）
for (auto &p : mp) {
    cout << p.first << " " << p.second << endl;
}

// 写法三：反向遍历（降序）
for (auto it = mp.rbegin(); it != mp.rend(); it++) {
    cout << it->first << " " << it->second << endl;
}
```
## 6.自定义排序（当默认升序不满足需求时）
```cpp
// 例子：按 key 降序排序（int 类型）
map<int, int, greater<int>> mp; 

// 例子：按结构体的某个字段排序
struct Person {
    string name;
    int age;
};
struct Cmp {
    bool operator()(const Person &a, const Person &b) const {
        return a.age < b.age; // 按年龄升序
    }
};
map<Person, int, Cmp> mp;
```
## 7.复杂度速查表
|  操作 |  时间复杂度 |
|:-:|:-:|
|  插入（insert / []） | O(logn)  |
|  删除（erase） | O(logn)  |
|  查找（find） | O(logn)  |
| 遍历（全表）  | O(n)  |

map适用于n的范围在1e6以下（不包括）
