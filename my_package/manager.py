from owlready2 import *
import time
import math
from interfaces import *


# MANAGER

class SimpleSDGenerationManager(SDGenerationManager):
    def __init__(self, path_to_ontology, path_to_onto_classes):
        self.__handlers_all: list[SDGenerationHandler] = []
        self.__handlers_iteration_normal: list[SDGenerationHandler] = []
        self.__handlers_iteration_end: list[SDGenerationHandler] = []
        self.__path_to_ontology: str = path_to_ontology
        self.__path_to_onto_classes = path_to_onto_classes
        self.__timer = RenderingTimer()


    def add(self, handler: SDGenerationHandler, at_end_of_iteration=False):
        self.__handlers_all.append(handler)
        if not at_end_of_iteration:
            self.__handlers_iteration_normal.append(handler)
        else:
            self.__handlers_iteration_end.append(handler)

    def start(self):

        # INIT
        self.__timer.start()

        w = World()

        onto_individuals = w.get_ontology(self.__path_to_ontology).load(only_local=True) # reload=True # World().get_ontology(... hat Probleme auch nicht gelöst
        ontology_classes = w.get_ontology(self.__path_to_onto_classes).load(only_local=True)

        # print("ONTO CLASSES:")
        # print( [el for el in ontology_classes.classes()] )
        # print(ontology_classes.imported_ontologies)
        # for el in ontology_classes.imported_ontologies:
        #     print( [el2 for el2 in el.classes()] )
        # print( [el for el in ontology_classes.classes()] )
        # print(ontology_classes.NewImportTestXYZ)
        # # print(ontology_classes.main22.NewImportTestXYZ) # .main22 is none
        # print( [el for el in w.classes()])
        # # print( w.RandomTexture  ) # Error
        # # print( w.NewImportTestXYZ  ) # Verm auch error, aber nciht explizit getestet
        # # with w: # error bereits durch das with
        # #     print(RandomTexture)
        # # print( w[RandomTexture]  ) # Error
        # return

        onto_wrapper = OntoWrapper(ontology_classes, onto_individuals)

        generation_scheme_instances_list = list( intersection( onto_wrapper.individuals.search(is_a=onto_wrapper.classes.GenerationScheme)  , onto_wrapper.individuals.individuals()  ) )

        if len(generation_scheme_instances_list) == 0:
            raise ValueError("No generation scheme root with the label specified in __init__ was found")
        root_individual = generation_scheme_instances_list[0]

        number_of_images = root_individual.Has_NumberOfImagesToRender[0]

        # Set up all handlers
        for el in self.__handlers_all:
            el.init(onto_wrapper, root_individual, manager=self)

        # ITERATE
        
        self.__timer.iterate_start()


        # Do the iteration
        for i in range(number_of_images):
            for el in self.__handlers_iteration_normal:
                el.iteration()
            for el in self.__handlers_iteration_end:
                el.iteration()
            self.__timer.iterate_round_finish()


        # END

        # Clean up all handlers
        for el in reversed(self.__handlers_all):
            el.end(onto_wrapper)

        onto_individuals.destroy()
        onto_individuals = None

        self.__timer.end()


    def get_timer(self):
        return self.__timer













class RenderingTimer():
    def __init__(self):
        self.__init_start = None
        self.__iterate_start = None
        self.__iterations = []
        self.__end = None

    def start(self):
        self.__init_start = time.time()

    def iterate_start(self):
        self.__iterate_start = time.time()

    def iterate_round_finish(self):
        self.__iterations.append(time.time())

    def end(self):
        self.__end = time.time()
    
    def calc_total_time(self):
        return self.__end - self.__init_start

    def calc_init_time(self):
        return self.__iterate_start - self.__init_start

    def calc_iterate_time(self):
        return self.__iterations[-1] - self.__iterate_start

    def calc_end_time(self):
        return self.__end - self.__iterations[-1]

    def calc_iterate_median(self):
        number_iterations = len(self.__iterations)
        if number_iterations == 0:
            return 0

        # Calculate intervals
        intervals = self.__calculate_intervals()

        # Calculate median
        intervals_sorted = sorted(intervals)
        if number_iterations % 2 == 1:
            i = int(math.floor(number_iterations/2.0))
            return intervals[i]
        else:
            i = int(number_iterations/2)
            return (intervals[i-1] + intervals[i]) / 2.0

    def calc_iterate_avg(self):
        number_iterations = len(self.__iterations)
        return self.calc_iterate_time() / number_iterations

    def calc_iterate_min(self):
        intervals = self.__calculate_intervals()
        return sorted(intervals)[0]

    def calc_iterate_max(self):
        intervals = self.__calculate_intervals()
        return sorted(intervals)[-1]

    def __calculate_intervals(self):
        intervals = []
        last = self.__iterate_start
        for el in self.__iterations:
            intervals.append( el - last )
            last = el
        return intervals
    
    def get_statistics(self):
        return {
            "total" : self.calc_total_time(),
            "init" : self.calc_init_time(),
            "iterate" : self.calc_iterate_time(),
            "end" : self.calc_end_time(),
            "iterate_median" : self.calc_iterate_median(),
            "iterate_avg" : self.calc_iterate_avg(),
            "iterate_min" : self.calc_iterate_min(),
            "iterate_max" : self.calc_iterate_max()
        }








class OntoWrapper():
    def __init__(self, onto_classes, onto_individuals):
        self.__onto_classes = onto_classes
        self.__onto_individuals = onto_individuals

    @property
    def classes(self):
        return self.__onto_classes

    @property
    def individuals(self):
        return self.__onto_individuals






def intersection(lst1, lst2): # hybrid method from https://www.geeksforgeeks.org/python-intersection-two-lists/
    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3









