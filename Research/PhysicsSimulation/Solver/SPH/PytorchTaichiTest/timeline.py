import torch

class Timeline:
	def __init__(self):
		self.key2dict: dict[str, dict[int, torch.Tensor]] = {}
		self.key2tensor: dict[str, torch.Tensor] = {}

	def memo(self, i, key2target: dict[str, torch.Tensor]):
		for key, target in key2target.items():
			if not key in self.key2dict.keys():
				self.key2dict[key] = {}
			self.key2dict[key][i] = target.clone()
	
	def tensoralize(self):
		for key, dic in self.key2dict.items():
			n = max(dic.keys())
			tensor = torch.empty(
				size=(n+1, *dic[n].shape),
				device=dic[n].device,
				dtype=dic[n].dtype
			)
			for i, v in dic.items():
				tensor[i] = v
			self.key2tensor[key] = tensor
	
	def __getitem__(self, key):
		return self.key2tensor[key]