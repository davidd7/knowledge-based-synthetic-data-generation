
from re import M
from socket import has_dualstack_ipv6
from xml.dom.expatbuilder import parseFragmentString
# from unnamed_sd_package.addons.components.sd_generation import sdgen_base
import json
from owlready2 import *
import itertools
# from rdflib import *







class SDGenBaseModule():
    def onto_to_sd(path_to_onto, path_where_to_save_result):
        pass


class SDGenModule(SDGenBaseModule):

    def json_to_onto(onto_classes, onto_individuals, individual_name, data):
        """
        Overreaching function creates new individual if 
        """

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
                Has_Label = [label]
            )



