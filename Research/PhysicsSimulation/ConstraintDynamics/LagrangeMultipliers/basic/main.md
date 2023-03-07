---
title: 约束动力学(Constrained Dynamics)：拉格朗日乘数法(Lagrange Multipliers)
zhihu-tags: 物理仿真, 
zhihu-url: https://zhuanlan.zhihu.com/p/612020467
---
本文将讨论使用 **拉格朗日乘数法(Lagrange Multipliers)** 对受约束的粒子系统进行物理仿真的过程。

（“拉格朗日乘数法”这名字是[4]里这么叫的，在[5]里它被叫做Lagrangian constraint-based method。）

（这里的“拉格朗日”和拉格朗日力学没有任何关系，拉格朗日乘数法是一种maximal coordinate method。）

（就我所知，该方法应该是在[1]中被最早提出。）


# 记号

* $t$表示某个时刻，也表示时间变量。
* $x$表示某个空间坐标。
* $q$表示系统状态。
* $\dot{f} = \frac{\partial f}{\partial t}$
* $\ddot{f} = \frac{\partial^2 f}{\partial t^2}$
* $\nabla f = \frac{\partial f}{\partial q}$

# 问题描述
太长不看版：系统状态为$q\in R^n$，约束为$C=0, C\in R^m$，外力为$F_e$，待求的约束力为$F_c$。


%%%%%%%%%%%%%%%%%%%

考虑一个受约束的粒子系统：

该系统中有$N_p$个粒子，
每个粒子都有$N_f$个自由度
（例如一个三维空间中的粒子会在xyz三个方向上各有一个自由度，合计3个自由度），
用列向量$q_i=[x_i^1, x_i^2, \dots, x_i^{N_f}]^T$表示第$i$个粒子的状态，
用列向量$q=[q_1^T, q_2^T, \dots, q_{N_p}^T]^T$表示系统状态。
设$n = N_p N_f$，
则$q \in R^n$。

该系统的运动受牛顿第二定律$F=am$控制。

第$i$个粒子的质量为$m_i$，
它不随时间发生变化，
在整个仿真过程中都为常量。
并设向量$\mathbf{m}_i=[m_i, m_i, \dots, m_i]^T \in R^{N_f}$。
设质量矩阵$M = \text{diag}(\mathbf{m}_1, \mathbf{m}_2, \dots, \mathbf{m}_{N_p})$。

该系统受到$N_c$个约束，
第$i$个约束表示为$C_i(q,t)=0$，
即系统状态$q$在$t$时刻必须满足$C_i(q,t)=0$。
称$C_i$为约束函数。
若$C_i$约束了系统的$N_c^i$个自由度的话，
那么$C_i$就是$R^n \rightarrow R^{N_c^i}$的函数。
设总的约束函数为$C=[C_1^T, C_2^T, \dots, C_{N_c}^T]^T$，
则系统要满足的总约束为$C(q,t)=0$。
设$m=\sum_i N_c^i$，
则$C: R^n\rightarrow R^m$。

（注：本文只考虑完整约束Holonomic constraints）

该系统受到外力影响，
设第$i$个粒子受到的合外力为$F_e^i \in R^{N_f}$，
并设系统受到的总的合外力为$F_e=[{F_e^1}^T, {F_e^2}^T, \dots, {F_e^{N_p}}^T]^T$。

显然，如果只有外力$F_e$作用的话，
系统状态$q$一般不会满足约束$C(q,t)=0$。
因此，
我们的目标是求得约束力，
使该系统在约束力的作用下系统状态$q$能始终满足约束$C(q,t)=0$。

设第$i$个粒子受到的合约束力为$F_c^i \in R^{N_f}$，
并设系统受到的总的合约束力为$F_c=[{F_c^1}^T, {F_c^2}^T, \dots, {F_c^{N_p}}^T]^T$。

则我们的目标即为求得约束力$F_c$，使由牛顿第二定律$F_c + F_e = Ma$解出的系统加速度$a$能让下一时刻$t'$的新的系统状态$q'$满足约束$C(q', t')=0$。

下文将讨论该如何构建方程组求解约束力$F_c$。


# 条件一、$\ddot{C}=0$
假设系统状态$q$在$t$时刻满足约束$C(q,t)=0$，
并进一步地满足约束函数关于时间的变化量为零：$\dot{C}(q,t)=\frac{\partial C}{\partial t}=0$。
那么只要让约束函数关于时间的二阶导为0，
约束函数的取值就将始终为0：

$$
\ddot{C}(q,t) = 0
$$

只要$F_c$满足该条件，那么系统状态就将总是向着满足约束的方向发展。



# 条件二、$F_c = \nabla C^T \lambda$
我们希望约束力是系统内力，
而在不考虑热力学因素的情况下，
系统内力总是不做功的，
因此约束力做的系统总功应当为0。

> 绝大多数文献中都是由达朗贝尔原理推出的约束力不做功，例如[1][2][3][4]。
> 但达朗贝尔原理实际上说的是合外力与惯性力在满足约束的位移下所做的功为零，而并没有说约束力不做功。
> 
> 事实上，如果一个约束的约束力在满足约束的位移下做功为零的话，那么该约束被称为理想约束(ideal constraint)。

假设系统状态$q$在经过一个不消耗时间的微小位移$\delta q$后依然满足约束，即$C(q+\delta q, t) = 0$（通常称$\delta q$为虚位移）。

那么约束力在该位移下所做的功即为$W_c = F_c \cdot \delta q$，
要使约束力不做功，也就是要让$W_c = F_c \cdot \delta q = 0$，即$F_c$垂直于$\delta q$：

