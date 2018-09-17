#!/usr/bin/env python3
import imageio
# https://imageio.github.io/

import numpy as np

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

nframes = 15
image = np.zeros((nframes, 100,100,3), dtype=np.uint8)
for i in range(nframes):
    image[i, 10:20+i,10:20+i,1] = 120

imageio.mimsave('./anim1.gif', image)
