import blenderproc as bproc # this import is required even if its not used in this file
import importlib
import pathlib
import sys



if __name__ == "__main__":
    print("Separate process for blenderproc started")

    # Save arguments into variables
    print(sys.argv)
    path_to_package = sys.argv[1]
    job_id = sys.argv[2]

    # Import relevant python modules in my_package
    sys.path.append(path_to_package)
    import util
    from custom_code.generation_components import onto_to_sd
    from custom_code.generation_components import *

    # Get path to ontology
    path_to_ontology = pathlib.Path(path_to_package) / "generated_datasets" / str(job_id) / "individuals.owl"
    path_to_ontology = f"file://{path_to_ontology}"

    path_to_onto_classes = pathlib.Path(path_to_package) / "ontology_classes" / "main.owl"
    path_to_onto_classes = f"file://{path_to_onto_classes}"

    onto_to_sd( path_to_ontology, pathlib.Path(path_to_package) / "generated_datasets" / str(job_id) , path_to_onto_classes )

    print("Separate process for blenderproc finished")






