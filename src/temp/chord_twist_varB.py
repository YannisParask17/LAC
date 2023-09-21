import numpy as np
import matplotlib.pyplot as plt

r_over_R = np.linspace(0.1,1,30)

c_l_design = 1

tsr = 8
B=3
# aoa = np.deg2rad(6)
aoa = 2/3/tsr


# Equation A
c_over_R = lambda c_l_design, tsr, B, r_over_R:16*np.pi/9/(c_l_design*tsr**2*B*(r_over_R))
            
# Equation B
theta = lambda tsr, r_over_R, aoa: 2/3/(tsr*r_over_R)-aoa
   

# Plotting         
#plt.plot(r_over_R, c_over_R(c_l_design, tsr, B, r_over_R))
#plt.show()

#plt.plot(r_over_R, np.rad2deg(theta(tsr, r_over_R, aoa)))
#plt.show()

B_lst = list(range(1,5))

# Plotting
plt.figure(dpi=300)
for B in B_lst  :    
    plt.plot(r_over_R, c_over_R(c_l_design, tsr, B, r_over_R), label=f'B={B}')
plt.plot(r_over_R, c_over_R(c_l_design, tsr, 100, r_over_R), label=f'B=100', ls='--')
plt.legend()
plt.xlabel('r/R [-]')
plt.ylabel('c/R [-]')
plt.show()

plt.figure(dpi=300)
for B in B_lst  :    
    plt.plot(r_over_R, np.rad2deg(theta(tsr, r_over_R, aoa)), label=f'B={B}')
plt.legend()
plt.show()

plt.plot(r_over_R, np.rad2deg(theta(tsr, r_over_R, aoa)))
plt.show()

fig, axs = plt.subplots(2,1)
for B in B_lst  :    
    axs[0].plot(r_over_R, np.rad2deg(theta(tsr, r_over_R, aoa)), label=f'B={B}')
    axs[1].plot(r_over_R, np.rad2deg(theta(tsr, r_over_R, aoa)), label=f'B={B}')
plt.legend()    
plt.show()        
