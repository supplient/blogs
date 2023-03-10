# Condition 1

Let $t'=t+\Delta t$,
and $q'$ is the system state at $t'$.
Then we want

$$
C(q')=0
$$

We get $q'$ using semi-implicit Euler:

$$
\left\{
\begin{aligned}
	q' = q + \Delta t v'\\
	v' = v + \Delta t a
\end{aligned}
\right.
$$

So $C(q')=0$ can be rewrite as:

$$
C(q+\Delta t(v+\Delta t a)) = 0
$$

Let $a=M^{-1}(F_E + F_C)$,
where $F_E$ is the external force,
and $F_C$ is the constraint force.

Rearrange the function variable:

$$
\begin{aligned}
& q+\Delta t(v+\Delta t a) \\
= & q + \Delta t v + \Delta t^2 M^{-1} F_E + \Delta t^2 M^{-1} F_C
\end{aligned}
$$

Let

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

Then the function variable can be rewritten as:

$$
\begin{aligned}
& q+\Delta t(v+\Delta t a) \\
= & q^* + \Delta q
\end{aligned}
$$

So $C(q')=0$ can be rewritten as:

$$
C(q^* + \Delta q) = 0
$$

where $\Delta q$ containing $F_C$ is what we want to solve.



# Condition 2
We want to conserve the momentum if there are only internal forces.
i.e. If $F_C$ is the internal force, then we want

$$
\begin{aligned}
p|_{q^*} &= p|_{q'} \\
\Rightarrow \Delta p :=& p|_{q'} - p|_{q^*} \\
=& Mq'\cdot \mathbf{1} - M q^* \cdot \mathbf{1} \\
=& M(q'-q^*) \cdot \mathbf{1} \\
=& M\Delta q \cdot \mathbf{1} = 0 \\
\end{aligned}
$$

If the constraint force $F_C$ of a constraint $C(q)=0$ is an internal force,
we make the following assumption on $C$:

$$
\forall q \forall \lambda: \nabla C^T \lambda \cdot \mathbf{1} = \mathbf{0}
$$

where $\nabla C = \frac{\partial C}{\partial q}$.

So if we let $\Delta q$ be

$$
\Delta q = M^{-1} \nabla C^T \lambda
$$

the momentum can be conserved for all internal forces as following:

$$
\begin{aligned}
\Delta p
=& M\Delta q \cdot \mathbf{1} \\
=& MM^{-1} \nabla C^T \lambda \cdot \mathbf{1} \\
=& \nabla C^T \lambda \cdot \mathbf{1} \\
\text{[Assumption } &\forall q \forall \lambda: \nabla C^T \lambda \cdot \mathbf{1} = \mathbf{0} \text{]} \\
=& \mathbf{0} \\
\end{aligned}
$$


# System to solve
We have following equations

$$
\left\{
\begin{aligned}
C(q^* + \Delta q) = 0 \\
\Delta q = M^{-1} \nabla C^T \lambda \\
\end{aligned}
\right.
$$

$$
\left\{
\begin{aligned}
	a^* &:= M^{-1} F_E \\
	v^* &:= v + \Delta t a^* \\
	q^* &:= q + \Delta t v^*
\end{aligned}
\right.
$$

Replace $\Delta q$, we have:

$$
C(q^* + M^{-1}\nabla C^T \lambda) = 0
$$

where $\lambda$ is unknown.

If $C$ is $m$-dim,
$\lambda$ is also a $m$-dim vector.
So the system has an unique solution (if it is a linear system and the solution exists).



# Example
![](example.drawio.png)

Notations are shown in the above figure.

Let the constraint be

$$
C(t) = \begin{bmatrix}
	x_A \\
	y_A \\
	(x_B-x_A, y_B-y_A)^2-2
\end{bmatrix}
= \mathbb{0}
$$

Let the external force be

$$
F_E = \begin{bmatrix}
	0 \\
	-g \\
	0 \\
	-g
\end{bmatrix}
$$

where $g$ is the gravitational constant.

Let mass be

$$
M = \begin{bmatrix}
	m_A & 0 & 0 & 0 \\
	0 & m_A & 0 & 0 \\
	0 & 0 & m_B & 0 \\
	0 & 0 & 0 & m_B \\
\end{bmatrix}
$$

where $m_A, m_B$ are the mass of A and B.


Put them into the system to solve(repeated here):


$$
C(q^* + M^{-1}\nabla C^T \lambda) = 0
$$

where $q^*$ is

$$
\left\{
\begin{aligned}
	a^* &:= M^{-1} F_E \\
	v^* &:= v + \Delta t a^* \\
	q^* &:= q + \Delta t v^*
\end{aligned}
\right.
$$

Calculate $q^*$ and $\nabla C$:

$$
q^* = \left[\begin{matrix}\Delta t v^{1}_{A} + x_{A}\\\Delta t \left(- \frac{\Delta t g}{m_{A}} + v^{2}_{A}\right) + y_{A}\\\Delta t v^{1}_{B} + x_{B}\\\Delta t \left(- \frac{\Delta t g}{m_{B}} + v^{2}_{B}\right) + y_{B}\end{matrix}\right]
$$

$$
\nabla C = \left[\begin{matrix}1 & 0 & 0 & 0\\0 & 1 & 0 & 0\\2 x_{A} - 2 x_{B} & 2 y_{A} - 2 y_{B} & - 2 x_{A} + 2 x_{B} & - 2 y_{A} + 2 y_{B}\end{matrix}\right]
$$

where $v=[v_A^1, v_A^2, v_B^1, v_B^2]^T$ is the velocity at time $t$.

Put them into 
$C(q^* + M^{-1}\nabla C^T \lambda) = 0$,
and assume following:

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

We can solve $\lambda$:

$$
\lambda = 
\left[\begin{matrix}- \frac{\Delta t^{2} g}{2} + \frac{\sqrt{- \Delta t^{4} g^{2} + 4}}{2} - 1\\\frac{3 \Delta t^{2} g}{2} - \frac{\sqrt{- \Delta t^{4} g^{2} + 4}}{2} + 1\\- \frac{\Delta t^{2} g}{4} + \frac{\sqrt{- \left(\Delta t^{2} g - 2\right) \left(\Delta t^{2} g + 2\right)}}{4} - \frac{1}{2}\end{matrix}\right]
$$

Replace into $q' = q^* + M^{-1}\nabla C^T \lambda$:

$$
q' = \left[\begin{matrix}0\\0\\- \frac{\Delta t^{2} g}{2} + \frac{\sqrt{- \Delta t^{4} g^{2} + 4}}{2}\\- \frac{\Delta t^{2} g}{2} - \frac{\sqrt{- \Delta t^{4} g^{2} + 4}}{2}\end{matrix}\right]
$$

If $\Delta t = 0.001, g=10$, then

$$
q' = \left[\begin{matrix}0\\0\\0.9999949999875\\-1.0000049999875\end{matrix}\right]
$$

Correct.

However, $\lambda$ has another solution:

$$
\lambda = \left[\begin{matrix}- \frac{\Delta t^{2} g}{2} - \frac{\sqrt{- \Delta t^{4} g^{2} + 4}}{2} - 1\\\frac{3 \Delta t^{2} g}{2} + \frac{\sqrt{- \Delta t^{4} g^{2} + 4}}{2} + 1\\- \frac{\Delta t^{2} g}{4} - \frac{\sqrt{- \left(\Delta t^{2} g - 2\right) \left(\Delta t^{2} g + 2\right)}}{4} - \frac{1}{2}\end{matrix}\right]
$$

which will result $q'$:

$$
q' = \left[\begin{matrix}0\\0\\-1.0000049999875\\0.9999949999875\end{matrix}\right]
$$

This solution corresponds the mirrored situation which should be discard.










