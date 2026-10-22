---
title: "dijkstra求最短路"
date: 2024-07-16T16:03:38+08:00
draft: false
math: false
tags: ["洛谷", "算法·理论"]
categories: ["算法·理论"]
summary: "P3371 【模板】单源最短路径（弱化版） 2026 8.11补充更加简便的模板"
slug: "luogu-k02ybw5w"
source: "https://www.luogu.com.cn/article/k02ybw5w"
---
[P3371 【模板】单源最短路径（弱化版）](https://www.luogu.com.cn/problem/P3371)
```
#include<bits/stdc++.h>
using namespace std;

#define inf 0x3f3f3f3f

int n,m,s,cnt,u,v,w;

struct node
{
	int next,to,val;
}edge[200005];
int head[100005],vis[100005],ans[100005];

void addedge(int u,int v,int w)
{
	edge[++cnt].next=head[u];
	edge[cnt].to=v;
	edge[cnt].val=w;
	head[u]=cnt;
}

struct priority
{
	int ans;
	int id;
	bool operator<(const priority &x)const{
		return x.ans<ans;
	}
};//记得加";" 

priority_queue<priority> q;//优先队列 

int main()
{
	cin>>n>>m>>s;
	for(int i=1;i<=m;i++)
	{
		cin>>u>>v>>w;
		addedge(u,v,w);//建图 
	}
	
	for(int i=1;i<=n;i++)
		ans[i]=inf;//初始为最大 
	ans[s]=0;//起始点距离为0 
	
	q.push((priority){0,s});//起始点s距离为0 
	
	while(!q.empty())
	{
		priority temp=q.top();
		q.pop();
		
		int u=temp.id;//取出当前处理点
		
		if(vis[u]) 
			continue;//处理过就跳 
		
		vis[u]=1;//标记入过栈
		 
		for(int i=head[u];i;i=edge[i].next)
		{
			v=edge[i].to;//指向的点 
			if(ans[u]+edge[i].val<ans[v])
			//先到点u再加上i的长度<直接到v 
			{
				ans[v]=ans[u]+edge[i].val;//更新
				
				q.push((priority){ans[v],v});
				//此时已得出到v的最小距离，从v出发往下找 
				
			}
			
		}
	}
	for(int i=1;i<=n;i++)
		cout<<ans[i]<<" ";
	
	return 0;
}
```


**2026 8.11补充更加简便的模板**
```cpp
#include<bits/stdc++.h>
using namespace std;

int n,m,s;
vector<pair<int,int>>g[10];// {目标点, 边权}
int dist[10];

void dijkstra(int s)
{
	memset(dist,0x3f3f3f3f,sizeof(dist));
	dist[s]=0;
	
	//小根堆：pair 默认先按 first（距离）排序，用 greater 实现小根堆
	priority_queue<pair<int,int>,vector<pair<int,int>>,greater<pair<int,int>>>pq;
	pq.push({0,s});//和上面的pair不是同一个;{距离, 节点}(为了排顺序)
	
	while(!pq.empty())
	{
		auto [d,u]=pq.top();
		pq.pop();
		
		if(d>dist[u]) continue;// ★ 关键剪枝：丢弃过时的旧数据
		
		for(auto &[v,w]:g[u])
		{
			if(dist[v]>dist[u]+w)
			{
				dist[v]=dist[u]+w;
				pq.push({dist[v],v});
			}
				
		}
	}
	
}

int main()
{
	cin>>n>>m>>s;
	for(int i=1;i<=m;i++)
	{
		int u,v,w;
		cin>>u>>v>>w;
		g[u].push_back({v,w});
	}
	
	dijkstra(s);
	
	for(int i=1;i<=n;i++)
	{
		if(dist[i]==0x3f3f3f3f) cout<<"2147483647 ";
		else cout<<dist[i]<<" ";
	}
	return 0;
}
```
