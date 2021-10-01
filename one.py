
import io
import os
import string
import math
import sys
from mayavi import mlab
from tvtk.api import tvtk
import numpy as np


def Gcode2Image(filePath):
    e1 = []
    e2 = []
    e3 = []

    CurrentZValue = 0
    k = 0
    e = open('extruder.gcode', 'r')
    while True:
        flin = e.readline()

        if flin == '':
            break
        elif flin[0:2] == 'G1':
            array1 = flin.split()
            if 'Z' in flin[2:]:
                CurrentZValue = float(array1[1][1:])

            elif 'X' in flin[2:] and 'Y' in flin[2:] and 'E' in flin[2:]:

                e1.append(float(array1[1][1:])+30)
                e2.append(float(array1[2][1:])+15)
                e3.append(CurrentZValue)
    i = 0
    x = []
    y = []
    z = []
    CurrentZValue = 0
    f = open(filePath+'.gcode', 'r')
    bedsize = 250
    x1, y1, z1 = (0, 230, -1.5)  # | => pt1
    x2, y2, z2 = (250, 230, -1.5)  # | => pt2
    x3, y3, z3 = (0, -20, -1.5)  # | => pt3
    x4, y4, z4 = (250, -20, -1.5)  # | => pt4

    mlab.figure(figure=None, bgcolor=(1, 1, 1),
                fgcolor=None, engine=None, size=(1080, 1080))
    bed = mlab.mesh([[x1, x2], [x3, x4]], [[y1, y2], [y3, y4]], [
                    [z1, z2], [z3, z4]], color=(0.7529, 0.7529, 0.7529))

    img = tvtk.JPEGReader(file_name="bed_texture.jpg")
    texture = tvtk.Texture(
        input_connection=img.output_port, interpolate=1, repeat=0)
    bed.actor.actor.texture = texture
    bed.actor.tcoord_generator_mode = 'plane'
    g = 1000
    while True:
        g = g + 1
        flin = f.readline()

        if flin == '':
            break
        elif flin[0:2] == 'G1':
            array1 = flin.split()
            if 'Z' in flin[2:]:
                CurrentZValue = float(array1[1][1:])

            elif 'X' in flin[2:] and 'Y' in flin[2:] and 'E' in flin[2:]:

                x.append(float(array1[1][1:]))
                y.append(float(array1[2][1:]))
                z.append(CurrentZValue)
        elif ';LAYER_CHANGE' in flin and x and g % 1000 == 0:
            mlab.clf()
            mlab.figure(figure=1, bgcolor=(1, 1, 1),
                        fgcolor=None, engine=None, size=(1080, 1080))
            x1, y1, z1 = (0, 230+(105-y[-1]), -1.5)  # | => pt1
            x2, y2, z2 = (250, 230+(105-y[-1]), -1.5)  # | => pt2
            x3, y3, z3 = (0, -20+(105-y[-1]), -1.5)  # | => pt3
            x4, y4, z4 = (250, -20+(105-y[-1]), -1.5)  # | => pt4
            bed = mlab.mesh([[x1, x2], [x3, x4]], [[y1, y2], [y3, y4]], [
                [z1, z2], [z3, z4]], color=(0.7529, 0.7529, 0.7529))

            img = tvtk.JPEGReader(file_name="bed_texture.jpg")
            texture = tvtk.Texture(input_connection=img.output_port,
                                   interpolate=1, repeat=0)
            bed.actor.actor.texture = texture
            bed.actor.tcoord_generator_mode = 'plane'
            Te1 = [t+(125-x[-1]) for t in e1]
            Ty = [t+(105-y[-1]) for t in y]
            Te3 = [t+z[-1] for t in e3]
            v = mlab.plot3d(x, Ty, z, color=(0, 0, 0.6),
                            line_width=2.0, representation='wireframe')
            mlab.points3d(Te1, e2, Te3, color=(0.5, 0.5, 0.5))
            mlab.view(268, 78, 543)
            print(i)
            mlab.savefig(filename='data1/Front/frame' +
                         str(i)+'.png', size=(1312, 1056))
            mlab.view(80, 85, 200)
            mlab.view(roll=3)
            mlab.savefig(filename='data1/Back/frame' +
                         str(i+1)+'.png', size=(1312, 1056))
            mlab.view(270, 20, 500)
            mlab.pitch(-10)
            mlab.savefig(filename='data1/TOP/frame' +
                         str(i+2)+'.png', size=(1312, 1056))
            mlab.view(350, 82, 380)
            mlab.yaw(10)
            mlab.pitch(5)
            mlab.savefig(filename='data1/Right/frame' +
                         str(i+3)+'.png', size=(1312, 1056))
            mlab.view(190, 85, 390)
            mlab.yaw(-8)
            mlab.pitch(9)
            mlab.savefig(filename='data1/Left/frame' +
                         str(i+4)+'.png', size=(1312, 1056))
            i += 5

    # Camera angles
    # Front    mlab.view(268, 78, 543)
    # Back mlab.view(80, 85, 200)
    # Right mlab.view(350, 82, 380) mlab.yaw(10) mlab.pitch(5)

    # top mlab.view(270, 20, 500)mlab.pitch(-10)

    # left mlab.view(190, 85, 390) mlab.yaw(-8) mlab.pitch(9)


Gcode2Image('Forme-Case_0.2mm_ABS_MK3S_2h15m')
