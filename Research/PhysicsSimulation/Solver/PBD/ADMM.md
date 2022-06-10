# 论文阅读：ADMM ⊇ Projective Dynamics

本文为对[ADMM ⊇ Projective Dynamics: Fast Simulation of Hyperelastic Models with Dynamic Constraints](https://mattoverby.net/pages/admmpd_abstract.html)的阅读笔记。
须注意，本文极其精简，只涉及极小一部分论文内容，并且哪怕是这一小部分也以我个人理解为主。

本文里大段篇幅都和[XPBD的这篇最优化视点](https://zhuanlan.zhihu.com/p/518244355)一模一样，这是有意为之的，我想让这篇文章独立成文，但又容易进行比较。

一些记号约定：
* 位移为$x$，速度为$v$，加速度为$a$，时间为$t$。
* 共$n$个质点。
* 所有向量均为列向量。标量对$n$维向量求导，结果为$n$维向量；$m$维向量对$n$维向量求导，结果为$m$行$n$列矩阵。
* 上标表示时刻，例如$x^n$表示第$n$个时刻的位移。
* 下标表示某个质点的值，例如$x_i$表示第$i$个质点的位移。
* 已知$n$时刻的所有状态信息，包括但不限于$x, v, a$。（注意这里为了和其他地方的标记统一，所以$n$同时具有$n$维和第$n$个时刻的含义，有点混用了）
* 质量矩阵为对角矩阵$M=diag\{m_1, m_2, \cdots, m_n\}$，其中$m_i$为第$i$个质点的质量。设质量与时间无关，始终不变。
* $\Delta t$为时步长度，即每帧之间的时间长度$Δt=t^{n+1}-t^n$。
* $∇U$为函数$U$对$x$求一阶导，$H(U)$为$U$对$x$求二阶导（即海森矩阵）。


# 1. 方法

我们的目标是要求出当前位移$x$，根据速度定义，其满足：

$$
\tag{1.1}
x^{n+1} = x^n + \int_{t^n}^{t^{n+1}}vdt
$$

速度又根据加速度定义，满足：

$$
\tag{1.2}
v = v^n + \int_{t^n}^{t}adt
$$

根据牛顿第二定律，可知：

$$
\tag{1.3}
a=M^{-1}F
$$

把式1.3代入到式1.2里，就能求出$v$关于$t$的函数，然后再代进式1.1里就能求出$x^{n+1}$关于$t^{n+1}$的函数。
不过因为$F$通常都很复杂，所以直接求积分不太现实，使用数值积分的方法近似求解比较现实。

对式1.1, 1.2**应用隐式欧拉法（第一个处理）**：

$$
\left\{
\begin{aligned}
	x^{n+1} = x^n + Δtv^{n+1} \\
	v^{n+1} = v^n + Δta^{n+1} \\
\end{aligned}
\right.
$$

这一近似就让$x^{n+1}$变得更容易求解了。为了让解更加明显，我们对它稍作变形，把下式的$v^{n+1}$代进上式，从而消掉并不是目标项的$v^{n+1}$，得到：

$$
x^{n+1}=x^n+Δtv^n+Δt^2a^{n+1}
$$

求解这一关于$x^{n+1}$的方程即可。
不过$a^{n+1}$还没有展开。
如果展开的话，因为$a^{n+1}=M^{-1}F^{n+1}$，
而$F^{n+1}$通常都是关于$x^{n+1}$或$v^{n+1}$的非线性函数，
这就导致上式变成了一个关于$x^{n+1}$的非线性方程。
我们希望能求解得更容易点。

我们先把这个非线性方程给写出来，为了方便，记$Δx=x^{n+1}-x^n-Δtv^n$。则有方程：

$$
\tag{1.4}
MΔx-Δt^2F(Δx)=0
$$

我们的目标是求解式1.4，这在解附近等价于求解以下最优化问题：

$$
\min_{Δx}\ G(Δx)=\frac{1}{2}Δx^TMΔx-Δt^2∫F(Δx)d(Δx)
$$

这是因为在没有约束条件的情况下，$G(Δx)$的极值点必定满足$\frac{∂G}{∂Δx}=MΔx-Δt^2F(Δx)=0$，也就是1.4式成立。

为了能方便地处理$F$，此处再引入一个假设：**$F$为保守力（第二个处理）**，即有势能场$U$满足：

$$
∇U=-F
$$

则最优化问题可记为：

$$
\tag{1.5}
\min_{Δx}\ G(Δx)=\frac{1}{2}Δx^TMΔx-Δt^2U(Δx)
$$

$G$的前半项$\frac{1}{2}Δx^TMΔx$是个关于$Δx$的二次项，求它的极值点很容易。
所以$G$的复杂度由其后半项$U$来决定。
通常而言，$U$都挺复杂的，不是一个简单的二次函数。



------
（下文和[XPBD的那篇](https://zhuanlan.zhihu.com/p/518244355)产生分歧）

因为$G$的两项在复杂度上的差距，所以我们会有一个很直接的想法：能不能分开来处理这两项？设

$$
\begin{aligned}
	G_1(\Delta x) &= \frac{1}{2}Δx^TMΔx \\
	G_2(\Delta x) &= -Δt^2U(Δx) \\
	\Rightarrow G(\Delta x) &= G_1(\Delta x) + G_2(\Delta x)
\end{aligned}
$$

在这基础上，我们**引入新的变量：$\Delta z$，将式1.5转换成[共识形式(consensus form)](https://statisticaloddsandends.wordpress.com/2020/01/03/consensus-admm/)（第三个处理）**：

$$
\tag{1.6}
\begin{aligned}
	\min_{Δx, \Delta z}&\ G(Δx, \Delta z)=G_1(\Delta x) + G_2(\Delta z) \\
	s.t.&\ \Delta x - \Delta z = 0
\end{aligned}
$$

不难发现式1.6和式1.5是等价的。

[ADMM(Alternating direction method of multipliers)](https://stanford.edu/~boyd/admm.html)适用于解决式1.6这类最优化问题。关于ADMM的详细介绍我放在了附录部分，在此仅简述它的过程。

ADMM是一种迭代求解最优化问题的方法，它将原本复杂的目标函数拆成若干较小的部分，然后因为这些若干较小的部分是比较容易优化的，所以逐个优化这些较小的部分能比直接优化原来的函数要容易得多。

设$\Delta x^+$为ADMM迭代里每步中待求的量（即当前步的量），$\Delta x^-$为每步中已知的量（即上一步的量）。其他符号也遵循同样的上标约定。

则**对式1.6应用ADMM方法求解得到方程组（第四个处理）**：

$$
\left\{
\begin{aligned}
\Delta x^+ &= \argmin_{\Delta x}\{G_1(\Delta x) + \frac{1}{2}\rho ||\Delta x-\Delta z^- + u^-|| \} \\
\Delta z^+ &= \argmin_{\Delta z}\{G_2(\Delta z) + \frac{1}{2}\rho ||\Delta z-\Delta x^+ - u^-|| \} \\
u^+ &= u^- + \Delta x^+ - \Delta z^+
\end{aligned}
\right.
$$

其中$\rho$为ADMM里的一个参数，论文里是直接取了$\rho = 1$。$u$为引入的辅助变量。

我们把上式中的$G_1, G_2$给写开来，则有：

$$
\tag{1.7}
\left\{
\begin{aligned}
\Delta x^+ &= \argmin_{\Delta x}\{\frac{1}{2}Δx^TMΔx + \frac{1}{2}\rho ||\Delta x-\Delta z^- + u^-||^2_2 \} \\
\Delta z^+ &= \argmin_{\Delta z}\{-Δt^2U(Δz) + \frac{1}{2}\rho ||\Delta z-\Delta x^+ - u^-||^2_2 \} \\
u^+ &= u^- + \Delta x^+ - \Delta z^+
\end{aligned}
\right.
$$

注意到第一步更新$Δx$里因为目标函数是两个二次函数的和，所以算起来是很快的，第三步更新$u$也很朴素。问题依然还是第二步更新$Δz$时$U(Δz)$可能是个非常复杂的函数。式1.7和式1.5在难度上并没有变化。

很遗憾，论文里并没有对$U$的处理提出一套统一的解决方法，原文中描述为：

	While this is still a nonlinear optimization problem that generally does not have a closed-form solution, for typical energy terms it is very low-dimensional and therefore feasible to solve numerically or using precomputation.

我并不理解他所说的"low-dimensional"是什么意思。


# 2. 讨论
我们为了求解式1.1里的$x^{n+1}$，一共做了四个处理：

1. 应用隐式欧拉法计算数值积分
2. 假设作用力均为保守力，从而可以将原问题转换为最优化问题
3. 引入新的变量，将无约束优化问题转化为与其等价的等式约束优化问题
4. 对上一步得到的等式约束优化问题应用ADMM进行求解

但这四个处理后依然需要面对一个目标函数比二次函数复杂的最优化问题，文中并没有给出统一的解法。

关于引入ADMM的意义，我觉得可能是直接优化一整个$G$可能要比分开来优化$G_1, G_2$来得慢，但引入ADMM并不能降低求解难度本身，依然需要寻求其他解决方案，文中也使用了各种solver来处理$U$。







