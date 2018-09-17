import imageio
# https://imageio.github.io/

import numpy as np

with imageio.get_writer('./anim1.gif', mode='I') as writer:
    for i in range(5):
        #image = imageio.imread(filename)
        image = np.zeros((100,100,3), dtype=np.uint8)
        image[10:20,10:20,1] = 120
        writer.append_data(image)

