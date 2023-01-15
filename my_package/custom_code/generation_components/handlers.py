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
from custom_code.generation_components.utilities import *
from interfaces import *


# HANDLER






class BlenderHandler(SDGenerationHandler):
    """General blenderproc-specific preperations"""
    def init(self, onto, generation_scheme_instance, manager):
        bproc.init()

    def iteration(self):
        pass

    def end(self, onto):
        pass






class RealImageRenderingHandler(SDGenerationHandler):
    """Renders (unlabelled) images of the respective current scenes and saves them in the specified folder. Labels for the same scene are generated by other handlers."""
    def __init__(self, path_where_to_save_result):
        # Set up target folder
        self.__outf = path_where_to_save_result
        Utility.create_folder_if_not_exists(path_where_to_save_result)

        # Set up counter for naming images
        self.__generation_index = 0

    def init(self, onto, generation_scheme_instance, manager):
        self.__generation_scheme_instance = generation_scheme_instance

    def iteration(self):
        data = bproc.renderer.render()
        data_image = data["colors"]
        data_image = np.array(data_image)

        # For every keyframe in the scene, one image was created in this iteration. All these created images are now iterated
        for keyframe, single_image in enumerate(data_image):
            img = Image.fromarray(single_image.astype('uint8'), 'RGB')
            img.save(f"{self.__outf}/{self.__generation_index}_{keyframe}.png", "PNG")

        self.__generation_index += 1

        self.__generation_scheme_instance.temp_data = data

    def end(self, onto):
        pass




class SimpleSegmentationLabelHandler(SDGenerationHandler):
    """
    Renders segmentation labels for the current scene in each iteration.

    Classes for when Has_SegmentType="SegmentClasses" are set automatically based on to which Object-individual a ObjectToRecognize belongs (remember: one Object individual are multiple blender objects (with the same model), when multiplicity is > 1). 
    """

    def __init__(self, path_where_to_save_result):
        # Set up target folder
        self.path_where_to_save_result = path_where_to_save_result
        Utility.create_folder_if_not_exists(path_where_to_save_result)

        # Set up counter for naming images and list of label types
        self.__generation_index = 0
        self.__label_type = []

    def init(self, onto, generation_scheme_instance, manager):
        # Remember generation scheme instance for later
        self.__generation_scheme_instance = generation_scheme_instance

        # Query ontology for segmentationLabel individuals. End method if there is no segmentationLabel individual (because there's nothing to do for this handler then)
        segmentation_label_individuals = intersection(self.__generation_scheme_instance.Has_Label, onto.individuals.search(is_a=onto.classes.SegmentationLabel))
        seg_individual = segmentation_label_individuals
        if len(seg_individual) == 0:
            return

        seg_individual = seg_individual[0] # Assumption: There is at most 1 segmentation individual (rendering multiple segmentation individuals at once is not supported at the moment)

        for i, object in enumerate(seg_individual.Has_ObjectToRecognize): # --> add all instances of the same ontology instance to the same segmentation label class (multiple instances of same object will have the same class tag)
            for blender_object in object.bp_reference: # nested for loop, but should only be O(k) where k is the number of objects loaded in blender
                # -> must be +1, because 0 ist background I think (although 0 is used in their own example...?)
                blender_object.set_cp("category_id", i + 1)

        self.__label_type = seg_individual.Has_SegmentationType


        # Query the ImageProperties-individual, which is needed to know the image size when no objects to recognize are visible in an image
        image_properties = intersection(
            seg_individual.Has_ImageProperties, onto.individuals.search(is_a=onto.classes.ImageProperties))
        if len(image_properties) == 0:
            self.__image_width = int(4032.0 * 0.1)
            self.__image_height = int(3024.0 * 0.1)
        else:
            image_properties = image_properties[0]
            scale_factor = image_properties.Has_ScaleFactor[0]
            self.__image_width = int(image_properties.Has_XLength[0] * scale_factor)
            self.__image_height = int(image_properties.Has_YLength[0] * scale_factor)


    def iteration(self):
        data = self.__generation_scheme_instance.temp_data

        # Find out which types of segmentation label(s) should be rendered
        map_by = []
        if "SegmentClasses" in self.__label_type:
            map_by.append("class")
        if "SegmentInstances" in self.__label_type:
            map_by.append("instance")


        try:
            # Render segmentation label(s) for current image
            data.update(bproc.renderer.render_segmap(map_by=map_by))

        except ValueError:
            for label_type in map_by:
                # "instance_segmaps" or "class_segmaps"
                data[label_type + "_segmaps"] = [ np.zeros( (self.__image_height, self.__image_width) ) ] * len(data["colors"]) # Note: will lead to error if multiple keyframes. Will also not work if no color image is present

                if len(data["colors"]) != 1:
                    raise ValueError('Empty segmentation mask lead to error in blenderproc. More than one keyframe was requested but in case of this error not all keyframes can be reconstructed.')


        # Save rendered images in files
        for label_type in map_by:
            # "instance_segmaps" or "class_segmaps"
            data_image = data[label_type + "_segmaps"]

            # For every keyframe in the scene, one image was created in this iteration. All these created images are now iterated
            for keyframe, single_image in enumerate(data_image):
                img = Image.fromarray(single_image.astype('uint8'), None)
                img.save(f"{self.path_where_to_save_result}/{self.__generation_index}_{keyframe}_{label_type}.png", "PNG")

        self.__generation_index += 1

    def end(self, onto):
        pass


