# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 14:13:34 2024

@author: khoac
"""

# -*- coding: utf-8 -*-


   
import operator as op
import numpy as np
import matplotlib.pyplot as plt
import math
from collections import Counter
from mpl_toolkits import mplot3d
from scipy.optimize import fsolve

fig = plt.figure()
ax = plt.axes(projection='3d')
def mostFrequent(arr, n): 
  
    # Sort the array 
    arr.sort() 
  
    # find the max frequency using 
    # linear traversal 
    max_count = 1
    res = arr[0] 
    curr_count = 1
  
    for i in range(1, n): 
        if (arr[i] == arr[i - 1]): 
            curr_count += 1
        else: 
            curr_count = 1
  
         # If last element is most frequent 
        if (curr_count > max_count): 
            max_count = curr_count 
            res = arr[i - 1] 
  
    return res 
  
def IntersecOfSets(arr1, arr2, arr3):
    # Converting the arrays into sets
    s1 = set(arr1)
    s2 = set(arr2)
    s3 = set(arr3)
    
    # Calculates intersection of 
    # sets on s1 and s2
    set1 = s1.intersection(s2)         #[80, 20, 100]
     
    # Calculates intersection of sets
    # on set1 and s3
    result_set = set1.intersection(s3)
     
    # Converts resulting set to list
    final_list = list(result_set)
    return final_list
def calc_angles(a,b,c):
    alpha = np.arccos(  (b**2 + c**2 - a**2) /(2.*b*c) )
    beta = np.arccos(  (-b**2 + c**2 + a**2) /(2.*a*c) )
    gamma = np.pi-alpha-beta
    
    return alpha, beta, gamma


def Circle(x, y, r, n):
    points = []
    theta = (np.pi * 2) / n
    
    
    for i in range(n):
        curr_angle = (theta * i) + np.pi/2
        pointX = (r * np.cos(curr_angle)) + x
        pointY = (r * np.sin(curr_angle)) + y
        points.append((pointX, pointY))
    return points



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


def round_tuples(tup, decimal):
    for i in range (0, len(tup)):
        tup[i]=list(tup[i])
        tup[i][0]=round(tup[i][0],decimal)
        tup[i][1]=round(tup[i][1],decimal)
        tup[i][2]=round(tup[i][2],decimal)
        tup[i]=tuple(tup[i])
    return tup
#cm
circle_points = Circle(0, 0, 27.4/2, 5)
y_coordinates, z_coordinates = zip(*circle_points)

Gx=20
Gy=20
Gz=20
Oxy=[]
Ox=[]
Oy=[]
Oz=[]

x_coordinates=[0,0,0,0,0]


mic_1=[[],[]]
mic_2=[[],[]]
mic_3=[[],[]]
mic_4=[[],[]]
mic_5=[[],[]]
l=[]
for i in range (0, len(y_coordinates)):
    Ox.extend(x_coordinates)
    Oy.extend(y_coordinates)
    Oz.extend(z_coordinates)
    l.append(math.dist([x_coordinates[i], y_coordinates[i], z_coordinates[i]], [Gx,Gy,Gz]))
    print("G to point",i+1,": ",l[i])
time=[]
for i in range (0,5):
    time.append(l[i]/330)
a=(min(time))

for i in range (0,5):
    time[i]=time[i]-a


mic_1[1]=time[0]*330
mic_2[1]=time[1]*330
mic_3[1]=time[2]*330
mic_4[1]=time[3]*330
mic_5[1]=time[4]*330

mic_1[0].append((Ox[0],Oy[0],Oz[0]))
mic_2[0].append((Ox[1],Oy[1],Oz[1]))
mic_3[0].append((Ox[2],Oy[2],Oz[2]))
mic_4[0].append((Ox[3],Oy[3],Oz[3]))
mic_5[0].append((Ox[4],Oy[4],Oz[4]))


x1, y1, z1, r1 = mic_2[0][0][0],mic_2[0][0][1],mic_2[0][0][2],mic_2[1]
x2, y2, z2, r2 = mic_3[0][0][0],mic_3[0][0][1],mic_3[0][0][2],mic_3[1]
x3, y3, z3, r3 = mic_4[0][0][0],mic_4[0][0][1],mic_4[0][0][2],mic_4[1]
x4, y4, z4, r4 = mic_5[0][0][0],mic_5[0][0][1],mic_5[0][0][2],mic_5[1]
x5, y5, z5, r5 = mic_1[0][0][0],mic_1[0][0][1],mic_1[0][0][2],mic_1[1]
xyz_1=[]
xyz_2=[]
xyz_3=[]
xyz_4=[]
xyz_5=[]
xyz_6=[]
xyz_7=[]
xyz_8=[]
xyz_9=[]
xyz_10=[]
for i in range (0,100):  

    xyz_1.append(three_sphere_intersection(x1, y1, z1, r1+i, x2, y2, z2, r2+i, x3, y3, z3, r3+i))
    xyz_2.append(three_sphere_intersection(x2, y2, z2, r2+i, x1, y1, z1, r1+i, x4, y4, z4, r4+i))
    xyz_3.append(three_sphere_intersection(x1, y1, z1, r1+i, x2, y2, z2, r2+i, x5, y5, z5, r5+i))
    xyz_4.append(three_sphere_intersection(x1, y1, z1, r1+i, x3, y3, z3, r3+i, x4, y4, z4, r4+i))
    xyz_5.append(three_sphere_intersection(x1, y1, z1, r1+i, x3, y3, z3, r3+i, x5, y5, z5, r5+i))
    xyz_6.append(three_sphere_intersection(x4, y4, z4, r4+i, x1, y1, z1, r1+i, x5, y5, z5, r5+i))
    xyz_7.append(three_sphere_intersection(x3, y3, z3, r3+i, x2, y2, z2, r2+i, x4, y4, z4, r4+i))
    xyz_8.append(three_sphere_intersection(x2, y2, z2, r2+i, x5, y5, z5, r5+i, x3, y3, z3, r3+i))
    xyz_9.append(three_sphere_intersection(x5, y5, z5, r5+i, x4, y4, z4, r4+i, x3, y3, z3, r3+i))
    xyz_10.append(three_sphere_intersection(x2, y2, z2, r2+i, x4, y4, z4, r4+i, x5, y5, z5, r5+i))





xyz_1=round_tuples(xyz_1,0)
xyz_2=round_tuples(xyz_2,0)
xyz_3=round_tuples(xyz_3,0)
xyz_4=round_tuples(xyz_4,0)
xyz_5=round_tuples(xyz_5,0)
xyz_6=round_tuples(xyz_6,0)
xyz_7=round_tuples(xyz_7,0)
xyz_8=round_tuples(xyz_8,0)
xyz_9=round_tuples(xyz_9,0)
xyz_10=round_tuples(xyz_10,0)


#fin = set1.intersection(set2, set3, set4, set5)


xyz=[]
xyz=xyz_1+xyz_2+xyz_3+xyz_4+xyz_5+xyz_6+xyz_7+xyz_8+xyz_9+xyz_10

fin=mostFrequent(xyz, len(xyz))


totx=0
toty=0
totz=0
for i in range (0,len(fin)):
    if abs(fin[0])!=0:
        x,y,z=abs(fin[0]),fin[1],fin[2]
       
        

print("x,y,z: ",x,y,z)
#φ=arctan(y/x)
#θ=arccos(z/r)


for i in range (0,5):
    if i <5:
        
            ax.plot3D([Ox[i], Ox[i+1],x,Ox[i]], [Oy[i], Oy[i+1],y,Oy[i]],[Oz[i], Oz[i+1],z,Oz[i]], marker='o')
            ax.text(Ox[i]+0.5,Oy[i]+0.5,Oz[i]+0.5,i+1, fontsize=12)
    else:
            ax.plot3D([Ox[i], Ox[0],x,Ox[i]],[Oy[i], Oy[0],y,Oy[i]], [Oz[i], Oz[0],z,Oz[i]], marker='o')

   
r=math.dist([0,0,0],[x,y,z])

horrizontal_angle=np.arctan(y/x)*180/np.pi
vertical_angle=np.arccos(z/r)*180/np.pi

print("horrizontal_angle: ",horrizontal_angle)
print("vertical_angle: ", vertical_angle)


# Set xyz-axis limits
ax.set_xlim(-20, 50)  
ax.set_ylim(-20, 50)
ax.set_zlim(-20, 50)


ax.plot3D(mic_1[0][0][0],mic_1[0][0][1],mic_1[0][0][2],"o")
ax.plot3D(mic_2[0][0][0],mic_2[0][0][1],mic_2[0][0][2],"o")
ax.plot3D(mic_3[0][0][0],mic_3[0][0][1],mic_3[0][0][2],"o")
ax.plot3D(mic_4[0][0][0],mic_4[0][0][1],mic_4[0][0][2],"o")
ax.plot3D(mic_5[0][0][0],mic_5[0][0][1],mic_5[0][0][2],"o")

ax.plot3D(Gx,Gy,Gz,"o")
plt.grid
plt.show()

