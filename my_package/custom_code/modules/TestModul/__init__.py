import json
from owlready2 import *



class SDGenBaseModule():
    def onto_to_sd(path_to_onto, path_where_to_save_result):
        pass


class SDGenModule(SDGenBaseModule):

    def json_to_onto(onto_classes, end_user_data):
        """
        Overreaching function creates new individual if 
        """

        parsed_data = json.loads(end_user_data)

        # Volumes
        vol_camera = onto_classes.SimpleVolume(
            Has_XCoordinate = [-1],
            Has_YCoordinate = [-1],
            Has_ZCoordinate = [parsed_data["camera_height"]],
            Has_XLength = [2],
            Has_YLength = [2]
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
        vol_objects_spawns = onto_classes.SimpleVolume(
            Has_XCoordinate = [-parsed_data["area_length_x"]/2],
            Has_YCoordinate = [-parsed_data["area_length_y"]/2],
            Has_ZCoordinate = [100.0],
            Has_XLength = [parsed_data["area_length_x"]],
            Has_YLength = [parsed_data["area_length_y"]]
        )
        vol_objects_ground = onto_classes.SimpleVolume(
            Has_XCoordinate = [-parsed_data["area_length_x"]/2],
            Has_YCoordinate = [-parsed_data["area_length_y"]/2],
            Has_ZCoordinate = [0.0],
            Has_XLength = [parsed_data["area_length_x"]],
            Has_YLength = [parsed_data["area_length_y"]]
        )
        
        

        # Location infos
        loc_inf_camera = onto_classes.EqualDistributedLocationInVolume(
            Has_Volume = [vol_camera]
        )
        loc_inf_objects = onto_classes.EqualDistributedLocationInVolume(
            Has_Volume = [vol_objects_spawns]
        )
        loc_inf_light = onto_classes.EqualDistributedLocationInVolume(
            Has_Volume = [vol_light]
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
        simple_random_ground = onto_classes.SimpleRandomGround(
            Has_Volume = [vol_ground]
        )

        # Label
        label = onto_classes.SegmentationLabel(
            Has_ObjectToRecognize = obj,
            Has_SegmentationType = ["SegmentClasses"]
        )

        # Light
        light = onto_classes.SimpleLight(
            Has_RotationInfo = [rot_inf_at_ground],
            Has_LocationInfo = [loc_inf_light],
            Has_Multiplicity = [onto_classes.EqualDistributionRangeMultiplicity(
                Has_MinimumInt = [1],
                Has_MaximumInt = [2]
            )]
        )

        # Create root
        new_root = onto_classes.GenerationScheme(
            Has_NumberOfImagesToRender = [3],
            Has_Volume = [vol_ground, vol_camera, vol_objects_spawns, vol_light, vol_objects_ground],
            Has_Object = obj,
            Has_Camera = [camera],
            Has_Ground = [simple_random_ground],
            Has_Label = [label],
            Has_Light = [light],
            Has_Effect = [onto_classes.SimpleBoxedPhysicalPlausibility(
                Has_FallingObject = obj,
                Has_Volume = [vol_objects_ground],
                Has_MinimumSimulationTime = [1.0],
                Has_MaximumSimulationTime = [2.0]
            )]
        )



