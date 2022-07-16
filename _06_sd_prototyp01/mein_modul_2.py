# In Vgl.,zu mein_modul_1 soll hier physical plausibility sein


# Declare functions, which will normally be in another file probably
import blenderproc as bproc
import numpy as np
import random
from PIL import Image
import os
import matplotlib.pyplot as plt
import bpy  # this package is related to blender functionalities and is only available from within the blender python environment


def initialize():
    global global_dict
    global_dict = {}

    bproc.init()


def global_dict_add(key=None, value=None):
    if key in global_dict:
        global_dict[key].append(value)
    else:
        global_dict[key] = [value]


def global_dict_get(key=None):
    return global_dict.get(key, [])


def create_rectangular_cuboid(x=None, y=None, z=None,
                              x_length=None, y_length=None, z_length=None):
    rect_cuboid = bproc.object.create_primitive(shape="CUBE")
    rect_cuboid.set_scale([x_length/2, y_length/2, z_length/2])
    rect_cuboid.set_location(
        [x + x_length/2,  y + y_length/2,  z + z_length/2])
    return rect_cuboid


def create_area(x=None, y=None, z=None,
                x_length=None, y_length=None, z_length=None,
                keys=[]):
    test = bproc.object.create_primitive(shape="CUBE")
    # Cube ist standardmäßig 2m x 2m x 2m groß. Scale von 10 in einer Richtung führt also zu 20m Länge in dieser Richtung
    test.set_scale([x_length/2/100, y_length/2/100, z_length/2/100])

    # location bezieht auf Mittelpunkt des Objektes. Das ist für Modelle ggf. oft cool, für Rechteck wär aber auch cool genau ausmessen zu können, weswegen anpassen werde
    test.set_location([x + x_length/2/100,  y + y_length/2/100,  z + z_length/2/100])

    test.hide(True)

    for el in keys:
        global_dict_add(key=el, value=test)


def create_floor(x=None, y=None, z=None,
                 x_length=None, y_length=None,
                 keys=[]):
    res = create_rectangular_cuboid(x, y, z, x_length, y_length, 0)

    for el in keys:
        global_dict_add(key=el, value=res)


def create_camera():
    # Set first camera pose (= first key frame)
    cam_pose = bproc.math.build_transformation_mat(
        [0, 0, 10], [0 * np.pi / 2, 0, 0])  # Für erste Tets setze Position einfach fest
    bproc.camera.add_camera_pose(cam_pose)


def create_objects(objects=[], how_many=1, keys=None):
    for obj in objects:
        for i in range(how_many):
            mesh = bproc.loader.load_obj(obj)
            for el in keys:
                global_dict_add(key=el, value=mesh[0])
            # mesh[0].set_location(0,0,0)
            # mesh.get_material().

            mat = mesh[0].get_materials()[0]
            mat.set_principled_shader_value(
                "Metallic", np.random.uniform(0.0, 0.0))
            mat.set_principled_shader_value("Base Color", (0.0, 1.0, 0.0, 1.0))
            print(mat)

    pass


global_tasks = []


def add_iteration_tasks(*list_of_tasks):
    global global_tasks  # dont use globals better?
    global_tasks += list_of_tasks


def get_task_RandomVisibleObjects(key=None, min=None, max=None):
    current_iteration = 0

    def local_function():
        number_visible = random.randint(min, max)
        print(f"from {min} to {max}, {number_visible} was chosen")
        for i, el in enumerate(global_dict_get(key)):
            print(f"iterating {i} of {len(global_dict_get(key))}")
            if i < number_visible:
                el.hide(False)
            else:
                el.hide(True)
    return local_function


def get_task_RandomPosition(key=None, area=None):
    def local_function():
        objects_to_sample_on = global_dict_get(area)
        for el in global_dict_get(key):
            print(objects_to_sample_on)
            location = bproc.sampler.upper_region(
                objects_to_sample_on=objects_to_sample_on)
            el.set_location(location)

    return local_function


