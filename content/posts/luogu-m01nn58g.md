---
title: "并查集"
date: 2024-03-10T21:05:59+08:00
draft: false
math: false
tags: ["洛谷", "算法·理论"]
categories: ["算法·理论"]
summary: "第一篇 新增一道例题 考虑将每一个点新增一个他对应的虚点 1和n+1对应，x和x+n对应 如果两个点互相排斥，他们就在一个集合，此时连接（x，y）和（x+n，y…"
slug: "luogu-m01nn58g"
source: "https://www.luogu.com.cn/article/m01nn58g"
---
第一篇

```
/*




并查集
作用：以最小的代价让n个点连接在一起

2024 3 10 
*/

新增并查集基本模板（含路径压缩）

```
```
#include<bits/stdc++.h>
using namespace std;

const int N=10;
int n,m;
int fa[N];
int z,x,y;

int find(int x)
{
	if(x==fa[x]) return x;
	else return fa[x]=find(fa[x]);
}

int main()
{
	cin>>n>>m;
	for(int i=1;i<=n;i++)
		fa[i]=i;
	
	for(int i=1;i<=m;i++)
	{
		cin>>z>>x>>y;
		if(z==1)
		{
			if(find(x)!=find(y))
			{
				fa[find(x)]=find(y);
			}
		}
		else
		{
			if(find(x)==find(y))
				cout<<"Y"<<endl;
			else
				cout<<"N"<<endl;
		}
	}
	
	
	
	return 0;
}
```




```




 
#include<bits/stdc++.h>
using namespace std;

int n,m;
struct node
{
	int s,e,w;//start end weight 
}a[114514];
int pre[114514];

int cmp(node x,node y)
{
	return x.w<y.w;
}//对权值进行一个比较，返回小的 

int find(int x)
{
	if(x==pre[x])
		return x;
	else
		return pre[x]=find(pre[x]);//通过递归查找是不是同一个祖先 
}

int main()
{
	cin>>n>>m;
	//n个点，m条边 
	for(int i=1;i<=n;i++)
	{
		pre[i]=i;
		//初始化，让每个人当自己祖先 
	}
	for(int i=1;i<=m;i++)
	{
		cin>>a[i].s>>a[i].e>>a[i].w;
	}
	sort(a+1,a+m+1,cmp);
	//权值从小到大排 
	for(int i=1;i<=m;i++)
	{
		if(find(a[i].s)!=find(a[i].e))
		{
			pre[find(a[i].s)]=find(a[i].e);
			//如果祖先不同，就随便让一个当另一个儿子
			n--;
			//处理好2个人，总共要处理的就少了1个 
			if(n==1)
				break; 
			//出口 
		}
		
	}
	
	return 0;
}
```

[新增一道例题](https://www.luogu.com.cn/problem/P10734)

考虑将每一个点新增一个他对应的虚点

1和n+1对应，x和x+n对应

如果两个点互相排斥，他们就在一个集合，此时连接（x，y）和（x+n，y+n）

相反如果吸引，就连接（x，y+n）和（x+n，y）

查询时注意x，y，x+n，y+n在不在一个集合就行


```cpp
#include<bits/stdc++.h>
using namespace std;

const int N=1e5+4;

int n,q;
int fa[N<<1];

int find(int x)
{
	if(x==fa[x])
		return x;
	else return fa[x]=find(fa[x]);
}

void merage(int x,int y)
{
	fa[find(x)]=find(y);
}

void query(int x,int y)
{
	if(find(x)==find(y)||find(x+n)==find(y+n))
		cout<<"R"<<endl;
	else if(find(x)==find(x+n)||find(x+n)==find(y))
		cout<<"A"<<endl;
	else
		cout<<"?"<<endl;
}

int main()
{
	cin>>n>>q;
	for(int i=1;i<=2*n;i++)
		fa[i]=i;
	for(int i=1;i<=q;i++)
	{
		char ch;
		int x,y;
		cin>>ch>>x>>y;
		if(ch=='A') merage(x,n+y),merage(y,n+x);
		else if(ch=='R') merage(x,y),merage(x+n,y+n);
		else query(x,y);
	}
	
	
	return 0;
}
```
