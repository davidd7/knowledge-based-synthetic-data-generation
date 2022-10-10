from flask import Blueprint, render_template, abort, current_app, g, jsonify, request, flash
from . import util


# Create Blueprint
modules_bp = Blueprint('modules_bp', __name__, template_folder='templates')


# ROUTES


@modules_bp.route('/', methods=['GET'])
def list_modules():
    folders = util.get_datascientist_modules_files()
    
    result = []    
    for folder in folders:
        result.append({
            "name" : folder.name
        })

    return jsonify(result)



