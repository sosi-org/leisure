#!/usr/bin/env python3
import imageio
# https://imageio.github.io/

import numpy as np
import math

"""
with imageio.get_writer('./anim1.gif', mode='I') as writer:
    for i in range(5):
        #image = imageio.imread(filename)
        image = np.zeros((100,100,3), dtype=np.uint8)
        image[10:20,10:20,1] = 120
        writer.append_data(image)
"""

"""
nframes = 15
with imageio.get_writer('./anim1.gif', mode='I') as writer:
    image = np.zeros((nframes, 100,100,3), dtype=np.uint8)
    for i in range(nframes):
        image[i, 10:20+i,10:20+i,1] = 120
        writer.append_data(image[i])
"""

#nframes = 15
dt = 0.02/1.0
cycles = 1.0
LOOP_BACKnFORTH = False
#resolution
nx, ny = (100, 100)

nframes = int(cycles/dt + 0.00000001)
print(nframes, "frames")

x0 = np.linspace(0, 1, nx)
y0 = np.linspace(0, 1, ny)

xx,yy = np.meshgrid(x0, y0)
image = np.zeros((nframes, nx,ny,3), dtype=np.uint8)
for i in range(nframes):
    #image[i, 10:20+i,10:20+i,1] = 120
    #image[i, 10:20+i,10:20+i,1] = 120
    for rgbi in range(3):
        t_linear = i*dt
        tb = int(i*dt)
        tr = (i*dt) % 1.0
        t_loopy = 1.0 - math.fabs(1.0-t_linear*2.0)

        if LOOP_BACKnFORTH:
            t = t_loopy
        else:
            # periodic without liooping back and forth
            t = t_linear


        sp_frq = 3.0/2.0

        RADIANS = np.pi * 2
        phi = t * RADIANS * 1.0 #0.3

        phix, phiy = phi, phi

        phixy = np.arctan2(xx,yy)
        mxx, myy = xx + np.sin(phixy) , yy + np.cos(phixy)

        v = (np.sin(mxx*RADIANS*sp_frq + phix)+np.cos(myy*RADIANS*sp_frq + phiy))
        #v = (np.sin(xx*RADIANS*sp_frq + phix) **2 +np.cos(yy*RADIANS*sp_frq + phiy) **2)-1.0
        v = np.clip(v, 0,1)
        image[i, :,:, rgbi] = np.floor(v*255)

imageio.mimsave('./anim1.gif', image, duration=dt)


#imageio.mimsave(exportname, frames, format='GIF', duration=5)

# https://www.programcreek.com/python/example/104522/imageio.mimsave



"""
# https://stackoverflow.com/questions/20104318/drawing-anti-aliased-lines-on-tkinter-canvas-in-python

import tkinter as tk
#from Tkinter import *
master = tk.Tk()
w = tk.Canvas(master, width=800, height=600)
w.pack()
w.create_line(100, 100, 400, 300, width=5)
tk.mainloop()
"""
