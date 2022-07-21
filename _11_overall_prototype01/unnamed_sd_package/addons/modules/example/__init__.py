
from re import M
from socket import has_dualstack_ipv6
from xml.dom.expatbuilder import parseFragmentString
from unnamed_sd_package.addons.components.sd_generation import sdgen_base
import json
from owlready2 import *
import itertools





class FutureUtilities():


    def load_classes_and_individuals(path_to_ontology_classes, path_to_ontology_individuals):
        #w = World()
        onto_classes = get_ontology("file://" + path_to_ontology_classes).load() # w.
        onto_individuals = get_ontology("file://" + path_to_ontology_individuals).load() # w.
        onto_individuals.imported_ontologies.append(onto_classes)
        #onto_individuals = onto_individuals.load()
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

        with onto_classes:
            x = list(default_world.sparql("""
                    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                    PREFIX owl: <http://www.w3.org/2002/07/owl#>
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                    PREFIX indiv: <http://www.semanticweb.org/david/ontologies/2022/6/synthetic-data-generation-individuals#>
                    PREFIX synt: <http://www.semanticweb.org/david/ontologies/2022/6/synthetic-data-generation#>
                    SELECT ?subject ?prop ?object
                        WHERE { 
                            { select distinct ?prop {[] ?prop []} }
                            ?subject ?prop+ ?object
                }
                """))

            print(x[:10]  )

            exit()



        """
        Overreaching function creates new individual if 
        """
        # Load user data
        data = """
            {
                "objects_to_recognize": [
                    {
                    "url": "media/untitled.obj",
                    "min": 3,
                    "max": 4
                    },
                    {
                    "url": "media/untitled.obj",
                    "min": 3,
                    "max": 4
                    },
                    {
                    "url": "media/untitled.obj",
                    "min": 3,
                    "max": 14
                    }
                ],
                "area_length_x": 3,
                "area_length_y": 7,
                "camera_height": 5
            }"""
        parsed_data = json.loads(data)


        

        with onto_individuals:
            # Volumes
            vol_camera = onto_classes.SimpleVolume(
                Has_XCoordinate = [-parsed_data["area_length_x"]/2],
                Has_YCoordinate = [-parsed_data["area_length_y"]/2],
                Has_ZCoordinate = [parsed_data["camera_height"]],
                Has_XLength = [parsed_data["area_length_x"]],
                Has_YLength = [parsed_data["area_length_y"]]
            )
            vol_ground = onto_classes.SimpleVolume(
                Has_XCoordinate = [-parsed_data["area_length_x"]/2],
                Has_YCoordinate = [-parsed_data["area_length_y"]/2],
                Has_ZCoordinate = [0.0],
                Has_XLength = [parsed_data["area_length_x"]],
                Has_YLength = [parsed_data["area_length_y"]]
            )
            vol_light = onto_classes.SimpleVolume(
                Has_XCoordinate = [-parsed_data["area_length_x"]/2],
                Has_YCoordinate = [-parsed_data["area_length_y"]/2],
                Has_ZCoordinate = [500.0],
                Has_XLength = [parsed_data["area_length_x"]],
                Has_YLength = [parsed_data["area_length_y"]]
            )
            vol_objects = onto_classes.SimpleVolume(
                Has_XCoordinate = [-parsed_data["area_length_x"]/2],
                Has_YCoordinate = [-parsed_data["area_length_y"]/2],
                Has_ZCoordinate = [100.0],
                Has_XLength = [parsed_data["area_length_x"]],
                Has_YLength = [parsed_data["area_length_y"]]
            )
            
            

            # Location infos
            loc_inf_camera = onto_classes.EqualDistributedLocationInVolume(
                Has_Volume = [vol_camera]
            )
            loc_inf_ground = onto_classes.EqualDistributedLocationInVolume( # <- verm. aktuell nicht in Benutzung?
                Has_Volume = [vol_ground]
            )
            loc_inf_objects = onto_classes.EqualDistributedLocationInVolume(
                Has_Volume = [vol_objects]
            )

            # Rotation Info
            rot_inf_at_ground = onto_classes.EqualDistributionRotationLookingAtVolume(
                Has_Volume = [vol_ground]
            )
            rot_inf_random = onto_classes.EqualDistributionRandomRotation()

            # Objects and characteristics that are object-specific in this example
            obj = []
            for object in parsed_data["objects_to_recognize"]:
                # Multiplicity
                mult_obj = onto_classes.EqualDistributionRangeMultiplicity(
                    Has_MinimumInt = [object["min"]],
                    Has_MaximumInt = [object["max"]]
                )

                # Model
                model_obj = onto_classes.Model(
                    Has_File = [object["url"]]
                )

                # Object
                obj.append(
                    onto_classes.Object(
                        Has_Multiplicity = [mult_obj],
                        Has_Model = [model_obj],
                        Has_RotationInfo = [rot_inf_random],
                        Has_LocationInfo = [loc_inf_objects]
                    )
                )


            # Camera
            camera = onto_classes.SimpleCamera(
                Has_LocationInfo = [loc_inf_camera],
                Has_RotationInfo = [rot_inf_at_ground]
            )

            # Ground
            ground = onto_classes.SimpleRandomGround()
        
            # Physical Plausibility
            effect_physical_plausibility = onto_classes.SimplePhysicalPlausibility(
                Has_FixedObjects = [ground],
                Has_FallingObject = obj
            )

            # Label
            label = onto_classes.SegmentationLabel(
                Has_ObjectToRecognize = obj,
                Has_SegmentationType = ["SegmentClasses"]
            )


            # Create root
            new_root = onto_classes.GenerationScheme(
                individual_name, # <- name of the new individual is first argument
                Has_Volume = [vol_camera, vol_objects, vol_light],
                Has_Object = obj,
                Has_Camera = [camera],
                Has_Ground = [ground],
                Has_Effect = [effect_physical_plausibility],
                #Has_Label = [label]
            )
            #new_root.Has_Label = [label]
            new_root.Has_Label = [label]



















