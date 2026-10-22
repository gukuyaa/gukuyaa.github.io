---
title: "tarjan"
date: 2024-08-26T21:12:59+08:00
draft: false
math: false
tags: ["洛谷", "算法·理论"]
categories: ["算法·理论"]
summary: "《自己写哪有抄作业来得爽》 强连通分量及缩点tarjan算法解析 P3387 【模板】缩点"
slug: "luogu-q5qk1mha"
source: "https://www.luogu.com.cn/article/q5qk1mha"
---
## 《自己写哪有抄作业来得爽》
[强连通分量及缩点tarjan算法解析](https://blog.csdn.net/acmmmm/article/details/16361033)

[P3387 【模板】缩点](https://www.luogu.com.cn/problem/P3387)



```cpp
#include<bits/stdc++.h>
using namespace std;
#define maxn 100001
#define maxm 500001

struct node{
    int to,next,from;
}edge[maxm];

queue <int> q;
vector <int> cb[maxn];
vector <int> rdr[maxn];
int ans[maxn],totq,x,y,v,rd[maxn],u,n,m,sum,vis[maxn],dis_[maxn],dis[maxn];
int dfn[maxn],low[maxn],f[maxn],times,cntqq;
int stack_[maxn],heads[maxm],visit[maxn],cnt,tot,index_;
void add(int x,int y)		//建边
{
    edge[++cntqq].next=heads[x];
    edge[cntqq].from=x;
    edge[cntqq].to=y;
    heads[x]=cntqq;
   	return;
}

void tuopu()
{
	for(int i=1;i<=tot;i++)
	{
		if(rd[i]==0)
		q.push(i);
	}
	while(!q.empty())
	{
		int u=q.front();
		q.pop();
		ans[++totq]=u;
		for(int i=0;i<cb[u].size();i++)
		{
			v=cb[u][i];
			rd[v]--;
			if(rd[v]==0) q.push(v);
		}
	}
}

void tarjan(int x)
{
	dfn[x]=low[x]=++times;
	/*
	DFS时我们维护两个数组dfn,low
	dfn[i]是i点的进入时间
	low[i]是从i点出发，所能访问到的最早的进入时间
	*/
	stack_[++index_]=x;//手写栈 
	visit[x]=1;//标记访问过
	for(int i=heads[x];i!=-1;i=edge[i].next) 
	{
		if(!dfn[edge[i].to])
		//没有访问过edge[i].to 
		{
			tarjan(edge[i].to);
			low[x]=min(low[x],low[edge[i].to]);
		}
		else
		{
			if(visit[edge[i].to])
				low[x]=min(low[x],dfn[edge[i].to]);	
		}
	}
	if(low[x]==dfn[x])
	//从外围进入的第一个点 
	{
		tot++;//强连通分量编号 
		while(1)
		{
			vis[stack_[index_]]=tot;//stack_[index[]]即存储点x1,x2,...;vis[x1,x2,...]表示这些x1,x2属于一个环，环编号为tot; 
			dis_[tot]+=dis[stack_[index_]];//强连通分量权值累加 
			visit[stack_[index_]]=0;//缩点后,该点可能同时在多个环里 
			index_--;//遍历整个栈 
			if(x==stack_[index_+1]) break;
		}
	}
}

int main()
{
	memset(heads,-1,sizeof(heads));
	cin>>n>>m;
	for(int i=1;i<=n;i++)
		cin>>dis[i];//dis[i]记录每个点的权值 
	for(int i=1;i<=m;i++)
	{
		cin>>x>>y;
		add(x,y);//x指向y的有向边 
	}
	for(int i=1;i<=n;i++)
		if(!dfn[i])
			tarjan(i);
	
	for(int i=1;i<=cntqq;i++)
	{
		if(vis[edge[i].from]!=vis[edge[i].to])
		//两者不在一个强联通分量(环) 
		{
			x=vis[edge[i].from];
			y=vis[edge[i].to];
			rd[y]++;
			cb[x].push_back(y);
			rdr[y].push_back(x);
		}
	}
	tuopu();
	for(int i=1;i<=tot;i++)
	{
		int w=ans[i];
		f[w]=dis_[w];
		for(int j=0;j<rdr[w].size();j++)
			f[w]=max(f[w],f[rdr[w][j]]+dis_[w]);
	}
	for(int i=1;i<=tot;i++)
		sum=max(sum,f[i]);
	cout<<sum<<endl;
	return 0;
}
```