$$
F_c \perp \delta q
$$

如果将$C(q)=0$看成是在$R^n$空间中的一个曲面的话
（即所有满足$C(q)=0$的$q$都属于这个曲面，这个曲面上的所有点$q$也都满足$C(q)=0$），
那么$\delta q$就是该曲面上$q$点处的一个切向量。

由$\delta q$的任意性可知，
要让$F_c$对任意$\delta q$都满足$F_c \perp \delta q$，
就是要让$F_c$垂直于曲面$C(q)=0$在$q$点处的切平面，
也就是要让$F_c$平行于曲面$C(q)=0$在$q$点处的法线：

$$
F_c = \nabla C^T \lambda
$$

其中$\nabla C = \frac{\partial C}{\partial q}$为曲面法向量，$\lambda$为未知的$m$维列向量（通常称$\lambda$为拉格朗日乘数Lagrange Multipler）。



# 系统方程组
联立条件一、条件二、运动方程（$F=am$），可得系统方程组：

$$
\left\{
\begin{aligned}

& \ddot{C} = 0 \\
& F_c = \nabla C^T \lambda \\
& F_c + F_e = Ma

\end{aligned}
\right.
$$

其中

* $\lambda, a, F_c$为待求变量，包含$m+n+n$个未知数。
* 条件一$\ddot{C}=0$可提供$m$个方程。
* 条件二$F_c = \nabla C^T \lambda$可提供$n$个方程。
* 运动方程$F_c + F_e = Ma$可提供$n$个方程。

因此未知数数量等于方程数量，该方程组要么无解，要么有唯一解。



# 例子

![](example.drawio.png)

如图所示，两个小球被一根杆连接。

对该系统的约束为：

1. A球固定在原地不动。
2. 杆子长度固定为$\sqrt{2}$。

假设当前状态下两小球满足约束并且当前速度为零。

使用图中记号，则约束可记为：

$$
C(t) = \begin{bmatrix}
	x_A \\
	y_A \\
	(x_B-x_A, y_B-y_A)^2-2
\end{bmatrix}
= \mathbb{0}
$$

设外力为重力（$g$为重力加速度常数）：

$$
F_e = \begin{bmatrix}
	0 \\
	-g \\
	0 \\
	-g
\end{bmatrix}
$$

设两小球质量分别为$m_A, m_B$。

代入上文中给出的系统方程组中（为了方便直观，此处重复一遍）：

$$
\left\{
\begin{aligned}

& \ddot{C} = 0 \\
& F_c = \nabla C^T \lambda \\
& F_c + F_e = Ma

\end{aligned}
\right.
$$

该方程组比较复杂的项是$\ddot{C}, \nabla C$，所以先简单列一下。
设$q_A=[x_A, y_A]^T, q_B = [x_B, y_B]^T, v=\dot{q}$，可以算得：

$$
\ddot{C}(t) = \begin{bmatrix}
	a_A \\
	2(v_B-v_A)^2 + 2(q_B-q_A) \cdot (a_B - a_A)
\end{bmatrix}
$$

$$
\nabla C^T = \left[\begin{matrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\2 x_{A} - 2 x_{B} & 2 y_{A} - 2 y_{B} & - 2 x_{A} + 2 x_{B} & - 2 y_{A} + 2 y_{B}\end{matrix}\right]
$$

设当前时刻的位移、速度和质量为：

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

则可以求解上面的系统方程组，得到：

$$
\begin{aligned}
	\lambda = \begin{bmatrix}
		-\frac{g}{2} \\
		\frac{3g}{2} \\
		-\frac{g}{4} \\
	\end{bmatrix} \\
	F_c = \begin{bmatrix}
		0 \\
		g \\
		-\frac{g}{2} \\
		\frac{g}{2} \\
	\end{bmatrix} \\
	a = \begin{bmatrix}
		0 \\
		0 \\
		-\frac{g}{2} \\
		-\frac{g}{2} \\
	\end{bmatrix}
\end{aligned}
$$

A的加速度为0，保持原地不动。
B的加速度向左下角。
结果正确。

这是计算用的代码（$\ddot{C}$是我手算的）：[colab](https://colab.research.google.com/drive/1JvgwRQrSH8tJ2ONWzlaroH7KvxSAH01o?usp=sharing)。
（我非常推荐使用sympy来进行符号运算）


# 一些本文没有讨论的
理论上来说保持$\ddot{C}=0$就能保证$C=0, \forall t$，
但实际上在数值积分过程中总是会出现$C\neq 0$的情况。
因此需要加一些修正项来维持$C=0$，请参考[2]或者[3]。


# 参考文献

1. Witkin, A., Gleicher, M. & Welch, W. Interactive dynamics. in Proceedings of the 1990 symposium on Interactive 3D graphics 11–21 (Association for Computing Machinery, 1990). doi:10.1145/91385.91400.
2. Andrew, W. & David, B. Physically Based Modeling. https://www.cs.cmu.edu/~baraff/sigcourse/ (1997).
3. Daniel, C. Constraints Derivation for Rigid Body Simulation in 3D - Real-Time Physics Simulation Forum. https://pybullet.org/Bullet/phpBB3/viewtopic.php?t=9541 (2013).
4. Bender, J., Erleben, K. & Trinkle, J. Interactive Simulation of Rigid Body Dynamics in Computer Graphics. Computer Graphics Forum 33, 246–270 (2014).
5. Mirtich, B. & Canny, J. Impulse-based simulation of rigid bodies. in Proceedings of the 1995 symposium on Interactive 3D graphics 181-ff. (Association for Computing Machinery, 1995). doi:10.1145/199404.199436.
