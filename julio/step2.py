import numpy as np

# It seems like I didn't save the file
# I created this quickly. Check input data

R_1 = 89.14
V_1 = 11.4
I_1=0.16
I_2=0.14

R_2 = ((1+2*I_1)/(1+2*I_2))**(18/15)*R_1
V_2 = (R_1/R_2)**(2/3)*V_1

print(R_2)
print(V_2)