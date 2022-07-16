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
path = path / "data/ontologies/"

path = path / "sdgen_ontology_1.owl"
path = f"file://{path}"
print(path)
# test = sdgen_base.SimpleSDGenerationManager(path)

# test.start(100, "")

test = addons.modules.example.SDGenExampleModule()
test.onto_to_sd(path)







