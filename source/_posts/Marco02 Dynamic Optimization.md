---
title: Marco-2 Dynamic Optimization
date: 2023-10-04 17:19:04
tags: [高宏, 金融学]
---

# Dynamic optimization

## finite horizon new classical growth model

考虑一个`有限期`的消费者模型，其效用函数为$U(c_0,c_1,\dots,c_T)$，假设这个效用是`可加可分的`（“additive separability），这个效用函数可以表示为
$$
\begin{align}
U(c_0,c_1,\dots,c_T) = \sum_{t=0}^{T} \beta^tu(c_t)
\end{align}
$$
$\beta$是折现因子，因为当期消费总比未来消费更有价值，所以一般假设$0<\beta<1$

现在考虑一个有限期新古典增长模型的动态优化问题
$$
\begin{array}{rl}\max_{\{c_i,k_{i+1}\}_{i=0}^T}&\sum\limits_{t=0}^T\beta^tu\left(c_t\right)\\
\text{s.t.}&c_t+k_{t+1}\leq f\left(k_t\right)\equiv F\left(k_t,N\right)+\left(1-\delta\right)k_t,\forall t=0,...,T\\&c_t\geq0,\forall t=0,...,T\\&k_{t+1}\geq0,\forall t=0,...,T\\&k_0>0\text{ given.}\end{array}
$$
在该模型中，个人的储蓄依靠$f(k_t)$生产下一期的总产出，市场不存在一个可以借贷的市场。

现在做出一些假设：

1. $u(\cdot)$是严格递增的，这意味着扔掉产出总是不明智的。$c_t+k_{t+1}\le f(k_t)$应该永远取等
2. $\lim_{c \to 0^{+}} u^{'}(c)= +\infty $同时$\lim_{c \to \infty} u^{'}(c)= 0 $，这说明任何$t$处$c_t=0$都是非最优的。每期都需要消费($c_t>0$)。这一条件也被称为稻田条件(Inada Conditions)

可以写下该最优化问题的拉格朗日函数：
$$
\begin{align}
L = \sum_{t=0}^T\beta^t[ u(c_t)-\lambda_t [c_t+k_{t+1}-f(k_t)]+\mu_tk_{t+1}+\gamma_tc_t] 
\end{align}
$$
一阶条件为：
$$
\begin{align}
\frac{\partial L}{\partial c_t} &= \beta^t[u^{’}(c_t)-\lambda_t+\gamma_t]=0 \ t=0,\dots,T \label3 \\
\frac{\partial L}{\partial k_{t+1}} &= \left\{\begin{matrix}
&-\beta^t\lambda_t+\beta^t\mu_t+\beta^{t+1}\lambda_{t+1}f^{'}(k_{t+1})=0 \ t=0,\dots,T-1\label4\\
& -\beta^t\lambda_t+\beta^t\mu_t=0 \ t=T


\end{matrix}\right.



\end{align}
$$
该问题的KKT条件为，
$$
\mu_tk_{t+1}=0 \\
\gamma_tc_t = 0 \\
\lambda_t\geq 0 \\
\mu_t \geq 0 \\
\gamma_t \geq 0
$$
由$c_t>0$可得，$\gamma_t =0$。假设$u^{'}(c_t)>0$从公式$\eqref{3}$得$\lambda_t=u^{'}(c_t)>0$

