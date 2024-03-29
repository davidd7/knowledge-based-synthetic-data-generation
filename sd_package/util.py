import os
import pathlib


def get_data_scientist_module_filenames():
    return [ f.name for f in os.scandir(path=pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / "custom_code" / "modules" ) if f.is_dir() ]



def get_datascientist_modules_files():
    return [ f for f in os.scandir(path=pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / "custom_code" / "modules" ) if f.is_dir() ]



def get_datascientist_formcomponents_files():
    return [ f for f in os.scandir(path=pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / "custom_code" / "form_components" ) ]



def get_path_to_package():
    return pathlib.Path(os.path.dirname(os.path.realpath(__file__)))

