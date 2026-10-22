---
title: "dp"
date: 2024-11-26T09:00:26+08:00
draft: false
math: false
tags: ["洛谷", "算法·理论"]
categories: ["算法·理论"]
summary: "动态规划 区间dp [P2285 [HNOI2004] 打鼹鼠](https://www.luogu.com.cn/problem/P2285) 常规思想：f[…"
slug: "luogu-j4ystuqk"
source: "https://www.luogu.com.cn/article/j4ystuqk"
---
# 动态规划


## 区间dp


[P2285 [HNOI2004] 打鼹鼠](https://www.luogu.com.cn/problem/P2285)

常规思想：f[t][i][j]:t时刻,(i,j)位置时最大收益
但是存在超时问题

正解：f[i]第i个鼹鼠**必须打**，最大收益

if j<i && |xj-xi|+|yi-yj|<=ti-tj

f[i]=max(f[j])+1

反思：注重dp数组的变量设置与循环过程的**一致性**

我们以i为最后必须打的鼹鼠，那么初始状态**dp[i]=1**

在之后的转移过程中，一定是从**比i小**的地方转移过来

---

[P1103 书本整理](https://www.luogu.com.cn/problem/P1103)

#### 错误思路

dp[i][j]到第i本书，去掉了j本的最小不整齐度

dp[i][j]=max(dp[i][j],dp[i][j+1]-abs()) ？？？

发现(看题解)正向“去掉做不了”，思考反向来 

去掉做不了：我们在去掉一本书时，它改变的不整齐度为前一本书和后一本本的宽度差和它与两本书的宽度差，**前一本书我们不能保证是哪一本书**，我们只能用枚举来表示，但后一本书呢，我们发现无法处理了



---

#### 正解

**从n本书中去掉k本即为选择n-k本书**，使不整齐度最小

dp[i][l]:到第i本书，选择了l本的最小不整齐度

dp[i][l]=min(dp[i][l],dp[i-1][l+1]+)???

发现也还是有问题

我们第i本书是从第j本书转移过来的，而不应定是i-1

所以必须考虑三个变量：当前的第i本书，可能转移过来的第j本书，以及当前选择了的书的数量l

**dp[i][l]=min(dp[i][l],dp[j][l-1]+abs(a[i].宽-a[j].宽))**


---


[P9242 [蓝桥杯 2023 省 B] 接龙数列](https://www.luogu.com.cn/problem/P9242)


dp[i]:到第i位最多保留的数 

```cpp
for(int i=1;i<=n;i++) dp[i]=1;
	for(int i=2;i<=n;i++)
		for(int j=1;j<i;j++)
			if(r[j]==l[i])
				dp[i]=max(dp[i],dp[j]+1);
```
错因：dp[i]的初始化为任何一个i都可作为一个接龙数列，**而不应仅仅初始化dp[1]=1**

n2的复杂度过不了，考虑优化

因为当新加入一个数字时，是否拼接紧会对和它第一位相同的最后一位产生影响（太jb绕了，具体看代码），因此我们可以用dp[i]表示最后一位是i的最长序列



**dp[r[i]]=max(dp[r[i]],dp[l[i]]+1);**

## 树状dp

### 模版
[P1352 没有上司的舞会](https://www.luogu.com.cn/problem/P1352)

#### dp数组设计：

dp[i][0]:i不参加舞会

dp[i][1]:i参加舞会

#### 状态转移：

dp[p][0]+=max(dp[v][0],dp[v][1]);

dp[p][1]+=dp[v][0];

获取子树的信息通过链式前向星+**dfs**实现


```cpp
#include<bits/stdc++.h>
using namespace std;

const int N=6e3+5;

int n,cnt,root;
int hp[N],v[N],head[N],dp[N][4],vis[N];

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

int read()
{
	int x=0,f=1;
	char ch=getchar();
	for(;ch<'0'||ch>'9';ch=getchar()) if(ch=='-') f=-1;
	for(;ch>='0'&&ch<='9';ch=getchar()) x=x*10+ch-'0';
	return x*f;
}

void dfs(int p)
{
	dp[p][0]=0;
	dp[p][1]=hp[p];
	for(int i=head[p];i;i=edge[i].next)
	{
		int v=edge[i].to;
		dfs(v);
		dp[p][0]+=max(dp[v][0],dp[v][1]);
		dp[p][1]+=dp[v][0];
	
	}
}

int main()
{
	n=read();
	for(int i=1;i<=n;i++)
		hp[i]=read();
	for(int i=1;i<n;i++)
	{
		int x,y;
		x=read(),y=read();
		add(y,x);
		v[x]=1;
	}
	for(int i=1;i<=n;i++)
		if(!v[i])
			root=i;//找寻根节点 
	dfs(root);	//往下搜 
	cout<<max(dp[root][0],dp[root][1]);
	return 0;
}
```


---



[P4084 [USACO17DEC] Barn Painting G](https://www.luogu.com.cn/problem/P4084)

考虑进行dfs，统计祖先p的左右儿子可以染色的数量，再算p的可染色数量

**dp[p][1]=(dp[p][1]*(dp[v][2]+dp[v][3])%mod)%mod;**

第一种颜色即为p的左右儿子2,3种颜色和

乘dp[p][1]是通过dp[p][1]初值为1或0来控制p点能不能染1颜色

---


[P2014 [CTSC1997] 选课](https://www.luogu.com.cn/problem/P2014)

#### 错误思路：


```cpp
void dfs(int p,int cnt,int flag)
{
	if(!flag)dp[p][0]=0;
	if(flag)dp[p][1]=val[p];
	for(int i=head[p];i;i=edge[i].next)
	{
		int v=edge[i].to;
		dfs(v,cnt-1,1);
        dfs(v,cnt,0);
		dp[p][1]+=max(dp[v][0],dp[v][1]);
	}
}
```
这么写有一个很严重的问题：实际上max动态规划部分未得到实现，两次dfs会覆盖dp[v][0/1],对于选与不选，要用**01背包**实现未实现的功能

#### 正解：

dp[i][j]:前i门课程，选择j门，能获得的最大学分

```cpp
void dfs(int p)
{
	dp[p][1]=val[p];
	for(int i=head[p];i;i=edge[i].next)
	{
		int v=edge[i].to;
		dfs(v);//先往下搜到叶子节点再往上累加 
	}
	for(int i=head[p];i;i=edge[i].next)//遍历物品 
	{
		for(int j=m;j>0;j--)//遍历背包空间 
		{
			for(int k=0;k<j;k++)//另一个空间 
			{
				int v=edge[i].to;
				dp[p][j]=max(dp[p][j],dp[p][j-k]+dp[v][k]);//p和v里选j个节点 
			}
		}
	}
}
```


---


[P2015 二叉苹果树](https://www.luogu.com.cn/problem/P2015)

f[i][j]:i的子树中选一个j条边的连通块，求最大的大小

[P3177 [HAOI2015] 树上染色](https://www.luogu.com.cn/problem/P3177)

f[i][j]:i的子树中选j个黑色点，子树内的最大收益

对每个点i，求所有两两子树的大小的乘积的和

对每个点i，求有多少路径以i为1ca

[P3478 [POI2008] STA-Station](https://www.luogu.com.cn/problem/P3478)

主要是**换根**思想，求出一个点后看周围的点与其细小的差别


## 背包问题

### 01背包

[P1048 [NOIP2005 普及组] 采药](https://www.luogu.com.cn/problem/P1048)


```cpp
for(int i=1;i<=n;i++)
	{
		for(int j=m;j>=0;j--)
		{
			if(j>=v[i])
				dp[j]=max(dp[j],dp[j-v[i]]+w[i]);
		}
	}
```


### 分组背包

[P1757 通天之分组背包](https://www.luogu.com.cn/problem/P1757)


```cpp
	for(int i=1;i<=n;i++)
	{
		cin>>v[i]>>w[i]>>c[i];
		t[c[i]]++;//桶 
		maxx=max(maxx,c[i]);//最多有几种 
		f[c[i]][t[c[i]]]=i;//第几种类中的第几件是物品i 
	}
	for(int i=1;i<=maxx;i++)
	{
		for(int j=m;j>=0;j--)
		{
			for(int k=1;k<=t[i];k++)
			{
				if(j>=v[f[i][k]])
					dp[j]=max(dp[j],dp[j-v[f[i][k]]]+w[f[i][k]]);
			}
		}
	}
```
### 完全背包

[P1616 疯狂的采药](https://www.luogu.com.cn/problem/P1616)


```cpp
for(int i=1;i<=n;i++)
	for(int j=w[i];j<=m;j++)//改为正向遍历即可
		f[j]=max(f[j],f[j-w[i]]+v[i]);
```



---



[P5322 [BJOI2019] 排兵布阵](https://www.luogu.com.cn/problem/P5322)

f[i][j]:前i个城堡，用了j个士兵的最大收益

f[i1[j1:前i组，用了j的背包体积的最大收益

## 数据结构优化dp

### 前置芝士：单调队列
[P1440 求m区间内的最小值](https://www.luogu.com.cn/problem/P1440)

入队/滑动窗口右滑。每年选拔新队员时，淘汰比这名新队员弱的老队员。对于单调队列，就是插入新元素时，把先前存在的比当前元素小的元素弹出（从队尾退队）。


退役/滑动窗口右滑。只需判断最老的队员是否需要退队。对于单调队列，只需判断队头是否已经超出滑动窗口范围，若超出，则从队头退队。


参赛/查询滑动窗口最大值。直接派最老的队员参赛/直接返回队头元素。


```cpp
q[head]=1;//q中记录的是索引,a[q[i]]才是数值 
	for(int i=2;i<=n;i++)
	{
		while((head<=tail)&&(i-q[head])>m) head++;//如果队首的数已经不再范围里了，出队。
		cout<<a[q[head]]<<endl;//队首即为保留的最大的 
		while((head<=tail)&&(a[q[tail]])>a[i]) tail--;//新a[i]太小,不配入队 
		q[++tail]=i; 
	}
```


[P1725 琪露诺](https://www.luogu.com.cn/problem/P1725)



滑动窗口用单调队列优化

```cpp
	head=1;
	tail=0;
	for(int i=l;i<=n;i++)
	{
		while((head<=tail)&&q[head]<i-r)head++;
		while(head<=tail&&dp[q[tail]]<dp[i-l])tail--;
		q[++tail]=i-l;
		dp[i]=dp[q[head]]+a[i];
		if(i+r>n)
			ans=max(dp[i],ans);
	}
```


---



[P2034 选择数字](https://www.luogu.com.cn/problem/P2034)

同样反着做，来进行删除

f[i]:最后一个没选的数字在i位置，没选的数尽可能小


---



[P3572 [POI2014] PTA-Little Bird](https://www.luogu.com.cn/problem/P3572)

从区间飞点，先以疲劳为第一关键字，选疲劳小的

若疲劳相同，则选树的高度高的


---

[P9344 去年天气旧亭台](https://www.luogu.com.cn/problem/P9344)


---



### 前后缀的优化

[P2344 [USACO11FEB] Generic Cow Protests G](https://www.luogu.com.cn/problem/P2344)

f[i]:[1,i]取完了，i位置是段结尾，有多少种方案

用前缀和+数据结构优化

## 状压dp

（主要见我另一篇专栏）

[P1879 [USACO06NOV] Corn Fields G](https://www.luogu.com.cn/problem/P1879)




[P3092 [USACO13NOV] No Change G](https://www.luogu.com.cn/problem/P3092)


f[S]:用了S这些钱最多拿了前多少个
