
from re import M
from socket import has_dualstack_ipv6
from xml.dom.expatbuilder import parseFragmentString
# from unnamed_sd_package.addons.components.sd_generation import sdgen_base
import json
from owlready2 import *
import itertools
# from rdflib import *
# import sdgen_base
from datascientist_addons.generation_components import sdgen_base







class SDGenBaseModule():
    def onto_to_sd(path_to_onto, path_where_to_save_result):
        pass



def onto_to_sd(path_to_onto, path_where_to_save_result, path_to_onto_classes):
    sd_generation_manager = sdgen_base.SimpleSDGenerationManager(path_to_onto, "EGS1", path_to_onto_classes)

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
        sdgen_base.SimpleLightHandler()
    )

    sd_generation_manager.add(
        sdgen_base.SimpleRandomGroundHandler()
    )

    sd_generation_manager.add(
        sdgen_base.SimpleBoxedPhysicalPlausibilityHandler(),
        at_end_of_iteration=True
    )

    sd_generation_manager.add(
        sdgen_base.RealImageRenderingHandler(path_where_to_save_result),
        at_end_of_iteration=True
    )

    sd_generation_manager.add(
        sdgen_base.SimpleSegmentationLabelHandler(path_where_to_save_result),
        at_end_of_iteration=True
    )

    sd_generation_manager.start()




