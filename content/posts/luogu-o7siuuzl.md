---
title: "树状数组（普通与差分）"
date: 2024-03-23T16:55:47+08:00
draft: false
math: false
tags: ["洛谷", "算法·理论"]
categories: ["算法·理论"]
summary: "普通版本：单点修改，区间查询 2024 3 23 差分版本：区间修改，单点修改 双bit版本：区间修改，区间查询 2026 9.5（军训时期）"
slug: "luogu-o7siuuzl"
source: "https://www.luogu.com.cn/article/o7siuuzl"
---
### 普通版本：单点修改，区间查询
```
/*
树状数组，用数组来模拟树形结构 
目前问题：对于lowbit,usm,add的神奇用法无法理解，只能死记硬背代码 


*/
lowbit 最低为的1对应的二进制的大小



#include<bits/stdc++.h>
using namespace std;

int n,m;
int a[500005];

int lowbit(int x)
{
	return x & (-x);
	/*-x就是取反+1；
	x= 110100
	-x=001011+1=001100
	 */ 
}

void add(int p,int x)//也叫update 
{
	while(p<=n)
	{
		a[p]+=x;//在p位置加上x 
		p+=lowbit(p);	
	}
	/*
	单点修改；
	a[p]+=x：单点修改值 
	p+=lowbit(p)：从最低节点开始向上修改 
	*/
}

int sum(int p)//也叫query,求1到i的数之和 
{
	int ans=0;
	while(p)
	{
		ans+=a[p];//加上值 
		p-=lowbit(p);//减去区间长度 
	}
	return ans;
	 
}

int main()
{
	cin>>n>>m;
	int b; 
	for(int i=1;i<=n;i++)
	{
		//初始化，给定值建立树状数组 
		cin>>b;
		add(i,b);
	}
		
	int x,y,z;	
		
	for(int i=1;i<=m;i++)
	{
		cin>>x>>y>>z;
		if(x==1)
			add(y,z);
		/*
			若想要实现区间修改，可用差分思想来进行
			例：给x到y的范围内，加上z;
			add(x,k); 
			add(y+1,-k);
		*/
		else if(x==2)
			cout<<sum(z)-sum(y-1)<<endl;
			//前缀和思想，求y到z的和;
	}
	
	
	return 0;
} 
```
2024 3 23


### 差分版本：区间修改，单点修改

```cpp
#include<bits/stdc++.h>
using namespace std;

int n,m;
int a[500005];

int lowbit(int x)
{
	return x & (-x);
}

void add(int p,int x)
{
	while(p<=n)
	{
		a[p]+=x;
		p+=lowbit(p);	
	}
}

int sum(int p)
{
	int ans=0;
	while(p)
	{
		ans+=a[p];
		p-=lowbit(p);
	}
	return ans;
}

int main()
{
	cin>>n>>m;
	int b,now=0; 
	for(int i=1;i<=n;i++)
	{
		cin>>b;
    //用树状数组模拟差分数组
		add(i,b-now);
		now=b;
	}
		
	int x,y,z,o;	
		
	for(int i=1;i<=m;i++)
	{
		cin>>o;
		if(o==1)
		{
			cin>>x>>y>>z;
			add(x,z);
			add(y+1,-z);
		}
			
		else if(o==2)
		{
			cin>>x;
      //查询原数组的第x个值，本质相当于求差分数组前x个数的前缀和
			cout<<sum(x)<<endl;
		}
	}
	
	
	return 0;
} 
```

### 双bit版本：区间修改，区间查询

```cpp
#include<bits/stdc++.h>
using namespace std;

int n,m;
int c1[500005]; // 维护差分数组 d[i]
int c2[500005]; // 维护 i * d[i]

int lowbit(int x)
{
    return x & (-x);
}

// 对指定的树状数组进行单点修改
void add(int tr[], int p, int x)
{
    while(p <= n)
    {
        tr[p] += x;
        p += lowbit(p);	
    }
}

// 对指定的树状数组进行前缀查询
int sum(int tr[], int p)
{
    int ans = 0;
    while(p)
    {
        ans += tr[p];
        p -= lowbit(p);
    }
    return ans;
}

int main()
{
    cin >> n >> m;
    
    // 初始化：用差分数组建树
    int last = 0; 
    for(int i = 1; i <= n; i++)
    {
        int x;
        cin >> x;
        int diff = x - last; // 差分值 d[i] = a[i] - a[i-1]
        
        add(c1, i, diff);      // c1 维护 d[i]
        add(c2, i, i * diff);  // c2 维护 i * d[i]
        
        last = x;
    }
    
    for(int i = 1; i <= m; i++)
    {
        int opt;
        cin >> opt;
        
        if(opt == 1) // 区间修改： [l, r] 加上 z
        {
            int l, r, z;
            cin >> l >> r >> z;
            
            // 差分数组的两个单点修改
            add(c1, l, z);
            add(c1, r + 1, -z);
            
            add(c2, l, l * z);
            add(c2, r + 1, -(r + 1) * z);
        }
        else if(opt == 2) // 区间查询：输出 [l, r] 的和
        {
            int l, r;
            cin >> l >> r;
            
            // 前缀和公式： S(x) = (x+1) * sum(d[i]) - sum(i * d[i])
            auto get_sum = [&](int x) -> int {
                return (x + 1) * sum(c1, x) - sum(c2, x);
            };
            
            int ans = get_sum(r) - get_sum(l - 1);
            cout << ans << endl;
        }
    }
    
    return 0;
}
```
2026 9.5（军训时期）
