'''
==============
3D scatterplot
==============

Demonstration of a basic scatterplot in 3D.
'''

import random as rand
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def randrange(n, vmin, vmax):
    '''
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    '''
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

n = 100

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
# for c, m, zlow, zhigh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
#     xs = randrange(n, 23, 32)
#     ys = randrange(n, 0, 100)
#     zs = randrange(n, zlow, zhigh)
#     ax.scatter(xs, ys, zs, c=c, marker=m)

# ax.scatter(10, 10, 10)

'''
Coordinates of the form (XXX/YYY/ZZZ)
X - Determines your position East/West in the map. A positive value increases your position to the East. A negative value increases your position to the West.
Y - Determines your position up/down in the map. A positive value increases your position upward. A negative value increases your position downward.
Z - Determines your position South/North in the map. A positive value increases your position to the South. A negative value increases your position to the North.
'''

places = {
    "Bed": (146, 58, 0, '<'),  # marker points true North
    "Chicken": (107, 65, -11, '$C$'),
    "Train Departure": (106, 96, -19, 'd'),
    "Train Arrival": (113, 96, -20, 'H'),
    "Nether Portal": (128, 89, 11, 's'),
    "Resource Hut": (-138, 64, 146, '$R$'),
    "Natural Cave": (-184, 89, 393, '.'),
    "Centre of Town 1": (556, 71, 28, '$1$'),
    "Birch Forest": (750, 64, -30, '.'),
    "Rest Stop": (920, 64, -93, '.'),
    "Centre of Town 2": (1065, 64, -304, '$2$'),
    "Amphitheatre": (960, 79, -310, '$A$'),
    "Centre of Town 3": (640, 66, -280, '$3$'),
    "Glacier": (720, 62, -560, '$G$'),
    "Coral Reef": (400, 62, -455, '.'),
    "Tower": (100, 96, 160, '$T$')
}

for n, coords in places.items():
    x = coords[2]  # replace x with North/South
    y = coords[0]  # replace y with East/West
    z = coords[1]  # Up/Down
    m = coords[3]
    c_r = rand.random()
    c_g = rand.random()
    c_b = rand.random()
    c = [[c_r, c_b, c_g]]
    if z < 64:
        c = [[0, 0, 0]]
    ax.scatter(x, y, z, marker=m, c=c)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()