class SimpleVolumeHandler(SDGenerationHandler):
    """Creates a "Volume" (= a space where objects can appear)"""

    def __init__(self, special_root=None):
        self.__special_root = special_root

    def init(self, onto, generation_scheme_instance, manager):
        # Save reference to ontology
        self.__generation_scheme_instance = generation_scheme_instance

        if self.__special_root is None:
            root_node = self.__generation_scheme_instance
        else:
            root_node = self.__special_root

        # Query all volumes directly connected to generation scheme and add them to blender
        for volume in intersection( root_node.Has_Volume, onto.individuals.search(is_a=onto.classes.SimpleVolume) ):
            created_volume = create_blender_volume(x=volume.Has_XCoordinate[0], y=volume.Has_YCoordinate[0], z=volume.Has_ZCoordinate[0],
                                         x_length=volume.Has_XLength[0], y_length=volume.Has_YLength[0], z_length=0)
            volume.bp_reference = created_volume

    def iteration(self):
        pass

    def end(self, onto):
        pass



class SimpleObjectHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance, manager: SDGenerationManager = None):
        # Save reference to ontology
        self.__generation_scheme_instance = generation_scheme_instance

        # 1. Query and iterate over all objects
        res = self.__generation_scheme_instance.Has_Object # There's no SimpleObject class in ontology yet so getting all Objects with Has_Object is enough
        self.__ontology_entities = res
        for object_individual in res:
            # Add object to blender
            res_objects = create_objects(
                obj_file_path=object_individual.Has_Model[0].Has_File[0], how_many=object_individual.Has_Multiplicity[0].Has_MaximumInt[0])
            object_individual.bp_reference = res_objects

            # 3. Instantiate LocationInfo- and RotationInfo-Handlers
            manager.add(
                SimpleMultiplicityHandler(object_individual, object_individual.Has_Multiplicity[0])
            )
            manager.add(
                SimpleLocationHandler(object_individual, object_individual.Has_LocationInfo[0])
            )
            addRotationHandler(manager, onto, object_individual)
            texture = intersection( object_individual.Has_Texture, onto.individuals.search(is_a=onto.classes.RandomTexture))
            if len(texture) == 1:
                manager.add(
                    RandomTextureHandler(object_individual, texture[0])
                )


    def iteration(self):
        pass

    def end(self, onto):
        pass




class RandomTextureHandler(SDGenerationHandler):
    def __init__(self, handled_object, individual):
        self.__handled_object = handled_object

    def init(self, onto, generation_scheme_instance, manager):
        pass

    def iteration(self):
        # Iterate over all blender objects accosiated with this object individual
        for blender_obj_el in self.__handled_object.bp_reference:

                blender_obj_el.clear_materials()
                mat = blender_obj_el.new_material(name="test_material")

                blender_obj_el.set_material(0, mat)
                
                mat.set_principled_shader_value( "Metallic", np.random.uniform(0.0, 0.0) )
                mat.set_principled_shader_value( "Transmission", np.random.uniform(0.0, 0.0) )

                # obj_mat.set_metallic(0)  # should 0 or 1      
                # obj_mat.set_transmission(0)  # should 0 or 1   

                if random.randint(0,2): mat.set_principled_shader_value("Roughness", np.random.uniform(0.9, 1.0) )
                else           : mat.set_principled_shader_value("Roughness", np.random.uniform(0.0, 0.1) )

                color = colorsys.hsv_to_rgb(
                    random.uniform(0,1),
                    random.uniform(0.7,1),
                    random.uniform(0.7,1)
                )
                mat.set_principled_shader_value("Base Color",  color + (1,) ) # the + (1,) specifies 100% opacity


    def end(self, onto):
        pass





class SimpleBoxedPhysicalPlausibilityHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance, manager):
        self.__generation_scheme_instance = generation_scheme_instance
        self.__active = True

        # Ontology-reference to physical plausibility
        effects = intersection(
            self.__generation_scheme_instance.Has_Effect, onto.individuals.search(is_a=onto.classes.SimpleBoxedPhysicalPlausibility))

        if len(effects) == 0:
            self.__active = False
            return
        effect = effects[0]

        
        try: 
            self.__minimum_simulation_time = effect.Has_MinimumSimulationTime[0]
        except:
            self.__minimum_simulation_time = 4.0
        try: 
            self.__maximum_simulation_time = effect.Has_MaximumSimulationTime[0]
        except:
            self.__maximum_simulation_time = 20.0

        # Prepare simulation
        if bpy.context.scene.rigidbody_world == None:
            # this was suggested in https://github.com/DLR-RM/BlenderProc/issues/254 to solve certain console errors that I also was getting
            bpy.ops.rigidbody.world_add()


        fixed_objects = []
        # Find out Base-Area
        # fixed_objects = []
        # base = effect.Has_Volume[0]
        # fixed_objects.append( base.bp_reference )
        base = effect.Has_Volume[0] #.bp_reference
        # Make copy of base so that we can set height ourselves without changing original
        base_new = create_blender_volume(
            base.Has_XCoordinate[0] -50,
            base.Has_YCoordinate[0] -50,
            base.Has_ZCoordinate[0] -50,
            base.Has_XLength[0] +100,
            base.Has_YLength[0] +100,
            50)
        fixed_objects.append( base_new )

        # Create Walls
        fixed_objects.append( create_rectangular_cuboid(
            base.Has_XCoordinate[0] -50,
            base.Has_YCoordinate[0] -50,
            base.Has_ZCoordinate[0],
            base.Has_XLength[0] +100,
            50,
            1000))
        fixed_objects[-1].hide(True)
        fixed_objects.append( create_rectangular_cuboid(
            base.Has_XCoordinate[0] -50,
            base.Has_YCoordinate[0] + base.Has_YLength[0] + 0,
            base.Has_ZCoordinate[0],
            base.Has_XLength[0] +100,
            50,
            1000))
        fixed_objects[-1].hide(True)
        fixed_objects.append( create_rectangular_cuboid(
            base.Has_XCoordinate[0] -50,
            base.Has_YCoordinate[0],
            base.Has_ZCoordinate[0],
            50,
            base.Has_YLength[0],
            1000))
        fixed_objects[-1].hide(True)
        fixed_objects.append( create_rectangular_cuboid(
            base.Has_XCoordinate[0] + base.Has_XLength[0],
            base.Has_YCoordinate[0],
            base.Has_ZCoordinate[0],
            50,
            base.Has_YLength[0],
            1000))
        fixed_objects[-1].hide(True)

        # Create roof
        fixed_objects.append( create_rectangular_cuboid(
            base.Has_XCoordinate[0],
            base.Has_YCoordinate[0],
            base.Has_ZCoordinate[0] + 1000,
            base.Has_XLength[0],
            base.Has_YLength[0],
            1))
        fixed_objects[-1].hide(True)


        for obj in fixed_objects:
            bp_ref = obj 
            bp_ref.enable_rigidbody(active=False, collision_shape="CONVEX_HULL") # COMPUND for complex objects


        # Find out which objects should fall
        self.__falling_objects = effect.Has_FallingObject
        # Adjust some properties for the participating objects
        # (assumption is here that no other function uses these properties so that they'll stay the same
        # across iterations)
        for obj in self.__falling_objects:
            for bp_ref in obj.bp_reference:
                bp_ref.enable_rigidbody(active=True, collision_shape="CONVEX_HULL") # COMPUND for complex objects



    def iteration(self):
        if not self.__active:
            return

        for obj in self.__falling_objects:
            for bp_ref in obj.bp_reference:
                if bp_ref.blender_obj.hide_render and bp_ref.has_rigidbody_enabled():
                    bp_ref.disable_rigidbody()
                elif (not bp_ref.blender_obj.hide_render) and (not bp_ref.has_rigidbody_enabled()):
                    bp_ref.enable_rigidbody(active=True, collision_shape="CONVEX_HULL") # COMPUND for complex objects

        bproc.object.simulate_physics_and_fix_final_poses(
            min_simulation_time=self.__minimum_simulation_time,
            max_simulation_time=self.__maximum_simulation_time,
            check_object_interval=1 #,
            # substeps_per_frame = 5
        )

        # bproc.object.simulate_physics( # TODO: COMMENT OUT THE ABOVE AGAIN AND REMOVE THIS AFTER DEBUGGING
        #     min_simulation_time=self.__minimum_simulation_time,
        #     max_simulation_time=self.__maximum_simulation_time,
        #     check_object_interval=1 #,
        #     # substeps_per_frame = 5
        # )


    def end(self, onto):
        pass










class SimpleRandomGroundHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance, manager):
        self.__generation_scheme_instance = generation_scheme_instance
        self.__active = True
        self.__last_random_image = None

        # Ontology-reference to physical plausibility
        simple_random_ground = intersection(
            self.__generation_scheme_instance.Has_Ground, onto.individuals.search(is_a=onto.classes.SimpleRandomGround))

        if len(simple_random_ground) == 0:
            self.__active = False
            return
        simple_random_ground = simple_random_ground[0]

        volume = simple_random_ground.Has_Volume[0]
        self.__ground = create_rectangular_cuboid(
            volume.Has_XCoordinate[0],
            volume.Has_YCoordinate[0],
            volume.Has_ZCoordinate[0]-30,
            volume.Has_XLength[0],
            volume.Has_YLength[0],
            30)

        # Load paths to images of image pool
        path_to_images = f'{ util.get_path_to_package() / "custom_code/generation_components/media/random_images_src" }'
        self.__images = list(pathlib.Path(path_to_images).rglob("*.jpg"))



    def iteration(self):
        if not self.__active:
            return

        # Clean last random image from memory
        if self.__last_random_image is not None:
            bpy.data.images.remove(self.__last_random_image)

        # Load one random image
        image = bpy.data.images.load(filepath=str(random.choice(self.__images)))
        self.__last_random_image = image

        mat = self.__ground.new_material(name="test_material2")

        node_texture_coordinate = mat.new_node('ShaderNodeTexCoord')
        
        node_mapping = mat.new_node('ShaderNodeMapping')
        node_mapping.inputs['Scale'].default_value = (1.0, 1.0, 1.0)

        node_base_color = mat.new_node('ShaderNodeTexImage')
        node_base_color.label = "Base Color"
        node_base_color.image = image

        node_principled_bsdf = mat.get_the_one_node_with_type("BsdfPrincipled")
        
        mat.link(node_base_color.outputs['Color'], node_principled_bsdf.inputs["Base Color"])
        mat.link(node_texture_coordinate.outputs['UV'], node_mapping.inputs["Vector"])
        mat.link(node_mapping.outputs["Vector"], node_base_color.inputs["Vector"])
        self.__ground.set_material(0, mat)


    def end(self, onto):
        pass




















class SimpleCameraHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance, manager: SDGenerationManager = None):
        # Save reference to root
        self.__generation_scheme_instance = generation_scheme_instance

        # Query the SimpleCamera-individual (there should only be one)
        cameras = intersection(
            self.__generation_scheme_instance.Has_Camera, onto.individuals.search(is_a=onto.classes.SimpleCamera))
        camera = cameras[0]

        # Query the ImageProperties-individual
        image_properties = intersection(
            camera.Has_ImageProperties, onto.individuals.search(is_a=onto.classes.ImageProperties))

        # Retrieve Image Properties
        # Default values for when no ImageProperties are set in ontology instances
        scale_factor = 0.1
        fx = 3325.84099
        cx = 2097.56825
        fy = 3336.41112
        cy = 1558.48315
        xlength = 4032.0
        ylength = 3024.0
        # See if ImagesProperties are set in ontology instances and use them if there are
        if len(image_properties) != 0:
            image_properties = image_properties[0]
            scale_factor = image_properties.Has_ScaleFactor[0]
            fx = image_properties.Has_FX[0]
            cx = image_properties.Has_CX[0]
            fy = image_properties.Has_FY[0]
            cy = image_properties.Has_CY[0]
            xlength = image_properties.Has_XLength[0]
            ylength = image_properties.Has_YLength[0]

        # Set ImageProperties in simulation
        kmatrix = np.array([
            [fx * scale_factor,  0.000000000,        cx * scale_factor],
            [0.00000000,         fy * scale_factor,  cy * scale_factor],
            [0.00000000,         0.0000000,          1.00000000]])
        image_width = int(xlength * scale_factor)
        image_height = int(ylength * scale_factor)

        # Add reference to CameraWrapper
        camera.bp_reference = [BlenderCameraWrapper()]

        # Instantiate LocationInfoHandler
        manager.add(
            SimpleLocationHandler(camera, camera.Has_LocationInfo[0])
        )

        # Instantiate RotationInfo-Handler
        addRotationHandler(manager, onto, camera)

        # fx, fx, cx, cy, imagewidth, imageheight, scalefactor
        # Set up intrinsics matrix
        bproc.camera.set_intrinsics_from_K_matrix(
            kmatrix, image_width, image_height
        )

    def iteration(self):
        pass

    def end(self, onto):
        pass














class SimpleLightHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance, manager: SDGenerationManager = None):
        # Save reference to root
        self.__generation_scheme_instance = generation_scheme_instance

        # Query all SimpleLight-individuals
        self.__lights = intersection(
            self.__generation_scheme_instance.Has_Light, onto.individuals.search(is_a=onto.classes.SimpleLight))

        # Create lights in blender and extend cached ontology with references to those blender objects
        for light_individual in self.__lights:
            bp_lights = []
            for _ in range(light_individual.Has_Multiplicity[0].Has_MaximumInt[0]):
                blender_light = bproc.types.Light("SPOT")
                blender_light.set_energy(300)
                bp_lights.append(blender_light)
            light_individual.bp_reference = bp_lights


            # Create local function that turns lights off for multiplicityhandler
            obj_ref_energy = 300
            def custom_hider(obj_ref, hide):
                nonlocal obj_ref_energy
                if hide:
                    obj_ref_energy = obj_ref.get_energy()
                    obj_ref.set_energy(0)
                else:
                    if obj_ref.get_energy() == 0:
                        obj_ref.set_energy(obj_ref_energy)

            # def custom_hider(self, obj_ref, hide):
            #     nonlocal obj_ref_energy
            #     if hide:
            #         obj_ref_energy = obj_ref.get_energy()
            #         obj_ref.set_energy(0)
            #     else:
            #         if obj_ref.get_energy() == 0:
            #             obj_ref.set_energy(obj_ref_energy)

            # for el in light_individual.bp_reference:
            #     el.hide = custom_hider

            # Instantiate Multiplicity, LocationInfo- and RotationInfo-Handlers
            manager.add(
                SimpleMultiplicityHandler(light_individual, light_individual.Has_Multiplicity[0], custom_hide_function=custom_hider)
            )
            # manager.add(
            #     SimpleMultiplicityHandler(light_individual, light_individual.Has_Multiplicity[0])  #   , custom_hide_function=custom_hider)
            # )
            manager.add(
                SimpleLocationHandler(light_individual, light_individual.Has_LocationInfo[0])
            )
            addRotationHandler(manager, onto, light_individual)


    def iteration(self):
        # Randomize strength of each light source
        for light_individual in self.__lights:
            for light_reference in light_individual.bp_reference:
                light_reference.set_energy(random.randint(15, 100*0.3)) # in example they used 300, but it's in watt and so 300 is really bright

    def end(self, onto):
        pass





