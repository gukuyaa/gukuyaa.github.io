---
title: "二分查找"
date: 2024-05-30T17:30:23+08:00
draft: false
math: false
tags: ["洛谷", "算法·理论"]
categories: ["算法·理论"]
summary: "二分查找与二分答案"
slug: "luogu-b95hvrd2"
source: "https://www.luogu.com.cn/article/b95hvrd2"
---
[二分查找与二分答案](https://www.luogu.com.cn/problem/P3853)

```
//p3853


/*
此题为二分求最优解的模板

对于任意一个给出的“空旷指数”G，我们应该怎样去判断它是否符合题目的意思呢？

我们可以想象，我们已知了这条路上的所有的路标，
我们从头开始枚举两两相邻的路标的间距，如果大于G,那么已经不符合G为最大距离的条件了，
为了使G满足,我们就可以在前一个路标前面G米处加一个路标，这样与前面一个就符合条件了，
再判断新设的路标和后面的路标是否距离小于G,如果不，继续重复操作设置新路标

当新设的路标数已经超过题目所给最大增设值时，
如果还有路标不满足G,但已经不能设置新路标了，所以该G值就不满足条件。相反，则G成立。

注意到，如果一个“空旷指数”成立，那么可能存在比它更小的解，
但如果一个“空旷指数”不成立，那么答案只能比该值更大
*/

#include<bits/stdc++.h>
using namespace std;

int L,n,k,l,r,ans=0x3f3f3f3f;
int a[114514];

bool check(int m)
{
	int kk=k,size=0;
	//size记录当前两个路标之间的距离 
	
	for(int i=1;i<=n;i++)
	{
		if(kk<0) return 0;
		if(a[i]-size<=m)
		{
			size=a[i];
			//核心，不断变化size的值来判断目前两个路标间的距离 
		}
		else
		{
			size+=m;
			kk--;
			i--;/*如果两个路标间的距离大于多个m,
			不能直接判断下两个，要在当前继续判断 */
		}
	}
	if(kk>=0)
	{
		return 1;
	}
}

int main()
{
	cin>>L>>n>>k;
	for(int i=1;i<=n;i++)
	{
		cin>>a[i];
	}
	int l=0,r=L;
	while(l<=r)
	{
		int mid=(l+r)/2;
		if(check(mid))
		{
			r=mid-1;
			ans=min(mid,ans);
		}
		else
		{
			l=mid+1;
		}
	}
	cout<<ans<<endl;
	return 0;
}
```
