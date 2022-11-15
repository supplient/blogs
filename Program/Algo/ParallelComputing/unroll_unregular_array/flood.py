import numpy as np
import torch
import numba.cuda as cu

@cu.jit
def enter(upside, down_value, down_index, dumb_R):
	di = cu.grid(1)
	if di >= down_value.shape[0]:
		return
	ui = di * 2

	AV = down_value[di]
	AI = down_index[di]
	L = upside[ui]
	if ui+1 < upside.shape[0]:
		R = upside[ui+1]
	else:
		R = dumb_R

	AV[0] = L[0]
	AI[0] = ui
	AV[1] = L[0]
	AI[1] = ui
	if R[0] != 0:
		AV[2] = R[0]
		AI[2] = ui + 1
		AV[3] = R[0]
		AI[3] = ui + 1
	else:
		AV[2] = L[0]
		AI[2] = ui
		AV[3] = L[0]
		AI[3] = ui

@cu.jit
def up2down(up_value, up_index, down_value, down_index, dumb_R_value, dumb_R_index):
	di = cu.grid(1)
	if di >= down_value.shape[0]:
		return
	ui = di * 2

	AV = down_value[di]
	AI = down_index[di]
	LV = up_value[ui]
	LI = up_index[ui]
	if ui+1 < up_value.shape[0]:
		RV = up_value[ui+1]
		RI = up_index[ui+1]
	else:
		RV = dumb_R_value
		RI = dumb_R_index

	# A0
	AV[0] = LV[0]
	AI[0] = LI[0]

	# A1
	if LV[3] != 0:
		AV[1] = LV[3]
		AI[1] = LI[3]
	elif LV[2] != 0:
		AV[1] = LV[2]
		AI[1] = LI[2]
	elif LV[1] != 0:
		AV[1] = LV[1]
		AI[1] = LI[1]
	else:
		AV[1] = AV[0]
		AI[1] = AI[0]

	# A2
	if RV[0] != 0:
		AV[2] = RV[0]
		AI[2] = RI[0]
	else:
		AV[2] = AV[1]
		AI[2] = AI[1]
	
	# A3
	if RV[3] != 0:
		AV[3] = RV[3]
		AI[3] = RI[3]
	elif RV[2] != 0:
		AV[3] = RV[2]
		AI[3] = RI[2]
	elif RV[1] != 0:
		AV[3] = RV[1]
		AI[3] = RI[1]
	else:
		AV[3] = AV[2]
		AI[3] = AI[2]


@cu.jit
def down2up(down_value, down_index, up_value, up_index):
	ui = cu.grid(1)
	if ui >= up_value.shape[0]:
		return
	di = int(ui / 2)
	is_L = (ui % 2) == 0

	AV = down_value[di]
	AI = down_index[di]
	XV = up_value[ui]
	XI = up_index[ui]

	off = 0 if is_L else 2
	XV[0] = AV[off + 0]
	XI[0] = AI[off + 0]

	if XV[1] == 0:
		XV[1] = XV[0]
		XI[1] = XI[0]

	if XV[2] == 0:
		XV[2] = XV[1]
		XI[2] = XI[1]

	XV[3] = AV[off + 1]
	XI[3] = AI[off + 1]

@cu.jit
def leave(down_value, down_index, up_value, up_index):
	ui = cu.grid(1)
	if ui >= up_value.shape[0]:
		return
	di = int(ui / 2)
	is_L = (ui % 2) == 0

	AV = down_value[di]
	AI = down_index[di]
	XV = up_value[ui]
	XI = up_index[ui]

	off = 0 if is_L else 2
	XV[0] = AV[off]
	XI[0] = AI[off]



block_size = 256
def cal_block_num(n):
	if n == 0: return 0
	return (int)((n-1)/block_size)+1

