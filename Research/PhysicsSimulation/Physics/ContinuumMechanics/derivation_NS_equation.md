# Balance Laws
如果只考虑等温流体，则可以忽略热力学相关的温度(temperature)、热(heat)，
则一共有$3+1+9=13$个未知数需要求解：

$$
\begin{aligned}
& v_i & 速度 & \quad \text{3 unknowns} \\
& \rho & 密度 & \quad \text{1 unknown} \\
& S_{ij} & 应力 & \quad \text{9 unknowns} \\
\end{aligned}
$$

而为了求解这13个未知数，我们手头有的公式目前只有balance law。
又因为忽略了热力学相关因素，所以Balance Laws里的热力学第一定律被丢掉了。
于是Balance Laws中剩下的公理都是和运动学相关的了(See Section 5.3):

$$
\left\{
\begin{aligned}

& \dot{\rho} + \rho\nabla^x\cdot \bm{v} = 0 & [\text{质量守恒}] \\
& \rho\dot{\bm{v}} = \nabla^x\cdot \bm{S} + \rho \bm{b} & [\text{线动量守恒}] \\
& S^T = S & [\text{角动量守恒}] \\

\end{aligned}
\right.
$$

这里我们选取的是Eulerian Form of Balance Laws，似乎在流体仿真的时候比较流行用Eulerian Form。

上述三个公式提供了$1+3+3=7$个等式，所以为了求解13个未知数，还需要$13-7=6$个等式。
这6个等式将由本构方程(constitutive equation)提供。

# Constitutive Model
称一个连续体为不可压缩的牛顿流体，若：
1. 密度均匀：$\rho_0(X, t)=\rho_0>0(\text{constant})$
2. 不可压缩：$\nabla^x\cdot \bm{v} = 0$
3. 应力满足：$\bm{S}=-p\bm{I}+2\mu \mathrm{sym}(\nabla^x\bm{v})$

上式三个条件即为不可压缩牛顿流体的本构方程。

# Constraints for Constitutive Model
* Result 6.8中验证了在该本构方程下连续体的Frame-Indifference性质依然被满足。
* Section 6.3.4中验证了在该本构方程下热力学第二定律依然被满足。

# 简化公式
联立Balance Laws和Constitutive Model：

$$
\left\{
\begin{aligned}

& \dot{\rho} + \rho\nabla^x\cdot \bm{v} = 0 & (\text{质量守恒}) \\
& \rho\dot{\bm{v}} = \nabla^x\cdot \bm{S} + \rho \bm{b} & (\text{线动量守恒}) \\
& S^T = S & (\text{角动量守恒}) \\

& \rho_0(X, t)=\rho_0>0(\text{constant}) & (密度均匀) \\
& \nabla^x\cdot \bm{v} = 0 & (不可压缩) \\
& \bm{S}=-p\bm{I}+2\mu \mathrm{sym}(\nabla^x\bm{v}) & (应力条件) \\

\end{aligned}
\right.
$$

其中$\bm{b}(x, t), \rho_0, \mu$为给定的body force field per unit mass, density, absolute viscosity。
注意$\rho_0, \mu$都为与$x, t$无关的常数。

## 1. 角动量守恒
注意到对式(应力条件)两边取转置会得到：

$$
\bm{S}^T = -p\bm{I} + 2\mu\mathrm{sym}(\nabla^x v)
$$

所以式(应力条件)隐含了$\bm{S}=\bm{S}^T$，已经隐含了式(角动量守恒)。


## 2. 质量守恒
将式（不可压缩）$\nabla^x\cdot \bm{v}$代入式（质量守恒）中会得到：

$$
\dot{\rho} = \frac{\mathrm{d}\rho}{\mathrm{d}t} = 0
$$

即$\rho$不随$t$发生变化，
所以$\rho(x, t) = \rho(x, 0)$，
代入式（密度均匀），即有：

$$
\rho(x, t) = \rho_0 > 0 (\text{constant})
\tag{常数密度}
$$

上式隐含了式（质量守恒）和式（密度均匀）。

## 3. 线动量守恒
将式（应力条件）和式（常数密度）代入式（线动量守恒）中，消掉$\bm{S}, \rho$，得到：

$$
\begin{aligned}
\rho_0\dot{\bm{v}} 
&= \nabla^x\cdot (-p\bm{I}+2\mu \mathrm{sym}(\nabla^x\bm{v})) + \rho_0 \bm{b} \\
&= -\nabla^x\cdot (p\bm{I}) + 2\mu \nabla^x \cdot \mathrm{sym}(\nabla^x\bm{v}) + \rho_0 \bm{b} \\
\end{aligned}
\tag{1}
$$

其中各项有：

$$
\left\{
\begin{aligned}
& \dot{\bm{v}} = \frac{\partial}{\partial t} \bm{v} + (\nabla^x \bm{v}) \bm{v} & \text{[Result 4.7]} \\
& \nabla^x\cdot(p\bm{I}) = p\nabla^x\cdot\bm{I} + \bm{I}\nabla^xp = \nabla^xp & \\
& \nabla^x\cdot\mathrm{sym}(\nabla^x\bm{v}) = \frac{1}{2} ( \nabla^x \cdot \nabla^x\bm{v} + \nabla^x \cdot (\nabla^x\bm{v})^T) = \frac{1}{2} \Delta^x\bm{v} & \text{[See Below]}\\
\end{aligned}
\right.
$$

展开其中对$\nabla^x\cdot\mathrm{sym}(\nabla^x\bm{v})$的推导：

$$
\begin{aligned}
& \nabla^x \cdot \nabla^x \bm{v} = \Delta^x \bm{v} & \text{[拉普拉斯算子的定义]} \\
\end{aligned}
$$

$$
\begin{aligned}
\nabla^x \cdot (\nabla^x\bm{v})^T 
&= \frac{\partial(\nabla^x \bm{v})^T_{ij}}{\partial x_j}\bm{e}_i & \text{[散度定义]} \\
&= \frac{\partial(\frac{\partial v_j}{\partial x_i})}{\partial x_j}\bm{e}_i  & \text{[梯度定义]} \\
&= \frac{\partial^2 v_j}{\partial x_i\partial x_j}\bm{e}_i  & \\
&= \frac{\partial(\frac{\partial v_j}{\partial x_j})}{\partial x_i}\bm{e}_i  & \text{[任意阶导数连续]} \\
&= \nabla^x(\frac{\partial v_j}{\partial x_j})  & \text{[梯度定义]} \\
&= \nabla^x(\nabla^x \cdot \bm{v})  & \text{[散度定义]} \\
&= \nabla^x\bm{0} & \text{[不可压缩]} \\
&= 0 & \\
\end{aligned}
$$

将这三项带回式1中，得到式（线动量守恒）化简后的结果：

$$
\begin{aligned}

\rho_0 \left[\frac{\partial}{\partial t} \bm{v} + (\nabla^x \bm{v}) \bm{v} \right]
&= -\nabla^xp + \mu \Delta^x\bm{v} + \rho_0 \bm{b} \\

\end{aligned}

\tag{2}
$$

上式隐含了式（应力条件）、式（常数密度）、式（线动量守恒）。

----------------------

## 4. 整理公式
最开始通过联立Balance Laws与Constitutive Model得到的方程组经过前文的化简后变为：
（联立式（不可压缩）和式2）

$$
\left\{
\begin{aligned}
\rho_0 \left[\frac{\partial}{\partial t} \bm{v} + (\nabla^x \bm{v}) \bm{v} \right]
&= -\nabla^xp + \mu \Delta^x\bm{v} + \rho_0 \bm{b} \\
\nabla^x\cdot \bm{v} &= 0 \\
\end{aligned}
\right.
$$

上式即为**Navier-Stokes Equations**。

其中：
* $\bm{b}, \rho_0, \mu$为给定的body force field per unit mass, density, absolute viscosity。
* 一共有4个等式和4个未知数：$p, \bm{v}$，因此可以解出来（笑）。