class SimpleMultiplicityHandler(SDGenerationHandler):
    def __init__(self, handled_object, individual, custom_hide_function=None):
        self.__handled_object = handled_object
        self.__individual = individual
        self.__custom_hide_function = custom_hide_function

    def init(self, onto, generation_scheme_instance, manager):
        pass

    def iteration(self):
        number = random.randint(
            self.__individual.Has_MinimumInt[0], self.__individual.Has_MaximumInt[0])

        # Iterate over all blender objects associated with this object individual. Show and hide the randomly chosen number of objects
        for count, el in enumerate(self.__handled_object.bp_reference):
            if count < number:
                if self.__custom_hide_function == None:
                    el.hide(False)
                else:
                    self.__custom_hide_function(el, False)
            else:
                if self.__custom_hide_function == None:
                    el.hide(True)
                else:
                    self.__custom_hide_function(el, True)

    def end(self, onto):
        pass





class SimpleLocationHandler(SDGenerationHandler):
    def __init__(self, handled_object, individual):
        self.__handled_object = handled_object
        self.__individual = individual

    def init(self, onto, generation_scheme_instance, manager):
        pass

    def iteration(self):
        # Iterate over all blender objects accosiated with this object individual
        for blender_object in self.__handled_object.bp_reference:
            location = bproc.sampler.upper_region(
                objects_to_sample_on=[self.__individual.Has_Volume[0].bp_reference],
                min_height=0,
                max_height=0)  # if z_length is introduced one day, max_height needs to be set to z_length. Perhaps min_height then also has to be set to the lower boundary of the object manually
            blender_object.set_location(location)

    def end(self, onto):
        pass




class SimpleRotationHandler(SDGenerationHandler):
    def __init__(self, handled_object, individual):
        self.__handled_object = handled_object

    def init(self, onto, generation_scheme_instance, manager):
        pass

    def iteration(self):
        # Iterate over all blender objects handled by this handler
        for blender_object in self.__handled_object.bp_reference:
            rotation = bproc.sampler.uniformSO3(True, True, True)
            blender_object.set_rotation_euler(rotation)

    def end(self, onto):
        pass






class LookDownRotationHandler(SDGenerationHandler):
    def __init__(self, handled_object, individual):
        self.__handled_object = handled_object
        self.__individual = individual

    def init(self, onto, generation_scheme_instance, manager):
        # Add another volumeHandler, because volume where to look at may only be referenced through this individual
        manager.add(
            SimpleVolumeHandler(special_root=self.__individual)
        )

    def iteration(self):
        # Get position of object
        origin = self.__handled_object.bp_reference[0].get_location()

        # Calculation that "looks down" straight
        rotation_matrix = R.from_quat([0, 0, 1, 1]).as_matrix()

        # Add homog cam pose based on location and rotation
        cam2world_matrix = bproc.math.build_transformation_mat( origin, rotation_matrix )

        # Add calculated rotation to the instance
        self.__handled_object.bp_reference[0].set_local2world_mat(cam2world_matrix)

    def end(self, onto):
        pass




class SimpleRotationLookingAtVolumeHandler(SDGenerationHandler):
    def __init__(self, handled_object, individual):
        self.__handled_object = handled_object
        self.__individual = individual

    def init(self, onto, generation_scheme_instance, manager):
        # Add another volumeHandler, because volume where to look at may only be referenced through this individual
        manager.add(
            SimpleVolumeHandler(special_root=self.__individual)
        )

        self.__points = []
        for el in self.__handled_object.bp_reference:
            # Create empty (=point) that will be set to random points in volume
            self.__points.append(bproc.object.create_empty("point", "plain_axes")) # bpy.data.objects.new( "empty", None )

            # Make handled object always look at this empty
            self.__track_constraint = el.blender_obj.constraints.new(type="TRACK_TO")
            self.__track_constraint.target = self.__points[-1].blender_obj
            self.__track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
            self.__track_constraint.up_axis = 'UP_Y'
            # self.__track_constraint.use_target_z = True

    def iteration(self):
        for i, el in enumerate(self.__handled_object.bp_reference):
            # Get position of object
            origin = el.get_location()

            # Get a random position onto which the object should "look at" (i.e. onto which it should be orientated)
            target = bproc.sampler.upper_region(
                objects_to_sample_on=[self.__individual.Has_Volume[0].bp_reference],
                min_height=0,
                max_height=0)
            
            self.__points[i].blender_obj.location = target



    def end(self, onto):
        pass
