def gpu_solve(x: torch.Tensor):
	# x must be 1-D tensor

	# Reshape to 2-D tensor
	x = x.reshape((*x.shape, 1))

	dn_list = []
	dn = x.shape[0]
	while True:
		dn = (int)((dn+1)/2)
		dn_list.append(dn)
		if dn == 1:
			break
	dn_sum = np.sum(dn_list)

	# Init d & dumb_R
	d_value = torch.empty((dn_sum, 4), dtype=x.dtype, device="cuda")
	d_index = torch.empty((dn_sum, 4), dtype=torch.int, device="cuda")
	dumb_R_enter = torch.zeros((1), dtype=x.dtype, device="cuda")
	dumb_R_value_up2down = torch.zeros((4), dtype=x.dtype, device="cuda")
	dumb_R_index_up2down = torch.zeros((4), dtype=torch.int, device="cuda")

	def get_d(left, right):
		left = min(int(left), d_value.shape[0])
		right = min(int(right), d_value.shape[0])
		return d_value[left:right], d_index[left:right]

	enter[cal_block_num(dn_list[0]), block_size](x, *get_d(0, dn_list[0]), dumb_R_enter)

	left = 0
	right = dn_list[0]
	for i in range(1, len(dn_list)):
		length = dn_list[i]
		nleft = right
		nright = nleft + length
		up2down[cal_block_num(length), block_size](*get_d(left, right), *get_d(nleft, nright), dumb_R_value_up2down, dumb_R_index_up2down)
		left = nleft
		right = nright

	for i in range(len(dn_list)-2, -1, -1):
		length = dn_list[i]
		nright = left
		nleft = nright - length
		down2up[cal_block_num(length), block_size](*get_d(left, right), *get_d(nleft, nright))
		left = nleft
		right = nright

	y_value = torch.empty_like(x, device="cuda")
	y_index = torch.empty_like(x, device="cuda")
	leave[cal_block_num(x.shape[0]), block_size](*get_d(0, dn_list[0]), y_value, y_index)
	y_value = y_value.reshape(y_value.shape[:-1])
	y_index = y_index.reshape(y_index.shape[:-1])
	return y_value, y_index


def cpu_solve(x):
	y = torch.empty_like(x)
	yi2xi = torch.empty_like(x, dtype=int)
	for i in range(0, x.shape[0]):
		if x[i] == 0:
			y[i] = y[i-1]
			yi2xi[i] = yi2xi[i-1]
		else:
			y[i] = x[i]
			yi2xi[i] = i
	return y, yi2xi


@cu.jit
def sum_grad(grad_x, grad_y, yi2xi):
	yi = cu.grid(1)
	if yi < grad_y.shape[0]:
		xi = yi2xi[yi]
		cu.atomic.add(grad_x, xi, grad_y[yi])

class RightFloodFunction(torch.autograd.Function):
	''' 
	## Parameter
	* `x`: must be a 1-D tensor.

	## Return
	* `y`: a 1-D tensor

	## Example
	In  >>> [1, 0, 0, 0, 3, 0, 2, 0, 0, 5, 2]
	Out <<< [1, 1, 1, 1, 3, 3, 2, 2, 2, 5, 2]

	In  >>> [0, 0, 3, 0, 3]
	Out <<< [0, 0, 3, 3, 3]
	'''
	@staticmethod
	def forward(ctx, x: torch.Tensor):
		if x.is_cuda:
			_req_memo = [x.requires_grad]
			x.requires_grad = False
			y, yi2xi = gpu_solve(x)
			x.requires_grad, = _req_memo
		else:
			y, yi2xi = cpu_solve(x)

		ctx.save_for_backward(x, yi2xi)
		return y

	@staticmethod
	def backward(ctx, grad_y: torch.Tensor):
		x, yi2xi = ctx.saved_tensors
		grad_x = None

		if ctx.needs_input_grad[0]:
			grad_x = torch.zeros_like(grad_y, device=grad_y.device)

			if grad_y.is_cuda:
				_req_memo = [grad_y.requires_grad]
				grad_y.requires_grad = False
				sum_grad[cal_block_num(grad_y.shape[0]), block_size](grad_x, grad_y, yi2xi)
				grad_y.requires_grad, = _req_memo
			else:
				for yi in range(grad_y.shape[0]):
					xi = yi2xi[yi]
					grad_x[xi] += grad_y[yi]

		return grad_x
rightflood = RightFloodFunction.apply



if __name__ == "__main__":
	x = torch.tensor([0, 0, 0, 3, 4, 0], dtype=torch.float, device="cuda", requires_grad=True)
	y = rightflood(x)
	print(x)
	print(y)
	# Output:
	# [1, 0, 0, 3, 0, 6, 0, 0]
	# [1, 1, 1, 3, 3, 6, 6, 6]

	if x.grad:
		x.grad.zero_()
	f = torch.sum(y)
	f.backward()
	print(x.grad)
	# Output:
	# [3, 0, 0, 2, 0, 3, 0, 0]