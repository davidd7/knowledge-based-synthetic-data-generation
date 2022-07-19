
from xml.dom.expatbuilder import parseFragmentString
from unnamed_sd_package.addons.components.sd_generation import sdgen_base
import json
from owlready2 import *
import itertools





class FutureUtilities():

    def load_classes_and_individuals(path_to_ontology_classes, path_to_ontology_individuals):
        w = World()
        onto_classes = w.get_ontology("file://" + path_to_ontology_classes).load()
        onto_individuals = w.get_ontology("file://" + path_to_ontology_individuals)
        onto_individuals.imported_ontologies.append(onto_classes)
        onto_individuals = onto_individuals.load()
        return onto_classes, onto_individuals


    def sys_update_generation_scheme(path_to_ontology_classes, path_to_ontology_individuals):
        pass


    def sys_create_new_generation_scheme(path_to_ontology_classes, path_to_ontology_individuals):
        # Load settings (later global?)
        settings = """ { "next_id" : 1 } """
        parsed_settings = json.loads(settings)

        # Get ontologies
        onto_classes, onto_individuals = FutureUtilities.load_classes_and_individuals(path_to_ontology_classes, path_to_ontology_individuals)

        # Get new ontology name
        old_scheme_names = [ individual.name for individual in onto_individuals.search(type=onto_classes.GenerationScheme) ]
        new_id = parsed_settings["next_id"]
        while (new_name := f"EGS{new_id:03}") in old_scheme_names: # resulting name is saved in new_id
            new_id += 1

        # Create new nodes in the ontology
        SDGenExampleModule.json_to_onto(onto_classes, onto_individuals, new_name)

        onto_individuals.save(file=path_to_ontology_individuals)
            
       


    def sys_delete_generation_scheme():
        pass




class SDGenBaseModule():
    def onto_to_sd(path_to_onto, path_where_to_save_result):
        pass


class SDGenExampleModule(SDGenBaseModule):
    def onto_to_sd(path_to_onto, path_where_to_save_result):
        sd_generation_manager = sdgen_base.SimpleSDGenerationManager(path_to_onto, "EGS1")

        sd_generation_manager.add(
            sdgen_base.BlenderHandler()
        )

        sd_generation_manager.add(
            sdgen_base.SimpleVolumeHandler()
        )

        sd_generation_manager.add(
            sdgen_base.SimpleObjectHandler()
        )

        sd_generation_manager.add(
            sdgen_base.SimpleCameraHandler()
        )

        sd_generation_manager.add(
            sdgen_base.RealImageRenderingHandler(path_where_to_save_result),
            at_end_of_iteration=True
        )

        sd_generation_manager.add(
            sdgen_base.SimpleSegmentationLabelHandler(path_where_to_save_result),
            at_end_of_iteration=True
        )

        sd_generation_manager.start(5, path_where_to_save_result)






    def json_to_onto(onto_classes, onto_individuals, individual_name):
        """
        Overreaching function creates new individual if 
        """
        # Load user data
        data = """
            {
                "objects_to_recognize": [
                    {
                    "url": "",
                    "min": 3,
                    "max": 4
                    }
                ],
                "area_length_x": 3,
                "area_length_y": 7,
                "camera_height": 5
            }"""

        parsed_data = json.loads(data)


        with onto_individuals:

            new_root = onto_classes.GenerationScheme(individual_name)

        
        # 1) Load ontology
        # w = World()
        # onto_classes = w.get_ontology(path_to_ontology_classes).load()
        # onto_individuals = w.get_ontology(path_to_ontology_individuals)#.load()
        # onto_individuals.imported_ontologies.append(onto_classes)
        # onto_individuals = onto_individuals.load()

        # a = onto_individuals.search(type=onto_classes.GenerationScheme)#.contains

        # with onto_individuals:
            # current_individuals = onto_individuals.search(type=onto_classes.GenerationScheme)
            # used_individual_names = [ individual.name for individual in current_individuals ]
            # new_individual_name = f"EGS{parsed_settings.next_id:03}"


            # Make sure that next_id is free or otherwise increase next_id
             # Findet auch die importierten
            # b = onto_individuals["EGS1"] # Findet nur die Individuals, die wirklich in der Klasse selbst sind ohne importierte


            # print("onto_individuals.search(type=Scheme)")
            # print (a)
            # #a._name
            # print(a[0])
            # print(   a[0]._name)
            # print(res)
            # print("onto_individuals['EGS1']")
            # print(b)

            #root = onto_individuals.GenerationScheme(f"EGS{1:03}")


        #print(f"EGS{1:03}")
        # exit()

        # print(onto_classes.individuals())
        
        # onto_classes.save(path_to_ontology_individuals)
        

        # #o1.load()
        # #o2.load()

        # # Create root
        # print(list(onto_classes.classes()))
        # print(list(onto_individuals.classes()))

        #o1 = o1 #.load()


        # root = ontology.GenerationScheme("GS2")
        
        # root = ontology.GenerationScheme("GS2")
        
        # root = ontology.GenerationScheme("GS3")

        # Label

        # Camera

        # Ground

        # Volumes
    
        # Objects

        # 

        # onto_classes.save(file = path_to_ontology_individuals)


        print(parsed_data)


        



















