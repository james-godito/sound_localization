# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 23:41:42 2024

@author: khoac
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 11:37:15 2024

@author: khoac
"""


import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import math
from scipy.optimize import fsolve

fig = plt.figure()
ax = plt.axes(projection='3d')

def calc_angles(a,b,c):
    alpha = np.arccos(  (b**2 + c**2 - a**2) /(2.*b*c) )
    beta = np.arccos(  (-b**2 + c**2 + a**2) /(2.*a*c) )
    gamma = np.pi-alpha-beta
    
    return alpha, beta, gamma


def Circle(x, y, r, n):
    import numpy as np
    points = []
    theta = (np.pi * 2) / n
    
    
    for i in range(n):
        curr_angle = (theta * i) + np.pi/2
        pointX = (r * np.cos(curr_angle)) + x
        pointY = (r * np.sin(curr_angle)) + y
        points.append((pointX, pointY))
    return points

def Slope(x1, x2, y1, y2):
    return (y2-y1)/(x2-x1)

def sphere_equation(x, y, z, center, radius):
    return (x - center[0])**2 + (y - center[1])**2 + (z - center[2])**2 - radius**2

def three_sphere_intersection(x1, y1, z1, r1, x2, y2, z2, r2, x3, y3, z3, r3):
    def equations(coords):
        x, y, z = coords
        return (round(sphere_equation(x, y, z, (x1, y1, z1), r1)),
                round(sphere_equation(x, y, z, (x2, y2, z2), r2)),
                round(sphere_equation(x, y, z, (x3, y3, z3), r3)))

    # Initial guess for the intersection point
    initial_guess = np.array([0.0, 0.0, 0.0])

    # Use fsolve to find the root (intersection point)
    result = fsolve(equations, initial_guess)

    return tuple(result)

#cm
circle_points = Circle(0, 0, 41.16/2, 5)
y_coordinates, z_coordinates = zip(*circle_points)

Gx=42.212
Gy=17.54
Gz=8.65
Oxy=[]
Ox=[]
Oy=[]
Oz=[]
l=[]
x_coordinates=[0,0,0,0,0]
xyz_co=[]

for i in range (0, len(y_coordinates)):
    Ox.extend(x_coordinates)
    Oy.extend(y_coordinates)
    Oz.extend(z_coordinates)
    l.append(math.dist([x_coordinates[i], y_coordinates[i], z_coordinates[i]], [Gx,Gy,Gz]))
    print("G to point",i,": ",l[i])



x1, y1, z1, r1 = Ox[1],Oy[1],Oz[1],l[1]
x2, y2, z2, r2 = Ox[2],Oy[2],Oz[2],l[2]
x3, y3, z3, r3 = Ox[3],Oy[3],Oz[3],l[3]
x4, y4, z4, r4 = Ox[4],Oy[4],Oz[4],l[4]
x5, y5, z5, r5 = Ox[0],Oy[0],Oz[0],l[0]
xyz_1= three_sphere_intersection(x1, y1, z1, r1, x2, y2, z2, r2, x3, y3, z3, r3)
xyz_2= three_sphere_intersection(x3, y3, z3, r3, x4, y4, z4, r4, x5, y5, z5, r5)
xyz_3= three_sphere_intersection(x1, y1, z1, r1, x4, y4, z4, r4, x5, y5, z5, r5)
xyz_4= three_sphere_intersection(x4, y4, z4, r4, x2, y2, z2, r2, x3, y3, z3, r3)

xyz_1 = [round(elem,3) for elem in xyz_1]
xyz_2 = [round(elem,3) for elem in xyz_2]
xyz_3 = [round(elem,3) for elem in xyz_3]
xyz_4 = [round(elem,3) for elem in xyz_4]



xyz=xyz_1 + xyz_2 + xyz_3 + xyz_4

xyz = list(Counter(xyz))





x=xyz[0]
y=xyz[1]
z=xyz[2]



print("x,y,z: ",x,y,z)
#φ=arctan(y/x)
#θ=arccos(z/r)

# Plot the triangles


for i in range (0, len(x_coordinates)):
    Ox.extend(x_coordinates)
    Oy.extend(y_coordinates)
    Oz.extend(z_coordinates)
for i in range (0,5):
    if i <5:
        
            ax.plot3D([Ox[i], Ox[i+1],x,Ox[i]], [Oy[i], Oy[i+1],y,Oy[i]],[Oz[i], Oz[i+1],z,Oz[i]], marker='o')
    else:
            ax.plot3D([Ox[i], Ox[0],x,Ox[i]],[Oy[i], Oy[0],y,Oy[i]], [Oz[i], Oz[0],z,Oz[i]], marker='o')

   
r=math.dist([0,0,0],[x,y,z])

horrizontal_angle=np.arctan(y/x)*180/np.pi
vertical_angle=np.arccos(z/r)*180/np.pi

print("horrizontal_angle: ",horrizontal_angle)
print("vertical_angle: ", vertical_angle)



ax.set_xlim(-10, 50)  # Set x-axis limits
ax.set_ylim(-10, 50)
ax.set_zlim(-10, 20)
ax.plot3D(Gx,Gy,Gz,"x")
#plt.plot(x,y,"o")
ax.plot3D(0,0,0,"x")

plt.gca().set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal
plt.grid
plt.show()

