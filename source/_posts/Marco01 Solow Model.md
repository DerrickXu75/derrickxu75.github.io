---
title: Marco01 Solow Model
date: 2023-09-29 22:51:44
tags: [高宏, 金融学]
---



# Solow Model 



## The Base model

考虑一个封闭的不含政府投资的基本模型：


$$
\begin{align}
C_{t}+I_{t} &= Y_{t}= F(K_{t}, L) \label{1}\newline
I_t &= K_{t+1} - (1-\delta)K_t  \label{2} \\
I_t &= sF(K_{t}, L) \label{3}
\end{align}
$$
其中 $C_t,I_t,k_t$, 分别为 t 期消费，投资和资本存量。而 $L,\delta,s$ 分别是固定不变的劳动力投入，资本折旧率和资产投入比（储蓄率）

> 生产函数的形式：
>
> - `Y=F(K,AL)`：技术进步被称为劳动增加型、哈罗德中性
> - `Y=F(AK,L)`：技术进步被称为资本增加型、索罗中性
> - `Y=AF(K,L)`：技术进步被称为产出增加型、希克斯中性
>
> 知识或劳动有效性 `A`（有效劳动 `AL`）

由公式 $\eqref{2}$ 和 $\eqref{3}$ 得资本积累方程为


$$
\begin{align}
K_{t+1} =(1-\delta)K_t +sF(K_{t}, L) \label4
\end{align}
$$

为了分析经济中的动态情况，做出一下假设：
$$
F(0, L)= 0 \\
F_{K}(0, L)>\frac{\delta}{s} \\
\mbox{F is strictly concave in K and strictly increasing in K} \\
\lim_{k \to \infty} sF(K, L)+1-\delta < 1
$$

满足这个假设的一个常用例子是，柯布-道格拉斯函数（Cobb-Douglas function）$F (K, L) = AK^α L
^{1 −α}$

## Theorem 1.1 $\exists  K^* >0,\forall K_0>0,K_t\to K^* $ (稳态 $K^*$ 必存在)

**Proof.**

$$
K_{t+1} - K_t = sF(K_t, L)-\delta K_t = H(K_t) \\
from\ the \ assumption: H(0)= 0\\
H_K(K_t) = sF_K(K_t, L)-\delta = 
\left \{ 
\begin{aligned}
&> 0 \ K\to 0 \\
&< 0 \ K\to +\infty 
\end{aligned}
\right.\\
H_{KK}(K_t)= sF_{KK}(K_t, L)< 0
$$

此时存在唯一驻点 $K^*$，且满足公式 $δK^∗ = sF(K^∗ , L)$ 使得 $\exists  K^* >0,\forall K_0>0,K_t\to K^*$

### 考虑放松假设 2-4

1. 假设方程 $F$ 是非严格凹函数

   eg. assume $F(K,L)=0 \quad if \ K<\underline{ K}$（资本存量达到一定程度才会产出）

   此时 $K^*= 0$

2. 假设 $F_{K}(0,L)<\frac{\delta}{s} $

   此时 $K^*= 0$


3. 假设 $\lim_{k \to \infty}  sF(K,L)+1-\delta>1$

​	此时 $K^*= +\infty$

当违反假设时，经济就不会有稳态，经济的资本存量 $K^*$ 要么收敛到零要么趋近无限大。

## 应用

### 考虑人口增长和技术进步

现在考虑人口增长与技术增长对索罗模型的影响，假设人口增长以恒定不变的 $\gamma _n$ 增长，同时劳动力技术水平（影响劳动力总投入）以 $\gamma $ 增长，此时生产函数是哈罗德中性的。
$$
\begin{align}
C_{t}+I_{t} = F(K_{t},(\gamma \gamma_n)^tL) \label5
\end{align}
$$
我们用人均资本的形式定义 t 期资本，$\hat{K}_t=K_t/(\gamma \gamma_n)^t)$，此时资本积累方程 $\eqref{4}$ 可以被写为
$$
\begin{align}
\gamma \gamma_n\hat{K}_{t+1}  =(1-\delta)\hat{K}_{t} +sF(\hat{K}_{t}, L) \label6
\end{align}
$$
由于 $F$ 是一阶齐次的，在达到稳态时，平衡增长的资本存量 $\hat{K}_{ss}$ 由下面式子给

$$
\begin{align}
\gamma \gamma_n +\delta -1 = sF(1,\frac{L}{\hat{K}_{ss}}) \label7
\end{align}
$$
比较静态的结果表明，人口增长率 $\gamma_n$ 和人均资本 $\hat{K}_t$ 成反比。直观地说，因为 $t$ 和 $t + 1$ 之间的人口增长率越高，在 $t$ 时人均储蓄的任何给定储蓄量转化为人均资本越少，储蓄率较低或人均教育程度较低的国家也是如此。

### 趋同或者缺乏趋同

索洛模型可以用来分析经济的收敛速度。当模型存在稳态点，那么可以从形式上用参数 $\lambda $ 来定义当前资本存量 $K_t$ 和稳态水平 $K^*$ 之间的差距 $K_t-K^*$：
$$
\begin{align}
K_{t+1}-K^*=(1-\lambda)(K_t-K^*) \label8
\end{align}
$$
方程 $\eqref{8}$ 可以被看做是资本积累方程 $\eqref{4}$ 的一阶泰勒展开，考虑简单的柯布-道格拉斯方程 $F(K,L)= AK^αL^{1−α}$。一阶泰勒展开的结果可表示为

$$
1-\lambda\approx \alpha s A(\frac{K^*}{L})^{\alpha -1}+1-\delta
$$
在稳态状态下 $s A(\frac{K^*}{L})^{\alpha -1} = \delta$ (在没有技术进步和人口增长的情况下)，所以 $ \lambda = \delta(1-\alpha)$

$\lambda$是模型的收敛速度，如果$\lambda=0$差距完全不收敛，$\lambda=1$收敛速度为无限。它与储蓄率$\alpha$成反比，与资本折旧率$\delta$成正比。

此时当$\alpha=1$时，$F(K,L)=AK$，生产函数在是关于资本线性增长的的。假设$SA+1-\delta>1$这种情况下，$F$被称为AK生产模型，他是最简单的内生增长模型。

