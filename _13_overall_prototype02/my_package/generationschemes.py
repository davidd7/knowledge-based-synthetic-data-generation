from unicodedata import name
from flask import Blueprint, render_template, abort, current_app, g, jsonify, request, flash
from flask.cli import with_appcontext
import click
import json
import sqlite3
from my_package.db import get_db


# Initialize Blueprint
generationschemes_bp = Blueprint('simple_page', __name__, template_folder='templates')



# ROUTES


@generationschemes_bp.route('/', methods=['GET'])
def list_schemes():
    # Query all schemes from DB
    db = get_db()
    schemes = db.execute(
        'SELECT * FROM generation_schemes ORDER BY id DESC', ()
    ).fetchall()

    # Save results in JSON
    list = []
    for row in schemes:
        list.append( {
                "id" : row["id"],
                "name" : row["name"],
                "module_name" : row["module_name"]
            } )

    # Return result
    return jsonify(list)



@generationschemes_bp.route('/', methods=['POST'])
def create_scheme():
    # Check that the right parameters were sent
    name = request.form['name'] # <- Das wift einen error, wenn name nicht gesendet wurde. Ich kapiere nicht, warum wir dann unten prüfen, ob es leer gelassen wurde wnen in dem Fall eh alles mit nem Error abstürzt....
    module_name = request.form['module_name']
    error = None
    if not name:
        error = 'name is required.'
    elif not module_name:
        error = 'module_name is required.'
    if error is not None:
        return "error"

    # Connect to DB
    db = get_db()
    cursor = db.cursor()

    # 
    try:
        cursor.execute(
            "INSERT INTO generation_schemes (name, module_name, data) VALUES (?, ?, '{}')",
            (name, module_name),
        )
        db.commit()
    except db.IntegrityError:
        error = f"User {name} is already registered."
        return "error"
    else:
        return jsonify( {
            "id" : cursor.lastrowid,
            "name" : name,
            "module_name" : module_name
        } )







@generationschemes_bp.route('/<int:scheme_id>', methods=['GET', 'PUT'])
def single_scheme(scheme_id):

    if request.method == 'PUT':
        data = request.get_data(as_text=True)
        db = get_db()
        cursor = db.cursor()
        error = None

        if error is None:
            try:
                cursor.execute(
                    "UPDATE generation_schemes SET data = ? WHERE id = ?",
                    (data, scheme_id),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {name} is already registered."
                return "error"
            else:
                pass

    if request.method == 'GET' or request.method == 'PUT':
        db = get_db()
        row = db.execute(
            'SELECT * FROM generation_schemes WHERE id = ?', (scheme_id,)
        ).fetchone()

        res =  {
            "id" : row["id"],
            "name" : row["name"],
            "module_name" : row["module_name"],
            "data" : row["data"]
        }

        return jsonify(res)



