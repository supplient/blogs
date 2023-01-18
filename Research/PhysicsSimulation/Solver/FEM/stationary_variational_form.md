* 欲求解边值问题
* 设一个在trial space $V$中的近似解trial funciton $u\in V$
* 我们想要让$u$尽可能接近精确解$u_e$，但我们不知道$u_e$的解析式，所以没法直接$\min ||u-u_e||$。
* Garlekin Method给出了一个定理：当$(R, v)=0 \quad \forall v \in V$时，$||u-u_e||_V = \min_{v\in V}||v-u_e||_V$，即$u$为$V$中的最优解。
* 因此我们转为求使得$(R,v) = 0 \quad \forall v \in V$成立的$u$。

$(R,v)=0 \quad \forall v \in V$被称为变分形式(variational form)。

通过对$(R,v)$应用分部积分，可以降低对$u$的导数要求（例如如果微分方程里有$u''$的话，那就要求$u$有二阶导，而降低一阶要求后，就只需要$u$有一阶导了），从而得到弱形式：

$$
F(u;v) = 0 \quad \forall v \in V
$$

如果$F(u;v)$是一个bilinear form的话，那常见的表现形式为：

$$
a(u,v) = L(v) \quad \forall v \in V
$$

原边值问题的狄利克雷边值条件（e.g. $u(0)=0$）被显式收进了$V$中，诺依曼边值条件（e.g. $u'(0)=1$）则在分部积分的过程中被隐式收入了弱形式中。

