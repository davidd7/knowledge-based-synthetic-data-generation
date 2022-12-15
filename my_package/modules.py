from flask import Blueprint, render_template, abort, current_app, g, jsonify, request, flash
from . import util
import pathlib


# Create Blueprint
modules_bp = Blueprint('modules_bp', __name__, template_folder='templates')


# ROUTES


@modules_bp.route('/', methods=['GET'])
def list_modules():
    folders = util.get_datascientist_modules_files()
    
    result = []    
    for folder in folders:

        path_to_default = pathlib.Path(folder.path) / "defaultdata_mlsystem.json"
        default_value = "{\n     \n}"
        if path_to_default.is_file():
            default_value = path_to_default.read_text()


        result.append({
            "name" : folder.name,
            "default_value" : default_value
        })

    return jsonify(result)


@modules_bp.route('/<string:module_name>', methods=['GET'])
def single_module(module_name):
    folders = util.get_datascientist_modules_files()
    
    result = []    
    for folder in folders:

        if folder.name != module_name:
            continue

        path_to_default = pathlib.Path(folder.path) / "defaultdata_mlsystem.json"
        default_value = "{\n     \n}"
        if path_to_default.is_file():
            default_value = path_to_default.read_text()


        result = {
            "name" : folder.name,
            "default_value" : default_value
        }

        return jsonify(result)

    return "error"





