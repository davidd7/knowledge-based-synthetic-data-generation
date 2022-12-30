import json
from owlready2 import *
from my_package.interfaces import *



class SDGenModule(SDGenBaseModule):

    def json_to_onto(onto_classes, end_user_data, ml_system_data):
        """
        Overreaching function creates new individual if 
        """

        # Volumes
        vol_camera = onto_classes.SimpleVolume(
            Has_XCoordinate = [-1],
            Has_YCoordinate = [-1],
            Has_ZCoordinate = [end_user_data["camera_height"]],
            Has_XLength = [2],
            Has_YLength = [2]
        )
        vol_ground = onto_classes.SimpleVolume(
            Has_XCoordinate = [-end_user_data["area_length_x"]/2],
            Has_YCoordinate = [-end_user_data["area_length_y"]/2],
            Has_ZCoordinate = [0.0],
            Has_XLength = [end_user_data["area_length_x"]],
            Has_YLength = [end_user_data["area_length_y"]]
        )
        vol_light = onto_classes.SimpleVolume(
            Has_XCoordinate = [-end_user_data["area_length_x"]/2],
            Has_YCoordinate = [-end_user_data["area_length_y"]/2],
            Has_ZCoordinate = [500.0],
            Has_XLength = [end_user_data["area_length_x"]],
            Has_YLength = [end_user_data["area_length_y"]]
        )
        vol_objects_spawns = onto_classes.SimpleVolume(
            Has_XCoordinate = [-end_user_data["area_length_x"]/2],
            Has_YCoordinate = [-end_user_data["area_length_y"]/2],
            Has_ZCoordinate = [100.0],
            Has_XLength = [end_user_data["area_length_x"]],
            Has_YLength = [end_user_data["area_length_y"]]
        )
        vol_objects_ground = onto_classes.SimpleVolume(
            Has_XCoordinate = [-end_user_data["area_length_x"]/2],
            Has_YCoordinate = [-end_user_data["area_length_y"]/2],
            Has_ZCoordinate = [0.0],
            Has_XLength = [end_user_data["area_length_x"]],
            Has_YLength = [end_user_data["area_length_y"]]
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
        rot_inf_at_ground = onto_classes.LookAtVolumeRotation(
            Has_Volume = [vol_ground]
        )
        rot_inf_random = onto_classes.RandomRotation()
        rot_inf_down = onto_classes.LookDownRotation()

        # Objects and characteristics that are object-specific in this example
        obj = []
        for object in end_user_data["objects_to_recognize"]:
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
        cam_image_properties = onto_classes.ImageProperties(
            Has_ScaleFactor = [0.1],
            Has_FX = [3325.84099],
            Has_CX = [2097.56825],
            Has_FY = [3336.41112],
            Has_CY = [1558.48315],
            Has_XLength = [4032.0],
            Has_YLength = [3024.0]
        )
        camera = onto_classes.SimpleCamera(
            Has_LocationInfo = [loc_inf_camera],
            Has_RotationInfo = [rot_inf_down],
            Has_ImageProperties = [cam_image_properties]
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
                Has_MinimumInt = [0], # 1
                Has_MaximumInt = [10]  # 2
            )]
        )

        # Create root
        new_root = onto_classes.GenerationScheme(
            Has_NumberOfImagesToRender = [ml_system_data["number_of_images_to_render"]],
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



