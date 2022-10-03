import os
import pathlib
from unicodedata import name
from flask import Blueprint, render_template, abort, current_app, g, jsonify, request, flash
from flask.cli import with_appcontext
import click
import json
import sqlite3
from my_package.db import get_db
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












