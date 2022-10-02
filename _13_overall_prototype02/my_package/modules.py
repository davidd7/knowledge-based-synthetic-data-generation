from unicodedata import name
from flask import Blueprint, render_template, abort, current_app, g, jsonify, request, flash
from flask.cli import with_appcontext
import click
import json

import sqlite3


from my_package.db import get_db















modules_bp = Blueprint('modules_bp', __name__, template_folder='templates')


@modules_bp.route('/', methods=['GET'])
def list_schemes():

    if request.method == 'GET':
        fake_result = [ # TODO: Später ersetzen durch Code, der in Verzeichnis Module sucht
            {
                "name" : "EinfachesModul"
            }
        ]

        return jsonify(fake_result)












