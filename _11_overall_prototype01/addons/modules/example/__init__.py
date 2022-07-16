
#import 
from addons.components.sd_generation import sdgen_base


class SDGenBaseModule():
    def onto_to_sd():
        pass




class SDGenExampleModule(SDGenBaseModule):
    def onto_to_sd(self, path_to_onto):
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



        sd_generation_manager.start(100, "")
