def start_generation(number_of_images=2):

    # Sachen für init eigentlich:
    outf = "output"
    if os.path.isdir(outf):
        print(f'folder {outf}/ exists')
    else:
        os.mkdir(outf)
        print(f'created folder {outf}/')

    bproc.renderer.set_noise_threshold(0.1)  # 0.01 0.1

    for i in range(number_of_images):
        for task in global_tasks:
            task()

        data = bproc.renderer.render()

        data.update(bproc.renderer.render_segmap(
            map_by=["class", "instance", "name"]))  # segmentation

        data_image = data["colors"]  # + data["instance_segmaps"]
        data_image = np.array(data_image)

        #data_image = np.concatenate( (data_image, data_image) )

        print(data.keys())

        img = None

        # Für jeden keyframe wurde ien Bild gerendert; diese Bilder werden hier durchgelaufen
        for num, single_image in enumerate(data_image):
            img = Image.fromarray(single_image.astype('uint8'), 'RGB')
            img.save(f"{outf}/{i}_{num}.png", "PNG")

        data_image = data["instance_segmaps"]
        # Für jeden keyframe wurde ien Bild gerendert; diese Bilder werden hier durchgelaufen
        for num, single_image in enumerate(data_image):
            img = Image.fromarray(single_image.astype('uint8'), None)
            img.save(f"{outf}/{i}_{num}_segmentation.png", "PNG")

            plt.figure()
            plt.subplot(1, 2, 1)
            plt.imshow(data_image[0], 'gray', interpolation='none')
            plt.subplot(1, 2, 2)
            #plt.imshow(im, 'gray', interpolation='none')
            #plt.imshow(masked, 'jet', interpolation='none', alpha=0.7)
            plt.show()
            plt.savefig('foo.png')


def get_task_PhysicallyPlausibleSimulation(participating_objects_keys=[], participating_fixed_objects_keys=[]):
    # Collect participating objects
    obj_falling = []
    for key in participating_objects_keys:
        obj_falling += global_dict_get(key)

    obj_fixed = []
    for key in participating_fixed_objects_keys:
        obj_fixed += global_dict_get(key)

    print(f"Count = {len(obj_falling)}")

    # bpy.ops.rigidbody.world_remove()
    if bpy.context.scene.rigidbody_world == None:
        # this was suggested in https://github.com/DLR-RM/BlenderProc/issues/254 solve certain console errors that I alsow as getting
        bpy.ops.rigidbody.world_add()

    # Adjust some properties for the participating objects
    # (assumption is here that no other function uses these properties so that they'll stay the same
    # across iterations)
    for obj in obj_falling:
        # COMPOUND for complex
        obj.enable_rigidbody(active=True, collision_shape="CONVEX_HULL")
        #obj.build_convex_decomposition_collision_shape("<Path where to store vhacd>")

    for obj in obj_fixed:
        # COMPOUND for complex
        obj.enable_rigidbody(active=False, collision_shape="CONVEX_HULL")
        #obj.build_convex_decomposition_collision_shape("<Path where to store vhacd>")

    # Define function that is executed in each iteration
    def local_function():
        bproc.object.simulate_physics_and_fix_final_poses(
            min_simulation_time=4,
            max_simulation_time=20,
            check_object_interval=1
        )

        # for el in global_dict_get(key):
        #     print(objects_to_sample_on)
        #     location = bproc.sampler.upper_region(objects_to_sample_on=objects_to_sample_on)
        #     el.set_location(location)

    return local_function


def create_unique_key():
    i = 0
    while True:
        i += 1
        yield f"unique_key_{i}"


# 01 - Initialize parameters as one would get them as inputs to algorithm-side
params = {
    "objects": [
        {
            "model": "models/dragon.obj",
            "quantity": {
                "min": 1,  # 5,
                "max": 1,  # 5
            }
        },
        {
            "model": "models/nut2.obj",
            "quantity": {
                "min": 1,  # 5,
                "max": 1,  # 5
            }
        }
    ],
    "area": {
        "length_in_x": 3,
        "length_in_y": 3
    },
    "camera": {
        "height": 10
    }
}


print(params)


# 03 - Combining the parameters and functions to generate synthetic data


initialize()  # creates the shared dictionary and executes a necessary blender initialization method

create_area(
    x=-params["area"]["length_in_x"] / 2,
    y=-params["area"]["length_in_y"] / 2,
    z=4,  # 20, weil von dort aus die Objekte fallen gelassen werden
    x_length=params["area"]["length_in_x"],
    y_length=params["area"]["length_in_y"],
    z_length=0,
    keys=["area_objects"]
)

create_area(
    x=- params["area"]["length_in_x"] / 2,
    y=- params["area"]["length_in_y"] / 2,
    z=params["camera"]["height"],
    x_length=params["area"]["length_in_x"],
    y_length=params["area"]["length_in_y"],
    z_length=0,
    keys=["area_cameras"]
)

create_floor(-10, -10, 0, 20, 20, keys=["floor"])

create_camera()

for el in params["objects"]:
    uniq = create_unique_key()
    create_objects(
        objects=[el["model"]],
        how_many=el["quantity"]["max"],
        keys=["to_recognize", uniq])
    add_iteration_tasks(
        get_task_RandomVisibleObjects(
            key=uniq,
            min=el["quantity"]["min"],
            max=el["quantity"]["max"])
    )

add_iteration_tasks(
    get_task_RandomPosition(key="to_recognize", area="area_objects"),
    get_task_PhysicallyPlausibleSimulation(["to_recognize"], ["floor"])
)

start_generation()





























