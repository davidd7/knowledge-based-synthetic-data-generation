
#import 
from addons.components.sd_generation import sdgen_base


class SDGenBaseModule():
    def onto_to_sd():
        pass




class SDGenExampleModule(SDGenBaseModule):
    def onto_to_sd(self, path_to_onto, path_where_to_save_result):
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
            sdgen_base.SegmentationLabelHandler(path_where_to_save_result),
            at_end_of_iteration=True
        )


        sd_generation_manager.start(5, path_where_to_save_result)
























