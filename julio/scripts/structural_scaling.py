import numpy as np

# Ix
def Ix_skin(t_skin, chord, t_blade, w_cap, t_cap):
    return np.pi/8*t_skin*(3*chord*t_blade**2+t_blade**3)

def Ix_cap(t_skin, chord, t_blade, w_cap, t_cap):
    return t_blade**2*w_cap*t_cap/2

def Ix(t_skin, chord, t_blade, w_cap, t_cap):
    return Ix_skin(t_skin, chord, t_blade, w_cap, t_cap)+Ix_cap(t_skin, chord, t_blade, w_cap, t_cap)

# Iy
def Iy_skin(t_skin, chord, t_blade, w_cap, t_cap):
    return np.pi/8*t_skin*(3*t_blade*chord**2+chord**3)

def Iy_cap(t_skin, chord, t_blade, w_cap, t_cap):
    return w_cap**3*(2*t_cap)/12

def Iy(t_skin, chord, t_blade, w_cap, t_cap):
    return Iy_skin(t_skin, chord, t_blade, w_cap, t_cap)+Iy_cap(t_skin, chord, t_blade, w_cap, t_cap)

# Ip
def Ip_skin(t_skin, chord, t_blade, w_cap, t_cap):
    return Ix_skin(t_skin, chord, t_blade, w_cap, t_cap)

def Ip_cap(t_skin, chord, t_blade, w_cap, t_cap):
    return Ix_cap(t_skin, chord, t_blade, w_cap, t_cap)

def Ip(t_skin, chord, t_blade, w_cap, t_cap):
    return Ip_skin(t_skin, chord, t_blade, w_cap, t_cap)+Ip_cap(t_skin, chord, t_blade, w_cap, t_cap)

# A
def A_skin(t_skin, chord, t_blade, w_cap, t_cap):
    return np.pi/2*t_skin*(t_blade+chord)

def A_cap(t_skin, chord, t_blade, w_cap, t_cap):
    return 2*t_cap*w_cap

# EIx (flap-wise bending stiffness)
Ex_skin = 7.33860101e+09 
Ex_cap = 2.41546358e+10
def EIx(t_skin, chord, t_blade, w_cap, t_cap):
    return (
        Ex_skin*Ix_skin(t_skin, chord, t_blade, w_cap, t_cap)
        +
        Ex_cap*Ix_cap(t_skin, chord, t_blade, w_cap, t_cap)
        )

# EIy (edge-wise bending stiffness)
Ey_skin = 6.99464773e+09
Ey_cap = 8.01480713e+11
def EIy(t_skin, chord, t_blade, w_cap, t_cap):
    return (
        Ey_skin*Iy_skin(t_skin, chord, t_blade, w_cap, t_cap)
        +
        Ey_cap*Iy_cap(t_skin, chord, t_blade, w_cap, t_cap)
        )

# GK (torsional stiffness)
G_skin = 3.50011480e+09
G_cap = 2.14903435e+09
def GK(t_skin, chord, t_blade, w_cap, t_cap):
    return (
        G_skin*Ip_skin(t_skin, chord, t_blade, w_cap, t_cap)
        +
        G_cap*Ip_cap(t_skin, chord, t_blade, w_cap, t_cap)
        )

# md (mass-density) [kg/m]
rho_skin = 1951.98646883
rho_cap = 2890.63651637
def md(t_skin, chord, t_blade, w_cap, t_cap):
    return (
        rho_skin*A_skin(t_skin, chord, t_blade, w_cap, t_cap)
        +
        rho_cap*A_cap(t_skin, chord, t_blade, w_cap, t_cap)
        )