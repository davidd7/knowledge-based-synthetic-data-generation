import json
from owlready2 import *
from my_package.interfaces import *



class SDGenModule(SDGenBaseModule):

    def json_to_onto(onto_classes, end_user_data, ml_system_data):
    
        # Set area based on location set in form
        area_length_y = None
        y_coordinate = None
        if end_user_data["location"] == "full":
            area_length_y = 200.0
            y_coordinate = -area_length_y/2
        elif end_user_data["location"] == "half_left":
            area_length_y = 100.0
            y_coordinate = -area_length_y
        elif end_user_data["location"] == "half_right":
            area_length_y = 100.0
            y_coordinate = 0

        # Volumes
        vol_camera = onto_classes.SimpleVolume(
            Has_XCoordinate = [-10.0],
            Has_YCoordinate = [-10.0],
            Has_ZCoordinate = [200.0],
            Has_XLength = [20.0],
            Has_YLength = [20.0]
        )
        vol_random_images_ground = onto_classes.SimpleVolume(
            Has_XCoordinate = [-500.0],
            Has_YCoordinate = [-500.0],
            Has_ZCoordinate = [0.0],
            Has_XLength = [1000.0],
            Has_YLength = [1000.0]
        )
        vol_light = onto_classes.SimpleVolume(
            Has_XCoordinate = [-75.0],
            Has_YCoordinate = [-100.0],
            Has_ZCoordinate = [500.0],
            Has_XLength = [150.0],
            Has_YLength = [200.0]
        )
        vol_objects_spawns = onto_classes.SimpleVolume(
            Has_XCoordinate = [-75.0],
            Has_YCoordinate = [y_coordinate],
            Has_ZCoordinate = [100.0],
            Has_XLength = [150.0],
            Has_YLength = [area_length_y]
        )
        vol_physical_plausibility_ground = onto_classes.SimpleVolume(
            Has_XCoordinate = [-75.0],
            Has_YCoordinate = [y_coordinate],
            Has_ZCoordinate = [0.0],
            Has_XLength = [150.0],
            Has_YLength = [area_length_y]
        )
        
        
        random_texture = onto_classes.RandomTexture()


        # Location infos
        loc_inf_camera = onto_classes.EqualDistributedLocationInVolume( #
            Has_Volume = [vol_camera]
        )
        loc_inf_objects = onto_classes.EqualDistributedLocationInVolume( #
            Has_Volume = [vol_objects_spawns]
        )
        loc_inf_light = onto_classes.EqualDistributedLocationInVolume(
            Has_Volume = [vol_light]
        )

        # Rotation Info
        rot_inf_lights_at_ground = onto_classes.LookAtVolumeRotation(
            Has_Volume = [vol_random_images_ground]
        )
        rot_inf_random = onto_classes.RandomRotation()
        rot_inf_down = onto_classes.LookDownRotation()

        # Objects and characteristics that are object-specific in this example
        obj_class_1 = onto_classes.Object(
            Has_Multiplicity = [ #
                onto_classes.EqualDistributionRangeMultiplicity( #
                    Has_MinimumInt = [end_user_data["class1_min"]],
                    Has_MaximumInt = [end_user_data["class1_max"]]
            )],
            Has_Model = [ #
                onto_classes.Model(
                    Has_File = ["gear_class1.obj"] #
            )],
            Has_RotationInfo = [rot_inf_random],
            Has_LocationInfo = [loc_inf_objects],
            Has_Texture = [random_texture]
        )
        obj_class_2 = onto_classes.Object(
            Has_Multiplicity = [
                onto_classes.EqualDistributionRangeMultiplicity( #
                    Has_MinimumInt = [end_user_data["class2_min"]],
                    Has_MaximumInt = [end_user_data["class2_max"]]
            )],
            Has_Model = [
                onto_classes.Model( #
                    Has_File = ["gear_class2.obj"] #
            )],
            Has_RotationInfo = [rot_inf_random],
            Has_LocationInfo = [loc_inf_objects],
            Has_Texture = [random_texture]
        )
        obj = [obj_class_1, obj_class_2]


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
        camera = onto_classes.SimpleCamera( #
            Has_LocationInfo = [loc_inf_camera], #
            Has_RotationInfo = [rot_inf_down], #
            Has_ImageProperties = [cam_image_properties]
        )

        # Ground
        simple_random_ground = onto_classes.SimpleRandomGround( #
            Has_Volume = [vol_random_images_ground]
        )

        # Label
        label = onto_classes.SegmentationLabel( #
            Has_ObjectToRecognize = obj,
            Has_SegmentationType = ["SegmentClasses"]
        )

        # Light
        light = onto_classes.SimpleLight( #
            Has_RotationInfo = [rot_inf_lights_at_ground],
            Has_LocationInfo = [loc_inf_light],
            Has_Multiplicity = [onto_classes.EqualDistributionRangeMultiplicity(
                Has_MinimumInt = [1],
                Has_MaximumInt = [2]
            )]
        )

        # Create root
        new_root = onto_classes.GenerationScheme(
            Has_NumberOfImagesToRender = [ml_system_data["number_of_images_to_render"]],
            Has_Volume = [vol_random_images_ground, vol_camera, vol_objects_spawns, vol_light, vol_physical_plausibility_ground], #
            Has_Object = obj, #
            Has_Camera = [camera], #
            Has_Ground = [simple_random_ground], #
            Has_Label = [label], #
            Has_Light = [light], #
            Has_Effect = [onto_classes.SimpleBoxedPhysicalPlausibility( #
                Has_FallingObject = obj,
                Has_Volume = [vol_physical_plausibility_ground],
                Has_MinimumSimulationTime = [4.0],
                Has_MaximumSimulationTime = [20.0]
            )]
        )



