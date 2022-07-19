
from xml.dom.expatbuilder import parseFragmentString
from unnamed_sd_package.addons.components.sd_generation import sdgen_base
import json
from owlready2 import *


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




    def json_to_onto(path_to_ontology_classes, path_to_ontology_individuals):
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


        # Load settings (later global?)
        settings = """
        {
            "next_id" : 1
        }
        """
        parsed_settings = json.loads(settings)


        
        # 1) Load ontology
        #ontology = get_ontology(path_to_ontology_in).load()
        w = World()
        onto_classes = w.get_ontology(path_to_ontology_classes)#.load()
        onto_classes = onto_classes.load()
        print(list(onto_classes.classes()))
        onto_individuals = w.get_ontology(path_to_ontology_individuals)#.load()
        #print(list(onto_individuals.classes()))
        onto_individuals.imported_ontologies.append(onto_classes)
        onto_individuals = onto_individuals.load()
        #print(onto_classes)
        #exit()



        # print("lol")
        # print(onto_classes.GenerationScheme)
        a = onto_individuals.search(type=onto_classes.GenerationScheme)#.contains

        with onto_individuals:
            # Make sure that next_id is free and otherwise increase next_id
            a = onto_individuals.search(type=onto_classes.GenerationScheme, _name="EGS1") # Findet auch die importierten
            b = onto_individuals["EGS1"] # Findet nur die Individuals, die wirklich in der Klasse selbst sind ohne importierte

            res = [ el.name for el in a ]

            print("onto_individuals.search(type=Scheme)")
            print (a)
            #a._name
            print(a[0])
            print(   a[0]._name)
            print(res)
            print("onto_individuals['EGS1']")
            print(b)

            #root = onto_individuals.GenerationScheme(f"EGS{1:03}")


        #print(f"EGS{1:03}")
        exit()

        print(onto_classes.individuals())
        
        onto_classes.save(path_to_ontology_individuals)
        

        #o1.load()
        #o2.load()

        # Create root
        print(list(onto_classes.classes()))
        print(list(onto_individuals.classes()))

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

        onto_classes.save(file = path_to_ontology_individuals)


        print(parsed_data)


        



















