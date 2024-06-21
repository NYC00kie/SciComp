import sys
sys.path.insert(0, './project-code')
from diffusion_cpu import main_cpu

big_itts = 20

if __name__ == '__main__':
	for i in range(big_itts):
		main_cpu()
		print(i)