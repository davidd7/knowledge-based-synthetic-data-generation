from owlready2 import *
import blenderproc as bproc
import bpy  # this package is related to blender functionalities and is only available from within the blender python environment
import numpy as np
import random
import os
from PIL import Image
import colorsys
from scipy.spatial.transform import Rotation as R
import pathlib
import util
import time
import math
from custom_code.generation_components import handlers as h


# INTERFACES


















# UTILITY FUNCTIONS

class Utility():
    def create_folder_if_not_exists(path):
        if os.path.isdir(path):
            print(f'folder {path}/ exists')
        else:
            os.mkdir(path)
            print(f'created folder {path}/')

    def print_syspath():
        import sys
        print("### In current sys.path ###")
        for el in sys.path:
            print(el)
        print("### ### ### ### ### ### ###")










class BlenderCameraWrapper():
    """
    Makes camera methods available in a way similar to how objects are manipulated. The camera is normally manipulated differently in blender, but it's advantageous to be able to change location/rotation of camera and objects in a similar way.
    """
    def set_location(self, location):
        # Set first camera pose (= first key frame)
        cam_pose = bproc.math.build_transformation_mat(location, [0, 0, 0])
        bproc.camera.add_camera_pose(cam_pose, frame=0) # Without frame=0 every method call adds a new frame (which would make an additional photo in each iteration of the same scene from another position)

    def set_local2world_mat(self, matrix):
        bproc.camera.add_camera_pose(matrix, frame=0)

    def get_location(self):
        matrix = bproc.camera.get_camera_pose(frame=0)
        translation = matrix[0:3, 3]
        return translation

    @property
    def blender_obj(self):
        return bpy.context.scene.camera # bproc.camera#. #.blender_obj





def create_rectangular_cuboid(x=None, y=None, z=None,
                              x_length=None, y_length=None, z_length=None):
    """
    x, y, z, x_length, y_length, z_length should all be given in Millimeters (mm)
    """
    # Create cube
    blender_object = bproc.object.create_primitive(shape="CUBE")

    # Set dimensions of cube (Default cube in blender has a size of 2m x 2m x 2m. A scale factor of 10 in one direction thus means a 20m length in this direction)
    blender_object.set_scale([
        x_length/2/1000,
        y_length/2/1000,
        z_length/2/1000])

    # Set position of cube (location is in relation to the objects center. This might be cool for models, but for a rectangle it would be easier measure sizes in reality not from their center, which is why this is adapted)
    blender_object.set_location([
        x/1000 + x_length/2/1000, 
        y/1000 + y_length/2/1000,
        z/1000 + z_length/2/1000])

    return blender_object


def create_blender_volume(x=None, y=None, z=None,
                x_length=None, y_length=None, z_length=None):
    # Create volume (i.e. create a cuboid)
    blender_object = create_rectangular_cuboid(x, y, z, x_length, y_length, z_length)
    blender_object.hide(True) # volumes should not be visible in rendering
    return blender_object


def intersection(lst1, lst2): # hybrid method from https://www.geeksforgeeks.org/python-intersection-two-lists/
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def create_objects(obj_file_path, how_many=1):
    res = []

    for _ in range(how_many):
        mesh_list = bproc.loader.load_obj( str(util.get_path_to_package() / "uploads/" / obj_file_path) ) # returns a list with the loaded object as its only element
        res += mesh_list # merge the two lists

    return res









def addRotationHandler(manager, onto, individual):
    rotation_info = individual.Has_RotationInfo[0]
    if onto.classes.LookDownRotation in rotation_info.is_a:
        manager.add(h.LookDownRotationHandler(individual, rotation_info))
    elif onto.classes.LookAtVolumeRotation in rotation_info.is_a:
        manager.add(h.SimpleRotationLookingAtVolumeHandler(individual, rotation_info))
    elif onto.classes.RandomRotation in rotation_info.is_a:
        manager.add(h.SimpleRotationHandler(individual, rotation_info))

















