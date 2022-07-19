import blenderproc as bproc
import pathlib
import sys
ABSOLUTE_PATH_TO_PACKAGE = "E:\\David (HDD)\\projects\\MATSE-bachelorarbeit-ss22-tests\\_11_overall_prototype01"
MODE = "bp_debug" # options: "normal", "bp_run", "bp_debug"
if MODE == "bp_run":
    new_sys_path = pathlib.Path(__file__).parent
    sys.path.append(str(new_sys_path)) # works only with str()!
elif MODE == "bp_debug":
    sys.path.append(ABSOLUTE_PATH_TO_PACKAGE) # Das ist doch nötig, wenn man blenderproc mit debug-Argument aufruft



def get_path_to_package():
    """
    Returns path object containing the path that should lead to the root of this package
    """
    if MODE == "":
        return pathlib.Path(__file__).parent.resolve()
    elif MODE == "bp_run" or MODE == "bp_debug":
        return pathlib.Path(ABSOLUTE_PATH_TO_PACKAGE) / "unnamed_sd_package"


import unnamed_sd_package.addons.modules.example



def generate_data():
    # Get path to ontology
    path_to_ontology = get_path_to_package() / "data/ontologies/"
    path_to_ontology = path_to_ontology / "sdgen_ontology_1.owl"
    path_to_ontology = f"file://{path_to_ontology}"

    # Get path to where the generated data set should be saved
    path_where_to_save_result = get_path_to_package() / "data/generated_training_data/"
    path_where_to_save_result = path_where_to_save_result / "1/"

    # Start the (example) module for data generation
    #example_module = unnamed_sd_package.addons.modules.example.SDGenExampleModule()
    #example_module.onto_to_sd(path_to_ontology, path_where_to_save_result)
    unnamed_sd_package.addons.modules.example.SDGenExampleModule.onto_to_sd(path_to_ontology, path_where_to_save_result)


def start_json_to_onto():
    # Get path to ontology
    path_to_ontology_input = f'file://{ get_path_to_package() / "data/ontologies/" / "sdgen_ontology_2_classes.owl" }'
    path_to_ontology_output = f'file://{ get_path_to_package() / "data/ontologies/" / "sdgen_ontology_2_individuals.owl" }'
    #unnamed_sd_package.addons.modules.example.SDGenExampleModule.json_to_onto(path_to_ontology_input, path_to_ontology_output)
    unnamed_sd_package.addons.modules.example.FutureUtilities.sys_create_new_generation_scheme(path_to_ontology_input, path_to_ontology_output)


if __name__ == "__main__":
    print("start")

    start_json_to_onto()

    print("end")






