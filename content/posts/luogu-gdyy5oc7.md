---
title: "状态压缩dp"
date: 2024-08-27T21:11:46+08:00
draft: false
math: false
tags: ["洛谷", "生活·游记"]
categories: ["生活·游记"]
summary: "1.什么是状压dp 用一个数的二进制来表示状态，即用0/1来表示有/没有的状态，搭配位运算可较方便的运算 2.状压dp的优势 1.相比用数组模拟，省下巨额空间 …"
slug: "luogu-gdyy5oc7"
source: "https://www.luogu.com.cn/article/gdyy5oc7"
---
## 1.什么是状压dp
用一个数的二进制来表示状态，即用0/1来表示有/没有的状态，搭配位运算可较方便的运算

## 2.状压dp的优势
1.相比用数组模拟，省下巨额空间

2.在状态转移上更加便捷

## 3.状压dp例题
[P1896 [SCOI2005] 互不侵犯](https://www.luogu.com.cn/problem/P1896)

```cpp
#include<bits/stdc++.h>
using namespace std;

#define int long long

int n,k,num;
int cnt[2000],ok[2000];
//cnt[i]:第i种状态的二进制中有几个1
//ok[i]:第i个行内不相矛盾(满足条件2:左右国王不相邻)的状态是多少

int dp[10][100][2000];
//dp[i][j][s]:我们已经放了i行,
//用了j个国王,第i行的状态为s的方案数

signed main()
{
	cin>>n>>k;
	for(int s=0;s<(1<<n);s++)
	{
		int tot=0,s1=s;
		while(s1)
		{
			if(s1&1) tot++;
			s1>>=1;
		}
		cnt[s]=tot;//统计s中有几个1 
		if((((s<<1)|(s>>1))&s)==0) ok[++num]=s;
		//s左边和右边的1不相邻，说明次s合法 
	}
	dp[0][0][0]=1;
	for(int i=1;i<=n;i++)
	{
		for(int l=1;l<=num;l++)//枚举第i行 
		{
			int s1=ok[l];
			for(int r=1;r<=num;r++)//枚举i-1行 
			{
				int s2=ok[r];
				if(((s2|(s2<<1)|(s2>>1))&s1)==0)
				{
					for(int j=0;j<=k;j++)
						if(j-cnt[s1]>=0)
							dp[i][j][s1]+=dp[i-1][j-cnt[s1]][s2];
				}
			}
		}
	}
	int ans=0;
	for(int i=1;i<=num;i++)
		ans+=dp[n][k][ok[i]];
	cout<<ans<<endl;
	return 0;
}
```


---
[P2704 [NOI2001] 炮兵阵地](https://www.luogu.com.cn/problem/P2704)

```cpp
#include<bits/stdc++.h>
using namespace std;

int n,m,ans,dp[(1<<10)][(1<<10)][3],a[105],sum[(1<<10)];
char x;
//dp[l][s][i]表示上一行的状态l,当前状态s,当前第i行 

int getsum(int s)
//求s中1的个数 
{
	int tot=0;
	while(s)
	{
		if(s&1) tot++;
		s>>=1;
	}
	return tot;
}

int main()
{
	cin>>n>>m;
	for(int i=0;i<n;i++)
		for(int j=0;j<m;j++)
		{
			cin>>x;
			a[i]<<=1;
			if(x=='H') a[i]+=1;
		}
	for(int i=0;i<(1<<m);i++)
		sum[i]=getsum(i);
	//sum[i]存储二进制i中1的个数
	for(int s=0;s<(1<<m);s++)
		if(!((s&(s<<2))||(s&(s<<1))||(s&a[0])))
			dp[0][s][0]=sum[s];
	for(int l=0;l<(1<<m);l++)//预处理第一行 
	{
		for(int s=0;s<(1<<m);s++)
		{
			if(!(s&l||l&a[0]||s&a[1]||l&(l<<1)||l&(l<<2)||s&(s<<1)||s&(s<<2)))
				dp[l][s][1]=sum[s]+sum[l];
		}
	}
	for(int i=2;i<n;i++)//从第二行开始 
	{
		for(int l=0;l<(1<<m);l++)//l表示i-1行 
		{
			if(l&a[i-1] || (l&(l<<1)) ||(l&(l<<2))) continue;
			for(int s=0;s<(1<<m);s++)
			{
				if(s&a[i] || (s&(s<<1)) || (s&(s<<2)) || s&l) continue;
				for(int fl=0;fl<(1<<m);fl++)//fl代表i-2行 
				{
					if(fl&l || fl&s || fl&a[i-2] || (fl&(fl<<1)) || (fl&(fl<<2)))	continue;
					dp[l][s][i%3]=max(dp[l][s][i%3],dp[fl][l][(i-1)%3]+sum[s]);
				}
			}
		}
	}
	for(int L=0;L<(1<<m);L++)
		for(int S=0;S<(1<<m);S++)
			ans=max(ans,dp[L][S][(n-1)%3]);	
	cout<<ans;
	return 0;
 } 
```
## 4.个人做题套路总结
1.dp数组基本都需要存当前的行数i和状态s

2.用滚动数组来缩小空间大小

3.都要预处理合法的s，记录其中1的个数，并将其存入数组（这就是状压的模版？）
