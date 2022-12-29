from owlready2 import *
from custom_code.generation_components import handlers







class SDGenBaseModule():
    def onto_to_sd(path_to_onto, path_where_to_save_result):
        pass



def onto_to_sd(path_to_onto, path_where_to_save_result, path_to_onto_classes, sd_generation_manager):

    sd_generation_manager.add(
        handlers.BlenderHandler()
    )

    sd_generation_manager.add(
        handlers.SimpleVolumeHandler()
    )

    sd_generation_manager.add(
        handlers.SimpleObjectHandler()
    )

    sd_generation_manager.add(
        handlers.SimpleCameraHandler()
    )

    sd_generation_manager.add(
        handlers.SimpleLightHandler()
    )

    sd_generation_manager.add(
        handlers.SimpleRandomGroundHandler()
    )

    sd_generation_manager.add(
        handlers.SimpleBoxedPhysicalPlausibilityHandler(),
        at_end_of_iteration=True
    )

    sd_generation_manager.add(
        handlers.RealImageRenderingHandler(path_where_to_save_result),
        at_end_of_iteration=True
    )

    sd_generation_manager.add(
        handlers.SimpleSegmentationLabelHandler(path_where_to_save_result),
        at_end_of_iteration=True
    )

    sd_generation_manager.start()




