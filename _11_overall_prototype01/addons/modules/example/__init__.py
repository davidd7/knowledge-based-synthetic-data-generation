
#import 
from addons.components.sd_generation import sdgen_base


class SDGenBaseModule():
    def onto_to_sd():
        pass




class SDGenExampleModule(SDGenBaseModule):
    def onto_to_sd(self, path_to_onto):
        test = sdgen_base.SimpleSDGenerationManager(path_to_onto)



        test.start(100, "")



















