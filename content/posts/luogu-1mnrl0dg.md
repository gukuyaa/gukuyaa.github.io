---
title: "数论"
date: 2024-07-21T11:46:32+08:00
draft: false
math: false
tags: ["洛谷", "算法·理论"]
categories: ["算法·理论"]
summary: "1.gcd和lcm 2.欧拉筛 3.扩展欧几里得 裴蜀定理： 不定方程𝑎𝑥+𝑏𝑦=𝑐有解，当且仅当gcd(𝑥,𝑦)|𝑐 | 证明&求解： | | : : | |…"
slug: "luogu-1mnrl0dg"
source: "https://www.luogu.com.cn/article/1mnrl0dg"
---
# 1.gcd和lcm

```
//辗转相除法求最大公约数 
int gcd(int a,int b)
{
	if(a<b) swap(a,b);
	if(b==0) return a;
	else return gcd(b,a%b);//一定不要忘了是gcd(b,a%b) 
}

//补充：gca(a,b)*lcm(a,b)=a*b;
```


------------
# 2.欧拉筛
```
#include<bits/stdc++.h>
using namespace std;

const int N=1145;
int n,num;
int prime[N],flag[N];

int main()
{
	cin>>n;
	flag[1]=1;//1不是质数 
	for(int i=2;i<=n;i++)
	{
		if(!flag[i])//i未作为基底向上筛选 
			prime[++num]=i;//添加到数组中方便调用
		
		for(int j=1;j<=num&&prime[j]*i<=n;j++)
		{
			flag[i*prime[j]]=1;//标记为合数
			if(i%prime[j]==0) 
				break;//及时退出，相比埃氏筛省时间的地方 
		}
		 
	}
	
	for(int i=1;i<=num;i++)
		cout<<prime[i]<<" ";//输出质数 
	return 0;
}
```



------------
# 3.扩展欧几里得
裴蜀定理：
不定方程𝑎𝑥+𝑏𝑦=𝑐有解，当且仅当gcd(𝑥,𝑦)|𝑐



| 证明&求解： |
| :----------: |
| ax+by=c |
| b'y+a'(x mod y)=c |
| a'(x-⌊𝑥/𝑦⌋*y)+b'y=c |
| a'x+(b'-a'⌊𝑥/𝑦⌋)y=c |




总结：每一次令𝑎=𝑎’,𝑏=𝑏'−𝑎'⌊𝑥/𝑦⌋。边界条件是当𝑦=0时，𝑎=𝑐/𝑥,𝑏=0。
```
//模板变量xy与ab和上述证明时刚好相反
void exgcd(int x,int y,int &a,int &b,int c)
int extgcd(int a,int b,int &x,int &y){
	if(!b){
		x=1,y=0;
		return a;
	}
	int d=extgcd(b,a%b,x,y);
	int temp=x;x=y,y=temp-a/b*y;
	return d;
}
```


------------

# 4.中国剩余定理（CRT）
| 解如下同余方程 |
| :----------: |
| x≡a1(mod b1) |
| x≡a2(mod b2) |
| ... |
| x≡an(mod bn) |
通过CRT即可求解最小的正整数x
```
int CRT(int *W,int *B,int k/*方程组数*/){
	int x,y,a=0,m,n=1;
	for(int i=0;i<k;i++) n*=W[i];
	for(int i=0;i<k;i++){
		m=n/W[i];
		extgcd(W[i],m,x,y);//即上文的exgcd
		a=(a+y*m*B[i])%n;
	}
	return a>0?a:a+n;
}
```
