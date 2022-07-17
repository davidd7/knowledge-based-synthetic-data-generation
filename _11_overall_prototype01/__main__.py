import blenderproc as bproc

import pathlib

import sys

state = "blender_run"
state = "blender_debug"

if state == "blender_run":
    path = pathlib.Path(__file__).parent
    sys.path.append(str(path)) # works only with str()!
elif state == "blender_debug":
    sys.path.append("E:\David (HDD)\projects\MATSE-bachelorarbeit-ss22-tests\_11_overall_prototype01") # Das ist doch nötig, wenn man blenderproc mit debug-Argument aufruft

# print("### In current sys.path ###")
# for el in sys.path:
#     print(el)
# print("### ### ### ### ### ### ###")


from addons.components.sd_generation import sdgen_base
import addons.modules.example

path = pathlib.Path(__file__).parent.resolve() # "C:/Users/david/Git Repositories/MATSE-bachelorarbeit-ss22-tests/_11_overall_prototype01/data/ontologies/sdgen_ontology_1.owl"
if state == "blender_debug":
    path = pathlib.Path("E:\David (HDD)\projects\MATSE-bachelorarbeit-ss22-tests\_11_overall_prototype01")


path_onto = path / "data/ontologies/"
path_onto = path_onto / "sdgen_ontology_1.owl"
path_onto = f"file://{path_onto}"
print(path_onto)


path_save = path / "data/generated_training_data/"
path_save = path_save / "1/"
#path_save = f"file://{path_onto}"
print(path_save)

test = addons.modules.example.SDGenExampleModule()
test.onto_to_sd(path_onto, path_save)







