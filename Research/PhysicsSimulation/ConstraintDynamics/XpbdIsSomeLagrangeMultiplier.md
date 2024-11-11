已知条件极值问题：

$$
\begin{aligned}
    \min_x\ & H(x) \\
    \text{s.t. } & C(x)=0
\end{aligned}
$$

其中$x\in R^n, H: R^n \rightarrow R, C: R^n \rightarrow R^m$.

如果我们应用拉格朗日乘数法求解该条件极值问题的话，会得到如下方程组：

$$
\mathcal{L} = H + \lambda^T C
\\

\left\{
\begin{aligned}
    & \frac{\partial \mathcal{L}}{\partial x}
    =
    \frac{\partial H}{\partial x}
    +
    \frac{\partial C}{\partial x}^T \lambda
    =0
    \\

    & \frac{\partial \mathcal{L}}{\partial \lambda}
    =
    C
    = 0
\end{aligned}
\right.
$$

以上是求解条件极值问题的常规解法，但我遇到有一种做法是给拉格朗日函数$\mathcal{L}$增加一个$\frac{1}{2}\lambda^T\alpha\lambda$项，即：

$$
\mathcal{L} = H + \lambda^T C + \frac{1}{2}\lambda^T\alpha\lambda
\\

\left\{
\begin{aligned}
    & \frac{\partial \mathcal{L}}{\partial x}
    =
    \frac{\partial H}{\partial x}
    +
    \frac{\partial C}{\partial x}^T \lambda
    =0
    \\

    & \frac{\partial \mathcal{L}}{\partial \lambda}
    =
    C + \alpha \lambda
    = 0
\end{aligned}
\right.
$$

请问这种解法有什么特定的名称吗？它属于哪类最优化方法？