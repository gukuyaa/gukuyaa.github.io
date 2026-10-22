---
title: "离散化（包含处理逆序对）"
date: 2024-03-23T16:59:58+08:00
draft: false
math: false
tags: ["洛谷", "算法·理论"]
categories: ["算法·理论"]
summary: "2024 3 23 2024 3 31 2024 7 10新添逆序对个数求解方法"
slug: "luogu-9s8yq0aj"
source: "https://www.luogu.com.cn/article/9s8yq0aj"
---
```c
//P1966 [NOIP2013 提高组] 火柴排队
#include<bits/stdc++.h>
using namespace std;

int n,mod=99999997;
int l[114514],tree[114514];

int lowbit(int x)
{
	return x&-x;
}

void add(int x,int k)
{
	for(int i=x;i<=n;i+=lowbit(i))
		tree[i]+=k;
}

int query(int x)
{
	int ans=0;
	for(int i=x;i;i-=lowbit(i))
		ans+=tree[i];
	return ans;
}

struct node1
{
	int val,num;
}a[114514],b[114514];


bool cmp(node1 x,node1 y)
{
	if(x.val==y.val)
		return x.num<y.num;
	return x.val<y.val;
}


int main()
{
	cin>>n;
	for(int i=1;i<=n;i++)
	{
		cin>>a[i].val;
		a[i].num=i;
	}
	for(int i=1;i<=n;i++)
	{
		cin>>b[i].val;
		b[i].num=i;
	}
	sort(a+1,a+n+1,cmp);
	sort(b+1,b+n+1,cmp);
	
	
	for(int i=1;i<=n;i++)
	{
		l[a[i].num]=b[i].num;
		//a中第i个数的val等于b中第l[i]个数的num
		//A中i这个位置的数在B中的位置。 
	}
	
	int cnt=0;
	for(int i=n;i>=1;i--)
	{
		cnt=(cnt+query(l[i]-1))%mod;
		add(l[i],1);
	}
	cout<<cnt<<endl;
	return 0;
}
```
```
//离散化 (数据量超出空间大小时使用)
#include<bits/stdc++.h>
using namespace std;

long long n; //十年oi一场梦，不开ll见祖宗 
struct node
{
	int val,pos;//pos记录原来的位置 
}a[11450014];
int ranks[11450014];
int tree[11451004];

bool cmp(node a,node b)
{
	if(a.val==b.val)
		return a.pos<b.pos;
		//如果两数相同，先返回位置靠前的 
	return a.val<b.val;
}//从小到大排序 

int lowbit(int x)
{
	return x&-x;
}

long long query(long long k)
{
	long long ans=0;
	while(k)
	{
		ans+=tree[k];
		k-=lowbit(k);
	}
	return ans;
}

void update(long long x,long long k)
{
	while(x<=n)
	{
		tree[x]+=k;
		x+=lowbit(x);
	}
}

int main()
{
	cin>>n;
	for(long long i=1;i<=n;i++)
	{
		cin>>a[i].val;
		a[i].pos=i;//记录位置，方便后面离散化 
	}
	sort(a+1,a+n+1,cmp);
	for(long long i=1;i<=n;i++)
	{
		ranks[a[i].pos]=i;
	}//原来位置上的val，从小到大
	/*for(int i=1;i<=n;i++)
		cout<<ranks[i]<<endl;
		*/
	long long ans=0;
	for(long long i=1;i<=n;i++)
	{
		update(ranks[i],1);//从0标记成1 
		ans+=(i-query(ranks[i]));
	}
    
        //另一种写法
   	for(int i=n;i>=1;i--)
	{
		ans+=query(ranks[i]-1);
		update(ranks[i],1);
	}
   
	cout<<ans<<endl;
	return 0;
}
```
2024 3 23

2024 3 31

2024 7 10新添逆序对个数求解方法
