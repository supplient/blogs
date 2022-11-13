import numpy as np
import torch
import numba.cuda as cu

@cu.jit
def enter(upside, downside):
	di = cu.grid(1)
	if di >= downside.shape[0]:
		return
	ai = di * 2

	I = downside[di, 0:4]
	S = downside[di, 4:8]
	li  = upside[ai]
	ri = 0 if ai+1 >= upside.shape[0] else upside[ai+1]

	I[0] = li
	I[1] = li
	I[2] = ri
	I[3] = ri

	ls = 1 if li != ri else 2
	rs = 1 if li != ri else 2

	S[0] = ls
	S[1] = ls
	S[2] = rs
	S[3] = rs


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

	AI = A[0:4]
	AS = A[4:8]
	LI = L[0:4]
	LS = L[4:8]
	RI = R[0:4]
	RS = R[4:8]

	AI[0] = LI[0]
	AI[1] = LI[3]
	AI[2] = RI[0]
	AI[3] = RI[3]

	AS[0] = LS[0]
	AS[0] += RS[0] if AI[0] == RI[0] else 0

	AS[1] = LS[3]
	AS[1] += RS[0] if AI[1] == RI[0] else 0

	AS[2] = RS[0]
	AS[2] += LS[3] if AI[2] == LI[3] else 0

	AS[3] = RS[3]
	AS[3] += LS[3] if AI[3] == LI[3] else 0


@cu.jit
def down2up(downside, upside):
	ui = cu.grid(1)
	if ui >= upside.shape[0]:
		return
	di = int(ui / 2)
	off = (ui % 2) * 2

	A = downside[di]
	X = upside[ui]

	AI = A[0+off:2+off]
	AS = A[4+off:6+off]

	XI = X[0:4]
	XS = X[4:8]

	for i in range(4):
		for j in range(2):
			if XI[i] == AI[j]:
				XS[i] = AS[j]
				break


@cu.jit
def leave(downside, upside):
	ai = cu.grid(1)
	if ai >= upside.shape[0]:
		return
	di = int(ai / 2)
	off = (ai % 2) * 2

	upside[ai] = downside[di, 4+off]



block_size = 256
def cal_block_num(n):
	if n == 0: return 0
	return (int)((n-1)/block_size)+1

def gpu_solve(a):
	a = torch.tensor(a, device="cuda")

	dn_list = []
	dn = a.shape[0]
	while True:
		dn = (int)((dn+1)/2)
		dn_list.append(dn)
		if dn == 1:
			break
	dn_sum = np.sum(dn_list)

	d = torch.empty((dn_sum, 8), device="cuda")
	dumb_R = torch.zeros((8), device="cuda")

	def get_d(left, right):
		left = min(int(left), d.shape[0])
		right = min(int(right), d.shape[0])
		return d[left:right]

	enter[cal_block_num(dn_list[0]), block_size](a, get_d(0, dn_list[0]))

	left = 0
	right = dn_list[0]
	for i in range(1, len(dn_list)):
		length = dn_list[i]
		nleft = right
		nright = nleft + length
		up2down[cal_block_num(length), block_size](get_d(left, right), get_d(nleft, nright), dumb_R)
		left = nleft
		right = nright

	for i in range(len(dn_list)-2, -1, -1):
		length = dn_list[i]
		nright = left
		nleft = nright - length
		down2up[cal_block_num(length), block_size](get_d(left, right), get_d(nleft, nright))
		left = nleft
		right = nright

	leave[cal_block_num(a.shape[0]), block_size](get_d(0, dn_list[0]), a)
	return a


def cpu_solve(a):
	import copy
	a = copy.copy(a)
	memo = {}
	for x in a:
		if not x in memo.keys():
			memo[x] = 0
		memo[x] += 1
	for i in range(len(a)):
		a[i] = memo[a[i]]
	return a


if __name__ == "__main__":
	import random
	n = 1000
	a = []
	i = 1
	while len(a) < n:
		delta = random.randint(1, n-len(a))
		a.extend([i] * delta)
		i += 1
	# a = [1, 1, 1, 2, 2, 2, 2, 3, 3]
	a = np.array(a)

	print("CPU solving...")
	cpu_res = cpu_solve(a)
	print("GPU solving...")
	gpu_res = gpu_solve(a).cpu().numpy()

	print("Origin:\t" + str(a))
	print("CPU:\t" + str(cpu_res))
	print("GPU:\t" + str(gpu_res))

	if np.any(~np.equal(cpu_res, gpu_res)):
		print("!!!!Failed!!!!")
	else:
		print("Succeed")