#!/usr/bin/env python3
import imageio
# https://imageio.github.io/

"""

pip3 install scikit-image

pip3 install Pillow
pip3 install images2gif
pip3 install imageio
pip3 install visvis
pip3 install scikit-image

"""

#import scipy.ndimage
#from skimage.transform import resize
import skimage.transform

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


def clip2(mat, vmin, vmax):
    v =  np.clip(mat, vmin, vmax)
    v = v - vmin
    v = v / (vmax - vmin)
    return v

def clip20(mat, vlist):

    """
    v1 =  (mat >= vmin) * mat + \
          (mat < vmin) * 0

    v2 =  (mat < vmax) * mat + \
          (mat >= vmax) * 0
    #v = v1 + v2
    """

    last_max = -1000

    master_mask = 0
    # [vmin, vmax]
    for vmin, vmax in vlist:

        assert vmin < vmax
        assert last_max < vmin


        msk = np.logical_and(mat >= vmin, mat < vmax)
        v =  msk * mat

        v = v - vmin
        v = v / (vmax - vmin)

        master_mask = master_mask + msk
        last_max = vmax

    #return v * msk
    return master_mask

def clip3(mat, vmin, vmid, vmax):
    assert vmin < vmid
    assert vmid < vmax
    v1 =  clip20(mat, [(vmin, vmid)])
    v2 =  1.0 - clip20(mat, [(vmid, vmax)])
    return v1 + v2


#nframes = 15
dt = 0.02/1.0*2
tcycles = 1.0
LOOP_BACKnFORTH = False
DECIMATION = 2
xcycles = 2

#resolution
rx, ry = (100*2, 100*2)
nx, ny = (rx*DECIMATION, ry*DECIMATION)

nframes = int(tcycles/dt + 0.00000001)
print(nframes, "frames")

x0 = np.linspace(0, xcycles, nx)
y0 = np.linspace(0, xcycles, ny)

xx,yy = np.meshgrid(x0, y0)
image = np.zeros((nframes, rx,ry,3), dtype=np.uint8)
#image_up = np.zeros((nframes, nx*DECIMATION,ny*DECIMATION,3), dtype=float)
print("downsampling from ", (nx,ny), "to", (rx,ry))
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

        phixy = np.arctan2(xx-0.5,yy-0.5)
        #mxx, myy = xx + np.sin(phixy) , yy + np.cos(phixy)
        mxx, myy = xx + np.sin((xx+t)*RADIANS) * 0.1 , yy #+ np.cos(phixy)
        #  + (3*yy*yy+1)

        v = (np.sin(mxx*RADIANS*sp_frq + phix)+np.cos(myy*RADIANS*sp_frq + phiy*0))
        #v = (np.sin(xx*RADIANS*sp_frq + phix) **2 +np.cos(yy*RADIANS*sp_frq + phiy) **2)-1.0
        #v = np.clip(v, 0,1)
        #v = clip2(v,0.5,0.7)
        #v = clip3(v,0.5,0.55,0.6)
        #v = clip20(v, [(0.5,0.8)])
        v = clip20(v, [(-2.5,-1.8), (-0.3,-0.1), (0.5,0.8)])
        #print(np.min(np.min(v)),  np.max(np.max(v)))
        #v = np.clip(np.abs(v*2), 0.5,0.7)


        #image_up[:,:, rbgi] = v

        #upsampled = scipy.ndimage.zoom(v, DECIMATION, order=3)
        #downsampled = skimage.transform.resize(v, (rx,ry), anti_aliasing=True)        #  mode='constant'
        downsampled = skimage.transform.downscale_local_mean(v, (DECIMATION, DECIMATION))
        #print(v.shape, downsampled.shape, "huh")
        print(i, end="", flush=True)

        image[i, :,:, rgbi] = np.floor(downsampled*255)

print()

imageio.mimsave('./anim1.gif', image, duration=dt)


#imageio.mimsave(exportname, frames, format='GIF', duration=5)

# https://www.programcreek.com/python/example/104522/imageio.mimsave

# http://scikit-image.org/docs/dev/auto_examples/transform/plot_rescale.html

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
