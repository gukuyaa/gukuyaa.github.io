---
title: "背包问题"
date: 2026-08-10T23:19:12+08:00
draft: false
math: false
tags: ["洛谷", "学习·资料"]
categories: ["学习·资料"]
summary: "普通背包模板"
slug: "luogu-69mxbiah"
source: "https://www.luogu.com.cn/article/69mxbiah"
---
[普通背包模板](https://www.luogu.com.cn/problem/P1048)
```cpp
#include<bits/stdc++.h>
using namespace std;

const int N=1005;

int n,m;
int v[N],w[N],dp[N];

int main()
{
	cin>>m>>n;//背包容量物品数量 
	for(int i=1;i<=n;i++)
	{
		cin>>v[i]>>w[i];//体积和价值 
	}
	for(int i=1;i<=n;i++)
	{
		for(int j=m;j>=0;j--)
		{
			if(j>=v[i])
				dp[j]=max(dp[j],dp[j-v[i]]+w[i]);
		}
	}
	cout<<dp[m];
	return 0;
} 
```
