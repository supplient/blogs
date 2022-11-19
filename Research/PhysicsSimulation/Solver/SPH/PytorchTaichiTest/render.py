import torch
from torch.nn import Module
from PIL import Image, ImageDraw

class PointRender2D(Module):
	def __init__(self) -> None:
		super().__init__()

	def forward(self, 
		centers: torch.Tensor, 
		radius: float, 
		viewport: list[float], 
		height: int, width: int,
	) -> Image:
		vx, vy, vw, vh = viewport
		r = radius
		
		if centers is torch.Tensor:
			centers = centers.numpy()

		canvas = Image.new(mode="RGBA", size=(width, height), color=(255, 255, 255, 255))
		draw = ImageDraw.Draw(canvas)
		for x, y in centers:
			x = (x-vx)/vw*width
			y = height - (y-vy)/vh*height
			draw.ellipse((x-r, y-r, x+r, y+r), fill=(255, 0, 0, 255))
		return canvas

def imgs2gif(imgs, output_dir, filename, framerate):
	import os
	filepath = os.path.join(output_dir, filename)
	os.makedirs(output_dir, exist_ok=True)
	with open(filepath, mode="bw") as fp:
		imgs[0].save(fp, format="gif", save_all=True, append_images=imgs[1:], optimize=False, duration=1000/framerate, loop=0)
	return filepath