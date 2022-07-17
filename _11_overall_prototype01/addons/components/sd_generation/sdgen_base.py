
from owlready2 import *
import blenderproc as bproc
import bpy  # this package is related to blender functionalities and is only available from within the blender python environment
import numpy as np
import random
import os
from PIL import Image



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
        self.__generation_scheme_instance_label = generation_scheme_instance_label

    def add(self, handler: SDGenerationHandler, at_end_of_iteration=False):
        self.__handlers_all += [handler]
        if not at_end_of_iteration:
            self.__handlers_iteration_normal += [handler]
        else:
            self.__handlers_iteration_end += [handler]


    def start(self, number_of_images, target_path):
        # Load ontology
        ontology = get_ontology(self.__path_to_ontology).load()
        generation_scheme_instance = list(ontology.search(label = self.__generation_scheme_instance_label))[0] # Error wenn keines finde hoffentlich

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

        # Perhaps remove ontology-connection
        pass



class BlenderHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance, manager):
        bproc.init()
    def iteration(self):
        pass
    def end(self, onto):
        pass


class RealImageRenderingHandler(SDGenerationHandler):
    def __init__(self, outf):
        # Set up target folder
        self.__outf = outf
        if os.path.isdir(self.__outf):
            print(f'folder {self.__outf}/ exists')
        else:
            os.mkdir(self.__outf)
            print(f'created folder {self.__outf}/')

        # Set up counter for naming images
        self.__i = 0

    def init(self, onto, generation_scheme_instance, manager):
        pass

    def iteration(self):
        data = bproc.renderer.render()
        data_image = data["colors"]  # + data["instance_segmaps"]
        data_image = np.array(data_image)

        img = None

        # Für jeden keyframe wurde ien Bild gerendert; diese Bilder werden hier durchgelaufen
        for num, single_image in enumerate(data_image):
            img = Image.fromarray(single_image.astype('uint8'), 'RGB')
            img.save(f"{self.__outf}/{self.__i}_{num}.png", "PNG")

        self.__i += 1

    def end(self, onto):
        pass



class SimpleVolumeHandler(SDGenerationHandler):
    def __init__(self, special_root=None):
        self.__onto = None
        self.__special_root = special_root

    def init(self, onto, generation_scheme_instance, manager):
        # Save reference to ontology
        self.__onto = onto
        self.__generation_scheme_instance = generation_scheme_instance

        if self.__special_root is None:
            root_node = self.__generation_scheme_instance
        else:
            root_node = self.__special_root

        # Query all volumes directly connected to generation scheme
        #print(self.__generation_scheme_instance.Has_Volume)
        for volume in root_node.Has_Volume: #onto.search(iri = list(self.__generation_scheme_instance.Has_Volume)): #    self.__generation_scheme_instance.Has_Volume: #onto.search(self.__generation_scheme_instance.Has_Volume, type=onto.Volume):
            if not onto.SimpleVolume in volume.is_a: # wär natürlich schöner direkt in Abfrage, aber das kriege mit bisherirgen sparql-Kenntnissen nicht hin (mit search kriege ggf über Schnittmenge der Ergebnis-Lsiten aus 2 Search-Abfragen hin, aber das wär denke icha uch nicht viel besser)
                continue
            created_volume = create_area(x=volume.Has_XCoordinate[0], y=volume.Has_YCoordinate[0], z=volume.Has_ZCoordinate[0],
                                         x_length=volume.Has_XLength[0], y_length=volume.Has_XLength[0], z_length=0)
            volume.bp_reference = created_volume

        # Add the queried volumes to blender

    def iteration(self):
        pass
    def end(self, onto):
        pass



class SimpleObjectHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance, manager: SDGenerationManager = None):
        # Save reference to ontology
        self.__onto = onto
        self.__generation_scheme_instance = generation_scheme_instance

        # 1. Query all objects
        res = self.__generation_scheme_instance.Has_Object #intersection(self.__generation_scheme_instance.Has_Object, onto.SimpleObject): # <- gibt aktuell noch kein SiomlesObject in Onto

        # 2. Add all objects to scene
        for object in res:
            res_objects = create_objects(obj=object.Has_Model[0].Has_File[0], how_many=object.Has_Multiplicity[0].Has_MaximumInt[0])
            object.bp_reference = res_objects

            # 3. Instantiate LocationInfo- and RotationInfo-Handlers
            manager.add(
                SimpleMultiplicityHandler(object, object.Has_Multiplicity[0])
            )
            manager.add(
                SimpleLocationHandler(object, object.Has_LocationInfo[0])
            )
            manager.add(
                SimpleRotationHandler(object, object.Has_RotationInfo[0])
            )

    def iteration(self):
        pass
    def end(self, onto):
        pass



class SimpleCameraHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance, manager: SDGenerationManager = None):
        # Save reference to ontology
        self.__onto = onto
        self.__generation_scheme_instance = generation_scheme_instance

        # 1. Query the SimpleCamera-individual (there should only be one)
        cameras = intersection(self.__generation_scheme_instance.Has_Camera , onto.search(is_a=onto.SimpleCamera)) # (Eig. kann in blenderproc nur 1 Kanera geben und mehrere wären mehrere Frames)
        camera = cameras[0]

        class BlenderCameraWrapper():
            def set_location(self, location):
                # print("It's me, Camera Wrapper!")
                # print(location)
                # print(b)
                # Set first camera pose (= first key frame)
                cam_pose = bproc.math.build_transformation_mat( location, [0, 0, 0] )
                bproc.camera.add_camera_pose(cam_pose, frame=0) # ohne frame=0 wird in jeder iteration neuer Frame hinzugefügt. Ggf. kann. i.wann wie in Blenderproc-Bsp ausnutzen und zbsp 10 Frames pro generierte Szene, damit einmal platzierte Objekte mehrfach verwendet. ggf. könnte dazu vershcieddene Kamera-Isntanzen dann doch auch machen. Einiges an Aufwand daher eher unattraktiv in Arbeit und ja auch unnötiger Optimierungs-Grad für mich.
            # def set_rotation_euler(self, rotation): # TODO: Ich glaube dass das nicht echt euler ist!
            #     # Set first camera pose (= first key frame)
            #     cam_pose = bproc.math.build_transformation_mat( self.get_location(), rotation )
            #     bproc.camera.add_camera_pose(cam_pose, frame=0)
                pass
            def set_local2world_mat(self, matrix):
                bproc.camera.add_camera_pose(matrix, frame=0)
            def get_location(self):
                matrix = bproc.camera.get_camera_pose(frame=0)
                translation = matrix[0:3, 3]#.reshape((-1,1))
                #translation = 
                print(matrix)
                print(translation)
                
                return translation


        camera.bp_reference = [BlenderCameraWrapper()]

        # 3. Instantiate LocationInfo- and RotationInfo-Handlers
        print(camera.__dict__)
        manager.add(
            SimpleLocationHandler(camera, camera.Has_LocationInfo[0])
        )
        manager.add(
            SimpleRotationLookingAtVolumeHandler(camera, camera.Has_RotationInfo[0])
        )

    def iteration(self):
        pass
    def end(self, onto):
        pass


class SimpleMultiplicityHandler(SDGenerationHandler):
    def __init__(self, handled_object, individual):
        self.__handled_object = handled_object
        self.__individual = individual

    def init(self, onto, generation_scheme_instance, manager):
        pass

    def iteration(self):
        number = random.randint(self.__individual.Has_MinimumInt[0], self.__individual.Has_MaximumInt[0])

        for count, el in enumerate(self.__handled_object.bp_reference): # Gehe über alle blender-Modelle. Daher muss nach SimpleObjectHandelr aufgerufen werden
            if count < number:
                el.hide(False)
            else:
                el.hide(True)

    def end(self, onto):
        pass


class SimpleLocationHandler(SDGenerationHandler):
    def __init__(self, handled_object, individual):
        self.__handled_object = handled_object
        self.__individual = individual

    def init(self, onto, generation_scheme_instance, manager):
        pass

    def iteration(self):
        for el2 in self.__handled_object.bp_reference: # Gehe über alle blender-Modelle. Daher muss nach SimpleObjectHandelr aufgerufen werden
            location = bproc.sampler.upper_region(
                objects_to_sample_on=[self.__individual.Has_Volume[0].bp_reference],
                min_height=0, max_height=0) # sobald z_length gibt, muss max_height zu z_length geändert werden vermute ich. Ggf. muss min_height dann auch stattdessen manuell zu unterkante des OBjekte gemacht werden?
            el2.set_location(location)

    def end(self, onto):
        pass


class SimpleRotationHandler(SDGenerationHandler):
    def __init__(self, handled_object, individual):
        self.__handled_object = handled_object
        self.__individual = individual
        
    def init(self, onto, generation_scheme_instance, manager):
        pass

    def iteration(self):
        for el2 in self.__handled_object.bp_reference: # Gehe über alle blender-Modelle. Daher muss nach SimpleObjectHandelr aufgerufen werden
            rotation = bproc.sampler.uniformSO3(True, True, True)
            el2.set_rotation_euler(rotation)

    def end(self, onto):
        pass


