#! https://zhuanlan.zhihu.com/p/511502862
# 论文阅读：Fast Simulation of Mass-Spring Systems

本文为对[Fast Simulation of Mass-Spring Systems](https://www.cs.utah.edu/~ladislav/liu13fast/liu13fast.html)的阅读笔记。本文并非翻译性质或公式推导性质的文章，文章的结构和内容与原论文有极大出入，甚至记号都不一致。内容以我个人的理解为主，不过只要我理解没有问题，那本文介绍的方法和原论文里的应该是一致的。

若有不正之处，烦请指正。

# 一、隐式欧拉法
从使用隐式欧拉法求解牛顿运动方程开始：

$$
\begin{aligned}
x^{n+1} = x^n + Δtv^{n+1} \\
v^{n+1} = v^n + Δta^{n+1} \\
\end{aligned}
$$

假设加速度分为外力$F_{ext}$与内力$F_{int}$，且$F_{ext}$与$x$无关（或设它与$x^n$有关，而非$x^{n+1}$），$F_{int}$为$x$的函数，即$a^{n+1}=M^{-1}(F_{ext}+F_{int}(x^{n+1}))$。

把$a^{n+1}$代入上式中，并把$v^{n+1}$消掉，得到：

$$
x^{n+1}=x^n+Δtv^n+Δt^2M^{-1}(F_{ext}+F_{int}(x^{n+1}))
$$

设$\tilde{x}=x^n+Δtv^n+Δt^2M^{-1}F_{ext}$，并略去上标$n+1$，则有：

$$
M(x-\tilde{x})=Δt^2F_{int}(x)
$$

我们的目标是解出上式的$x$，式中左边的$x$是个线性项，在解方程时候很好处理，但右边的$F_{int}(x)$还没定义。

论文里认为$F_{int}$是个保守力，即是说它是由某种势能产生的力。设该势能为$U$：

$$
F_{int}=-∇U
$$

代入隐式欧拉法的方程里：

$$
\tag{1}
M(x-\tilde{x})=-Δt^2∇U(x)
$$

1式是不是线性方程组这就完全是由$U$的定义决定的了。


# 二、一个小例子

通常而言$∇U(x)$都不是关于$x$的线性项。

例如对于两个质点之间的弹性势能$U=\frac{1}{2}(||x_2-x_1||-l)^2$，$x_1, x_2$为质点位移，$l$为弹簧的rest length。其关于$x$的梯度$∇U$为：

$$
∇U = 
\begin{bmatrix}
	x_1-x_2-\frac{l}{||x_2-x_1||}(x_1-x_2) \\
	x_2-x_1-\frac{l}{||x_2-x_1||}(x_2-x_1) \\
\end{bmatrix}
$$

注意到$∇U$的非线性性质基本都是由$\frac{l}{||x_2-x_1||}$引入的。

引入变量$\hat{x}$:

$$
\hat{x} = 
\begin{bmatrix}
	\hat{x}_1 \\
	\hat{x}_2
\end{bmatrix}
=
\begin{bmatrix}
	\frac{l}{||x_2-x_1||}(x_1-x_2) \\
	\frac{l}{||x_2-x_1||}(x_2-x_1) \\
\end{bmatrix}
$$

则$∇U$变为：

$$
∇U = 
\begin{bmatrix}
	x_1-x_2-\hat{x}_1 \\
	x_2-x_1-\hat{x}_2 \\
\end{bmatrix}
$$

注意到如果我们认为$\hat{x}$是个与$x$无关的变量，那么$∇U(x)$就是个$x$的线性项了，于是1式的求解（隐式欧拉法的求解）就变成了个线性方程组求解了。

那么此时我们该怎么计算$\hat{x}$呢？显然我们得代入个$x$才能算出来呀。现在我们把上标$n+1$, $n$给取回来。我们想求的是$x^{n+1}$，我们假设$\hat{x}$与之无关的也是$x^{n+1}$，这就避免了1式变成$x^{n+1}$的非线性方程组。而我们已知的量是$x^n$，所以我们可以把$x^n$代入$\hat{x}$。

这本质就是把$∇U$的一部分用显式欧拉法的方法来处理了。


# 三、形式化：弹簧约束
我们把上一节中的小例子给形式化写一下。

设有一组弹簧约束$C=[C_1\ C_2\ \cdots\ C_m]^T$, $C_i=||x_{s_i}-x_{t_i}||-l_i$, 其中$s_i, t_i, l_i$为已知量。

则弹簧势能$U=\frac{1}{2}C^TC$，其梯度为

$$
∇U=∇C^TC = \begin{bmatrix}
	\sum_i\frac{∂C_i}{∂x_j}C_i
\end{bmatrix}_{n×1}
$$

这里为了简略，只写了第$j$项的表达式，$∇U$为一个n维的列向量。

与上一节一样，引入变量$\hat{x}$：

$$
\hat{x}=\begin{bmatrix}
	\frac{l_i}{||x_{s_i}-x_{t_i}||}(x_{s_i}-x_{t_i})
\end{bmatrix}_{m×1}
$$

为了方便，记$D_i=x_{s_i}-x_{t_i}$，则有：

$$
\frac{∂C_i}{∂x_j}C_i=
\left\{
\begin{aligned}
	&D_i - \hat{x}_i	&, \text{if}\ j=s_i \\
	-&D_i + \hat{x}_i	&, \text{if}\ j=t_i \\
	&0					&, \text{otherwise} \\
\end{aligned}
\right.
$$

显然，如果$\hat{x}$与$x$无关的话，那么$\frac{∂C_i}{∂x_j}C_i$就是个关于$x$的线性项，而求和$\sum_i\frac{∂C_i}{∂x_j}C_i$显然也是个关于$x$的线性项（n个线性项的和肯定还是线性项），所以此时$∇U$就是个关于$x$的线性项。

如果把这个$∇U$代回1式的话，那就是解个线性方程组了。


# 四、讨论
原文中是把该问题视为一个使用block coordinate descent分别对$\hat{x}, x$进行优化的二次优化问题，相当于是：
1. 第一次优化：把计算$\hat{x}(x^n)$的过程视为local step
2. 第二次优化：把求解隐式欧拉法方程的过程视为global step

实际的处理过程与我上文中讨论的其实是一样的，本质也就是在处理$∇U(x^{n+1})$时，把其中非线性的部分剥离出来单独用显式方法处理。

除此之外，注意到上文中没有更新速度。原文中采取了和XPBD一样的做法，将“外力和惯性速度”与“势能力”区分开来处理，然后对“外力和惯性速度”使用韦尔莱积分法。所以这里和XPBD的区别仅仅只是求解只有“势能力”的系统的运动方程时用了不同的方法。

总结来说，这篇论文（Projective Dynamics的前身）的关键点是：
* 抽离出$∇U$中的非线性部分，并用显式方法处理它，从而使得隐式欧拉法的求解方程变为一个线性方程组。

然后Projective Dynamics那篇论文我应该短时间内不会写它的paper reading，因为那篇论文的主要贡献是对连续体里的$∇U$给出各种各样抽离非线性部分的方法，但我对FEM不熟悉，所以看不太懂。

# 2022.5.10追记：与拟牛顿法的关系
在[Quasi-Newton Methods for Real-time Simulation of Hyperelastic Materials](https://www.cs.utah.edu/~ladislav/liu17towards/liu17towards.pdf)一文中，作者站的视角就和本文差不多了，他注意到PD的本质是一种拟牛顿法。拟牛顿法解方程就是用找东西去近似方程的一阶导数（最优化视角看的话，那就是找东西去近似目标函数的二阶导数）。

在这重新列一下1式，这是我们想解的方程：

$$
\tag{1}
M(x-\tilde{x})=-Δt^2∇U(x)
$$

我们把前文中“抽离$∇U$中的非线性部分”这一思想给泛化一下，设：

$$
∇U(x) = Lx+D(x)
$$

其中，$L$为一个$R^n→R^n$的线性映射，$Lx$即为关于$x$的线性项，$D(x)$为一个非线性函数。

代入1式得到：

$$
\tag{2}
(M+Δt^2L)x=M\tilde{x}-Δt^2D(x)
$$

Projective Dynamics的思想就是把2式右边的$D(x)$给用显式方法处理，认为$D(x)$与欲求的$x^{n+1}$无关，而与已知的$x^n$有关。从而使得2式是个线性方程组，可以直接快速求解。

关于显式方法处理$D(x)$，也可以理解为做泰勒展开：$D(x^{n+1})≈D(x^n)+∇D(x^n)(x^{n+1}-x^n)$，然后假设$∇D(x^n)=0$，那么就得到$D(x^{n+1})≈D(x^n)$。

所以如果不使用这一思想的话，就得求$∇D(x^n)$了。注意到

$$
\begin{aligned}
∇U &= Lx + D \\
\stackrel{两边求导}{⇒} H(U) &= L + ∇D
\end{aligned}
$$

所以要求$∇D$，也就是要求$U$的Hessian矩阵$H(U)$了。那二阶导数的计算量可就大了。

拟牛顿法就是找个矩阵去近似$H(U)$，这里设$H(U)(x^n)=L$也属于一种近似的方法。

然后这篇论文我最近也不会写paper reading，因为他主要贡献是材质刚度计算的问题，我对FEM不熟悉，看不懂。