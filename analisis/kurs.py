import scipy
import scipy.integrate as integrate
import numpy as np
import math
g = 0.5
g_v = [0.5, 2.3, 4.8]
global m
delta = 0

def fn_1(z):
	return (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * (z-(1 - delta)*g*np.sqrt(2**n)))**2*(0.5*(math.erfc(z/np.sqrt(2))))**(m-1)

q_m = []
for k in range(3, 13 + 1, 2):
	i = 1
	z = 0
	for n in range(0, 10):
		m = 2**k
		q_m.append(integrate.quad(fn_1, -math.inf, math.inf))

		
		