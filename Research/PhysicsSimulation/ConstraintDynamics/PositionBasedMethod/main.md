---
title: 约束动力学(Constrained Dynamics)：基于位置的方法(Position Based Method)（检索用：PBD）
zhihu-tags: 物理仿真,
zhihu-url: https://zhuanlan.zhihu.com/p/613111930
---

本文将讨论使用 **基于位置的方法(Position Based Method)** 对受约束的粒子系统进行物理仿真的过程。

（Position Based Method这名字是我自己起的，与impulse based method相对。
因为本文内容相当于是Position Based Dynamics(PBD)的一个子集，
仅关注在受束系统下系统方程组的建立上，
因此为了避免让读者误以为这就是PBD的全部了，
我就另外起了一个名字。）

（笔者曾写过另一篇[PBD的阅读笔记](https://zhuanlan.zhihu.com/p/339879519)，
因所站视点不同，故另开此文。）



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


# 条件二、内力作用下动量守恒
由动量守恒定律可知，
如果约束力$F_C$为系统内力，
那么在它的作用下系统动量应当保持不变。

我们先将由约束力$F_C$引起的动量变化量给抽离出来，
展开$q'$：

$$
\begin{aligned}
q'
= & q+\Delta tv' \\
= & q+\Delta t(v+\Delta t a) \\
= & q + \Delta t v + \Delta t^2 M^{-1} F_E + \Delta t^2 M^{-1} F_C
\end{aligned}
$$

记

$$
\left\{
\begin{aligned}
	a^* &:= M^{-1} F_E \\
	v^* &:= v + \Delta t a^* \\
	q^* &:= q + \Delta t v^*
\end{aligned}
\right.
$$

$$
\Delta q = \Delta t^2 M^{-1} F_C
$$

于是$q'$可重写为：

$$
q' = q^* + \Delta q
$$

其中$\Delta q$为在约束力$F_C$的作用下系统状态的变化量。

我们希望在内力约束力$F_C$的作用下系统动量保持不变，
即：

$$
\begin{aligned}
p|_{q^*} &= p|_{q'} \\
\Rightarrow \Delta p :=& p|_{q'} - p|_{q^*} \\
=& Mq'\cdot \mathbf{1} - M q^* \cdot \mathbf{1} \\
=& M(q'-q^*) \cdot \mathbf{1} \\
=& M\Delta q \cdot \mathbf{1} = 0 \\
\end{aligned}
$$

为了进一步推导，
此处我们需要先对约束$C(q)=0$做一个假设：

> 若约束$C(q)=0$的约束力$F_C$为系统内力，
> 则约束函数$C$应满足：
> 
> $$
> \forall q \forall \lambda: \nabla C^T \lambda \cdot \mathbf{1} = \mathbf{0}
> $$
> 
> 其中 $\nabla C = \frac{\partial C}{\partial q}$.

例如，约束$C([x_1, x_2]^T)=x_1-x_2-1=0$总是满足该假设：

$$
\begin{aligned}
& \nabla C^T \lambda \cdot \mathbf{1} \\

= & \begin{bmatrix}
	1 \\
	-1
\end{bmatrix} \lambda \cdot \begin{bmatrix}
	1 \\
	1
\end{bmatrix} \\

= & \begin{bmatrix}
	\lambda \\
	-\lambda
\end{bmatrix} \cdot  \begin{bmatrix}
	1 \\
	1
\end{bmatrix} \\

= & \lambda -\lambda = 0

\end{aligned}
$$

为了让系统动量在内力作用下保持不变$\Delta p= M\Delta q \cdot \mathbf{1} = 0$，
我们设

$$
\Delta q = M^{-1} \nabla C^T \lambda
$$

则内力作用下的系统动量变化量$\Delta p$为：

$$
\begin{aligned}
\Delta p
=& M\Delta q \cdot \mathbf{1} \\
=& MM^{-1} \nabla C^T \lambda \cdot \mathbf{1} \\
=& \nabla C^T \lambda \cdot \mathbf{1} \\
\text{[假设 } &\forall q \forall \lambda: \nabla C^T \lambda \cdot \mathbf{1} = \mathbf{0} \text{]} \\
=& \mathbf{0} \\
\end{aligned}
$$

因此当$\Delta q = M^{-1} \nabla C^T \lambda$时，
若约束函数$C$满足$\forall q \forall \lambda: \nabla C^T \lambda \cdot \mathbf{1} = \mathbf{0}$，
则在该约束对应的约束力$F_C$作用下，
系统动量保持不变$\Delta p = 0$。

进一步地，
当$\Delta q = M^{-1} \nabla C^T \lambda$时，
若所有约束力为系统内力的约束函数$C$都满足
$\forall q \forall \lambda: \nabla C^T \lambda \cdot \mathbf{1} = \mathbf{0}$，
则动量守恒定律被满足。



# 系统方程组
列出至今为止我们的所有方程——

半隐式欧拉法：

$$
\left\{
\begin{aligned}
	q' = q + \Delta t v'\\
	v' = v + \Delta t a
\end{aligned}
\right.
$$

$$
a=M^{-1}(F_E+F_C)
$$

条件一：

$$
C(q')=\mathbf{0}
$$

重写$q'$：

$$
\left\{
\begin{aligned}
	a^* &:= M^{-1} F_E \\
	v^* &:= v + \Delta t a^* \\
	q^* &:= q + \Delta t v^*
\end{aligned}
\right.
$$

$$
\Delta q = \Delta t^2 M^{-1} F_C
$$

$$
q' = q^* + \Delta q
$$

条件二：

$$
\Delta q = M^{-1} \nabla C^T \lambda
$$

联立它们，经化简可以得到一个关于$\lambda$的系统方程组：

$$
C(q^* + M^{-1}\nabla C^T \lambda) = 0
$$

$\lambda$为$m$维向量，该方程组也提供了$m$个方程，
因此当该方程组为线性方程组且各方程之间线性无关时，
则总是要么有唯一解，要么无解。

解出$\lambda$后，

1. 由$\Delta q=M^{-1}\nabla C^T \lambda,\quad q'=q+\Delta q$可以算出下一时步的系统状态$q'$。
2. 再由$q'=q+\Delta t v'$可以算出下一时步的系统速度$v'$。

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
