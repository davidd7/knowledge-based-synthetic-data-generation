from imp import reload
from owlready2 import *
import blenderproc as bproc
import bpy  # this package is related to blender functionalities and is only available from within the blender python environment
import numpy as np
import random
import os
from PIL import Image
import matplotlib.pyplot as plt
import pathlib
ABSOLUTE_PATH_TO_PACKAGE = "E:\\David (HDD)\\projects\\MATSE-bachelorarbeit-ss22-tests\\_11_overall_prototype01"
# ABSOLUTE_PATH_TO_PACKAGE = "C:\\Users\\david\\Git Repositories\\MATSE-bachelorarbeit-ss22-tests\\_11_overall_prototype01"
MODE = "bp_debug" # options: "normal", "bp_run", "bp_debug"
def get_path_to_package():
    """
    Returns path object containing the path that should lead to the root of this package
    """
    if MODE == "":
        return pathlib.Path(__file__).parent.resolve()
    elif MODE == "bp_run" or MODE == "bp_debug":
        return pathlib.Path(ABSOLUTE_PATH_TO_PACKAGE) / "unnamed_sd_package"
#from unnamed_sd_package import get_path_to_package


#get_path_to_package()

#import 



class SDGenerationManager():
    def __init__(self, path_to_ontology, generation_scheme_instance_label):
        pass

    def add(self):
        pass

    def start(self):
        pass


class SDGenerationHandler():
    def init(self, onto, generation_scheme_instance, manager):
        pass

    def iteration(self):
        pass

    def end(self, onto):
        pass


class SimpleSDGenerationManager(SDGenerationManager):
    def __init__(self, path_to_ontology, generation_scheme_instance_label):
        self.__handlers_all: list[SDGenerationHandler] = []
        self.__handlers_iteration_normal: list[SDGenerationHandler] = []
        self.__handlers_iteration_end: list[SDGenerationHandler] = []
        self.__path_to_ontology: str = path_to_ontology
        self.__generation_scheme_instance_label: str = generation_scheme_instance_label

    def add(self, handler: SDGenerationHandler, at_end_of_iteration=False):
        self.__handlers_all.append(handler)
        if not at_end_of_iteration:
            self.__handlers_iteration_normal.append(handler)
        else:
            self.__handlers_iteration_end.append(handler)

    def start(self, number_of_images, target_path):
        # Load ontology (note: ontology is not closed or anything at the end at the moment)
        #print("===> " + self.__path_to_ontology)
        # try:
        #     print(ontology)
        # except:
        #     print("An exception occurred")


        w = World()
        ontology = w.get_ontology(self.__path_to_ontology).load() # reload=True # World().get_ontology(... hat Probleme auch nicht gelöst
        #ontology.save(f'{ get_path_to_package() / "data/ontologies/" / "start.owl" }')

        #with ontology:
        generation_scheme_instance = list(ontology.search(label=self.__generation_scheme_instance_label))[0]  # Error wenn keines finde hoffentlich

        # Set up all handlers
        for el in self.__handlers_all:
            el.init(ontology, generation_scheme_instance, manager=self)

        # Do the iteration
        for i in range(number_of_images):
            for el in self.__handlers_iteration_normal:
                el.iteration()
            for el in self.__handlers_iteration_end:
                el.iteration()

        # Clean up all handlers
        for el in reversed(self.__handlers_all):
            el.end(ontology)

        ontology.destroy()
        ontology = None



class BlenderHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance, manager):
        bproc.init()

    def iteration(self):
        pass

    def end(self, onto):
        pass




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


class RealImageRenderingHandler(SDGenerationHandler):
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
        data_image = data["colors"]  # + data["instance_segmaps"]
        data_image = np.array(data_image)

        # Für jeden keyframe wurde ien Bild gerendert; diese Bilder werden hier durchgelaufen
        for keyframe, single_image in enumerate(data_image):
            img = Image.fromarray(single_image.astype('uint8'), 'RGB')
            img.save(f"{self.__outf}/{self.__generation_index}_{keyframe}.png", "PNG")

        self.__generation_index += 1

        self.__generation_scheme_instance.temp_data = data

    def end(self, onto):
        pass




