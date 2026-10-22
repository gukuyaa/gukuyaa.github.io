---
title: "floyed求最短路以及路径记录"
date: 2024-03-26T21:03:03+08:00
draft: false
math: false
tags: ["洛谷", "算法·理论"]
categories: ["算法·理论"]
summary: "2024 3 26"
slug: "luogu-e91elh9u"
source: "https://www.luogu.com.cn/article/e91elh9u"
---
```c
//luogu p3906

#include<bits/stdc++.h>
using namespace std;

priority_queue <int,vector<int>,greater<int> > q;
//进行升序排列，小的数据在队首

//priority_queue <int,vector<int>,less<int> >q; 
//进行降序排列，大的数据在队首

/*
和队列基本操作相同:

q.top() 访问队头元素  ()不加参数 
q.empty() 队列是否为空  ()不加参数
q.size() 返回队列内元素个数  ()不加参数 
q.push(k) 把k插入元素到队尾 (并排序)  ()里加要插入的 
emplace 原地构造一个元素并插入队列  没用过 
q.pop() 弹出队头元素  ()不加参数
swap 交换内容  没用过 

*/

int n,m;
int f[100][100];
//记录最短路径的地图 

int main()
{
	cin>>n>>m;
	int a,b;
	for(int i=1;i<=n;i++)
	{
		for(int j=1;j<=n;j++)
		{
			if(i!=j)//除了自己到自己这条路 
			f[i][j]=0x3f3f3f3f;//其他先设置成最长 
		}
	}
	for(int i=1;i<=m;i++)
	{
		cin>>a>>b;
		f[a][b]=1;
		f[b][a]=1;
		//注意是不是无向图 
	}
	
	//floyd算法，三重循环 
	for(int k=1;k<=n;k++)
	{
		for(int i=1;i<=n;i++)
		{
			for(int j=1;j<=n;j++)
			{
				f[j][i]=f[i][j]=min(f[i][j],f[i][k]+f[k][j]);
			}
		}
	}
	int k;
	cin>>k;
	for(int i=1;i<=k;i++)
	{
		cin>>a>>b;
		//q.push(a),q.push(b);
		for(int k=1;k<=n;k++)
		{
			if(k!=a||k!=b)
			{
				if(f[a][k]+f[k][b]==f[a][b])
				{
					q.push(k);
					//说明k可以作为从a到b中间的一个过渡
					//让k入队列，排序交给优先队列 
				}
			}
		}
		//cout<<endl<<q.size()<<endl;
		//emm,长度为1时好像还可以拿来求最短路长度？ 
		while(!q.empty())//非空 
		{
			cout<<q.top()<<" ";//输出队首 
			q.pop();//出列 
		}
		cout<<endl;
	}
	return 0;
}
```
2024 3 26
