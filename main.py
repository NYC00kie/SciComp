import sys
sys.path.insert(0, './project-code')
from diffusion_cpu import main_cpu

itterations = 10

if __name__ == '__main__':
	for i in range(itterations):
		main_cpu()