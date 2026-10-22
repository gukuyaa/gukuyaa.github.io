---
title: "欧拉路径与欧拉回路"
date: 2024-08-25T10:48:48+08:00
draft: false
math: false
tags: ["洛谷", "算法·理论"]
categories: ["算法·理论"]
summary: "前置芝士： 1. 欧拉路径定义： 图中经过所有边恰好一次的路径叫欧拉路径（也就是一笔画）。如果此路径的起点和终点相同，则称其为一条欧拉回路。 2. 欧拉路径判定…"
slug: "luogu-1zlvcnwr"
source: "https://www.luogu.com.cn/article/1zlvcnwr"
---
# 前置芝士：
### 1. 欧拉路径定义：

图中经过所有边恰好一次的路径叫欧拉路径（也就是一笔画）。如果此路径的起点和终点相同，则称其为一条欧拉回路。


---



### 2. 欧拉路径判定（是否存在）：

有向图欧拉路径：图中恰好存在 1 个点出度比入度多 1（这个点即为 起点 S），1 个点入度比出度多 1（这个点即为 终点 T），其余节点出度=入度。

有向图欧拉回路：所有点的入度=出度（起点 S 和终点 T 可以为任意点）。

无向图欧拉路径：图中恰好存在 2 个点的度数是奇数，其余节点的度数为偶数，这两个度数为奇数的点即为欧拉路径的 起点 S 和 终点 T。

无向图欧拉回路：所有点的度数都是偶数（起点 S 和终点 T 可以为任意点）。


---


注：存在欧拉回路（即满足存在欧拉回路的条件），也一定存在欧拉路径。

当然，一副图有欧拉路径，还必须满足将它的有向边视为无向边后它是连通的（不考虑度为 0 的孤立点），连通性的判断我们可以使用并查集或 dfs 等。


---

### 3.求有向图的欧拉路径模版
[P7771 【模板】欧拉路径](https://www.luogu.com.cn/problem/P7771)

```cpp
#include<bits/stdc++.h>
using namespace std;

const int MAX=100010;
int n,m,u,v,del[MAX];
int du[MAX][2];
stack <int> st;//存储欧拉路径 
vector <int> G[MAX];//存储从u到v的边 

void dfs(int now)
{
	for(int i=del[now];i<G[now].size();i=del[now])
	{
		del[now]=i+1;
		dfs(G[now][i]);
	}
	st.push(now);
}
//其中 del[now]表示 
//G[now][1,2……,del[now]-1] 都已经被标记访问过
//下一次要从G[now][del[now]]开始访问。

int main()
{
	cin>>n>>m;
	for(int i=1;i<=m;i++)
	{
		cin>>u>>v;
		G[u].push_back(v);
		du[u][1]++;//出度 
		du[v][0]++;//入度 
	}
	
	for(int i=1;i<=n;i++)
		sort(G[i].begin(),G[i].end());
	//分别对G[1],G[2]...进行升序排序 
	int s=1,cnt[2]={0,0};
	bool flag=1;//flag=1表示所有点入度等于出度 
	
	for(int i=1;i<=n;i++)//寻找起点来dfs 
	{
		if(du[i][1]!=du[i][0])
		{
			flag=0;
			if(du[i][1]-du[i][0]==1)
			//出度比入度大1,那么i是起点 
			{
				cnt[1]++;
				s=i;
			}
			else if(du[i][0]-du[i][1]==1)
				cnt[0]++;
			else
			{
				
				cout<<"No"<<endl;
				return 0;	
			} 
		}
		
	}
	if((!flag)&&!(cnt[0]==cnt[1]&&cnt[0]==1)) return !puts("No"),0;
	dfs(s);//从起点开始搜 
	while(!st.empty())
	{
		cout<<st.top()<<" ";
		st.pop();
	}
	return 0;
}
```
