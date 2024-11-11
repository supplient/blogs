ref:

1. [P. J. Schneider and D. H. Eberly, Geometric tools for computer graphics. in The Morgan Kaufmann series in computer graphics and geometric modeling. Amsterdam: Boston Morgan Kaufmann Publishers, 2003.](http://lib.ysu.am/open_books/312121.pdf)
2. [D. Eberly, “Robust Computation of Distance Between Line Segments”.](https://www.geometrictools.com/Documentation/DistanceLine3Line3.pdf)
3. [D. Eberly, “Distance to Circles in 3D”.](https://www.geometrictools.com/Documentation/DistanceToCircle3.pdf)



# Problem

Linear Component:
$$
\mathcal{L}(t) = L + td
$$

Planar Component:
$$
\mathcal{P}(u, v) = P + ue_0 + ve_1
$$

assuming $e_0 \cdot e_1 = 0$.

Let $X$ be the aggregated vector:

$$
X = (u, v, t)
$$

Assume the domain is $\mathcal{D}$:

$$
\left\{
\begin{aligned}
    u \in [0,1] \\
    v \in [0,1] \\
    t \in [0,1] \\
\end{aligned}
\right.
\Rightarrow
\mathcal{D} = [0,1] \times [0,1] \times [0,1]
$$

$$
X \in \mathcal{D}
$$

Distance function:
$$
Q(X) = Q(u,v,t) = ||\mathcal{L}(t) - \mathcal{P}(u,v)||^2, \quad X \in \mathcal{D}
$$

Closest points:
$$
X_{min} = \argmin_{X} Q(X)
$$

So the problem is solving the following conditional extremum problem of quadratic function:

$$
\begin{aligned}
    \argmin_{X}\quad & Q(X) \\
    s.t.\quad & X \in \mathcal{D}
\end{aligned}
$$


# Q


$$
\begin{aligned}
    Q(X)
    =&
        ||\mathcal{P}(u,v) - \mathcal{L}(t)||^2 
    \\
    =&
        e_0^2u^2 + e_1^2v^2 + d^2t^2 + 2(e_0\cdot e_1)uv - 2(e_0\cdot d)ut - 2(e_1\cdot d)vt \\
        & + 2(P-L)\cdot e_0 u + 2(P-L)\cdot e_1 v - 2(P-L)\cdot d t \\
        & + (P-L)^2
    \\
\end{aligned}
$$

Let
$$
g = P - L
$$

$$
\left\{
\begin{aligned}
    & a_{00} = e_0^2 \\
    & a_{01} = e_0\cdot e_1 \\
    & a_{02} = e_0\cdot d \\
    & a_{11} = e_1^2 \\
    & a_{12} = e_1\cdot d \\
    & a_{22} = d^2 \\
    & b_0 = g\cdot e_0 \\
    & b_1 = g\cdot e_1 \\
    & b_2 = g\cdot d \\
    & c = g^2 \\
\end{aligned}
\right.
$$

Then

$$
\begin{aligned}
    Q(X)
    =
    & a_{00}u^2 + a_{11}v^2 + a_{22}t^2 + 2a_{01}uv - 2a_{02}ut - 2a_{12}vt \\
    & + 2b_0 u + 2b_1 v - 2b_2 t \\
    & + c
\end{aligned}
$$


# Unconditional minimum

用符号$Y$表示无条件极值

$$
\left\{
\begin{aligned}
    \deriv{Q}{u} = 2a_{00}u + 2a_{01}v - 2a_{02}t + 2b_0 = 0 \\
    \deriv{Q}{v} = 2a_{11}v + 2a_{01}u - 2a_{12}t + 2b_1 = 0 \\
    \deriv{Q}{t} = 2a_{22}t - 2a_{02}u - 2a_{12}v - 2b_2 = 0 \\
\end{aligned}
\right.
\\

\Rightarrow
\left\{
\begin{aligned}
    u: + a_{00}u + a_{01}v - a_{02}t = - b_0 \\
    v: + a_{01}u + a_{11}v - a_{12}t = - b_1 \\
    t: - a_{02}u - a_{12}v + a_{22}t = + b_2 \\
\end{aligned}
\right.
\\

\Rightarrow
\left\{
\begin{aligned}
    u = \frac{- a_{01}v + a_{02}t - b_0}{a_{00}} \\
    v = \frac{- a_{01}u + a_{12}t - b_1}{a_{11}} \\
    t = \frac{+ a_{02}u + a_{12}v + b_2}{a_{22}} \\
\end{aligned}
\right.
$$


## corner
Minimum on the (8) points:
$$
Y_{(0,0,0)}=(0,0,0)\ 
Y_{(0,0,1)}=(0,0,1)\  \\
Y_{(0,1,0)}=(0,1,0)\ 
Y_{(0,1,1)}=(0,1,1)\  \\
Y_{(1,0,0)}=(1,0,0)\ 
Y_{(1,0,1)}=(1,0,1)\  \\
Y_{(1,1,0)}=(1,1,0)\ 
Y_{(1,1,1)}=(1,1,1)\ 
$$

## edge
Minimum on the (12) edges:

$$
\begin{aligned}

    & \left\{
    \begin{aligned}
        & Y_{(u,0,0)} = \left( \frac{              -b_0}{a_{00}},0,0 \right) \\
        & Y_{(u,0,1)} = \left( \frac{        a_{02}-b_0}{a_{00}},0,1 \right) \\
        & Y_{(u,1,0)} = \left( \frac{       -a_{01}-b_0}{a_{00}},1,0 \right) \\
        & Y_{(u,1,1)} = \left( \frac{-a_{01}+a_{02}-b_0}{a_{00}},1,0 \right) \\
    \end{aligned}
    \right.
    \\

    & \left\{
    \begin{aligned}
        & Y_{(0,v,0)} = \left( 0,\frac{              -b_1}{a_{11}},0 \right) \\
        & Y_{(0,v,1)} = \left( 0,\frac{        a_{12}-b_1}{a_{11}},1 \right) \\
        & Y_{(1,v,0)} = \left( 1,\frac{       -a_{01}-b_1}{a_{11}},0 \right) \\
        & Y_{(1,v,1)} = \left( 1,\frac{-a_{01}+a_{12}-b_1}{a_{11}},0 \right) \\
    \end{aligned}
    \right.
    \\

    & \left\{
    \begin{aligned}
        & Y_{(0,0,t)} = \left( 0,0,\frac{              b_2}{a_{22}} \right) \\
        & Y_{(0,1,t)} = \left( 0,1,\frac{       a_{12}+b_2}{a_{22}} \right) \\
        & Y_{(1,0,t)} = \left( 1,0,\frac{       a_{02}+b_2}{a_{22}} \right) \\
        & Y_{(1,1,t)} = \left( 1,0,\frac{a_{02}+a_{12}+b_2}{a_{22}} \right) \\
    \end{aligned}
    \right.
    \\

\end{aligned}
$$

## face
Minimum on the (6) faces (ignored known dim):

$$
\begin{aligned}

    &
    Y_{(u,v,0)} = \frac{1}{a_{00}a_{11}-a_{01}^2} \begin{bmatrix}
        a_{11} & -a_{01} \\
        -a_{01} & a_{00} \\
    \end{bmatrix} \begin{bmatrix}
        -b_0 \\
        -b_1 \\
    \end{bmatrix}
    \\

    &
    Y_{(u,v,1)} = \frac{1}{a_{00}a_{11}-a_{01}^2} \begin{bmatrix}
        a_{11} & -a_{01} \\
        -a_{01} & a_{00} \\
    \end{bmatrix} \begin{bmatrix}
        -b_0 + a_{02}\\
        -b_1 + a_{12}\\
    \end{bmatrix}
    \\

    &
    Y_{(u,0,t)} = \frac{1}{a_{00}a_{22}-a_{02}^2} \begin{bmatrix}
        a_{22} & a_{02} \\
        a_{02} & a_{00} \\
    \end{bmatrix} \begin{bmatrix}
        -b_0 \\
        b_2 \\
    \end{bmatrix}
    \\

    &
    Y_{(u,1,t)} = \frac{1}{a_{00}a_{22}-a_{02}^2} \begin{bmatrix}
        a_{22} & a_{02} \\
        a_{02} & a_{00} \\
    \end{bmatrix} \begin{bmatrix}
        -b_0 - a_{01} \\
        b_2 + a_{12} \\
    \end{bmatrix}
    \\

    &
    Y_{(0,v,t)} = \frac{1}{a_{11}a_{22}-a_{12}^2} \begin{bmatrix}
        a_{22} & a_{12} \\
        a_{12} & a_{11} \\
    \end{bmatrix} \begin{bmatrix}
        -b_1 \\
        b_2 \\
    \end{bmatrix}
    \\

    &
    Y_{(1,v,t)} = \frac{1}{a_{11}a_{22}-a_{12}^2} \begin{bmatrix}
        a_{22} & a_{12} \\
        a_{12} & a_{11} \\
    \end{bmatrix} \begin{bmatrix}
        -b_1 - a_{01}\\
        b_2 + a_{02} \\
    \end{bmatrix}
    \\

\end{aligned}
$$




## volume

Minimum in the whole space

$$
\begin{aligned}
    &
    \nabla Q = 0
    \\

    \Rightarrow
    &
    \left\{
    \begin{aligned}
        \deriv{Q}{u} = 2a_{00}u + 2a_{01}v - 2a_{02}t + 2b_0 = 0 \\
        \deriv{Q}{v} = 2a_{11}v + 2a_{01}u - 2a_{12}t + 2b_1 = 0 \\
        \deriv{Q}{t} = 2a_{22}t - 2a_{02}u - 2a_{12}v - 2b_2 = 0 \\
    \end{aligned}
    \right.
    \\

    \Rightarrow
    &
    \left\{
    \begin{aligned}
        a_{00}u + a_{01}v - a_{02}t = - b_0 \\
        a_{01}u + a_{11}v - a_{12}t = - b_1 \\
        - a_{02}u - a_{12}v + a_{22}t = b_2 \\
    \end{aligned}
    \right.
    \\

    \Rightarrow
    &
    \begin{bmatrix}
        a_{00} & a_{01} & -a_{02} \\
        a_{01} & a_{11} & -a_{12} \\
        -a_{02} & -a_{12} & a_{22} \\
    \end{bmatrix}
    \begin{bmatrix}
        u \\
        v \\
        t
    \end{bmatrix}
    =
    \begin{bmatrix}
        -b_0 \\
        -b_1 \\
        b_2 \\
    \end{bmatrix}
    \\

    \Rightarrow
    &
    Y_{(u,v,t)}
    =
    \begin{bmatrix}
        a_{00} & a_{01} & -a_{02} \\
        a_{01} & a_{11} & -a_{12} \\
        -a_{02} & -a_{12} & a_{22} \\
    \end{bmatrix}^ {-1}
    \begin{bmatrix}
        -b_0 \\
        -b_1 \\
        b_2 \\
    \end{bmatrix}
    \\
\end{aligned}
$$




# Conditional minimum

用符号$X$表示有条件极值。




## corner

$$
X_{(u,v,t)} = Y_{(u,v,t)} \text{ where } u,v,t \in \{0,1\}
$$


## edge

假设欲求边$(1,1,t)$上的有条件最小点$X_{(1,1,t)}$。

边$(1,1,t)$被划分成了3个区域:

$$
\begin{aligned}
& E_{+}: t>1 \\
& E_{0}: t\in[0,1]\\
& E_{-}: t<0 \\
\end{aligned}
$$

若$E_{?}$的下标：
* 为0，则该区域为interior类型(E.I)
* 不为0，则该区域为corner类型(E.C)

根据无条件最小点$Y_{(1,1,t)}$落在哪个region进行分类讨论：

$$
X_{(1,1,t)} = \left\{
\begin{aligned}
    & Y_{(1,1,1)} &\text{ if } Y_{(1,1,t)} \in E_+ \\
    & Y_{(1,1,t)} &\text{ if } Y_{(1,1,t)} \in E_0 \\
    & Y_{(1,1,0)} &\text{ if } Y_{(1,1,t)} \in E_- \\
\end{aligned}
\right.
$$



## face

假设欲求面$(1,v,t)$上的有条件最小点$X_{(1,v,t)}$。

面$(1,v,t)$被划分成了9个区域:

$$
\begin{aligned}
& F_{++}: u=1, v>1, t>1 \\
& F_{00}: u=1, v\in[0,1], t\in[0,1]\\
& F_{--}: u=1, v<0, t<0 \\
& F_{+-}: u=1, v>0, t<0 \\
& F_{-0}: u=1, v<0, t\in[0,1] \\
& \quad \vdots \\
\end{aligned}
$$

若$F_{??}$的下标：
* 三个为0，则该区域为interior类型(F.I)
* 两个为0，则该区域为edge类型(F.E)
* 一个为0，则该区域为corner类型(F.C)

当无条件最小点$Y_{(1,v,t)}$
* 落在interior区域时，$X_{(1,v,t)} = Y_{(1,v,t)}$
* 落在edge类型的区域时，$X_{(1,v,t)}$落在该区域对应的边，因此它等于边上的有条件最小点
* 落在corner region时需要根据偏导数情况进一步分类讨论——

### corner类型的区域

假设$Y_{(1,v,t)}$落在区域$F_{++}$，则有条件最小点$X_{(1,v,t)}$可能落在边$(1,1,t)$、边$(1,v,1)$、角$(1,1,1)$上。

计算角$(1,1,1)$上$Q$关于$v,t$的梯度$\deriv{Q}{v}|_{(1,1,1)}, \deriv{Q}{t}|_{(1,1,1)}$：
* 若$\deriv{Q}{v}>0$，则$X_{(1,v,t)}$落在边$(1,v,1)$上
* 若$\deriv{Q}{t}>0$，则$X_{(1,v,t)}$落在边$(1,1,t)$上
* 若$\deriv{Q}{v},\deriv{Q}{t}\leq0$，则$X_{(1,v,t)}$落在角$(1,1,1)$上
* 不可能出现$\deriv{Q}{v},\deriv{Q}{t}>0$的情况

引入辅助记号$Z_{(1,v,t)}^{0++}$表示无条件最小点$Y_{(1,v,t)}$落到区域$F_{++}$时的分类讨论结果：

$$
Z_{(1,v,t)}^{0++} = \left\{
\begin{aligned}
    & X_{(1,v,1)} &\text{ if } \deriv{Q}{v}|_{(1,1,1)} > 0 \\
    & X_{(1,1,t)} &\text{ if } \deriv{Q}{t}|_{(1,1,1)} > 0 \\
    & X_{(1,1,1)} &\text{ otherwise} \\
\end{aligned}
\right.
$$

类比可以得到区域$F_{+-}, F_{-+}, F_{--}$时的$Z$:

$$
\begin{aligned}

    Z_{(1,v,t)}^{0+-} = \left\{
    \begin{aligned}
        & X_{(1,v,0)} &\text{ if } \deriv{Q}{v}|_{(1,1,0)} > 0 \\
        & X_{(1,1,t)} &\text{ if } \deriv{Q}{t}|_{(1,1,0)} < 0 \\
        & X_{(1,1,0)} &\text{ otherwise} \\
    \end{aligned}
    \right.
    \\

    Z_{(1,v,t)}^{0-+} = \left\{
    \begin{aligned}
        & X_{(1,v,1)} &\text{ if } \deriv{Q}{v}|_{(1,0,1)} < 0 \\
        & X_{(1,0,t)} &\text{ if } \deriv{Q}{t}|_{(1,0,1)} > 0 \\
        & X_{(1,0,1)} &\text{ otherwise} \\
    \end{aligned}
    \right.
    \\

    Z_{(1,v,t)}^{0--} = \left\{
    \begin{aligned}
        & X_{(1,v,0)} &\text{ if } \deriv{Q}{v}|_{(1,0,0)} < 0 \\
        & X_{(1,0,t)} &\text{ if } \deriv{Q}{t}|_{(1,0,0)} < 0 \\
        & X_{(1,0,0)} &\text{ otherwise} \\
    \end{aligned}
    \right.
    \\

\end{aligned}
$$





### summary

综合上述讨论得到：

$$
X_{(1,v,t)} = \left\{
\begin{aligned}
    & Y_{(1,v,t)} &\text{ if } Y_{(1,v,t)} \in F_{00} \\
    & X_{(1,v,1)} &\text{ if } Y_{(1,v,t)} \in F_{0+} \\
    & X_{(1,1,t)} &\text{ if } Y_{(1,v,t)} \in F_{+0} \\
    & X_{(1,v,0)} &\text{ if } Y_{(1,v,t)} \in F_{0-} \\
    & X_{(1,0,t)} &\text{ if } Y_{(1,v,t)} \in F_{-0} \\
    & Z_{(1,v,t)}^{++} &\text{ if } Y_{(1,v,t)} \in F_{++} \\
    & Z_{(1,v,t)}^{+-} &\text{ if } Y_{(1,v,t)} \in F_{+-} \\
    & Z_{(1,v,t)}^{-+} &\text{ if } Y_{(1,v,t)} \in F_{-+} \\
    & Z_{(1,v,t)}^{--} &\text{ if } Y_{(1,v,t)} \in F_{--} \\
\end{aligned}
\right.
$$




## volume

整个空间被划分成了27个区域:

$$
\begin{aligned}
& V_{+++}: u>1, v>1, t>1 \\
& V_{000}: u\in[0,1], v\in[0,1] t\in[0,1]\\
& V_{---}: u<0, v<0, t<0 \\
& V_{+0-}: u>1, v\in[0,1], t<0 \\
& \cdots \\
\end{aligned}
$$

若$V_{???}$的下标：
* 三个为0，则该区域为interior类型(V.I)
* 两个为0，则该区域为face类型(V.F)
* 一个为0，则该区域为edge类型(V.E)
* 零个为0，则该区域为corner类型(V.C)

当无条件最小点$Y_{(u,v,t)}$：
* 落在interior区域时，$X_{(u,v,t)} = Y_{(v,v,t)}$
* 落在face类型的区域时，$X_{(u,v,t)}$落在该区域对应的面上，因此它等于该面上的有条件最小点
    * 例如若落在$V_{00+}$，则$X_{(u,v,t)}=X_{(u,v,1)}$
* 落在edge, corner类型的区域时需要根据偏导数情况进一步分类讨论——



### edge类型的区域

假设$Y_{(u,v,t)}$落在区域$V_{0++}$，则有条件最小点$X_{(u,v,t)}$可能落在边$(u,1,1)$、面$(u,v,1)$、面$(u,1,t)$上。

计算边$(u,1,1)$上的有条件最小点$X_{(u,1,1)}$上$Q$关于$v,t$的梯度$\deriv{Q}{v}|_{X_{(u,1,1)}}, \deriv{Q}{t}|_{X_{(u,1,1)}}$：
* 若$\deriv{Q}{v}>0$，则$X_{(u,v,t)}$落在面$(u,v,1)$上
* 若$\deriv{Q}{t}>0$，则$X_{(u,v,t)}$落在面$(u,1,t)$上
* 若$\deriv{Q}{v},\deriv{Q}{t}\leq0$，则$X_{(u,v,t)}$落在边$(u,1,1)$
* 不可能出现$\deriv{Q}{v},\deriv{Q}{t}>0$的情况

引入辅助记号$Z_{(u,v,t)}^{0++}$表示无条件最小点$Y_{(u,v,t)}$落到区域$V_{0++}$时的分类讨论结果：

$$
Z_{(u,v,t)}^{0++} = \left\{
\begin{aligned}
    & X_{(u,v,1)} &\text{ if } \deriv{Q}{v}|_{X_{(u,1,1)}} > 0 \\
    & X_{(u,1,t)} &\text{ if } \deriv{Q}{t}|_{X_{(u,1,1)}} > 0 \\
    & X_{(u,1,1)} &\text{ otherwise} \\
\end{aligned}
\right.
$$

总计12个edge类型的region都可以类比得到。



### corner类型的区域

假设$Y_{(u,v,t)}$落在区域$V_{+++}$，则有条件最小点$X_{(u,v,t)}$可能落在角$(1,1,1)$、边$(u,1,1)$、边$(1,v,1)$、边$(1,1,t)$、面$(u,v,1)$、面$(u,1,t)$、面$(1,v,t)$。

计算角$(1,1,1)$上$Q$关于$u,v,t$的梯度$\deriv{Q}{u}|_{(1,1,1)}, \deriv{Q}{v}|_{(1,1,1)}, \deriv{Q}{t}|_{(1,1,1)}$：
* 若$\deriv{Q}{u},\deriv{Q}{v}>0$，则$X_{(u,v,t)}$落在面$(u,v,1)$上
* 若$\deriv{Q}{u},\deriv{Q}{t}>0$，则$X_{(u,v,t)}$落在面$(u,1,t)$上
* 若$\deriv{Q}{v},\deriv{Q}{t}>0$，则$X_{(u,v,t)}$落在面$(1,v,t)$上
* 若$\deriv{Q}{u}>0$，则等价于$Y_{(u,v,t)}$落在edge类型区域$V_{0++}$中
* 若$\deriv{Q}{v}>0$，则等价于$Y_{(u,v,t)}$落在edge类型区域$V_{+0+}$中
* 若$\deriv{Q}{t}>0$，则等价于$Y_{(u,v,t)}$落在edge类型区域$V_{++0}$中
* 若$\deriv{Q}{u},\deriv{Q}{v},\deriv{Q}{t}\leq0$，则$X_{(u,v,t)}$落在角$(1,1,1)$
* 不可能出现$\deriv{Q}{u},\deriv{Q}{v},\deriv{Q}{t}>0$的情况

引入辅助记号$Z_{(u,v,t)}^{+++}$表示无条件最小点$Y_{(u,v,t)}$落到区域$V_{+++}$时的分类讨论结果（以下梯度都在点${(1,1,1)}$处求值）：

$$
Z_{(u,v,t)}^{+++} = \left\{
\begin{aligned}
    & X_{(u,v,1)} &\text{ if } \deriv{Q}{u}, \deriv{Q}{v} > 0 \\
    & X_{(u,1,t)} &\text{ if } \deriv{Q}{u}, \deriv{Q}{t} > 0 \\
    & X_{(1,v,t)} &\text{ if } \deriv{Q}{v}, \deriv{Q}{t} > 0 \\
    & Z_{(u,v,t)}^{0++} &\text{ if }  \deriv{Q}{u} > 0 \\
    & Z_{(u,v,t)}^{+0+} &\text{ if }  \deriv{Q}{v} > 0 \\
    & Z_{(u,v,t)}^{++0} &\text{ if }  \deriv{Q}{t} > 0 \\
    & Y_{(1,1,1)} &\text{ otherwise} \\
\end{aligned}
\right.
$$

总计8个corner类型的region都可以类比得到。



### summary

综合上述讨论得到：

If $Y_{(u,v,t)}$ in interior type region:

$$
X_{(u,v,t)} = \left\{
\begin{aligned}
    & Y_{(u,v,t)} &\text{ if } Y_{(u,v,t)} \in V_{000} \\
\end{aligned}
\right.
$$

If $Y_{(u,v,t)}$ in face type region:

$$
X_{(u,v,t)} = \left\{
\begin{aligned}
    & X_{(u,v,0)} &\text{ if } Y_{(u,v,t)} \in V_{00-} \\
    & X_{(u,v,1)} &\text{ if } Y_{(u,v,t)} \in V_{00+} \\
    \\
    & X_{(u,0,t)} &\text{ if } Y_{(u,v,t)} \in V_{0-0} \\
    & X_{(u,1,t)} &\text{ if } Y_{(u,v,t)} \in V_{0+0} \\
    \\
    & X_{(0,v,t)} &\text{ if } Y_{(u,v,t)} \in V_{-00} \\
    & X_{(1,v,t)} &\text{ if } Y_{(u,v,t)} \in V_{+00} \\
\end{aligned}
\right.
$$

If $Y_{(u,v,t)}$ in edge type region:

$$
X_{(u,v,t)} = \left\{
\begin{aligned}
    & Z_{(u,v,t)}^{0--} &\text{ if } Y_{(u,v,t)} \in V_{0--} \\
    & Z_{(u,v,t)}^{0-+} &\text{ if } Y_{(u,v,t)} \in V_{0-+} \\
    & Z_{(u,v,t)}^{0+-} &\text{ if } Y_{(u,v,t)} \in V_{0+-} \\
    & Z_{(u,v,t)}^{0++} &\text{ if } Y_{(u,v,t)} \in V_{0++} \\
    \\
    & Z_{(u,v,t)}^{-0-} &\text{ if } Y_{(u,v,t)} \in V_{-0-} \\
    & Z_{(u,v,t)}^{-0+} &\text{ if } Y_{(u,v,t)} \in V_{-0+} \\
    & Z_{(u,v,t)}^{+0-} &\text{ if } Y_{(u,v,t)} \in V_{+0-} \\
    & Z_{(u,v,t)}^{+0+} &\text{ if } Y_{(u,v,t)} \in V_{+0+} \\
    \\
    & Z_{(u,v,t)}^{--0} &\text{ if } Y_{(u,v,t)} \in V_{--0} \\
    & Z_{(u,v,t)}^{-+0} &\text{ if } Y_{(u,v,t)} \in V_{-+0} \\
    & Z_{(u,v,t)}^{+-0} &\text{ if } Y_{(u,v,t)} \in V_{+-0} \\
    & Z_{(u,v,t)}^{++0} &\text{ if } Y_{(u,v,t)} \in V_{++0} \\
\end{aligned}
\right.
$$

If $Y_{(u,v,t)}$ in corner type region:

$$
X_{(u,v,t)} = \left\{
\begin{aligned}
    & Z_{(u,v,t)}^{---} &\text{ if } Y_{(u,v,t)} \in V_{---} \\
    & Z_{(u,v,t)}^{--+} &\text{ if } Y_{(u,v,t)} \in V_{--+} \\
    & Z_{(u,v,t)}^{-+-} &\text{ if } Y_{(u,v,t)} \in V_{-+-} \\
    & Z_{(u,v,t)}^{-++} &\text{ if } Y_{(u,v,t)} \in V_{-++} \\
    \\
    & Z_{(u,v,t)}^{+--} &\text{ if } Y_{(u,v,t)} \in V_{+--} \\
    & Z_{(u,v,t)}^{+-+} &\text{ if } Y_{(u,v,t)} \in V_{+-+} \\
    & Z_{(u,v,t)}^{++-} &\text{ if } Y_{(u,v,t)} \in V_{++-} \\
    & Z_{(u,v,t)}^{+++} &\text{ if } Y_{(u,v,t)} \in V_{+++} \\
\end{aligned}
\right.
$$






# Algorithm

## 辅助变量$D_{(u,v,t)}^\delta$
引入辅助变量$D_{(u,v,t)}^\delta$，其中$\delta \in \{u,v,t\}$为任一变元。
$D$的取值由$Q$关于$\delta$在点$(u,v,t)$的偏导数决定——

若$\delta$为$u$：

$$
D_{(u,v,t)}^u = \left\{
\begin{aligned}
    & 1 & \text{ if } u=1 \text{ and } \deriv{Q}{u}|_{(1,v,t)} > 0 \\
    & 1 & \text{ if } u=0 \text{ and } \deriv{Q}{u}|_{(0,v,t)} < 0 \\
    & 0 & \text{ otheriwse}
\end{aligned}
\right.
$$

若$\delta$为$v$，则也是一样的讨论：

$$
D_{(u,v,t)}^v = \left\{
\begin{aligned}
    & 1 & \text{ if } v=1 \text{ and } \deriv{Q}{v}|_{(u,1,t)} > 0 \\
    & 1 & \text{ if } v=0 \text{ and } \deriv{Q}{v}|_{(u,0,t)} < 0 \\
    & 0 & \text{ otheriwse}
\end{aligned}
\right.
$$

若$\delta$为$t$，则也是一样的讨论：

$$
D_{(u,v,t)}^t = \left\{
\begin{aligned}
    & 1 & \text{ if } t=1 \text{ and } \deriv{Q}{t}|_{(u,v,1)} > 0 \\
    & 1 & \text{ if } t=0 \text{ and } \deriv{Q}{t}|_{(u,v,0)} < 0 \\
    & 0 & \text{ otheriwse}
\end{aligned}
\right.
$$

$D$的取值为1时表示$Q$在$\delta \in [0,1]$描述的线/面边界上必定存在比当前点$(u,v,t)$上还小的点，
后文中我们将使用该辅助变量来简化式子。







## 算法

* 子方法`SolveVolume`:
    * 计算$Y_{(u,v,t)}$的值，判断属于哪个区域$V_{???}$
    * 若$Y_{(u,v,t)}$属于interior region $V_{000}$
        * $X_{(u,v,t)}=Y_{(u,v,t)}$
        * END
    * 若$Y_{(u,v,t)}$属于face region $V_{00?}, V_{0?0}, V_{?00}$
        * 设超过范围的坐标变元为$\delta$，并设其截断到$[0,1]$后的值为$\bar{\delta}$
        * 调用子方法`SolveFace`求在面$\delta=\bar{\delta}$上的最小点$X_{\delta=\bar{\delta}}$
        * $X_{(u,v,t)} = X_{\delta=\bar{\delta}}$
        * END
    * 若$Y_{(u,v,t)}$属于edge region $V_{0??}, V_{?0?}, V_{??0}$
        * 设两个超过范围的坐标变元分别为$\delta_0, \delta_1$
            * 设将$\delta_0, \delta_1$截断到$[0,1]$后的值为$\bar{\delta}_0, \bar{\delta}_1$
            * 并设直线$L: \delta_0=\bar{\delta}_0, \delta_1=\bar{\delta}_1$
        * 子方法`SolveEdgeRegion(L)`：
            * 调用子方法`SolveEdge`求在直线$L$上的最小点$X_L$
            * 计算$Q$在$X_L$上关于$\delta_0, \delta_1$的偏导数，并得到对应的$D^{\delta_0}, D^{\delta_1}$
                * 若$D^{\delta_0}=1$，调用子方法`SolveFace`求在面$\delta_1=\bar{\delta}_1$上的最小点$X_{\delta_1=\bar{\delta}_1}$
                    * $X_{(u,v,t)}=X_{\delta_1=\bar{\delta}_1}$
                    * END
                * 若$D^{\delta_1}=1$，调用子方法`SolveFace`求在面$\delta_0=\bar{\delta}_0$上的最小点$X_{\delta_1=\bar{\delta}_0}$
                    * $X_{(u,v,t)}=X_{\delta_1=\bar{\delta}_0}$
                    * END
                * 否则
                    * $X_{(u,v,t)} = X_L$
                    * END
    * 若$Y_{(u,v,t)}$属于corner region $V_{???}$
        * 将$u,v,t$截断到$[0,1]$的范围内得到$\bar{u}, \bar{v}, \bar{t}$
        * 计算$Q$在$(\bar{u}, \bar{v}, \bar{t})$上关于$u,v,t$的偏导数，并得到对应的$D^u, D^v, D^t$
            * 若$D^u, D^v=1$，调用子方法`SolveFace`求在面$t=\bar{t}$上的最小点$X_{t=\bar{t}}$
                * $X_{(u,v,t)}=X_{t=\bar{t}}$
                * END
            * 若$D^u, D^t=1$，调用子方法`SolveFace`求在面$v=\bar{v}$上的最小点$X_{v=\bar{v}}$
                * $X_{(u,v,t)}=X_{v=\bar{v}}$
                * END
            * 若$D^v, D^t=1$，调用子方法`SolveFace`求在面$u=\bar{u}$上的最小点$X_{u=\bar{u}}$
                * $X_{(u,v,t)}=X_{u=\bar{u}}$
                * END
            * 若$D^u=1$，令$L:v=\bar{v}, t=\bar{t}$，调用子方法`SolveEdgeRegion(L)`得到最小点$Z^{0??}$
                * $X_{(u,v,t)}=Z^{0??}$
                * END
            * 若$D^v=1$，令$L:u=\bar{u}, t=\bar{t}$，调用子方法`SolveEdgeRegion(L)`得到最小点$Z^{?0?}$
                * $X_{(u,v,t)}=Z^{?0?}$
                * END
            * 若$D^t=1$，令$L:u=\bar{u}, v=\bar{v}$，调用子方法`SolveEdgeRegion(L)`得到最小点$Z^{??0}$
                * $X_{(u,v,t)}=Z^{??0}$
                * END
            * 否则
                * $X_{(u,v,t)} = (\bar{u}, \bar{v}, \bar{t})$
                * END
* 子方法`SolveFace`:
    * 记当前Face为$i = \bar{i}$，自由变元为$j,k$
        * 后文中坐标将忽略$i$，而仅使用二维向量$(j,k)$
    * 计算$Y_{(j,k)}$的值，判断属于哪个区域$F_{??}$
    * 若$Y_{(j,k)}$属于interior region $F_{00}$
        * $X_{(j,k)} = Y_{(j,k)}$
        * END
    * 若$Y_{(j,k)}$属于edge region $F_{0?}, F_{?0}$
        * 设超过范围的坐标变元为$\delta$，并设其截断到$[0,1]$后的值为$\bar{\delta}$
        * 调用子方法`SolveEdge`求在边$\delta=\bar{\delta}$上的最小点$X_{\delta=\bar{\delta}}$
        * $X_{(u,v,t)} = X_{\delta=\bar{\delta}}$
        * END
    * 若$Y_{(j,k)}$属于corner region $F_{??}$
        * 将$j,k$截断到$[0,1]$的范围内得到$\bar{j}, \bar{k}$
        * 计算$Q$在$(\bar{j}, \bar{k})$上关于$j,k$的偏导数，并得到对应的$D^j, D^k$
            * 若$D^{j}=1$，调用子方法`SolveEdge`求在边$k=\bar{k}$上的最小点$X_{(j,\bar{k})}$
                * $X_{(j,k)}=X_{(j,\bar{k})}$
                * END
            * 若$D^{k}=1$，调用子方法`SolveEdge`求在边$j=\bar{j}$上的最小点$X_{(\bar{j},k)}$
                * $X_{(j,k)}=X_{(\bar{j},k)}$
                * END
            * 否则
                * $X_{(j,k)} = (\bar{j}, \bar{k})$
                * END
* 子方法`SolveEdge`
    * 记当前Edge为$i=\bar{i}, j=\bar{j}$，自由变元为$k$
        * 后文中坐标将忽略$i,j$，而仅使用一维向量$(k)$
    * 计算$Y_{(k)}$的值
    * 区域判断法：
        * 判断属于哪个区域$E_{?}$
        * 若$Y_{(k)}$属于interior region $E_{0}$
            * $X_{(k)} = Y_{(k)}$
            * END
        * 若$Y_{(k)}$属于corner region $E_{?}$
            * 将$k$截断到$[0,1]$的范围内得到$\bar{k}$
            * $X_{(k)} = Y_{(\bar{k})}$
            * END
    * 截断法：
        * 注意到corner region相较于interior region只多了一步截断而已
        * 因此我们可以无视$Y_{(k)}$的具体值，而总是直接将它截断到$[0,1]$的范围得到$\bar{k}$
        * $X_{(k)} = Y_{(\bar{k})}$
        * END