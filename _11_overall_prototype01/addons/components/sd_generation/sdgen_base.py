from owlready2 import *

path = "C:/Users/david/Git Repositories/MATSE-bachelorarbeit-ss22-tests/_11_overall_prototype01/data/ontologies/sdgen_ontology_1.owl"


# res = onto.search(type=onto.GenerationScheme)




# for el in res:
#     print("lol")
#     print(el.__dict__)
#     pass

# print(res[0].Has_Volume)




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

        # Set up all handlers
        for el in self.__handlers:
            el.init(ontology)

        # Do the iteration
        for i in range(number_of_images):
            for el in self.__handlers:
                el.iteration()

        # Clean up all handlers
        for el in self.__handlers:
            el.end(ontology)

        # Perhaps remove ontology-connection
        pass








# 1. Bereiche hinzufügen



# Boden hinzufügen


# 















