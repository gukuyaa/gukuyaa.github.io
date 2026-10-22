---
title: "倍增求lca"
date: 2024-08-25T21:28:58+08:00
draft: false
math: false
tags: ["洛谷", "算法·理论"]
categories: ["算法·理论"]
summary: "P3379 【模板】最近公共祖先（LCA） 链式前向星版本 邻接表版本 2026 9.5（军训时补）"
slug: "luogu-3fg1eqkd"
source: "https://www.luogu.com.cn/article/3fg1eqkd"
---
[P3379 【模板】最近公共祖先（LCA）](https://www.luogu.com.cn/problem/P3379)

### 链式前向星版本

```cpp
#include<bits/stdc++.h>
using namespace std;

const int N=5e5+5;

int n,m,s,cnt;
int depth[N],head[N],lg[N],fa[N][22];

struct node
{
	int next,to;
}edge[N<<1];

void add(int u,int v)
{
	edge[++cnt].next=head[u];
	edge[cnt].to=v;
	head[u]=cnt;
}

void dfs(int now,int fath)
{
	depth[now]=depth[fath]+1;
	fa[now][0]=fath;
	for(int i=1;i<=lg[depth[now]];i++)
		fa[now][i]=fa[fa[now][i-1]][i-1];
		//意思是now的2^i祖先等于now的2^(i-1)祖先的2^(i-1)祖先
        //2^i = 2^(i-1) + 2^(i-1)
	for(int i=head[now];i;i=edge[i].next)
		if(edge[i].to!=fath)
			dfs(edge[i].to,now);	
}

int lca(int x,int y)
{
	if(depth[x]<depth[y])
		swap(x,y);
	while(depth[x]>depth[y])
	{
		x=fa[x][lg[depth[x]-depth[y]]-1];	
	}	
	if(x==y) return x;
	for(int k=lg[depth[x]]-1;k>=0;k--)
	{
		if(fa[x][k]!=fa[y][k])
		{
			x=fa[x][k];
			y=fa[y][k];
		}
	}
	return fa[x][0];
}

int main()
{
	cin>>n>>m>>s;
	for(int i=1;i<=n-1;i++)
	{
		int u,v;
		cin>>u>>v;
		add(u,v);
		add(v,u);
	}
	for(int i=1;i<=n;i++)
		lg[i]=lg[i-1]+(1<<lg[i-1]==i);
		//先将1<<lg[i-1],再判断是不是==i; 
	dfs(s,0);
	for(int i=1;i<=m;i++)
	{
		int x,y;
		cin>>x>>y;
		cout<<lca(x,y)<<endl;
	}
	return 0;
}
```

### 邻接表版本
```cpp
#include<bits/stdc++.h>
using namespace std;

const int N=500005;
const int LOG=20;
int n,m,s;
int dep[N];
int fa[N][LOG];
vector<int>g[N];

void dfs(int u,int father)
{
	dep[u]=dep[father]+1;
	fa[u][0]=father;
	
	for(int i=1;i<LOG;i++)
		fa[u][i]=fa[fa[u][i-1]][i-1];
	
	for(int v:g[u])
		if(v!=father)
			dfs(v,u);
		
						
}

int lca(int u,int v)
{
	//将u当成默认深度大的点
	if(dep[u]<dep[v]) swap(u,v);
	
	//目标：把深的那个节点u往上提，直到它和v在同一层
	for(int i=LOG-1;i>=0;i--)
	{
		if(dep[fa[u][i]]>=dep[v])
			u=fa[u][i];
	}
	
	
	if(u==v) return u;
	for(int i=LOG-1;i>=0;i--)
	{
		if(fa[u][i]!=fa[v][i])
		{
			u=fa[u][i];
			v=fa[v][i];
		}
	}
	//保证循环结束后,u和v被卡在了 “LCA 的下一层”
	
	return fa[u][0];
	
}

int main()
{
	cin>>n>>m>>s;
	for(int i=1;i<=n-1;i++)
	{
		int u,v;
		cin>>u>>v;
		g[u].push_back(v);
		g[v].push_back(u);
	}
	
	dep[0]=0;
	dfs(s,0);
	
	for(int i=1;i<=m;i++)
	{
		int u,v;
		cin>>u>>v;
		cout<<lca(u,v)<<endl;
	}
	
	return 0;
}
```
2026 9.5（军训时补）