class SimpleRotationLookingAtVolumeHandler(SDGenerationHandler):
    def __init__(self, handled_object, individual):
        self.__handled_object = handled_object
        self.__individual = individual
        
    def init(self, onto, generation_scheme_instance, manager):
        manager.add(
            SimpleVolumeHandler(special_root=self.__individual)
        )
        pass

    def iteration(self):
        # Get position of object and random psotion to look at
        origin = self.__handled_object.bp_reference[0].get_location()
        target = bproc.sampler.upper_region(
                objects_to_sample_on=[self.__individual.Has_Volume[0].bp_reference],
                min_height=0, max_height=0) # <- Kandidat für in eigene Helper-Fkt., um DRY zu erfüllen später (so mit height immer passend wählen - sofern überhaupot noch Objekte in Blender als Hilfen verwenden möchte zum samplen anstatt selbst zu machen)
        
        print(origin)
        print(target)

        # Calculate and set rotation
        rotation_matrix = bproc.camera.rotation_from_forward_vec(target - origin, inplane_rot=np.random.uniform(-3.14159, 3.14159))
        # Add homog cam pose based on location an rotation
        print(f"rotation matrix: {rotation_matrix}")
        cam2world_matrix = bproc.math.build_transformation_mat(origin, rotation_matrix)
        print( cam2world_matrix )
        self.__handled_object.bp_reference[0].set_local2world_mat(cam2world_matrix) # Begriff set_local2world_mat von blenderproc gebort, hoffe dass passt


        # for el2 in self.__handled_object.bp_reference: # Gehe über alle blender-Modelle. Daher muss nach SimpleObjectHandelr aufgerufen werden
        #     rotation = bproc.sampler.uniformSO3(True, True, True)
        #     el2.set_rotation_euler(rotation)

    def end(self, onto):
        pass







def create_rectangular_cuboid(x=None, y=None, z=None,
                              x_length=None, y_length=None, z_length=None):
    rect_cuboid = bproc.object.create_primitive(shape="CUBE")
    rect_cuboid.set_scale([x_length/2, y_length/2, z_length/2])
    rect_cuboid.set_location(
        [x + x_length/2,  y + y_length/2,  z + z_length/2])
    return rect_cuboid


def create_area(x=None, y=None, z=None,
                x_length=None, y_length=None, z_length=None):
    test = bproc.object.create_primitive(shape="CUBE")
    # Cube ist standardmäßig 2m x 2m x 2m groß. Scale von 10 in einer Richtung führt also zu 20m Länge in dieser Richtung
    test.set_scale([x_length/2/1000, y_length/2/1000, z_length/2/1000])

    # location bezieht auf Mittelpunkt des Objektes. Das ist für Modelle ggf. oft cool, für Rechteck wär aber auch cool genau ausmessen zu können, weswegen anpassen werde

    print(f"z = {z}")
    print(f"z_length = {z_length}")

    test.set_location([x/1000 + x_length/2/1000,  y/1000 + y_length/2/1000,  z/1000 + z_length/2/1000])

    test.hide(True)

    return test







def intersection(lst1, lst2): # from https://www.geeksforgeeks.org/python-intersection-two-lists/
    # Use of hybrid method
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3






def create_objects(obj, how_many=1):
    res = []

    for i in range(how_many):
        #mesh = bproc.loader.load_obj("E:\\David (HDD)\\projects\\MATSE-bachelorarbeit-ss22-tests\\_11_overall_prototype01\\data\\ontologies\\media\\" + obj) # returned liste, eigentliches Objekt leigt dann glaube ich in mesh[0]
        #mesh = bproc.loader.load_obj("E:/David (HDD)/projects/MATSE-bachelorarbeit-ss22-tests/_11_overall_prototype01/data/ontologies/" + obj) # returned liste, eigentliches Objekt leigt dann glaube ich in mesh[0]
        mesh = bproc.loader.load_obj("E:/David (HDD)/projects/MATSE-bachelorarbeit-ss22-tests/_11_overall_prototype01/data/ontologies/" + obj) # returned liste, eigentliches Objekt leigt dann glaube ich in mesh[0]
        # mesh[0].set_location(0,0,0)
        # mesh.get_material().

        print(mesh)

        #mat = mesh[0].get_materials()[0]
        mat = mesh[0].new_material(name="test_material")
        mat.set_principled_shader_value(
            "Metallic", np.random.uniform(0.0, 0.0))
        mat.set_principled_shader_value("Base Color", (0.0, 1.0, 0.0, 1.0))
        print(mat)

        res += mesh # note: this works only, because mesh is a list (containing only the 1 created mesh)

    return res











