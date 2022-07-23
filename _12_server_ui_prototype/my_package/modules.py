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
                "name" : "Einfaches Modul"
            }
        ]




        # db = get_db()
        # schemes = db.execute(
        #     'SELECT * FROM generation_schemes ORDER BY id DESC', ()
        # ).fetchall()

        # list = []
        # for row in schemes:
        #     list.append( {
        #             "id" : row["id"],
        #             "name" : row["name"],
        #             "module_name" : row["module_name"]
        #         } )

        return jsonify(fake_result)












