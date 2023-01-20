
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