class SimpleSegmentationLabelHandler(SDGenerationHandler):
    """
    Classes for when Has_SegmentType is "SegmentClasses" are set automatically based on to which Object individual a ObjectToRecognize belongs (remember: one Object individual are multiple blender objects (with the same model), when multiplicity is > 1). 
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
        segmentation_label_individuals = intersection(self.__generation_scheme_instance.Has_Label, onto.search(is_a=onto.SegmentationLabel))
        seg_individual = segmentation_label_individuals
        if len(seg_individual) == 0:
            return

        seg_individual = seg_individual[0] # Assumption: There is at most 1 segmentation individual (rendering multiple segmentation individuals at once is not supported at the moment)

        for i, object in enumerate(seg_individual.Has_ObjectToRecognize):  # --> macht automatisch, dass jedes Modell eigene Klasse ist (Multiplizitätm eines OBjekts zählt alles zur selben Klasse)  Im PÖrinzip sollte o(k) sein, wobei k die Anzahl an Objekten im Blender ist, die erkannt werden sollen (weil inneren beiden Schleifen nur Weg sind um alle Objekte auszuwählen)
            for blender_object in object.bp_reference:
                # -> must be +1, because 0 ist background I think (although 0 is used in their own example...?)
                blender_object.set_cp("category_id", i + 1)

        self.__label_type = seg_individual.Has_SegmentationType

    def iteration(self):
        data = self.__generation_scheme_instance.temp_data

        # Find out which types of segmentation label(s) should be rendered
        map_by = []
        if "SegmentClasses" in self.__label_type:
            map_by.append("class")
        if "SegmentInstances" in self.__label_type:
            map_by.append("instance")

        # Render segmentation label(s) for current image
        data.update(bproc.renderer.render_segmap(map_by=map_by))

        # Save rendered images in files
        for label_type in map_by:
            # "instance_segmaps" or "class_segmaps"
            data_image = data[label_type + "_segmaps"]

            # Für jeden keyframe wurde ien Bild gerendert; diese Bilder werden hier durchgelaufen
            for keyframe, single_image in enumerate(data_image):
                # Save image for label
                img = Image.fromarray(single_image.astype('uint8'), None)
                img.save(f"{self.path_where_to_save_result}/{self.__generation_index}_{keyframe}_{label_type}.png", "PNG")

                # Save a second image highlighting the label for human eyes
                plt.figure()
                plt.subplot(1, 1, 1)
                plt.imshow(data_image[0], 'jet', interpolation='none')
                plt.savefig(
                    f"{self.path_where_to_save_result}/{self.__generation_index}_{keyframe}_{label_type}_visualization.png")

        self.__generation_index += 1

    def end(self, onto):
        pass


class SimpleVolumeHandler(SDGenerationHandler):
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
        for volume in intersection( root_node.Has_Volume, onto.search(is_a=onto.SimpleVolume) ):
            created_volume = create_blender_volume(x=volume.Has_XCoordinate[0], y=volume.Has_YCoordinate[0], z=volume.Has_ZCoordinate[0],
                                         x_length=volume.Has_XLength[0], y_length=volume.Has_XLength[0], z_length=0)
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
                obj=object_individual.Has_Model[0].Has_File[0], how_many=object_individual.Has_Multiplicity[0].Has_MaximumInt[0])
            object_individual.bp_reference = res_objects

            # 3. Instantiate LocationInfo- and RotationInfo-Handlers
            manager.add(
                SimpleMultiplicityHandler(object_individual, object_individual.Has_Multiplicity[0])
            )
            manager.add(
                SimpleLocationHandler(object_individual, object_individual.Has_LocationInfo[0])
            )
            manager.add(
                SimpleRotationHandler(object_individual, object_individual.Has_RotationInfo[0])
            )
            texture = intersection( object_individual.Has_Texture, onto.search(is_a=onto.RandomTexture))
            if len(texture) == 1:
                manager.add(
                    RandomTextureHandler(object_individual, texture[0])
                )



    def iteration(self):
        # for el in self.__ontology_entities:
        #     for blender_obj_el in el.bp_reference:
        #         # texture = bproc.material.create_procedural_texture(random.choice(["CLOUDS"]))

        #         # print(texture.xxxx)

        #         blender_obj_el.clear_materials()
        #         mat = blender_obj_el.new_material(name="test_material")
        #         # mat.set_principled_shader_value(
        #         #     "Metallic", np.random.uniform(1.0, 1.0))
        #         # mat.set_principled_shader_value("Base Color", (0.0, 1.0, 0.0, 1.0))
        #         # mesh[0].set_material(0, mat) # (i don't know yet what index does, but this works). Also not sure why material is not added without this stept (perhaps existing material with higher priority overriding it?)

        #         # slot = mat.texture_slots.add()
        #         # slot.texture = texture
        #         blender_obj_el.set_material(0, mat) 

        #         # mat = blender_obj_el.get_materials()[0]


        #         # mat.set_principled_shader_value(
        #         #     "Metallic", np.random.uniform(0.0, 1.0))
                

        #         mat.set_principled_shader_value( "Metallic", np.random.uniform(0.0, 0.0) )
        #         mat.set_principled_shader_value( "Transmission", np.random.uniform(0.0, 0.0) )

        #         # obj_mat.set_metallic(0)  # should 0 or 1      
        #         # obj_mat.set_transmission(0)  # should 0 or 1   

        #         if random.randint(0,2): mat.set_principled_shader_value("Roughness", np.random.uniform(0.9, 1.0) )
        #         else           : mat.set_principled_shader_value("Roughness", np.random.uniform(0.0, 0.1) )

        #         mat.set_principled_shader_value("Base Color", (  np.random.uniform(0.0, 1.0)  , np.random.uniform(0.0, 1.0), np.random.uniform(0.0, 1.0), 1.0))

        #         # blender_obj_el.set_material(0, mat)
        #         # bproc.


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

                mat.set_principled_shader_value("Base Color", (  np.random.uniform(0.0, 1.0)  , np.random.uniform(0.0, 1.0), np.random.uniform(0.0, 1.0), 1.0))


    def end(self, onto):
        pass














class SimpleBoxedPhysicalPlausibilityHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance, manager):
        self.__generation_scheme_instance = generation_scheme_instance

        # Ontology-reference to physical plausibility
        effects = intersection(
            self.__generation_scheme_instance.Has_Effect, onto.search(is_a=onto.SimpleBoxedPhysicalPlausibility))
        # print(effects)
        # print(len(effects))
        # exit()
        if len(effects) == 0:
            return
        effect = effects[0]

        # Prepare simulation
        # bpy.ops.rigidbody.world_remove()
        if bpy.context.scene.rigidbody_world == None:
            # this was suggested in https://github.com/DLR-RM/BlenderProc/issues/254 solve certain console errors that I alsow as getting
            bpy.ops.rigidbody.world_add()


        # Find out Base-Area
        fixed_objects = []
        base = effect.Has_Volume[0]
        fixed_objects.append( base.bp_reference )
        # Create Walls
        fixed_objects.append( create_rectangular_cuboid(
            base.Has_XCoordinate[0],
            base.Has_YCoordinate[0],
            base.Has_ZCoordinate[0],
            base.Has_XLength[0],
            1,
            500))
        fixed_objects[-1].hide(True)
        fixed_objects.append( create_rectangular_cuboid(
            base.Has_XCoordinate[0],
            base.Has_YCoordinate[0] + base.Has_YLength[0],
            base.Has_ZCoordinate[0],
            base.Has_XLength[0],
            1,
            500))
        fixed_objects[-1].hide(True)
        fixed_objects.append( create_rectangular_cuboid(
            base.Has_XCoordinate[0],
            base.Has_YCoordinate[0],
            base.Has_ZCoordinate[0],
            1,
            base.Has_YLength[0],
            500))
        fixed_objects[-1].hide(True)
        fixed_objects.append( create_rectangular_cuboid(
            base.Has_XCoordinate[0] + base.Has_XLength[0],
            base.Has_YCoordinate[0],
            base.Has_ZCoordinate[0],
            1,
            base.Has_YLength[0],
            500))
        fixed_objects[-1].hide(True)

        for obj in fixed_objects:
            # COMPOUND for complex
            bp_ref = obj 
            bp_ref.enable_rigidbody(active=False, collision_shape="CONVEX_HULL")
            #obj.build_convex_decomposition_collision_shape("<Path where to store vhacd>")


        # Falling objects herausfinden
        falling_objects = effect.Has_FallingObject
        # Adjust some properties for the participating objects
        # (assumption is here that no other function uses these properties so that they'll stay the same
        # across iterations)
        for obj in falling_objects:
            # COMPOUND for complex
            for bp_ref in obj.bp_reference:
                bp_ref.enable_rigidbody(active=True, collision_shape="CONVEX_HULL")
                #obj.build_convex_decomposition_collision_shape("<Path where to store vhacd>")


    def iteration(self):
        bproc.object.simulate_physics_and_fix_final_poses(
            min_simulation_time=4,
            max_simulation_time=20,
            check_object_interval=1
        )

        # for el in global_dict_get(key):
        #     print(objects_to_sample_on)
        #     location = bproc.sampler.upper_region(objects_to_sample_on=objects_to_sample_on)
        #     el.set_location(location)


    def end(self, onto):
        pass



























class SimpleRandomGroundHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance, manager):
        self.__generation_scheme_instance = generation_scheme_instance

        # Ontology-reference to physical plausibility
        simple_random_ground = intersection(
            self.__generation_scheme_instance.Has_Ground, onto.search(is_a=onto.SimpleRandomGround))
        # print(effects)
        # print(len(effects))
        # exit()
        if len(simple_random_ground) == 0:
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

        # Mögliche Bilder laden
        # images = list(Path(args.image_dir).rglob("material_manipulation_sample_texture*.jpg"))
        path_to_images = f'{ get_path_to_package() / "addons/components/sd_generation/media/random_images_src" }'
        self.__images = list(pathlib.Path(path_to_images).rglob("*.jpg"))


    def iteration(self):
        # Load one random image
        image = bpy.data.images.load(filepath=str(random.choice(self.__images)))
        # Set it as base color of the current material


        self.__ground.clear_materials()
        mat = self.__ground.new_material(name="test_material2")
        mat.set_principled_shader_value("Base Color", image)

        self.__ground.set_material(0, mat)



        # for el in global_dict_get(key):
        #     print(objects_to_sample_on)
        #     location = bproc.sampler.upper_region(objects_to_sample_on=objects_to_sample_on)
        #     el.set_location(location)


    def end(self, onto):
        pass























































class BlenderCameraWrapper():
    """
    Makes camera methods available in a way similar to how objects are manipulated. The camera is normally manipulated differently in blender, but it's advantageous to be able to change location/rotation of camera and objects in a similar way.
    """
    def set_location(self, location):
        # Set first camera pose (= first key frame)
        cam_pose = bproc.math.build_transformation_mat(location, [
                                                        0, 0, 0])
        # ohne frame=0 wird in jeder iteration neuer Frame hinzugefügt. Ggf. kann. i.wann wie in Blenderproc-Bsp ausnutzen und zbsp 10 Frames pro generierte Szene, damit einmal platzierte Objekte mehrfach verwendet. ggf. könnte dazu vershcieddene Kamera-Isntanzen dann doch auch machen. Einiges an Aufwand daher eher unattraktiv in Arbeit und ja auch unnötiger Optimierungs-Grad für mich.
        bproc.camera.add_camera_pose(cam_pose, frame=0)

    def set_local2world_mat(self, matrix):
        bproc.camera.add_camera_pose(matrix, frame=0)

    def get_location(self):
        matrix = bproc.camera.get_camera_pose(frame=0)
        translation = matrix[0:3, 3]
        return translation



class SimpleCameraHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance, manager: SDGenerationManager = None):
        # Save reference to root
        self.__generation_scheme_instance = generation_scheme_instance

        # Query the SimpleCamera-individual (there should only be one)
        cameras = intersection(
            self.__generation_scheme_instance.Has_Camera, onto.search(is_a=onto.SimpleCamera))
        camera = cameras[0]

        # Add reference to CameraWrapper
        camera.bp_reference = [BlenderCameraWrapper()]

        # Instantiate LocationInfo- and RotationInfo-Handlers
        manager.add(
            SimpleLocationHandler(camera, camera.Has_LocationInfo[0])
        )
        manager.add(
            SimpleRotationLookingAtVolumeHandler(
                camera, camera.Has_RotationInfo[0])
        )

    def iteration(self):
        pass

    def end(self, onto):
        pass



class SimpleLightHandler(SDGenerationHandler): # TODO: Simple light hat eigentlich auch multiplicity-info
    def init(self, onto, generation_scheme_instance, manager: SDGenerationManager = None):
        # Save reference to root
        self.__generation_scheme_instance = generation_scheme_instance

        # Query all SimpleLight-individuals
        self.__lights = intersection(
            self.__generation_scheme_instance.Has_Light, onto.search(is_a=onto.SimpleLight))

        # Create lights in blender and extend cached ontology with referencesw to those blender objects
        for light in self.__lights:
            blender_lights = []
            for _ in range(light.Has_Multiplicity[0].Has_MaximumInt[0]):
                blender_light = bproc.types.Light("SPOT")
                blender_light.set_energy(300)
                blender_lights.append(blender_light)

            light.bp_reference = blender_lights

            # Instantiate LocationInfo- and RotationInfo-Handlers
            obj_ref_energy = 300
            def custom_hider(obj_ref, hide):
                nonlocal obj_ref_energy
                if hide:
                    obj_ref_energy = obj_ref.get_energy()
                    obj_ref.set_energy(0)
                else:
                    if obj_ref.get_energy() == 0:
                        obj_ref.set_energy(obj_ref_energy)
            manager.add(
                SimpleMultiplicityHandler(light, light.Has_Multiplicity[0], custom_hide_function=custom_hider)
            )
            manager.add(
                SimpleLocationHandler(light, light.Has_LocationInfo[0])
            )
            manager.add(
                SimpleRotationLookingAtVolumeHandler(
                    light, light.Has_RotationInfo[0])
            )

    def iteration(self):
        for light in self.__lights:
            light.bp_reference[0].set_energy(random.randint(15, 100)) # in example they used 300, but it's in watt and so 300 is really bright probably
        # pass

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

        # Iterate over all blender objects accosiated with this object individual. Show and hide the randomly chosen number of objects
        print(self.__handled_object.bp_reference)
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
                # el.hide(True)

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
                objects_to_sample_on=[
                    self.__individual.Has_Volume[0].bp_reference],
                min_height=0, max_height=0)  # sobald z_length gibt, muss max_height zu z_length geändert werden vermute ich. Ggf. muss min_height dann auch stattdessen manuell zu unterkante des OBjekte gemacht werden?
            blender_object.set_location(location)

    def end(self, onto):
        pass


class SimpleRotationHandler(SDGenerationHandler):
    def __init__(self, handled_object, individual):
        self.__handled_object = handled_object

    def init(self, onto, generation_scheme_instance, manager):
        pass

    def iteration(self):
        # Iterate over all blender objects accosiated with this object individual
        for blender_object in self.__handled_object.bp_reference:
            rotation = bproc.sampler.uniformSO3(True, True, True)
            blender_object.set_rotation_euler(rotation)

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
        pass

    def iteration(self):
        # Get position of object and random position to look at
        origin = self.__handled_object.bp_reference[0].get_location()
        target = bproc.sampler.upper_region(
            objects_to_sample_on=[
                self.__individual.Has_Volume[0].bp_reference],
            min_height=0, max_height=0)
            
        # Calculate and set rotation
        rotation_matrix = bproc.camera.rotation_from_forward_vec(
            target - origin, inplane_rot=np.random.uniform(-3.14159, 3.14159))
        # Add homog cam pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(
            origin, rotation_matrix)
        self.__handled_object.bp_reference[0].set_local2world_mat(
            cam2world_matrix)

    def end(self, onto):
        pass


def create_rectangular_cuboid(x=None, y=None, z=None,
                              x_length=None, y_length=None, z_length=None):
    """
    x, y, z, x_length, y_length, z_length should all be given in Millimeters (mm)
    """
    blender_object = bproc.object.create_primitive(shape="CUBE")
    # Cube ist standardmäßig 2m x 2m x 2m groß. Scale von 10 in einer Richtung führt also zu 20m Länge in dieser Richtung
    blender_object.set_scale([x_length/2/1000, y_length/2/1000, z_length/2/1000])
    blender_object.set_location([x/1000 + x_length/2/1000,  y/1000 +
                      y_length/2/1000,  z/1000 + z_length/2/1000]) # location bezieht auf Mittelpunkt des Objektes. Das ist für Modelle ggf. oft cool, für Rechteck wär aber auch cool genau ausmessen zu können, weswegen anpassen werde
    return blender_object


def create_blender_volume(x=None, y=None, z=None,
                x_length=None, y_length=None, z_length=None):
    blender_object = create_rectangular_cuboid(x, y, z, x_length, y_length, z_length)
    blender_object.hide(True) # volumes should not be visible in rendering
    return blender_object


def intersection(lst1, lst2):  # from https://www.geeksforgeeks.org/python-intersection-two-lists/
    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def create_objects(obj, how_many=1):
    res = []

    for i in range(how_many):
        # returned liste, eigentliches Objekt leigt dann glaube ich in mesh[0]
        mesh = bproc.loader.load_obj(
            str(get_path_to_package() / "data/ontologies/" / obj))
        # mesh.get_material().

        #mat = mesh[0].get_materials()[0]
        mat = mesh[0].new_material(name="test_material")
        mat.set_principled_shader_value(
            "Metallic", np.random.uniform(1.0, 1.0))
        mat.set_principled_shader_value("Base Color", (0.0, 1.0, 0.0, 1.0))
        mesh[0].set_material(0, mat) # (i don't know yet what index does, but this works). Also not sure why material is not added without this stept (perhaps existing material with higher priority overriding it?)

        res += mesh # works only because mesh is a list (containing only the 1 created mesh)

    return res
