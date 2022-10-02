import os
import pathlib
from unicodedata import name
from flask import Blueprint, render_template, abort, current_app, g, jsonify, request, flash
from flask.cli import with_appcontext
import click
import json
import sqlite3
from my_package.db import get_db


# Create Blueprint
modules_bp = Blueprint('modules_bp', __name__, template_folder='templates')



# ROUTES


@modules_bp.route('/', methods=['GET'])
def list_modules():
    folders = [ f for f in os.scandir(path=pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / "data_scientist_modules" ) if f.is_dir() ]

    result = []    
    for folder in folders:
        result.append({
            "name" : folder.name
        })

    return jsonify(result)












