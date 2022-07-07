

import blenderproc as bproc
import numpy as np
from PIL import Image

bproc.init()

# Create a simple object:
obj = bproc.object.create_primitive("MONKEY")


obj_rotation = [0, 0, 0] #bproc.math.build_transformation_mat([0, 0, 0], [(np.pi / 2) + 0, np.pi, 0])
obj.set_rotation_euler(obj_rotation, frame = 1) # Ist der 2. Frame, weil beginnt bei 0 zu zählen




obj_rotation = [0, (2*np.pi) * 0.5, 0] #bproc.math.build_transformation_mat([0, 0, 0], [(np.pi / 2) + 0, np.pi, 0])
obj.set_rotation_euler(obj_rotation, frame = 3)





# Create a point light next to it
light = bproc.types.Light()
light.set_location([2, -2, 0])
light.set_energy(1000) #300

# Set first camera pose (= first key frame)
cam_pose = bproc.math.build_transformation_mat([0, -5, 0], [np.pi / 2, 0, 0])
bproc.camera.add_camera_pose(cam_pose)


# Set second camera pose (= first key frame)
cam_pose = bproc.math.build_transformation_mat([0, -7, 0], [(np.pi / 2) + 0, 0, 0])
bproc.camera.add_camera_pose(cam_pose)


# Set third camera pose (= first key frame)
cam_pose = bproc.math.build_transformation_mat([0, -9, 0], [(np.pi / 2) + 0, 0, 0]) # +0.2
bproc.camera.add_camera_pose(cam_pose)


# Set seventh camera pose (= first key frame)
cam_pose = bproc.math.build_transformation_mat([0, -20, 0], [(np.pi / 2) + 0, 0, 0]) # +0.2
bproc.camera.add_camera_pose(cam_pose, 7)






# Render the scene
data = bproc.renderer.render()

data_image = data["colors"]
data_image = np.array(data_image)

img = None

for num, single_image in enumerate(data_image): # Für jeden keyframe wurde ien Bild gerendert; diese Bilder werden hier durchgelaufen
    img = Image.fromarray(single_image.astype('uint8'), 'RGB')
    img.save(f"{num}.png", "PNG")
    #img.show()

img.show()

#print(len(data_image))
#print( type(data_image[0]) )

# Write the rendering into an hdf5 file
#bproc.writer.write_hdf5("output/", data)
#bproc.writer.write_hdf5("E:/David (HDD)/blenderproc/output/", data)
#bproc.writer.write_hdf5("E:/David (HDD)/blenderproc/output/", data)




