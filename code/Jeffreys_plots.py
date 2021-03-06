import pylab as plt
import numpy as np
import fisher
from config import IM, C, path
from data import get_S_A

plt.ion()
plt.show()

##

S, A = get_S_A(path, IM, C)

num_theta = 20
theta_tab = np.zeros((num_theta,2))
theta_tab[:,0] = np.linspace(0.1, A.max(), num=num_theta)
theta_tab[:,1] = np.linspace(1/10,1/2, num=num_theta)
tmin = theta_tab.min()
tmax = theta_tab.max()
theta_grid1, theta_grid2 = np.meshgrid(theta_tab[:,0], theta_tab[:,1])

##


J_MC = fisher.Jeffreys_MC(theta_tab[:,0], theta_tab[:,1], A)


a_tab, h_a = np.linspace(10**-10, 2*A.max(), num=1000, retstep=True)
J_t = fisher.Jeffreys_rectangles(theta_tab[:,0], theta_tab[:,1], a_tab, h_a)


a_tab, h_a = np.linspace(10**-10, 2*A.max(), num=100, retstep=True)
J_s = fisher.Jeffreys_simpson(theta_tab[:,0], theta_tab[:,1], a_tab)



plt.figure(1)
plt.clf()
axes = plt.axes(projection="3d")
axes.plot_surface(theta_grid1, theta_grid2, J_MC.T)

plt.title('Jeffreys Monte-Carlo')
axes.set_xlabel('alpha')
axes.set_ylabel('beta')
axes.set_zlabel('J_MC')



plt.figure(2)
plt.clf()
axes = plt.axes(projection="3d")
axes.plot_surface(theta_grid1, theta_grid2, J_t.T)

plt.title('Jeffreys approx. rectangles')
axes.set_xlabel('alpha')
axes.set_ylabel('beta')
axes.set_zlabel('J_t')



plt.figure(3)
plt.clf()
axes = plt.axes(projection="3d")
axes.plot_surface(theta_grid1, theta_grid2, J_s.T)

plt.title('Jeffreys via Simson')
axes.set_xlabel('alpha')
axes.set_ylabel('beta')
axes.set_zlabel('J_s')



j_min, j_max = 0, np.max(J_t)
levels = np.linspace(j_min, j_max, 15)

plt.figure(figsize=(4.5, 2.5))
plt.contourf(theta_grid1, theta_grid2, J_s.T, cmap='viridis', levels=levels)
plt.title(r'Objective prior via simpson')
plt.axis([theta_grid1.min(), theta_grid1.max(), theta_grid2.min(), theta_grid2.max()])
plt.colorbar()
plt.xlabel(r"$\alpha$")
plt.ylabel(r"$\beta$")
plt.tight_layout()
plt.show()

##
# test de méthode de simpson via numba

a_tab, h_a = np.linspace(10**-10, 2*A.max(), num=50, retstep=True)

import time
atime = time.time()
JJ = fisher.Fisher_Simpson_Numb_paral(theta_tab[:,0], theta_tab[:,1], a_tab)
# fisher.Fisher_rectangles(theta_tab[:,0], theta_tab[:,1], a_tab, h_a)
btime = time.time()

##

c= time.time()
JJJ = fisher.Jeffreys_simpson_numba(theta_tab[:,0], theta_tab[:,1], a_tab)
d= time.time()



