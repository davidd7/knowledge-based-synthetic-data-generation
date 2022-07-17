
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




    def json_to_onto(path_to_ontology_in, path_to_ontology_out=None):
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
        
        # 1) Load ontology
        #ontology = get_ontology(path_to_ontology_in).load()
        w = World()
        o1 = w.get_ontology("http://test.org/onto300.owl")
        o2 = w.get_ontology(path_to_ontology_in).load()
        o1.imported_ontologies.append(o2)
        print(o1)
        #exit()

        with o1:
            root = o2.GenerationScheme("EGS1")


        print(o1.individuals())
        
        o1.save(path_to_ontology_out)
        

        #o1.load()
        #o2.load()

        # Create root
        print(list(o1.classes()))
        print(list(o2.classes()))

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

        o1.save(file = path_to_ontology_out)


        print(parsed_data)


        



















