
from owlready2 import *
# import blenderproc as bproc
# import bpy  # this package is related to blender functionalities and is only available from within the blender python environment


class SDGenerationManager():
    def add(self):
        pass
    def start(self):
        pass

class SDGenerationHandler():
    def init(self, onto):
        pass
    def iteration(self):
        pass
    def end(self):
        pass




class SimpleSDGenerationManager(SDGenerationManager):
    def __init__(self, path_to_ontology):
        self.__handlers: list[SDGenerationHandler] = []
        self.__path_to_ontology: str = path_to_ontology

    def add(self, handler: SDGenerationHandler):
        self.__handlers += handler

    def start(self, number_of_images, target_path):
        # Load ontology
        ontology = get_ontology(self.__path_to_ontology).load()

        # print(list(ontology.classes())) # -> klappt aktuell ==>  Später so etwas in Art zu Tests hinzufügen?

        # Set up all handlers
        for el in self.__handlers:
            el.init(ontology)

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
    def init(self, onto):
        pass
    def iteration(self):
        pass
    def end(self):
        pass


class SimpleVolumeHandler(SDGenerationHandler):
    def __init__(self):
        self.__onto = None

    def init(self, onto):
        # Save reference to ontology
        self.__onto = onto.search(type=onto.GenerationScheme)

        # Query all volumes directly connected to generation scheme

        # Add the queried volumes to blender


    def iteration(self):
        pass
    def end(self):
        pass





# 1. Bereiche hinzufügen



# Boden hinzufügen


# 















