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
			_req_memo = [x.requires_grad]
			x.requires_grad = False
			IncFunction.cuda_inc[_cal_block_num(x.flatten().shape[0]), _block_size](y.flatten(), x.flatten())
			x.requires_grad, = _req_memo
		else:
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
		device="cpu"
		# device="cuda"
	)

	print(f"Check inc(x).grad_fn: {inc(x).grad_fn}")

	testres = torch.autograd.gradcheck(inc, x)
	print(f"Check grad by gradcheck: {testres}")
