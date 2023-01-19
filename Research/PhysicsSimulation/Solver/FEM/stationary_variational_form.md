# 1. 变分形式

## 1.1 边值问题

欲求解**边值问题**([Boundary value problem](https://en.wikipedia.org/wiki/Boundary_value_problem))：

$$
\left\{
\begin{aligned}
	\mathcal{L}(u) &= 0, \quad x \in \Omega \\
	\mathcal{B_i}(u) &= 0, \quad i=1,2,\dots, n_B
\end{aligned}
\right.
$$

其中$\mathcal{L}(u)=0$为微分方程，例如$\mathcal{L}(u)=f+u''$；$\mathcal{B}_i(u)=0$为边界条件，例如$\mathcal{B}_i(u)=u(x_i)-g(x_i)$；$\Omega$为定义域；$u$为关于$x$的未知函数。

理想目标是找到满足边值问题的$u$。



## 1.2. 求解策略：试函数法

我们采取的求解策略是在**试空间(trial space)**$V$中找一个完全满足边界条件$\mathcal{B}_i(u)=0$、并尽可能满足微分方程$\mathcal{L}(u)=0$的近似解$u\in V$（被称为**试函数trial function**）。

例如试空间可能是$V=\{kx+b: k,b \in R\}$，
显然，能被该空间完全满足的微分方程并不多，
例如微分方程$u''=2$就永远不可能在$V=\{kx+b: k,b \in R\}$中找到解，因为$(kx+b)''\equiv 0$。

设边值问题的精确解为$u_e$，
我们的期望是近似解能尽可能地接近精确解，即它俩的差在某种模下尽可能小：$\min_{u\in V}||u_e-u||$。

但我们不知道精确解$u_e$的解析式，所以没法直接求$\argmin_{u\in V}||u_e-u||$。



## 1.3 Céa引理、变分形式与伽辽金法

[**Céa引理**](https://en.wikipedia.org/wiki/C%C3%A9a%27s_lemma)（见[2]的2.8.1）指出当一些有关$u$和边值问题的条件被满足时，有：

$$
||u_e-u|| \leq C\min_{v\in V} ||u_e-v|| , \quad C \text{ is constant}
$$

即近似解$u$关于$V$中的最优解呈线性关系。
因此我们的目标可以转为找到满足Céa引理条件的$u$。

Céa引理的条件比较复杂，我们一般也不会去验证，所以这里我们只挑选其中最重要的一条，它对我们计算近似解$u$有用：

$$
\begin{aligned}
R := &\mathcal{L}(u) \\
(R,v) &= 0 \quad \forall v \in V \\
\end{aligned}
$$

其中$(R,v) = \int_\Omega Rv dx$为函数内积（或称为$L^2$内积）。

也就是将近似解$u$代入微分方程$\mathcal{L}$后得到的 **残值$R$** 要与$V$中的任意函数$v$都内积为0（即$R$与$V$正交）。

通常称$(R,v)=0, \forall v \in V$为原边值问题的 **变分形式(variational formulation)** ，
并称通过求解该变分形式来获取原边值问题的近似解的方法为**伽辽金法(Garlekin Method)** 。

> 伽辽金法是一种**加权残值法(Weighted Residual Method)** 。
> 加权残值法也是求解变分形式来获取近似解，不过它的变分形式为：
> $$
> (R,v) = 0 \quad \forall v \in W
> $$
> 其中$W$为有别于试空间$V$的另一个空间，它被称为*test space*，而$v\in W$被称为*test function*。
> 伽辽金法就是当$W=V$时的加权残值法。



## 1.4. 强形式与弱形式

通过对$(R,v)$应用分部积分，有时可以降低对试函数$u$的可导性要求。
例如当$\mathcal{L}(u)=u'', \Omega=[0,1]$时：

$$
\begin{aligned}
(R, v) &= \int_\Omega u''vdx \\
&= \int_\Omega vdu' \\
&= \int_\Omega u'v'dx + u'v|^1_0 \\
\end{aligned}
$$

可以看到，原本$(R,v)$的计算要求$u$有二阶导数$u''$，但在经过一步分部积分后就只要一阶导数$u'$了。

一般地，我们将$(R,v)=0$经过分部积分后得到的形式称为**弱形式(weak formulation)** ，记为：

$$
F(u;v)=0 \quad \forall v \in V
$$

而原本那个有更高可导性要求的形式则称为 **强形式(strong formulation)** 。
强形式和弱形式都是变分形式，只是对试函数$u$的可导性要求不同而已。

特别地，实际问题中经常碰到满足双线性性质的$F(u;v)$，即满足如下性质的$F(u;v)$：

$$
\begin{aligned}
F(u+w;v) &= F(u;v) + F(w;v) \\
F(u;v+w) &= F(u;v) + F(u;w) \\
\end{aligned}
$$

称满足该性质的$F(u;v)$为双线性形式(bilinear form)，此时弱形式更常见的记法为：

$$
a(u,v) = L(v) \quad \forall v \in V
$$

其中$a(u,v)$为双线性形式，$L(v)$为线性形式，即满足$L(v+w)=L(v)+L(w)$。


## 1.5. 边界条件

至今我们都只关注在边值问题中的微分方程部分$\mathcal{L}(u)=0$，
而没有讨论边界条件$\mathcal{B}_i(u)=0$。

为了简化问题，这里我们只允许两类边界条件：

1. **狄利克雷边界条件(Dirichlet boundary condition)** ：$\mathcal{B}_i(u)=u(x_i)-g(x_i)$，$g$为某个已知函数。
2. **诺依曼边界条件(Neumann boundary condition)** ：$\mathcal{B}_i(u)=u'(x_i)-g(x_i)$，$g$为某个已知函数。


### 1.5.1. 狄利克雷条件

为了让近似解$u$完全满足狄利克雷边界条件，我们修改试空间，使$\forall v \in V: \mathcal{B}_i(v)=0$，
即让试空间$V$中的所有函数都满足狄利克雷边界条件，
那么近似解$u\in V$自然也就满足狄利克雷边界条件了。

不过要注意这一做法仅适用于齐次狄利克雷边界条件$\mathcal{B}_i(v) = v(x_i) = 0$，
而对非齐次的狄利克雷边界条件$\mathcal{B}_i(v)=v(x_i) = C \neq 0$ 如果也使用该方法的话，
就会导致$V$不可能是线性空间：

$$
\begin{aligned}
&\qquad v_1, v_2 \in V \\
&\Rightarrow v_1(x_i)=v_2(x_i)=C \\
&\Rightarrow v_1(x_i)-v_2(x_i) = 0 \neq C \\
&\Rightarrow v_1 - v_2 \notin V
\end{aligned}
$$

而$V$如果不是线性空间的话，也就没法在$V$中找到一组基$\{\psi_i\}$使得$\forall v \in V: v = \sum c_i \psi_i$。
这会给我们求解$(R,v)=0, \forall v \in V$时带来麻烦，
因为我们没法利用$(R,v)$的线性性质来把它转换为$(R, \psi_i)=0$了。

所以非齐次的狄利克雷边界条件处理起来是需要一些技巧的。
本文将跳过这部分，请参阅[1]的1.11节和第4章。

【TODO：[1]中的讨论缺乏理论支撑，而[2]中的理论分析则仅对齐次狄利克雷边界条件进行，我需要再去查阅一下对非齐次狄利克雷边界条件进行的理论分析】



### 1.5.2. 诺依曼边界条件

为了让近似解$u$满足诺依曼边界条件$\mathcal{B}_i(u)=u'(x_i)-g(x_i)=0$，我们需要使用弱形式。

还是沿用之前的例子，当$\mathcal{L}(u)=u'', \Omega=[0,1]$时，对$(R,v)$应用分部积分得到：

$$
\begin{aligned}
(R, v) &= \int_\Omega u'v'dx + u'v|^1_0 \\
\end{aligned}
$$

将变分形式$(R,v)=0, \forall v \in V$写为常见的弱形式：

$$
\begin{aligned}
	a(u,v) = L(v) \quad \forall v \in V \\
\end{aligned}
$$

$$
\text{where}\left\{
\begin{aligned}
	& a(u,v) = \int_\Omega u'v' dx \\
	& L(v) = u'(0)v(0) - u'(1)v(1) \\
\end{aligned}
\right.
$$

注意到$L(v)$中包含$u'(0)$和$u'(1)$，也就是包含了所有可能的诺依曼。
假设我们有诺依曼边界条件$u'(0)=0, u'(1)=1$，则可以联立得到方程组：

$$
\left\{
\begin{aligned}
	a(u,v) &= L(v) \quad \forall v \in V \\
	u'(0) &= 0 \\
	u'(1) &= 1 \\
\end{aligned}
\right.

$$

该方程组的解$u$一定同时满足弱形式和诺依曼边界条件。

（别忘了，Céa引理说明$u$满足弱形式时它一定是试空间里最接近精确解$u_e$的函数）


### 1.5.3. 别名

* 狄利克雷边值条件被显式地写进了试空间的条件中，因此通常被称为*essential boundary condition* 。
* 诺依曼边值条件在推导弱形式时被自然地联立进弱形式中，因此通常被称为*natural boundary condition* 。


# 有限元试空间

我们希望trial space $V$ 能让弱形式
$a(u,v) = L(v) \quad \forall v \in V$ 的计算方便又轻松。
其中一个选项就是将分段多项式函数作为trial function $u$ 。

将定义域$\Omega$剖分，得到剖分$\mathcal{T}$。
设剖分中每个单元(element)$K_i$内的插值函数为$\mathcal{I}_{K_i}f$，
则trial function为全局的插值函数$\mathcal{I}f|_{K_i} = \mathcal{I}_{K_i}f$，
trial space $V = \{\mathcal{I}f: f \in \mathcal{F}\}$。

为单元$K$内的局部插值函数$\mathcal{I}_{K}f$做定义。
设每个单元中都有三元组$(K, \mathcal{P}, \mathcal{N})$：

* $K$为该单元的定义域，称为单元域element domain。
* $\mathcal{P}$为$K$上的一个有限维函数空间，称为shape function的所在空间。
* $\mathcal{N}=\{N_1, N_2, \dots, N_k\}$为$P$的对偶空间$P'$中的一组基，称为nodal variables。
	* $\mathcal{N}$的一个例子是$N_i(v)=v(x_i)$，也就是说$N_i$接收$\mathcal{P}$中的一个函数，然后返回该函数在$x_i$上的取值。
	* 另一个例子是$N_i(v)=v'(x_i)$，此时$N_i$接收$\mathcal{P}$中的一个函数，然后返回该函数在$x_i$上的一阶导数。

若$\mathcal{P}$中的一组基$\{\phi_1, \phi_2, \dots, \phi_k\}$满足$N_i(\phi_j)=\delta_{ij}$（$i=j \Rightarrow \delta_{ij}=1 ; i\neq j \Rightarrow \delta_{ij}=0$），则称这组基$\{\phi_i\}$为nodal basis。

* 例如当$N_i(v)=v(x_i)$时，$N_i(\phi_j)=\phi_j(x_i)$，若$\{\phi_j\}$为nodal basis的话，则$\phi_j(x_i)=\delta_{ij}$意味着$\phi_j$是一个仅在$x_j$处取值为1而在其他所有$x_i$处都取值为0的函数（例子就是克罗内克函数$\delta_{ij}$）。

则局部插值函数$\mathcal{I}_{K}f$定义为：

$$
\mathcal{I}_{K}f = \sum_{i=1}^k N_i(f)\phi_i
$$


不同的$(K, \mathcal{P}, \mathcal{N})$就构成了不同类型的有限元:

* $K$为三角形时为Triangular Element
	* $N_i(v)=v(z_i)$时，该有限元为Lagrange Element
		* 可以选取不同的$\mathcal{P}$和$\mathcal{N}$，只要满足$\mathcal{N}$为$\mathcal{P}$的一组基即可。
		* 例如$\mathcal{P}=\mathcal{P}_1$，$\mathcal{N}=\{N_1, N_2, N_3\}$，$z_i$为$K$的三个顶点。
			* $\mathcal{P}_k$为由次数小于等于$k$的多项式构成的函数空间。
	* Hermite Element会要求有$N_i(v)=v'(z_i)$，Argyris Element会要求有$N_i(v)=v''(z_i)$，这两类在此略过。
* $K$为四边形时为Rectangular Element，其他形状时也都类似，例如Tetrahedron Element，Cuboid Element。

而不同类型的有限元就定义了不同的局部插值函数$\mathcal{I}_Kf$，从而也就定义了不同的全局插值函数$\mathcal{I}f$，产生了不同的trial space $V=\{\mathcal{I}f: f\in \mathcal{F}\}$。

用有限元定义的全局插值函数具有下面两个在Garlekin Method里特别实用的性质：

* 3.3.17连续性：Lagrange Element和Hermite Element定义的$\mathcal{I}f \in C^0$，Angyris Element定义的$\mathcal{I}f \in C^1$。
	* 这确保了一阶导数的存在。
* 误差估计
	* 4.4.28导数误差估计：用Lagrange, Hermite, Angyris Element定义的$\mathcal{I}f$在使用Garlekin Method求解$u$时都满足误差估计$||u-\mathcal{I}u||_{H^1(\Omega)} \leq C h^m||u||_{H^{m+1}(\Omega)}$
		* 其中$C$为一个与有限元单元形状有关的常数，$h\in (0,1]$为有限元单元相对于定义域全局的大小比例（也就是$h$越小，剖分得就越细、单元就越小），$m$为有限元定义中的$\mathcal{P}$对应的阶次（即$P=P^m$），$H^m=W^m_2$为索博列夫空间
		* 可以大致理解为：导数误差$||u'-\mathcal{I}u'||$总是关于$h^m$成线性关系
	* 5.4.8解误差估计：$||u-\mathcal{I}u||_{L^2(\Omega)} \leq C h^{m+1} ||u||_{H^{m+1}(\Omega)}$
		* 可以大致理解为：误差$||u-\mathcal{I}u||$总是关于$h^{m+1}$成线性关系
	* 总的来说就是当有限元定义中使用$m$阶多项式时，误差$||u-\mathcal{I}u||=O(h^{m+1})$，$O(\cdot)$为渐进大$O$记号。






# 参考文献
【TODO】