import blenderproc as bproc # this import is required even if its not used in this file
import importlib
import pathlib
import sys
# ABSOLUTE_PATH_TO_PACKAGE = "E:\\David (HDD)\\projects\\MATSE-bachelorarbeit-ss22-tests\\_11_overall_prototype01"
# # ABSOLUTE_PATH_TO_PACKAGE = "C:\\Users\\david\\Git Repositories\\MATSE-bachelorarbeit-ss22-tests\\_11_overall_prototype01"
# MODE = "bp_debug" # options: "normal", "bp_run", "bp_debug"
# if MODE == "bp_run":
#     new_sys_path = pathlib.Path(__file__).parent
#     sys.path.append(str(new_sys_path)) # works only with str()!
# elif MODE == "bp_debug":
#     sys.path.append(ABSOLUTE_PATH_TO_PACKAGE) # Das ist doch nötig, wenn man blenderproc mit debug-Argument aufruft



def get_path_to_package():
    """
    Returns path object containing the path that should lead to the root of this package
    """
    if MODE == "":
        return pathlib.Path(__file__).parent.resolve()
    elif MODE == "bp_run" or MODE == "bp_debug":
        return pathlib.Path(ABSOLUTE_PATH_TO_PACKAGE) / "unnamed_sd_package"


# import unnamed_sd_package.addons.modules.example



def generate_data():
    # Get path to ontology
    path_to_ontology = get_path_to_package() / "data/ontologies/"
    # path_to_ontology = path_to_ontology / "sdgen_ontology_t6_ba_6_fullwidth.owl"
    path_to_ontology = path_to_ontology / "debug01.owl"
    path_to_ontology = f"file://{path_to_ontology}"

    # Get path to where the generated data set should be saved
    path_where_to_save_result = get_path_to_package() / "data/generated_training_data/"
    path_where_to_save_result = path_where_to_save_result / "debug01/"

    # Start the (example) module for data generation
    unnamed_sd_package.addons.modules.example.SDGenExampleModule.onto_to_sd(path_to_ontology, path_where_to_save_result)



    

if __name__ == "__main__":
    print("start")

    print(sys.argv)

    path_to_package = sys.argv[1]
    job_id = sys.argv[2]
    # generate_data() # <- uncomment to see data generation test


    # Import my_package
    sys.path.append(path_to_package)
    
    import util
    from datascientist_addons.generation_components import onto_to_sd
    from datascientist_addons.generation_components import *















    # Get path to ontology
    path_to_ontology = pathlib.Path(path_to_package) / "generated_datasets" / str(job_id) / "individuals.owl"
    path_to_ontology = f"file://{path_to_ontology}"



    path_to_onto_classes = pathlib.Path(path_to_package) / "ontology_classes" / "main.owl"
    path_to_onto_classes = f"file://{path_to_onto_classes}"



    onto_to_sd( path_to_ontology, pathlib.Path(path_to_package) / "generated_datasets" / str(job_id) , path_to_onto_classes )




    # path = pathlib.Path(path_to_package) / "bp_executor.py"
    # spec = importlib.util.spec_from_file_location("xyz", path)
    # module = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(module)


    print("end")






