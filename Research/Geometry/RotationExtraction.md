<!-- title: 旋转提取 -->

$$
% works in MathJax
\def\*#1{\mathbf{#1}}
\def\^#1{\mathrm{#1}}
\def\deriv#1#2{\frac{\partial #1}{\partial #2}}
\def\tr#1{\text{tr}\left( #1 \right)}
\def\det#1{\text{det}\left( #1 \right)}
\def\frao#1{\frac{1}{#1}}
\def\argmin#1{\text{argmin}#1}
$$

本文将阐述旋转提取问题的原理，并介绍两种求解旋转提取问题的方法:
1. 拉格朗日乘数法（极分解法）
2. Gauss-Seidel法（Müller法）: https://dl.acm.org/doi/10.1145/2994258.2994269




# 旋转提取的形式化表述：Wahba's problem

旋转提取问题可以形式化描述为[Wahba's problem](https://en.wikipedia.org/wiki/Wahba%27s_problem)，
该问题的原型是：

$$
\begin{aligned}
    \argmin_\*R\ & J(\*R)
    =
    \frao{2} \sum_{k=1}^{N}a_k ||\*w_k - \*R \*v_k||^2, \quad \forall N \geq 2
    \\

    \text{s.t. }
    & \*R^T\*R = \*I \\
    & \det{\*R} = 1
\end{aligned}
$$

若所有$\*v_k$都由标准正交基
$\begin{bmatrix}1\\0\\0\end{bmatrix}, \begin{bmatrix}0\\1\\0\end{bmatrix}, \begin{bmatrix}0\\0\\1\end{bmatrix}$
生成，
$\*w_k$都由标准正交基$\*A = \begin{bmatrix} \*a_1 & \*a_2 & \*a_3 \end{bmatrix}$生成，
则Wahba问题等价为（忽略权重$a_k$）：

$$
\begin{aligned}
    \argmin_\*R\ & J(\*R) =
    \frao{2} \sum_{i=1}^{3} ||\*a_i - \*r_i||^2
    \\

    \text{s.t. }
    & \*R^T\*R = \*I \\
    & \det{\*R} = 1
\end{aligned}
$$

其中$\*R = \begin{bmatrix} \*r_1 & \*r_2 & \*r_3 \end{bmatrix}$。

该问题也可以用Frobenius norm的形式表示：

$$
\begin{aligned}
    \argmin_\*R\ & J(\*R) =
    \frao{2}  ||\*A - \*R||^2_\^F
    \\

    \text{s.t. }
    & \*R^T\*R = \*I \\
    & \det{\*R} = 1
\end{aligned}
$$

这一形式就可以比较容易看出它是在做“旋转提取”了：
有线性变换矩阵$\*A$，求旋转矩阵$\*R$，
使得$\*A-\*R$的模尽可能小。


# 方法一：拉格朗日乘数法求解（极分解法）

如果带着约束$\det{\*R}=1$应用拉格朗日乘数法的话，
那会因为约束过紧导致难以取得有意义的结果，
因此这里放松一下约束，仅要求$\*R$为正交矩阵（允许它行列式为-1）：

$$
\begin{aligned}
    \argmin_\*R\ & J(\*R) =
    \frao{2} ||\*A - \*R||^2_\^F
    \\

    \text{s.t. } & \*R^T\*R = \*I
\end{aligned}
$$

应用拉格朗日乘数法求解该条件极值问题，
构造拉格朗日函数：

$$
\mathcal{L}(\*R;\gamma_i) = J(\*R) + \sum_i \gamma_i g_i \\

\text{where}\ 
\left\{
\begin{aligned}
    g_1 = \*r_1^2 - 1 \\
    g_2 = \*r_2^2 - 1 \\
    g_3 = \*r_3^2 - 1 \\
    g_4 = \*r_1\cdot \*r_2 \\
    g_5 = \*r_2\cdot \*r_3 \\
    g_6 = \*r_3\cdot \*r_1 \\
\end{aligned}
\right.
$$

对加号左右两项分别求关于$\*R$的导：

$$
\deriv{J}{\*R} = \*R - \*A
$$

$$
\deriv{\sum_i \gamma_i g_i}{\*R} = \begin{bmatrix}
    2\gamma_1\*r_1 + \gamma_4 \*r_2 + \gamma_6 \*r_3 &
    \gamma_4 \*r_1 + 2\gamma_2\*r_2 + \gamma_5 \*r_3 &
    \gamma_6 \*r_1 + \gamma_5 \*r_2 + 2\gamma_3\*r_3
\end{bmatrix}
$$

记

$$
\*Y = \begin{bmatrix}
    2\gamma_1 & \gamma_4 & \gamma_6 \\
    \gamma_4 & 2\gamma_2 & \gamma_5 \\
    \gamma_6 & \gamma_5 & 2\gamma_3
\end{bmatrix}
$$

则第二项关于$\*R$的导数可以表示为：

$$
\deriv{\sum_i \gamma_i g_i}{\*R} =
\*R \*Y
$$

令导数为0：

$$
\left\{
\begin{aligned}
    \deriv{\mathcal{L}}{\*R}
    &= \*R - \*A + \*R\*Y
    &= \*0
    \\
    \deriv{\mathcal{L}}{\gamma_i}
    &= g_i
    &= 0
\end{aligned}
\right.

\\
\Leftrightarrow
\\

\left\{
\begin{aligned}
    &
    \*R (\*I + \*Y)
    = \*A
    \\

    &
    \*R^T \*R 
    = \*I
\end{aligned}
\right.
$$

求解上述关于$\*R$的方程组即可得到结果。

对其做变形以得到熟悉的极分解形式，
首先引入$\*S$：

$$
\*S := \*I + \*Y
$$

于是有极分解法的旋转提取公式：

$$
\left\{
\begin{aligned}
    & \*R \*S = \*A \\
    & \*R^T \*R = \*I
\end{aligned}
\right.
\\
\Rightarrow
\left\{
\begin{aligned}
    & \*S^2 = \*S^T\*S = (\*R^{-1}\*A)^T\*R^{-1}\*A = \*A^T\*A
    \\
    & \*R = \*A \left(
        \sqrt{\*A^T\*A}
    \right)^{-1}
\end{aligned}
\right.
$$









# 方法二：Gauss-Seidel法（Müller法）

本节介绍的方法与[1]中的方法是完全一致的，
但因为[1]中的推导过程存在省略且不够严谨，
因此本节将重新给出一套推导过程。

\[1]: Müller, M., Bender, J., Chentanez, N. & Macklin, M. A robust method to extract the rotational part of deformations. in Proceedings of the 9th International Conference on Motion in Games 55–60 (ACM, Burlingame California, 2016). doi:10.1145/2994258.2994269

## 分解问题

回顾以下形式的Wahba问题：

$$
\begin{aligned}
    \argmin_\*R\ & J(\*R) =
    \frao{2} \sum_{i=1}^{3} ||\*a_i - \*r_i||^2
    \\

    \text{s.t. }
    & \*R^T\*R = \*I \\
    & \det{\*R} = 1
\end{aligned}
$$

因为$J$关于$\*R$的导数为$\deriv{J}{\*R} = \*R - \*A$，
所以该优化问题等价于求解以下方程组：

$$
\left\{
\begin{aligned}
    \*a_1 - \*r_1 = \*0 \\
    \*a_2 - \*r_2 = \*0 \\
    \*a_3 - \*r_3 = \*0 \\
\end{aligned}
\right.
\\

\begin{aligned}
    \text{s.t. }
    & \*R^T\*R = \*I \\
    & \det{\*R} = 1
\end{aligned}
$$

使用Gauss-Seidel法求解该方程组，即每次迭代一个方程
（注意该方程依然是关于$\*r_1, \*r_2, \*r_3$的方程，而不只是关于$\*r_i$的方程）：

$$
\begin{aligned}
    \*a_i - \*r_i = \*0 \\
\end{aligned}
\\

\begin{aligned}
    \text{s.t. }
    & \*R^T\*R = \*I \\
    & \det{\*R} = 1
\end{aligned}
$$

如果我们让每次求解过程都是往上一次迭代结果上叠加一个旋转的话，
那只要初始解是一个满足约束的旋转矩阵，
则每次迭代结果都是旋转矩阵，自动满足了约束。

记$\*R=[\*r_1\ \*r_2\ \*r_3]$为上一次迭代的结果，
这次迭代求解时叠加上的旋转为$\Delta \*R$，
则每次迭代都为求解以下关于$\Delta \*R$的方程：

$$
\begin{aligned}
    \*a_i - \Delta \*R\*r_i = \*0 \\
\end{aligned}
\\

\begin{aligned}
    \text{s.t. }
    & \Delta\*R^T\Delta\*R = \*I \\
    & \det{\Delta\*R} = 1
\end{aligned}
$$

另外注意到对于大多数$\*a_i$而言，该方程都是无解的，
因此我们采用最小二乘法来近似求解该方程，
即求解以下优化问题：

$$
\argmin_{\Delta \*R} ||\*a_i - \Delta \*R \*r_i||_2
\\

\begin{aligned}
    \text{s.t. }
    & \Delta\*R^T\Delta\*R = \*I \\
    & \det{\Delta\*R} = 1
\end{aligned}
$$

该问题的解可以通过简单的几何学来得到，如下图所示：

![](pic\OneConstraint.PNG)

该问题等价于以下方程：

$$
\Delta \*R \*r_i = \frac{\*a_i}{|\*a_i|}
\\

\begin{aligned}
    \text{s.t. }
    & \Delta\*R^T\Delta\*R = \*I \\
    & \det{\Delta\*R} = 1
\end{aligned}
$$

解$\Delta \*R$为绕
$\frac{\*r_i \times \*a_i}{|\*r_i \times \*a_i|}$旋转
$\arccos\frac{\*r_i\cdot\*a_i}{|\*a_i|}$的旋转。
附录中给出了该解的严谨验证。





## 混合一轮迭代的三个旋转

为了提高计算效率，我们修改一下Gauss-Seidel法的求解顺序：
* 每轮迭代把整个方程组都求解一遍
    * 原来的话是每轮迭代求解一个方程
* 求解时依然按序逐个求解方程，计算时依然使用上一轮的迭代结果$\*R$

每轮迭代按序求解以下三个方程，每次求解得到一个旋转$\Delta \*R$：

$$
\left\{
\begin{aligned}
    \Delta \*R \*r_1 = \frac{\*a_1}{|\*a_1|} \\
    \Delta \*R \*r_2 = \frac{\*a_2}{|\*a_2|} \\
    \Delta \*R \*r_3 = \frac{\*a_3}{|\*a_3|} \\
\end{aligned}
\right.
$$

记第$i$个方程得到的旋转的四元数表示为$\*q_i$：

$$
\*q_i =
\left(
    \cos{\frac{\theta_i}{2}},
    \phi_i
    \sin{\frac{\theta_i}{2}}
\right)
$$

其中

$$
\left\{
\begin{aligned}
    \phi_i &= \frac{\*r_i \times \*a_i}{|\*r_i \times \*a_i|} \\
    \theta_i &= \arccos\frac{\*r_i\cdot\*a_i}{|\*a_i|}
\end{aligned}
\right.
$$

当$\theta$较小时可以做如下近似：

$$
\theta \approx \tan\theta
= \frac{\sin\theta}{\cos\theta}
= \frac{|\*r||\*a|\sin\theta}{|\*r||\*a|\cos\theta}
= \frac{|\*r\times\*a|}{\*r\cdot\*a}
$$

于是有：

$$
\left\{
\begin{aligned}
    \phi_i &= \frac{\*r_i \times \*a_i}{|\*r_i \times \*a_i|} \\
    \theta_i &= \frac{|\*r_i\times\*a_i|}{\*r_i\cdot\*a_i}
\end{aligned}
\right.
$$

引入$\omega$：

$$
\omega_i = \frac{\*r_i \times \*a_i}{\*r_i\cdot\*a_i} \\
$$


则：

$$
\left\{
\begin{aligned}
    \omega_i &= \theta_i \phi_i \\
    \*q_i &= \exp{\frac{\omega_i}{2}}
\end{aligned}
\right.
$$

其中$\exp$为[Exponential map](https://en.wikipedia.org/wiki/Euler%27s_formula#Other_applications)
（原论文里这里没$\frao{2}$，估计只是作者笔误）。
则每轮迭代的三次旋转的合计效果可以化简为：

$$
\*q_3\*q_2\*q_1
=
\exp{\frac{\sum_i \omega_i}{2}}
=
\exp{\left(
    \frao{2}
    \sum_i
    \frac{\*r_i \times \*a_i}{\*r_i \cdot \*a_i}
\right)}
$$

为旋转角度引入一个权重系数$\alpha_i$（TODO 为啥引入？目前我还没找到理由）:

$$
\alpha_i = \frac{
    \*r_i \cdot \*a_i
}{
    \sum_j \*r_j \cdot \*a_j
}
$$

则带权旋转$\*{\bar{q}}_i$为：

$$
\*{\bar{q}}_i = \exp{\frac{\alpha_i\omega_i}{2}}
$$


三次带权旋转的合计效果为：

$$
\*{\bar{q}}_3
\*{\bar{q}}_2
\*{\bar{q}}_1
=
\exp{\frac{\sum_i \alpha_i \omega_i}{2}}
=
\exp{\left(
    \frao{2}
    \frac{
        \sum_i \*r_i \times \*a_i
    }{
        \sum_i \*r_i \cdot \*a_i
    }
\right)}
$$

这也就是原论文里每轮迭代施加的旋转。





## 每轮迭代之间的旋转叠加

（本节内容在原论文中并没有出现）

上一节中我们得到了每轮迭代施加的旋转为

$$
\exp{\left(
    \frao{2}
    \frac{
        \sum_i \*r_i \times \*a_i
    }{
        \sum_i \*r_i \cdot \*a_i
    }
\right)}
$$

将该旋转的旋转角和旋转轴记为：

$$
\omega =
\frac{
    \sum_i \*r_i \times \*a_i
}{
    \sum_i \*r_i \cdot \*a_i
}
\\

\left\{
\begin{aligned}
    \phi &= \frac{\omega}{|\omega|} \\
    \theta &= |\omega|
\end{aligned}
\right.
$$

该旋转表示为轴角表示，可以很容易地转换成四元数表示，
但比较难转换成矩阵表示（而且用矩阵乘法表示旋转叠加的话开销更高）。
而因为不管是线性变换$\*A$还是上一轮的迭代结果$\*R$都是矩阵表示，
因此需要寻找一种方法能够高效地叠加轴角表示的旋转和矩阵表示的旋转。

记叠加后的旋转为$\*R' = \begin{bmatrix}\*r'_1 &\*r'_2 &\*r'_3\end{bmatrix}$。

当旋转角$\theta$较小时，我们可以做如下近似：

$$
\*r_i' = \*r_i + \omega \times \*r_i
$$

> 这是因为$\omega \times \*r_i$为切向速度，因此当$\theta$极小时，它可以被近似为$\*r_i$在旋转$\omega$下的位移

利用上式就能在得出$\omega$的情况下，
仅进行三次叉积和加法就叠加旋转。



## 总结

本节总结计算式。
已知线性变换$\*A=[\*a_1\ \*a_2\ \*a_3]$，
上一轮迭代结果$\*R=[\*r_1\ \*r_2\ \*r_3]$，
求本轮迭代结果$\*R'=[\*r'_1\ \*r'_2\ \*r'_3]$：

$$
\omega =
\frac{
    \sum_i \*r_i \times \*a_i
}{
    \sum_i \*r_i \cdot \*a_i
}
\\

\left\{
\begin{aligned}
    \*r_1' = \*r_1 + \omega \times \*r_1 \\
    \*r_2' = \*r_2 + \omega \times \*r_2 \\
    \*r_3' = \*r_3 + \omega \times \*r_3 \\
\end{aligned}
\right.
$$


## 实验

本节对该方法进行了实验测试。
我们关注两个变量：
* 迭代次数
* 旋转角度：这一项指的是输入的$\*R$（上一轮迭代结果）要转多少角度才能到达线性变换$\*A$中包含的旋转，会有这一项是因为前文中我们多次假设$\theta$极小

评估结果的值为该方法的误差关于极分解方法(Ground Truth)的比值。
记极分解方法提取的旋转为$\*R_P$，
该方法提取的旋转为$\*R_M$，
则评估值$v$为：

$$
v = \frac{
    ||\*A - \*R_M||_F^2
}{
    ||\*A - \*R_P||_F^2
}
$$

对10000组随机生成的$\*A, \*R$进行实验，实验结果如下：

![](pic\muller.extrot.errors.png)

其中：
* 横轴为迭代次数
* 纵轴为旋转角与$\pi$的比值：$\frac{\theta}{\pi}$
* z轴（每一格的数值）为评估值$v$，数值越大（越黄）说明误差越高，数值越小（越蓝）说明误差越小

可以看到：
* 当旋转角度大于$1 \approx 0.3\pi$时，muller方法的误差值会陡增
    * 因此旋转角度应当小于$1$
* 性价比最高的迭代次数应该是3次
  * 性价比第二高的是2次
  * 1次迭代的话误差会显著增大
  * 4次再往上的话提升效果很不明显，且也很不稳定了
    * 我怀疑该方法没有收敛性：即，当迭代次数无穷大时也收敛不到精确解























# 附录

## 验证$\Delta \*R$

$$
\argmin_{\Delta \*R} ||\*a_i - \Delta \*R \*r_i||_2
\\

\begin{aligned}
    \text{s.t. }
    & \Delta\*R^T\Delta\*R = \*I \\
    & \det{\Delta\*R} = 1
\end{aligned}
$$

本节将验证该优化问题的解为绕
$\frac{\*r_i \times \*a_i}{|\*r_i \times \*a_i|}$旋转
$\arccos\frac{\*r_i\cdot\*a_i}{|\*a_i|}$的旋转。

首先证明$\Delta \*R\*r_i = \frac{\*a_i}{|\*a_i|}$——

采用四元数来表示$\Delta \*R$，将其记为$\*q$：

$$
\*q =
\left(
    \cos{\frac{\theta}{2}},
    \phi
    \sin{\frac{\theta}{2}}
\right)
$$

其中（省略下标$\ _i$）

$$
\left\{
\begin{aligned}
    \phi &= \frac{\*r \times \*a}{|\*r \times \*a|} \\
    \theta &= \arccos\frac{\*r\cdot\*a}{|\*a|}
\end{aligned}
\right.
$$

则$\Delta \*R$旋转施加的结果为：


$$
\begin{aligned}
    &
    \*q 
    \left(
        0,
        \*r
    \right)
    \*q^{-1}
    \\

    =&
    \left(
        \cos{\frac{\theta}{2}},
        \phi
        \sin{\frac{\theta}{2}}
    \right)
    \left(
        0,
        \*r
    \right)
    \left(
        \cos{\frac{\theta}{2}},
        -
        \phi
        \sin{\frac{\theta}{2}}
    \right)
    \\

    =&
    \left(
        0,
        \left(
            \cos^2\frac{\theta}{2} - \sin^2\frac{\theta}{2} ||\phi||^2
        \right)
        \*r
        +
        2\sin^2\frac{\theta}{2} (\phi \cdot \*r) \phi
        +
        2\sin\frac{\theta}{2}\cos\frac{\theta}{2} (\phi \times \*r)
    \right)
    \\

    =&
    \left(
        0,
        \cos\theta \*r
        +
        \sin\theta (\phi \times \*r)
    \right)
    \\
\end{aligned}
$$

其中

$$
\begin{aligned}
    & \phi \times \*r
    \\
    =&
    \frac{\*r \times \*a}{|\*r \times \*a|} \times \*r
    \\
    =&
    \frac{
        \*a (\*r \cdot \*r) - \*r (\*a \cdot \*r)
    }{
        |\*r \times \*a|
    }
    \\
    =&
    \frac{
        \*a - (\*a \cdot \*r) \*r
    }{
        |\*a| \sin\theta
    }
    \\
\end{aligned}
$$

因此：

$$
\begin{aligned}
    &
    \cos\theta \*r
    +
    \sin\theta (\phi \times \*r)
    \\
    =&
    \cos\theta \*r
    +
    \frac{
        \*a - |\*a| \cos\theta \*r
    }{
        |\*a|
    }
    \\
    =&
    \frac{\*a}{|\*a|}
    \\
\end{aligned}
$$

总结上述推导，可得：

$$
\Delta \*R\*r_i = \frac{\*a_i}{|\*a_i|}
$$

然后再是要证明$\frac{\*a_i}{|\*a_i|}$为以下优化问题的解：

$$
\argmin_{\*r_i} ||\*a_i - \*r_i||_2
\\

\begin{aligned}
    \text{s.t. }
    & |\*r_i| = 1
\end{aligned}
$$

很显然，不证明了。

