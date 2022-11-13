---
title: 利用Numba为Pytorch自定义Function
zhihu-tags: Pytorch, Numba, CUDA
zhihu-url: https://zhuanlan.zhihu.com/p/582978353
---
本文简要介绍如何利用Numba为Pytorch自定义Function，
从而能够在不编写C++ Extension的情况下，
使用纯Python编写使用CUDA Kernel的Function。


# 1. 继承`torch.autograd.Function`
为了自定义一个能集成进pytorch的自动求导系统的操作，
我们需要继承`torch.autograd.Function`，
并重载它的`forward`, `backward`函数。

这部分的详情请参阅[Extending PyTorch](https://pytorch.org/docs/stable/notes/extending.html#extending-torch-autograd)。

``` python
import torch
class IncFunction(torch.autograd.Function):
	@staticmethod
	def forward(ctx, x: torch.Tensor):
		ctx.save_for_backward(x)

		y = x * x

		return y

	@staticmethod
	def backward(ctx, grad_y: torch.Tensor):
		x, = ctx.saved_tensors
		grad_x = None

		if ctx.needs_input_grad[0]:
			grad_x = 2 * x * grad_y
		
		return grad_x
inc = IncFunction.apply
```


# 2. 编写CUDA kernel
我们使用[Numba](https://numba.pydata.org/)来编写CUDA kernel，替换掉上面代码中的`y = x * x`。

Numba是一个JIT库，能够在运行时将一个python函数编译成可执行代码。
这里我们就是依靠它的`numba.cuda`模块来将python函数编译成调用CUDA API的可执行代码。

具体的CUDA kernel编写方法请参阅[Numba的教程](https://numba.readthedocs.io/en/stable/cuda/kernels.html)
和更全面复杂的[Nvidia的CUDA Programming Guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html)。

``` python
import torch
import numba.cuda as cu


# Convenient function for specifying CUDA thread block size
_block_size = 512
def _cal_block_num(n):
	return int((n-1)/_block_size) + 1

class IncFunction(torch.autograd.Function):
	@staticmethod
	@cu.jit
	def cuda_inc(y, x):
		i = cu.grid(1)
		if i >= x.shape[0]:
			return
		y[i] = x[i] * x[i]

	@staticmethod
	def forward(ctx, x: torch.Tensor):
		ctx.save_for_backward(x)

		y = torch.empty_like(x, device=x.device)

		_req_memo = [x.requires_grad]
		x.requires_grad = False
		IncFunction.cuda_inc[_cal_block_num(x.flatten().shape[0]), _block_size](y.flatten(), x.flatten())
		x.requires_grad, = _req_memo

		return y

	@staticmethod
	def backward(ctx, grad_y: torch.Tensor):
		x, = ctx.saved_tensors
		grad_x = None

		if ctx.needs_input_grad[0]:
			grad_x = 2 * x * grad_y
		
		return grad_x
inc = IncFunction.apply
```

注意上文代码中有一处细节：`x.requires_grad = False`。
这是因为如果传给Numba一个`requires_grad == True`的Tensor的话，
它会报错：

> `Can't get __cuda_array_interface__ on Variable that requires grad. If gradients aren't required, use var.detach() to get Variable that doesn't require grad.`

我觉得这是Pytorch的bug，
因为根据[Pytorch的官方文档](https://pytorch.org/docs/stable/notes/extending.html#how-to-use)：

> Tensor arguments that track history (i.e., with requires_grad=True) will be converted to ones that don’t track history before the call, and their use will be registered in the graph. 

也就是不管`x`的`requires_grad`是否为`True`，
它在`forward`函数里进行的计算都不会被逐一记录，
它在graph中的记录只有一整个`Function`的。
通过查看`grad_fn`也很容易验证这一现象：

``` python
>>> y = inc(x)
>>> y.grad_fn
<torch.autograd.function.IncFunctionBackward object at 0x000002114A1BE5E0>
```

可以看到，`y`的`grad_fn`确实是一整个`IncFunction.backward`。


所以其实Pytorch应该帮我把`requires_grad`在`forward`函数里给临时设为`False`的，
但Pytorch没有这么做，
也就导致Numba接收到一个`requires_grad`为True的张量，
弄得它以为我想让它自动求导了，
可它确实做不到，于是就报错了。

因此我们需要临时手动关掉`requires_grad`，从而也就有了上文的代码：

``` python
_req_memo = [x.requires_grad]
x.requires_grad = False
# Call Numba Kernel Function
x.requires_grad, = _req_memo
```


# 3. 兼容CPU
最后一个问题是如果输入的Tensor `x`不在GPU上而是在CPU上，
那会报错：

> `Cannot determine Numba type of <class 'torch.Tensor'>`


这是因为我们的kernel函数`cuda_inc`是被编译为CUDA函数的，
它之前之所以能接受Pytorch的Tensor是因为Pytorch在GPU上的Tensor实现了[`__cuda_array_interface__`](https://numba.readthedocs.io/en/stable/cuda/cuda_array_interface.html)。

而在CPU上的Pytorch tensor当然是没有实现这个接口的，
所以numba就无法识别出来了，结果也就报了上面的错。

解决方案很简单：提供一个专门的CPU版本即可。
例如可以根据`x`的`is_cuda`来分支判断：

``` python
import torch
import numba.cuda as cu


# Convenient function for specifying CUDA thread block size
_block_size = 512
def _cal_block_num(n):
	return int((n-1)/_block_size) + 1

class IncFunction(torch.autograd.Function):
	@staticmethod
	@cu.jit
	def cuda_inc(y, x):
		i = cu.grid(1)
		if i >= x.shape[0]:
			return
		y[i] = x[i] * x[i]

	@staticmethod
	def forward(ctx, x: torch.Tensor):
		ctx.save_for_backward(x)

		y = torch.empty_like(x, device=x.device)
		if x.is_cuda:
			# GPU implementation
			_req_memo = [x.requires_grad]
			x.requires_grad = False
			IncFunction.cuda_inc[_cal_block_num(x.flatten().shape[0]), _block_size](y.flatten(), x.flatten())
			x.requires_grad, = _req_memo
		else:
			# CPU implementation
			# Silly implementation, just for demonstration purpose
			xf = x.flatten()
			yf = y.flatten()
			for i in range(xf.shape[0]):
				yf[i] = xf[i] * xf[i]

		return y

	@staticmethod
	def backward(ctx, grad_y: torch.Tensor):
		x, = ctx.saved_tensors
		grad_x = None

		if ctx.needs_input_grad[0]:
			grad_x = 2 * x * grad_y
		
		return grad_x
inc = IncFunction.apply


if __name__ == "__main__":
	x = torch.randn([5, 5], dtype=torch.float64, requires_grad=True, 
		# device="cpu"
		device="cuda"
	)

	y = inc(x)
	print(f"Check inc(x).grad_fn: {y.grad_fn}")

	testres = torch.autograd.gradcheck(inc, x)
	print(f"Check grad by gradcheck: {testres}")
```

上述代码中我还加入了测试代码，可以直接运行来检查结果。
为了方便下载，我也上传了一份在[gist](https://gist.github.com/supplient/2373a571f7d09a06879446b622b6b609)上。






