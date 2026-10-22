---
title: "树的重心与直径"
date: 2024-06-08T09:20:41+08:00
draft: false
math: false
tags: ["洛谷", "算法·理论"]
categories: ["算法·理论"]
summary: "树的重心 1.概念： 如果在树中选择某个节点并删除， 这棵树将分为若干棵子树， 统计子树节点数并记录最大值。 取遍树上所有节点， 使此最大值取到最小的节点被称为…"
slug: "luogu-2s60g21j"
source: "https://www.luogu.com.cn/article/2s60g21j"
---
# 树的重心
## 1.概念：
	如果在树中选择某个节点并删除，
    这棵树将分为若干棵子树，
    统计子树节点数并记录最大值。
    取遍树上所有节点，
    使此最大值取到最小的节点被称为整个树的重心。
## 2.重心的特点：
	树的重心如果不唯一，则至多有两个，且这两个重心相邻。
	以树的重心为根时，所有子树的大小都不超过整棵树大小的一半。

	树中所有点到某个点的距离和中，到重心的距离和是最小的；如果有两个重心，那么到它们的距离和一样。

	把两棵树通过一条边相连得到一棵新的树，那么新的树的重心在连接原来两棵树的重心的路径上。

	在一棵树上添加或删除一个叶子，那么它的重心最多只移动一条边的距离
    
## 3.代码实现：
```
#include<bits/stdc++.h>
using namespace std;

int n,x,y;
int tree[100][100];//邻接矩阵存储树节点间关系
int sum[100];//sum[i]:以i为根节点时子树节点数量 
int maxval[100];//maxval[i]:删除i后节点数量最大值 

void dfs(int u,int f)
//u代表当前所在节点,f代表u的父亲节点 
{
	sum[u]=1;//初始设为1 
	
	int maxw=0;//记录子树中节点数最大值
	
	for(int v=1;v<=n;v++)
	{
		if(!tree[v][u]||v==f)//无路或者是往回走 
			continue;
			
		dfs(v,u);//往下搜 
		
		sum[u]+=sum[v];//更新当前子树数量
		 
		if(sum[v]>maxw)
			maxw=sum[v];//更新子树中节点数最大值 
	}
	
	
	/*如果知道了以节点3为根节点的子树的节点数，
	则其它部分的节点数量可以轻松计算出来：
	整棵树的节点数n-以3为根节点的子树的数量。*/ 
	 if(n-sum[u]>maxw)
		maxw=n-sum[u];
	
	maxval[u]=maxw;//记录 
}

int main()
{
	cin>>n;
	for(int i=1;i<n;i++)
	{
		cin>>x>>y;
		tree[x][y]=tree[y][x]=1;
	}
	
	dfs(1,0);//dfs(u,v):以u为根节点时节点数量最大值 
	
	int count=n,nid=0;
	for(int i=1;i<=n;i++)
	{
		if(maxval[i]<count)
		{
			count=maxval[i];
			nid=i;
		}
	}
	cout<<nid<<" "<<count<<endl;
	return 0;
}
/*

9
1 2
1 3
1 4
2 5
2 6
3 7
3 8
7 9
*/


```
## 4.应用案例
[P1364 医院设置](https://www.luogu.com.cn/problem/P1364)


# 树的直径
## 1.概念:
	给定一棵树，每条边上有边权，
    树上距离最远的两个点之间的距离叫树的直径
  
## 2.性质
①直径两端点一定是两个叶子节点

②距离任意点最远的点一定是直径的一个端点，这个基于贪心求直径方法的正确性可以得出

③如果第一棵树直径两端点为
(
u
,
v
)
，第二棵树直径两端点为
(
x
,
y
)
，用一条边将两棵树连接，那么新树的直径一定是
u
,
v
,
x
,
y
中的两个点

④对于一棵树，如果在一个点的上接一个叶子节点，那么最多会改变直径的一个端点

⑤若一棵树存在多条直径，那么这些直径交于一点且交点是这些直径的中点


## 3.代码实现
```
#include<bits/stdc++.h>
using namespace std;

const int N=10000;

int n,idx=0,dis[N];
vector<int>edge[N];


void dfs(int u,int fa)
{
	for(int i=0;i<edge[u].size();i++)//此处循环对于v的值好像有点问题 
	{
		int v=edge[u][i];
		if(v==fa)	continue;
		
		dis[v]=dis[u]+1;
		
		if(dis[v]>dis[idx])
			idx=v;
			
		dfs(v,u);
	}
		
}

int main()
{
	cin>>n;
	for(int i=1;i<n;i++)
	{
		int u,v;
		cin>>u>>v;
		edge[u].push_back(v);
		edge[v].push_back(u);
		dis[i]=0;
	}
	
	dfs(1,0);
	dis[idx]=0;
	dfs(idx,0);
	
	cout<<dis[idx];
	return 0;
}


/*

9
1 2
1 3
1 4
2 5
2 6
3 7
3 8
7 9
*/
```
