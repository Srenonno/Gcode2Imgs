
import io
import os
import string
import math
import sys
from mayavi import mlab
from tvtk.api import tvtk
import numpy as np

shift = [0, 0]
print(shift[1])
e1 = []
e2 = []
e3 = []
x = [0]
y = [0]
z = [0]

CurrentZValue = 0
k = 0
#e = open('3dbenchy_0.2mm_PLA_MK3S_1h34m.gcode', 'r')
e = open('geared_heart_stand_-_heart25deg_stand15deg_0.3mm_ABS_MK3S_1h28m.gcode', 'r')
while True:
    flin = e.readline()

    if flin == '':
        break
    elif flin[0:2] == 'G1':
        array1 = flin.split()
        if 'Z' in flin[2:]:
            CurrentZValue = float(array1[1][1:])

        elif 'X' in flin[2:] and 'Y' in flin[2:] and 'E' in flin[2:]:

            e1.append(float(array1[1][1:])+shift[0])
            e2.append(float(array1[2][1:]))
            e3.append(CurrentZValue)

mlab.figure(bgcolor=(1, 1, 1),
            fgcolor=None, engine=None, size=(1080, 1080))
x1, y1, z1 = (0, 230+shift[1], -1.5)  # | => pt1
x2, y2, z2 = (250, 230+shift[1], -1.5)  # | => pt2
x3, y3, z3 = (0, -20+shift[1], -1.5)  # | => pt3
x4, y4, z4 = (250, -20+shift[1], -1.5)  # | => pt4
bed = mlab.mesh([[x1, x2], [x3, x4]], [[y1, y2], [y3, y4]], [
    [z1, z2], [z3, z4]], color=(0.7529, 0.7529, 0.7529))

img = tvtk.JPEGReader(file_name="bed_texture.jpg")
texture = tvtk.Texture(input_connection=img.output_port,
                       interpolate=1, repeat=0)
bed.actor.actor.texture = texture
bed.actor.tcoord_generator_mode = 'plane'

mlab.plot3d(e1[:-50000], e2[:-50000], e3[:-50000], color=(0.5, 0.5, 0.5),
            line_width=2.0, representation='wireframe')


#mlab.view(focalpoint=(250/2, 250/2, 40))
mlab.savefig(filename='test1000.png')

# mlab.show()
