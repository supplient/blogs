本文为[1]的第0~5章的读书笔记。


-------------


欲求解边值问题（泊松方程的一维形式）：

$$
-u'' = f \text{, where } x \in [0, 1]
$$

$$
\left\{
\begin{aligned}
u(0)&=0 \\ 
u'(1)&=0
\end{aligned}
\right.
$$

其中$u$为关于$x$的未知函数，$f$为关于$x$的已知函数，$u'=\frac{du}{dx}, u''=\frac{d^2u}{dx^2}$。

-------

第一步是给出边值问题的弱形式的定义。

首先引入**变分空间(variational space)**$V$，它是下述空间的一个**子空间(subspace)**（子空间定义见[1]的2.2.3，简单来说就是线性封闭子集）：

$$
\Theta=\{v\in H^1(\Omega): v(0)=0\}
$$

其中$\Omega=\{x: x\in [0, 1]\}$，$H^1=W^1_2$为索博列夫空间(Sobolev spaces)（其定义见[1]的1.3.1）。

$v(0)=0$是边值问题中的本质边界条件(essential boundary condition, 或称为Dirichlet boundary condition，见[1]的0.1.6)。

取任意$v\in V$，使它与已知函数$f$作内积：

$$
\begin{aligned}
(f, v) &= \int_0^1 f(x)v(x)dx \\
&= \int_0^1 -u''(x)v(x)dx \\
&= \int_0^1 u'(x)v'(x)dx & [v(0)=0]
\end{aligned}
$$

记**变分形式(variational form)**$a(\cdot,\cdot)$为：

$$
a(u, v) = \int_0^1 u'(x)v'(x) dx
$$

【TODO：分部积分那一步可以不做吗？我可以直接设$a(u,v)=\int_0^1 -u''(x)v(x)dx$吗？】

现在给出边值问题的**弱形式**(weak formulation，或称为**变分形式** variational formulation、**变分问题** variational problem）：

$$
\left\{
\begin{aligned}
	& u \in V \\
	& a(u, v) = (f, v) \quad \forall v \in V
\end{aligned}
\right.
$$


--------
第二步是证明弱形式的解也为原边值问题的解。

略去证明，参见[1]的0.1.4。

我们最后会得到的结论是若$u$满足弱形式：

$$
\left\{
\begin{aligned}
	& u \in V \\
	& a(u, v) = (f, v) \quad \forall v \in V
\end{aligned}
\right.
$$

，则$u$为原边值问题的一个解：

$$
-u'' = f \text{, where } x \in [0, 1]
$$

$$
\left\{
\begin{aligned}
u(0)&=0 \\ 
u'(1)&=0
\end{aligned}
\right.
$$


---------------
第三步是证明弱形式有且仅有一个解。

这一步要用到Lax-Milgram定理（见[1]中的2.7.7），在这里复述一遍该定理：

> *给定一个希尔伯特空间$(V, (\cdot,\cdot))$，一个连续的、强压的双线性形式$a(\cdot, \cdot)$，和一个连续线性泛函$F\in V'$，则存在唯一解$u \in V$满足$a(u,v)=F(v)\quad \forall v\in V$。*

因此为了应用Lax-Milgram定理来证明弱形式有且仅有一个解，我们需要证明如下条件：

1. 变分空间$V$和函数内积$(\cdot, \cdot)$构成一个希尔伯特空间$(V, (\cdot,\cdot))$。
2. 变分形式$a(\cdot, \cdot)$为连续的、强压的双线性形式。
3. 存在连续线性泛函$F$使得$F(v) = (f,v) \quad \forall v \in V$，其中$f$为边值问题中的已知函数。

第一个条件和第三个条件在此略去：第一个条件参见[1]的2.7.12，第三个条件我也不知道怎么证。

第二个条件中需要先解释一下*连续*、*强压*、*双线性形式*。

**双线性形式(bilinear form)** 为关于两个参数都呈线性的双变量函数，即是说$a(\cdot, \cdot)$为双变量形式当且仅当：

$$
\begin{aligned}
a(u, v+w) = a(u, v) + a(u, w) \\
a(u+w, v) = a(u, v) + a(w, v) \\
\end{aligned}
$$

一个双线性形式在一个带模线性空间$V$中**连续(continuous)** ，或称为 **有界(bounded)** 是指$\exist  C < \infty$：

$$
|a(u, v)| \leq C ||u||_V ||v||_V \quad \forall u,v \in V
$$

一个双线性形式在一个带模线性空间$V$中**强压(coercive)** ，或称为 **椭圆(elliptic)** 是指$\exist \alpha > 0$：

$$
\alpha(v, v) \geq \alpha ||v||_V^2 \quad \forall v \in V
$$

连续和强压的定义在[1]中的2.5.2出现。“强压”一词我没有找到统一的中文译名，因此参照的是日语翻译“強圧”。

下证第二个条件：变分形式$a(\cdot, \cdot)$为连续的、强压的双线性形式。

因为$a(u, v) = \int_0^1 u'v'dx$，所以有：

$$
\left\{
\begin{aligned}
a(u,v+w) &= \int_0^1 u'(v+w)'dx &= \int_0^1 u'v'dx + \int_0^1 u'w'dx  &= a(u,v) + a(u,w) \\
a(u+w,v) &= \int_0^1 (u+w)'v'dx &= \int_0^1 u'v'dx + \int_0^1 w'v'dx  &= a(u,v) + a(w,v) \\
\end{aligned}
\right.
$$

因此$a(\cdot, \cdot)$为双线性形式。

这里我们的带模线性空间是由变分空间$V$和函数内积$(\cdot, \cdot)$构成的希尔伯特空间$(V, (\cdot, \cdot))$。

$a(\cdot, \cdot)$的连续性在[1]的5.3节开头说是*obvious*，但可惜我不会证，所以在此略过。

而$a(\cdot, \cdot)$的强压性则是由[1]中的5.3.4给出，在此略过证明。

最后尽管略去了几乎所有证明（笑），但我们还是证明了希尔伯特空间$(V, (\cdot,\cdot))$，双线性形式$a(\cdot, \cdot)$和已知函数$f$满足Lax-Milgram定理的条件，因此可以应用该定理，从而证明了弱形式有且仅有唯一解。




-------------------
第四步是对$V$做出进一步限制，对于只有有限维的子空间$V_h \subset V$，给出伽辽金近似问题。

设$V_h \sub V$为$V$的有限维子空间，则**伽辽金近似问题(Galerkin approximation problem)** 为：

$$
\left\{
\begin{aligned}
	& u_h \in V_h \\
	& a(u_h, v) = (f, v) \quad \forall v \in V_h
\end{aligned}
\right.
$$

该定义出现在[1]的2.6.3。



------------------
第五步是证明近似问题有且仅有一个解。

该步骤和第三步相同，都是使用Lax-Milgram定理进行证明。

相较于第三步中对弱形式的证明而言，此处仅仅只是$V$变成了$V_h$，所以只需要证明$(V_h, (\cdot, \cdot))$也是希尔伯特空间即可。

因为$V_h$为$V$的子空间，由[1]的2.2.4可知，一个希尔伯特空间的子空间依然是希尔伯特空间，因此$(V_h, (\cdot, \cdot))$也是希尔伯特空间。

其余条件同第三步的证明（如[1]的2.7.13），因此可以应用Lax-Milgram定理，从而证明了近似问题有且只有一个解。



------------------
第六步是对近似问题的解进行误差估计，即要给$u-u_h$求一个上界。

我们通过Céa引理（见[1]的2.8.1）来给出误差估计。复述Céa引理如下：

> *若有如第四步中给出的近似问题，其满足$V$为一个希尔伯特空间的子空间，$a(\cdot, \cdot)$为一个连续的、强压的双线性形式，且$u$为该近似问题对应的变分问题的解，则该近似问题的解$u_h$满足：*
> $$
> ||u-u_h||_V \leq \frac{C}{\alpha}\min_{v\in V_h} ||u-v||_V
> $$
> *其中$C$和$\alpha$为[1]的2.5.2中连续性和强压性的系数。*

直观来讲就是求解近似问题得到的解$u_h$与原变分问题的解$u$之间的误差$||u-u_h||$总是关于能在$V_h$中能找到的最优解的误差$\min_{v\in V_h} ||u-v||$呈线性关系。

为了应用该定理需要证明其条件成立：

1. $(V, (\cdot, \cdot))$为希尔伯特空间
2. $a(\cdot, \cdot)$为一个连续的、强压的双线性形式

这两个条件都在第三步被证明了。

因此满足Céa引理的条件，对近似问题有误差估计：

$$
||u-u_h||_V \leq \frac{C}{\alpha}\min_{v\in V_h} ||u-v||_V
$$



-----------------------
第七步是剖分作用域$\Omega$，将其离散化为有限元集合，从而得到一个知道其基底的有限维子空间。

具体的离散化方法参见[1]的第三章，下文中我们不会特定在某一种离散化方法上，而总是假定采用的离散化方法满足各个定理的条件（通常来说采用常见的离散化方法就总是满足的）。

这一步后我们应当得到

* 作用域$\Omega$上的剖分$\mathcal{T}^h$。剖分(subdivision)的定义见[1]的3.3.8，简单来说就是不相交的子集集合，其并集为整个$\Omega$。其上标$^h$的含义见[1]的4.4.13，简单来说就是$h$越小、剖分得就越细。
* 一个全局插值估计$\mathcal{I}^hf$，它表示对$f$按当前的离散化方法进行插值估计，其定义见[1]的3.3.9，实质上就是在$\mathcal{T}^h$上的分片函数，在哪个finite element里就取哪个finite element的插值结果。



-----------------------
第八步是对离散化后得到的全局插值估计进行误差估计。

因为我们假定采用的离散化方法满足各个定理的条件，所以这一步我们直接套用[1]的4.4.28，得到$\forall u \in W^m_2(\Omega)$：

$$
||u-\mathcal{I}^hu||_{W^1_2(\Omega)} \leq C h^{m-1} ||u||_{W^m_2(\Omega)}
$$

【TODO：原文中右边是$|u|_{W^m_2(\Omega)}$，我不太清楚单杠的模是什么意思】

其中$m>l+n/2$，$l$为[1]的4.4.4的$(iii)$所定义的基底函数拥有的最高次连续导数的次数，$n$为$x\in R^n$的$n$。

事实上我们实际应用时只关心第八步的误差分析，它说明只要使用$m-1$阶的多项式就可以达到$h^m$的近似精度。


----------------------
第九步是拼接第八步和第六步，给出近似问题的具体的误差上界。

假设[1]的5.4.3成立，即$\mathcal{I}^h(V\cap C^k(\Omega)) \subset V_h$，则有：

$$
\min_{v\in V_h} ||u-v||_V \leq ||u-\mathcal{I}^hu||_V
$$

注意到$||\cdot||_{W^1_2(\Omega)} = ||\cdot||_{V}$，所以根据第八步的误差估计，可以得到：

$$
\begin{aligned}
\min_{v\in V_h} ||u-v||_V 
&\leq ||u-\mathcal{I}^hu||_V \\
&\leq  C h^{m-1} ||u||_{W^m_2(\Omega)} \\
\end{aligned}
$$

最后根据第六步的误差估计，可以得到近似问题的误差上界：

$$
||u-u_h||_V \leq Ch^{m-1}||u||_{W^m_2(\Omega)}
$$

这一步我们实际应用的时候其实不太关心的。





# 参考文献
1. Brenner, S. C. & Scott, L. R. The mathematical theory of finite element methods. (Springer, 2008).
