---
title: "线段树+树链剖分"
date: 2024-07-12T08:31:47+08:00
draft: false
math: false
tags: ["洛谷", "文化·漫谈"]
categories: ["文化·漫谈"]
summary: "p3258 头文件和初始 线段树部分 树链剖分 dfs1（找到树的重链并记录重要量） dfs2（按照优先走重边的原则走出一个dfs序，x在dfs序中的位置记为i…"
slug: "luogu-j7z1utdk"
source: "https://www.luogu.com.cn/article/j7z1utdk"
---
p3258
# 头文件和初始
```
#include<bits/stdc++.h>
using namespace std;

const long long maxn=1200100;

int a[maxn],tree[maxn],tag[maxn],n,m,mode,x,y,z,S,cnt;
int large[maxn],seg[maxn],father[maxn],vis[maxn],dep[maxn],son[maxn],rev[maxn],top[maxn];
int Next[maxn],head[maxn],from[maxn],to[maxn],id[maxn],tot;
```


------------

# 线段树部分
```
void pushdown(int p,int l,int r)
{
	if(tag[p])
	{
		int m=(l+r)/2;
		tree[p*2]+=tag[p]*(m-l+1);
		tree[p*2+1]+=tag[p]*(r-m);
		tag[p*2]+=tag[p];
		tag[p*2+1]+=tag[p];
		tag[p]=0;
	}
}

int query(int p,int l,int r,int x,int y)
{
	if(x<=l&&y>=r)
		return tree[p];
	else
	{
		int m=(l+r)/2,res=0;
		pushdown(p,l,r);
		if(x<=m)
			res+=query(p*2,l,m,x,y);
		if(y>m)
			res+=query(p*2+1,m+1,r,x,y);
		return res;
	}
}

void update(int p,int l,int r,int x,int y,int val)
{
	if(x<=l&&r<=y)
	{
		tree[p]+=val*(r-l+1);
		tag[p]+=val;
	}
	else
	{
		
		int m=(l+r)/2;
		pushdown(p,l,r);
		if(x<=m)
		{
			update(p*2,l,m,x,y,val);
		}
		if(y>m)
		{
			update(p*2+1,m+1,r,x,y,val);
		}
		tree[p]=tree[p*2]+tree[p*2]+1;
	}
}

```


------------

# 树链剖分
### dfs1（找到树的重链并记录重要量）
```
void dfs1(int x,int f)
//x代表现在,f代表父亲 
{
	large[x]=1;//记录一条边下去有多少节点 
	
	father[x]=f;//记录父亲节点 
	dep[x]=dep[f]+1;//深度+1 
	
	int maxy=0;
	
	for(int i=head[x];i!=-1;i=Next[i])
	{
		//i代表边 
		int u=to[i],big=0;//u代表这条边指向的点
		if(u==f) continue;//避免往回走
		
		dfs1(u,x);//向下探 
		
		large[x]+=large[u];//寻找重链 
		
		if(large[u]>maxy)
		{
			son[x]=u;//x的重儿子u
			maxy=large[u];//记录以比较大小	
		} 
		 
	}
}
```


------------

### dfs2（按照优先走重边的原则走出一个dfs序，x在dfs序中的位置记为id[x]，并算出每个点所属重链的起点top[x]。）
```
void dfs2(int x,int f)
//x指代当前，f指代祖先节点（不是父亲） 
{
	top[x]=f;//x的祖先是谁 
	id[x]=++tot;//x位于这条重链的第几个 
	
	if(!son[x])
		return;//是叶子节点就结束 
	
	dfs2(son[x],f);//继续探 
	
	for(int i=head[x];i!=-1;i=Next[i])
	{
		int u=to[i];
		if(u!=son[x]&&u!=father[x])//不在重链上
		{
			dfs2(u,u);//u就是他下面的儿子的祖先
		}
		
	}
}
```


------------

### lca（寻找最近公共祖先）
```
void updatelong(int x,int y,int z)
{
	while(top[x]!=top[y])
	{
		if(dep[top[x]]<=dep[top[y]])
		{
			update(1,1,n,id[top[y]],id[y],z);
			y=father[top[y]];
		}
		else
		{
			update(1,1,n,id[top[x]],id[x],z);
			x=father[top[x]];
		}
	}
	if(dep[x]>dep[y]) swap(x,y);
	update(1,1,n,id[x],id[y],z);
}
```


------------

### 建边（链式前向星）
```
void add(int x,int y)
//建立一条从x到y的有向边
{
	cnt++;//第cnt条边
	from[cnt]=x,to[cnt]=y;//fron,to都指代点
	Next[cnt]=head[x];head[x]=cnt;//指代边
}
```


------------




# 主函数
```
int main()
{
	cin>>n;
	memset(head,-1,sizeof(head));
	for(int i=1;i<=n;i++)
		cin>>a[i];
		
	for(int i=1;i<=n-1;i++)
	{
		cin>>x>>y;
		add(x,y);
		add(y,x);
	}
	
	dfs1(1,0);
	dfs2(1,1);
	
	for(int i=1;i<=n-1;i++)
	{
		updatelong(a[i],a[i+1],1);
		updatelong(a[i+1],a[i+1],-1);
	}
	for(int i=1;i<=n;i++)
	{
		printf("%d\n",query(1,1,n,id[i],id[i]));
	}
	return 0;
}
```
