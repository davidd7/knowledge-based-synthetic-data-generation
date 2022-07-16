

import pathlib


from addons.components.sd_generation import sdgen_base



# if __name__ == "__main__":
#     print("lol")


path = pathlib.Path(__file__).parent.resolve() / "data/ontologies/" # "C:/Users/david/Git Repositories/MATSE-bachelorarbeit-ss22-tests/_11_overall_prototype01/data/ontologies/sdgen_ontology_1.owl"
path = path / "sdgen_ontology_1.owl"
path = f"file://{path}"
print(path)
test = sdgen_base.SimpleSDGenerationManager(path)

#test.start()

print (pathlib.Path(__file__).parent.resolve()) # -> E:\...\MATSE-bachelorarbeit-ss22-tests\_11_overall_prototype01 # --> das ist, was wollen
print(pathlib.Path().resolve()) # -> E:\...\MATSE-bachelorarbeit-ss22-tests







