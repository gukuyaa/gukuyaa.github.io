---
title: "线段树"
date: 2024-04-11T17:07:44+08:00
draft: false
math: false
tags: ["洛谷", "算法·理论"]
categories: ["算法·理论"]
summary: "2024 4 11"
slug: "luogu-0sxhy4md"
source: "https://www.luogu.com.cn/article/0sxhy4md"
---
```
//p3372

#include<bits/stdc++.h>
using namespace std;


long long a[11451400],tree[11045140],laz[11451400];
//laz和tree都是模拟二叉树的结构 
long long n,m,f;


void build(long long p,long long l,long long r)
{
	if(l==r)//如果是叶子结点 
	{
		tree[p]=a[l];//直接给到tree 
		return;
	}
	long long mid=(l+r)/2;
	build(p*2,l,mid);
	build(p*2+1,mid+1,r);
	
	tree[p]=tree[p*2]+tree[p*2+1];
}/*建树 
p代表在tree数组中的当前位置，
初始时从根节点开始查询，
因此刚开始传入1 
*/ 

void pushdown(long long p,long long l,long long r)
{
	long long mid=(l+r)>>1;
	
	laz[p*2]+=laz[p];
	laz[p*2+1]+=laz[p];//让该点的懒标记下传 
	
	tree[p*2]+=(mid-l+1)*laz[p];
	tree[p*2+1]+=(r-mid)*laz[p];//通过懒标记修改儿子的值 
	
	laz[p]=0;//下传后该点的懒标记已经使用，故清0 
}/*
向下传递 
*/


long long query(long long p,long long l,long long r,long long x,long long y)
{
	long long mid=(l+r)/2;
	if(x<=l&&r<=y)//如果当前的范围（l,r）是要求范围(x,y)的子集 
	{
		return tree[p];//直接整段加上 
	}
	
	pushdown(p,l,r);//进函数，先下移 
	
	long long ans=0;
	if(x<=mid) ans+=query(p*2,l,mid,x,y);
	if(y>mid) ans+=query(p*2+1,mid+1,r,x,y);
	return ans;
}/*区间查询
l,r代表的是当前的数据范围，一开始传入（1，n）（局部） 
x,y代表要查询的区间的左右端点（整体,即题目要求修改的） 
*/
void update(long long p,long long l,long long r,long long x,long long y,long long val)
{
	if(x<=l&&r<=y)//在范围内 
	{
		tree[p]+=(r-l+1)*val;//当前结点要变化的大小，就是它的子孙数量和*val 
		laz[p]+=val;//当单独查询子孙时，通过laz数组给子孙赋值 
		return; 
	}
	
	pushdown(p,l,r);//进函数，先下移 
	
	long long mid=(l+r)/2;
	if(x<=mid) update(p*2,l,mid,x,y,val);
	if(y>mid) update(p*2+1,mid+1,r,x,y,val);
	tree[p]=tree[p*2]+tree[p*2+1];
}/*
对于一棵完全二叉树而言
p节点的左右儿子结点分别是p*2和p*2+1; 
*/ 

int main()
{
	cin>>n>>m;
	for(long long i=1;i<=n;i++)
		cin>>a[i];
	build(1,1,n);//建树 
	long long x,y,k;
	for(long long i=1;i<=m;i++)
	{
		cin>>f;
		if(f==1)
		{
			cin>>x>>y>>k;
			update(1,1,n,x,y,k);
		}
		else
		{
			cin>>x>>y;
			cout<<query(1,1,n,x,y)<<endl;;
		}
	}
	
	return 0;
} 
```
2024 4 11
