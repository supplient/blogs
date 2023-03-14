---
title: 约束动力学(Constrained Dynamics)：基于位置的方法(Position Based Method)（检索用：PBD）
zhihu-tags: 物理仿真,
zhihu-url: https://zhuanlan.zhihu.com/p/613111930
---

本文将讨论使用 **基于位置的方法(Position Based Method)** 对受约束的粒子系统进行物理仿真的过程。

> Position Based Method这名字是我自己起的，与impulse based method相对。
> 
> 因为本文内容相当于是Position Based Dynamics(PBD)的一个子集，
> 仅关注在受束系统中系统方程组的建立上，
> 因此为了避免让读者误以为这就是PBD的全部了，
> 我就另外起了一个名字。
> 
> 不过本文方法其实也不关注Position就是了（笑）。

> 笔者曾写过另一篇[PBD的阅读笔记](https://zhuanlan.zhihu.com/p/339879519)，
> 因所站视点不同，故另开此文。



# 记号与问题描述

系统描述：

* 系统为粒子系统
* 系统状态为位置坐标，记为$q\in R^n$
* 系统速度记为$v$
* 系统加速度记为$a$
* 下一时刻的系统状态/速度用上标$'$来表示：$q', v'$
* 质量矩阵$M = \text{diag}(\mathbf{m}_1, \mathbf{m}_2, \dots) \in R^{n \times n}$，其中$\mathbf{m}_i = [m_i, m_i, \dots]^T$，$\mathbf{m}_i$的维数为第$i$个粒子的自由度，$m_i$为第$i$个粒子的质量
* 约束记为$C(q)=0$，约束函数$C: R^n \Rightarrow R^m$
* 外力为$F_E$
* 约束力为$F_C$

记号说明：

* 本文中所有向量均为列向量
* 本文仅在容易引起混淆的地方对矢量值采用粗体
* $\mathbf{1}=[1, 1, \dots]^T$
* 本文中雅克比矩阵的运算采用与[wiki](https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant)中一致的运算规则，即：$J_{ij} = \frac{\partial f_i}{\partial x_j}$

待求项为下一时刻的系统状态和系统速度$q', v'$，
要求其满足约束$C(q')=0$。


# 数值积分

应用半隐式欧拉法(semi-implicit Euler)来计算$q'=q+\int v\mathrm{d}t, v'=v+\int a\mathrm{d} t$的数值积分：

$$
\left\{
\begin{aligned}
	q' = q + \Delta t v'\\
	v' = v + \Delta t a
\end{aligned}
\right.
$$

其中加速度$a=M^{-1}(F_E+F_C)$，
因为约束力$F_C$未知，
所以$a$也未知。

因此该方程组中未知变量为$q', v', a$，
未知数一共有$3n$个，
而方程数量仅有$2n$个，
因此该方程组为欠定方程组，无法求出唯一解。
我们需要寻找更多方程来进行求解。


# 条件一、$C(q')=0$
我们当然希望下一时步的系统状态$q'$能够满足约束：

$$
C(q')=\mathbf{0}
$$

但该方程组也只能提供$m$个方程，
若$m<n$，则还差$n-m$个方程。


# 条件二、动量守恒
由动量守恒定律可知，
如果约束力$F_C$为系统内力，
那么在它的作用下系统动量应当保持不变。

若约束力$F_C$为系统内力，
因此由牛顿第三定律可知，
其对系统造成的合外力为0，
即：

$$
F_C \cdot \mathbf{1} = 0
$$

则从$t$到$t'$这段时间中由$F_C$引起的冲量为：

$$
\Delta p = \Delta t F_C \cdot \mathbf{1} = 0
$$

约束力冲量为0，满足动量守恒定律。


# 条件三、保守约束力

【TODO：这个条件还有待进一步的推敲】

我们假设约束力$F_C$为保守力，
并且希望其对应的势能$U$仅与约束函数$C(q)$有关。

也就是说，当$C(q')=C(q)$时，
$U(C(q'))=U(C(q))$，
即从$q$到$q'$，约束力$F_C$不做功
（这里假设了$F_C$在沿$q$到$q'$的直线路径上保持不变）：

$$
\begin{aligned}
& U(C(q')) - U(C(q)) \\
=& \int_q^{q'} F_C \cdot \mathrm{d}s \\
\approx& F_C \cdot (q'-q) \\
=& 0
\end{aligned}
$$

为了让约束力$F_C$满足上式，
我们首先引入一条假设：

$$
C(q') \approx C(q) + \nabla C|_q (q'-q)
$$

也就是对$C(q')$在$q$点做泰勒展开，并仅保留一阶导。

下文中为了简洁，将默认把$\nabla C|_q$记为$\nabla C$。

则当$C(q')=C(q)$时，由该假设可得：

$$
\nabla C(q'-q) = C(q')-C(q) = 0
$$

此时若我们设约束力$F_C = \nabla C^T \lambda$，
则有：

$$
\begin{aligned}
& F_C \cdot (q'-q) \\
=& F_C^T (q'-q) \\
=& (\nabla C^T \lambda)^T (q'-q) \\
=& \lambda^T \nabla C (q'-q) \\
=& \lambda^T 0 \\
=& 0
\end{aligned}
$$

约束力$F_C$沿$q$到$q'$的路径上做功为0，
满足条件。


## 和最优化视角之间的一点联系
如果读者曾阅读过我撰写的[XPBD(最优化视角)](https://zhuanlan.zhihu.com/p/518244355)，
可能也会注意到我们希望约束力$F_C$对应的势能$U$仅与约束函数$C(q)$有关，
其实也就类似那篇文章中的第三个处理规定势能结构：

$$
U = \frac{1}{2} C^T \alpha C
$$

【TODO：我目前还没有理清这之间的细节，有待后续的进一步研究。】




# 系统方程组

## 总结上文
数值积分部分，我们使用半隐式欧拉法：

$$
\left\{
\begin{aligned}
	q' = q + \Delta t v'\\
	v' = v + \Delta t a
\end{aligned}
\right.
$$

运动方程为：

$$
a=M^{-1}(F_E+F_C)
$$

条件一要求：

$$
C(q')=\mathbf{0}
$$

条件二动量守恒被自动满足。

条件三的两条假设：

$$
\left\{
\begin{aligned}
	& F_C \text{为保守力} \\
	& C(q') \approx C(q) + \nabla C|_q (q'-q) \\
\end{aligned}
\right.
$$

条件三要求：

$$
F_C = \nabla C^T \lambda
$$

在两条假设和一条要求被满足时，条件三被满足。


## 系统方程组

联立

* 半隐式欧拉法
* 运动方程
* 条件一的要求
* 条件三的要求

$$
\left\{
\begin{aligned}
	q' &= q + \Delta t v' \\
	v' &= v + \Delta t a \\

	a &= M^{-1}(F_E+F_C) \\

	C(q') &= 0 \\

	F_C &= \nabla C^T \lambda \\
\end{aligned}
\right.
$$

经化简可以得到一个关于$\lambda$的方程组，

$$
C(q^* + M^{-1}\nabla C^T \lambda) = 0
$$

其中$q^*$为已知项：

$$
\left\{
\begin{aligned}
	q^* &:= q + \Delta t v^* \\
	v^* &:= v + \Delta t a^* \\
	a^* &:= M^{-1} F_E \\
\end{aligned}
\right.
$$

因为$\lambda$为$m$维向量，该方程组也提供了$m$个方程，
因此当该方程组为线性方程组且各方程之间线性无关时，
则总是要么有唯一解，要么无解。

解出$\lambda$后，

1. 由$q' = q^* + M^{-1}\nabla C^T \lambda$算出$q'$
2. 由$q' = q + \Delta t v'$算出$v'$

或者

1. 由$F_C = \nabla C^T \lambda$算出$F_C$
2. 由$a = M^{-1}(F_E+F_C)$算出$a$
3. 由$v' = v + \Delta t a$算出$v'$
4. 由$q' = q + \Delta t v'$算出$q'$

（实际求解时，通常会线性化约束函数$C$来简化计算。
PBD里还会采用Gauss–Seidel method来近似求解线性方程组。
不过本文的重点在建立方程组而非求解方程组，因此不做讨论。）



# 例子

![](example.drawio.png)

如图所示，两个小球被一根杆连接。

对该系统的约束为：

1. A球固定在原地不动。
2. 杆子长度固定为$\sqrt{2}$。

使用图中记号，则约束可记为：

$$
C(t) = \begin{bmatrix}
	x_A \\
	y_A \\
	(x_B-x_A, y_B-y_A)^2-2
\end{bmatrix}
= \mathbb{0}
$$

约束函数$C$关于$q$的梯度为：

$$
\nabla C = \left[\begin{matrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\2 x_{A} - 2 x_{B} & 2 y_{A} - 2 y_{B} & - 2 x_{A} + 2 x_{B} & - 2 y_{A} + 2 y_{B}\end{matrix}\right]
$$

设外力为重力（$g$为重力加速度常数）：

$$
F_E = \begin{bmatrix}
	0 \\
	-g \\
	0 \\
	-g
\end{bmatrix}
$$

设两小球质量分别为$m_A, m_B$。

记$v=[v_A^1, v_A^2, v_B^1, v_B^2]^T$为当前的系统速度。

由

$$
\left\{
\begin{aligned}
	a^* &:= M^{-1} F_E \\
	v^* &:= v + \Delta t a^* \\
	q^* &:= q + \Delta t v^*
\end{aligned}
\right.
$$

可算得$q^*$：

$$
q^* = \left[\begin{matrix}\Delta t v^{1}_{A} + x_{A}\\\Delta t \left(- \frac{\Delta t g}{m_{A}} + v^{2}_{A}\right) + y_{A}\\\Delta t v^{1}_{B} + x_{B}\\\Delta t \left(- \frac{\Delta t g}{m_{B}} + v^{2}_{B}\right) + y_{B}\end{matrix}\right]
$$

将$\nabla C$与$q^*$代入系统方程组：

$$
C(q^* + M^{-1}\nabla C^T \lambda) = 0
$$

并取已知值为：

$$
\begin{aligned}
	q_A = (0, 0) \\
	q_B = (1, -1) \\
	v_A = (0, 0) \\
	v_B = (0, 0) \\
	m_A = 1 \\
	m_B = 1 \\
\end{aligned}
$$

则可由系统方程组解得$\lambda$：

$$
\lambda = 
\left[\begin{matrix}- \frac{\Delta t^{2} g}{2} + \frac{\sqrt{- \Delta t^{4} g^{2} + 4}}{2} - 1\\\frac{3 \Delta t^{2} g}{2} - \frac{\sqrt{- \Delta t^{4} g^{2} + 4}}{2} + 1\\- \frac{\Delta t^{2} g}{4} + \frac{\sqrt{- \left(\Delta t^{2} g - 2\right) \left(\Delta t^{2} g + 2\right)}}{4} - \frac{1}{2}\end{matrix}\right]
$$

代入$q' = q^* + M^{-1}\nabla C^T \lambda$，
可算得:

$$
q' = \left[\begin{matrix}0\\0\\- \frac{\Delta t^{2} g}{2} + \frac{\sqrt{- \Delta t^{4} g^{2} + 4}}{2}\\- \frac{\Delta t^{2} g}{2} - \frac{\sqrt{- \Delta t^{4} g^{2} + 4}}{2}\end{matrix}\right]
$$

若$\Delta t = 0.001, g=10$，则：

$$
q' = \left[\begin{matrix}0\\0\\0.9999949999875\\-1.0000049999875\end{matrix}\right]
$$

也就是A球保持不动，B球向左下角移动，与预期相符。

> 读者可能会发现在求解系统方程组$C(q^*+M^{-1}\nabla C \lambda)=0$的过程中，
> 由于$C$非线性，所以会得到两个解。
> 而另一个解的$\lambda$为：
>
> $$
> \lambda = \left[\begin{matrix}- \frac{\Delta t^{2} g}{2} - \frac{\sqrt{- \Delta t^{4} g^{2} + 4}}{2} - 1\\\frac{3 \Delta t^{2} g}{2} + \frac{\sqrt{- \Delta t^{4} g^{2} + 4}}{2} + 1\\- \frac{\Delta t^{2} g}{4} - \frac{\sqrt{- \left(\Delta t^{2} g - 2\right) \left(\Delta t^{2} g + 2\right)}}{4} - \frac{1}{2}\end{matrix}\right]
> $$
>
> 由它可算得 $q'$:
>
> $$
> q' = \left[\begin{matrix}0\\0\\-1.0000049999875\\0.9999949999875\end{matrix}\right]
> $$
>
> 该解对应的是一个镜像情况，
> 该情况也满足约束$C(q')=0$，
> 此时B球沿直线$y=x$翻转到了左上角，
> 显然该解是应当被舍弃的。
> （可能有某种方法能够用来判定哪个解应当被舍弃？么，不过反正一般都会线性化$C(q')=0$的，所以可能不是大问题。）

计算用的代码：[colab](https://colab.research.google.com/drive/1bS35qZcegSK24-KgLQh4PmgnohC2vfch?usp=sharing)
（我非常推荐使用sympy进行符号计算）



# 参考文献
我在文中并没有引用任何一篇参考文献（因为我懒），
不过我依然想把催生了这篇文章的文献列于此处，
以供感兴趣的读者参考。

1. Müller, M., Heidelberger, B., Hennix, M. & Ratcliff, J. Position based dynamics. Journal of Visual Communication and Image Representation 18, 109–118 (2007).
2. Macklin, M., Müller, M. & Chentanez, N. XPBD: position-based simulation of compliant constrained dynamics. in Proceedings of the 9th International Conference on Motion in Games 49–54 (Association for Computing Machinery, 2016). doi:10.1145/2994258.2994272.
3. Bender, J., Müller, M. & Macklin, M. Position-Based Simulation Methods in Computer Graphics. (2015) doi:10.2312/egt.20151045.
4. Bender, J., Erleben, K. & Trinkle, J. Interactive Simulation of Rigid Body Dynamics in Computer Graphics. Computer Graphics Forum 33, 246–270 (2014).


# 更新日志

* 2023-3-14：重写条件二动量守恒，更改为由$F_C \cdot \mathbf{1} = 0$推得动量守恒，并新增条件三。
* 2023-3-13：将系统动量计算从$mq$修正为$mv$。
