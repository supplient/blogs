import numpy as np
import torch
import numba.cuda as cu

@cu.jit(device=True)
def assign_slice(dst, src, col_n):
	for i in range(col_n):
		dst[i] = src[i]

@cu.jit
def enter(upside, downside, dumb_R):
	di = cu.grid(1)
	if di >= downside.shape[0]:
		return
	ui = di * 2

	A = downside[di]
	L = upside[ui]
	if ui+1 < upside.shape[0]:
		R = upside[ui+1]
	else:
		R = dumb_R

	A[0, 0] = L[0]
	A[0, 1] = ui
	A[1, 0] = L[0]
	A[1, 1] = ui
	A[2, 0] = R[0]
	A[2, 1] = ui + 1
	A[3, 0] = R[0]
	A[3, 1] = ui + 1

@cu.jit
def up2down(upside, downside, dumb_R):
	di = cu.grid(1)
	if di >= downside.shape[0]:
		return
	ui = di * 2

	A = downside[di]
	L = upside[ui]
	if ui+1 < upside.shape[0]:
		R = upside[ui+1]
	else:
		R = dumb_R

	# A0
	assign_slice(A[0], L[0], 2)

	# A1
	if L[3, 0] != 0:
		assign_slice(A[1], L[3], 2)
	elif L[2, 0] != 0:
		assign_slice(A[1], L[2], 2)
	elif L[1, 0] != 0:
		assign_slice(A[1], L[1], 2)
	else:
		assign_slice(A[1], A[0], 2)

	# A2
	if R[0, 0] != 0:
		assign_slice(A[2], R[0], 2)
	else:
		assign_slice(A[2], A[1], 2)
	
	# A3
	if R[3, 0] != 0:
		assign_slice(A[3], R[3], 2)
	elif R[2, 0] != 0:
		assign_slice(A[3], R[2], 2)
	elif R[1, 0] != 0:
		assign_slice(A[3], R[1], 2)
	else:
		assign_slice(A[3], A[2], 2)

@cu.jit
def down2up(downside, upside):
	ui = cu.grid(1)
	if ui >= upside.shape[0]:
		return
	di = int(ui / 2)
	is_L = (ui % 2) == 0

	A = downside[di]
	X = upside[ui]

	off = 0 if is_L else 2
	assign_slice(X[0], A[off + 0], 2)
	assign_slice(X[1], X[1] if X[1, 0] != 0 else X[0], 2)
	assign_slice(X[2], X[2] if X[2, 0] != 0 else X[1], 2)
	assign_slice(X[3], A[off + 1], 2)

@cu.jit
def leave(downside, upside):
	ui = cu.grid(1)
	if ui >= upside.shape[0]:
		return
	di = int(ui / 2)
	is_L = (ui % 2) == 0

	A = downside[di]
	X = upside[ui]

	off = 0 if is_L else 2
	assign_slice(X, A[off], 2)



block_size = 256
def cal_block_num(n):
	if n == 0: return 0
	return (int)((n-1)/block_size)+1

def gpu_solve(a: torch.Tensor):
	# a must be 1-D tensor

	# Reshape to 2-D tensor
	a = a.reshape((*a.shape, 1))

	dn_list = []
	dn = a.shape[0]
	while True:
		dn = (int)((dn+1)/2)
		dn_list.append(dn)
		if dn == 1:
			break
	dn_sum = np.sum(dn_list)

	# Init d & dumb_R
	d = torch.empty((dn_sum, 4, 2), device="cuda")
	dumb_R_enter = torch.zeros((1), device="cuda")
	dumb_R_up2down = torch.zeros((4, 2), device="cuda")

	def get_d(left, right):
		left = min(int(left), d.shape[0])
		right = min(int(right), d.shape[0])
		return d[left:right]

	enter[cal_block_num(dn_list[0]), block_size](a, get_d(0, dn_list[0]), dumb_R_enter)

	left = 0
	right = dn_list[0]
	for i in range(1, len(dn_list)):
		length = dn_list[i]
		nleft = right
		nright = nleft + length
		up2down[cal_block_num(length), block_size](get_d(left, right), get_d(nleft, nright), dumb_R_up2down)
		left = nleft
		right = nright

	for i in range(len(dn_list)-2, -1, -1):
		length = dn_list[i]
		nright = left
		nleft = nright - length
		down2up[cal_block_num(length), block_size](get_d(left, right), get_d(nleft, nright))
		left = nleft
		right = nright

	res = torch.empty((*a.shape[:-1], 2), device="cuda")
	leave[cal_block_num(a.shape[0]), block_size](get_d(0, dn_list[0]), res)
	return res.select(-1, 0), res.select(-1, 1).int()




def cpu_solve(a):
	import copy
	b = np.empty_like(a)
	t = np.empty_like(a, dtype=int)
	for i in range(0, len(a)):
		if a[i] == 0:
			b[i] = b[i-1]
			t[i] = t[i-1]
		else:
			b[i] = a[i]
			t[i] = i
	return b, t

if __name__ == "__main__":
	n = 1773
	sn = int(n/2)
	a = np.random.randint(1, 10, size=(n))
	a[np.random.choice(n, sn)] = 0

	print("CPU solving...")
	cpu_res, cpu_ri2oi = cpu_solve(a)
	print("GPU solving...")
	gpu_res, gpu_ri2oi = gpu_solve(torch.tensor(a, device="cuda", dtype=torch.float))
	gpu_res = gpu_res.cpu().numpy()
	gpu_ri2oi = gpu_ri2oi.cpu().numpy()

	print("Origin:\t" + str(a))
	print("CPU:\t" + str(cpu_res))
	print("GPU:\t" + str(gpu_res))

	print("Check result...")
	if np.any(~np.equal(cpu_res, gpu_res)):
		print("!!!!Failed!!!!")
	else:
		print("Succeed")

	print("Check resIndex -> originIndex...")
	if np.any(~np.equal(cpu_ri2oi, gpu_ri2oi)):
		print("!!!!Failed!!!!")
	else:
		print("Succeed")