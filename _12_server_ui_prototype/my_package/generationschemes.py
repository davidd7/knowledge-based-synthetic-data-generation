from unicodedata import name
from flask import Blueprint, render_template, abort, current_app, g, jsonify, request, flash
from flask.cli import with_appcontext
import click
import json

import sqlite3


from my_package.db import get_db















simple_page = Blueprint('simple_page', __name__, template_folder='templates')


@simple_page.route('/', methods=['GET', 'POST'])
def list_schemes():

    if request.method == 'GET':
        db = get_db()
        schemes = db.execute(
            'SELECT * FROM generation_schemes ORDER BY id DESC', ()
        ).fetchall()

        list = []
        for row in schemes:
            list.append( {
                    "id" : row["id"],
                    "name" : row["name"],
                    "module_name" : row["module_name"]
                } )

        return jsonify(list)

    if request.method == 'POST':
        name = request.form['name'] # <- Das wift einen error, wenn name nicht gesendet wurde. Ich kapiere nicht, warum wir dann unten prüfen, ob es leer gelassen wurde wnen in dem Fall eh alles mit nem Error abstürzt....
        module_name = request.form['module_name']
        db = get_db()
        cursor=db.cursor()
        error = None

        if not name:
            error = 'name is required.'
        elif not module_name:
            error = 'module_name is required.'

        if error is None:

            try:
                cursor.execute(
                    "INSERT INTO generation_schemes (name, module_name, data) VALUES (?, ?, '')",
                    (name, module_name),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {name} is already registered."
            else:
                print(cursor.lastrowid)

                return jsonify( {
                    "id" : cursor.lastrowid,
                    "name" : name,
                    "module_name" : module_name
                } )

        return "error"
        #return flash(error)







