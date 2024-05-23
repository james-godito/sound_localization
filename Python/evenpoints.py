import matplotlib.pyplot as plt
import math

def circle(x, y, r, n): # makes evenly space points on a circle
    import numpy as np
    points = []
    theta = (np.pi * 2) / n
    
    for i in range(n):
        curr_angle = (theta * i) + np.pi/2
        pointX = (r * np.cos(curr_angle)) + x
        pointY = (r * np.sin(curr_angle)) + y
        points.append((pointX, pointY))
    return points

def slope(x1, x2, y1, y2):
    return (y2 - y1)/(x2 - x1)

if __name__ == "__main__":
    #cm
    circle_points = circle(0, 0, 27.44/2, 5)
    x_coordinates, y_coordinates = zip(*circle_points)
    print(circle_points)
    # for i in range(len(x_coordinates)):
    #     print(math.dist([x_coordinates[i+1], y_coordinates[i+1]], [x_coordinates[i], y_coordinates[i]]))
    print(math.dist([x_coordinates[2], y_coordinates[2]], [x_coordinates[4], y_coordinates[4]]))
    m = slope(x_coordinates[2], x_coordinates[4], y_coordinates[2], y_coordinates[4])
    a = y_coordinates[2] - m*x_coordinates[2]
    
    print(abs(m*0 + a))
    
    print("\n")
    print(x_coordinates)
    print("\n")
    print(y_coordinates)
    
    plt.plot(x_coordinates, y_coordinates, "o")
    plt.gca().set_aspect('equal', adjustable='box')  # Set aspect ratio to be equal
    plt.show()
