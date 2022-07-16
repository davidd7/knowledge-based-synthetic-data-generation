
from owlready2 import *
import blenderproc as bproc
import bpy  # this package is related to blender functionalities and is only available from within the blender python environment


class SDGenerationManager():
    def __init__(self, path_to_ontology, generation_scheme_instance_label):
        pass
    def add(self):
        pass
    def start(self):
        pass

class SDGenerationHandler():
    def init(self, onto, generation_scheme_instance):
        pass
    def iteration(self):
        pass
    def end(self, onto):
        pass




class SimpleSDGenerationManager(SDGenerationManager):
    def __init__(self, path_to_ontology, generation_scheme_instance_label):
        self.__handlers: list[SDGenerationHandler] = []
        self.__path_to_ontology: str = path_to_ontology
        self.__generation_scheme_instance_label = generation_scheme_instance_label

    def add(self, handler: SDGenerationHandler):
        self.__handlers += [handler]

    def start(self, number_of_images, target_path):
        # Load ontology
        ontology = get_ontology(self.__path_to_ontology).load()
        generation_scheme_instance = list(ontology.search(label = self.__generation_scheme_instance_label))[0] # Error wenn keines finde hoffentlich

        # Set up all handlers
        for el in self.__handlers:
            el.init(ontology, generation_scheme_instance)

        # Do the iteration
        for i in range(number_of_images):
            for el in self.__handlers:
                el.iteration()

        # Clean up all handlers
        for el in reversed(self.__handlers):
            el.end(ontology)

        # Perhaps remove ontology-connection
        pass



class BlenderHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance):
        bproc.init()
    def iteration(self):
        pass
    def end(self, onto):
        pass


class SimpleVolumeHandler(SDGenerationHandler):
    def __init__(self):
        self.__onto = None

    def init(self, onto, generation_scheme_instance):
        # Save reference to ontology
        self.__onto = onto
        self.__generation_scheme_instance = generation_scheme_instance

        # Query all volumes directly connected to generation scheme
        print(self.__generation_scheme_instance.Has_Volume)
        for volume in self.__generation_scheme_instance.Has_Volume: #onto.search(iri = list(self.__generation_scheme_instance.Has_Volume)): #    self.__generation_scheme_instance.Has_Volume: #onto.search(self.__generation_scheme_instance.Has_Volume, type=onto.Volume):
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
    def init(self, onto, generation_scheme_instance):
        # Save reference to ontology
        self.__onto = onto
        self.__generation_scheme_instance = generation_scheme_instance

        # 1. Query all objects
        for object in self.__generation_scheme_instance.Has_Object: #intersection(self.__generation_scheme_instance.Has_Object, onto.SimpleObject): # <- gibt aktuell noch kein SiomlesObject in Onto
            create_objects(obj=object.Has_Model[0].Has_File[0], how_many=object.Has_Multiplicity[0].Has_MaximumInt[0])


        # 2. Add all objects to scene


        # 3. Instantiate LocationInfo- and RotationInfo-Handlers



    def iteration(self):
        pass
    def end(self, onto):
        pass


class SimpleLocationHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance):
        pass
    def iteration(self):
        pass
    def end(self, onto):
        pass


class SimpleRotationHandler(SDGenerationHandler):
    def init(self, onto, generation_scheme_instance):
        pass
    def iteration(self):
        pass
    def end(self, onto):
        pass


# 1. Bereiche hinzufügen



# Boden hinzufügen


# 







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
    test.set_scale([x_length/2/100, y_length/2/100, z_length/2/100])

    # location bezieht auf Mittelpunkt des Objektes. Das ist für Modelle ggf. oft cool, für Rechteck wär aber auch cool genau ausmessen zu können, weswegen anpassen werde

    print(f"z = {z}")
    print(f"z_length = {z_length}")

    test.set_location([x/100 + x_length/2/100,  y/100 + y_length/2/100,  z/100 + z_length/2/100])

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
        mesh = bproc.loader.load_obj("E:/David (HDD)/projects/MATSE-bachelorarbeit-ss22-tests/_11_overall_prototype01/data/ontologies/" + obj) # returned liste, eigentliches Objekt leigt dann glaube ich in mesh[0]
        # mesh[0].set_location(0,0,0)
        # mesh.get_material().

        print(mesh)

        #mat = mesh[0].get_materials()[0]
        mat = mesh[0].new_material()
        mat.set_principled_shader_value(
            "Metallic", np.random.uniform(0.0, 0.0))
        mat.set_principled_shader_value("Base Color", (0.0, 1.0, 0.0, 1.0))
        print(mat)

        res += mesh # note: this works only, because mesh is a list (containing only the 1 created mesh)

    return res











