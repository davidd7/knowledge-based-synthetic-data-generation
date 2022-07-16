import blenderproc as bproc

import pathlib

import sys

path = pathlib.Path(__file__).parent
sys.path.append(str(path)) # works only with str()!
# print("### In current sys.path ###")
# for el in sys.path:
#     print(el)
# print("### ### ### ### ### ### ###")


from addons.components.sd_generation import sdgen_base
import addons.modules.example


# if __name__ == "__main__":
#     print("lol")





path = pathlib.Path(__file__).parent.resolve() / "data/ontologies/" # "C:/Users/david/Git Repositories/MATSE-bachelorarbeit-ss22-tests/_11_overall_prototype01/data/ontologies/sdgen_ontology_1.owl"
path = path / "sdgen_ontology_1.owl"
path = f"file://{path}"
print(path)
# test = sdgen_base.SimpleSDGenerationManager(path)

# test.start(100, "")

test = addons.modules.example.SDGenExampleModule()
test.onto_to_sd(path)


# print(pathlib.Path(__file__).parent.resolve()) # -> E:\...\MATSE-bachelorarbeit-ss22-tests\_11_overall_prototype01 # --> das ist, was wollen
# print(pathlib.Path().resolve()) # -> E:\...\MATSE-bachelorarbeit-ss22-tests







