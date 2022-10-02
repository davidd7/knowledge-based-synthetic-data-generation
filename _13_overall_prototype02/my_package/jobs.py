import os
from unicodedata import name
from flask import Blueprint, render_template, abort, current_app, g, jsonify, request, flash
from flask.cli import with_appcontext
import click
import json
import sqlite3
from my_package.db import get_db


# Create Blueprint
jobs_bp = Blueprint('jobs_bp', __name__, template_folder='templates')



# Helper functions
def row_to_dict(row):
    return {
        "id" : row["id"],
        "scheme_id" : row["scheme_id"],
        "creation_date" : row["creation_date"],
        "status" : row["state"],
        "scheme_name" : row["scheme_name"]
    }



# ROUTES


@jobs_bp.route('/', methods=['GET'])
def list_jobs():
    db = get_db()
    jobs = db.execute(
        'SELECT j.id as id, j.scheme_id, j.creation_date, j.state, s.name as scheme_name, s.module_name FROM generation_jobs j JOIN generation_schemes s on j.scheme_id = s.id ORDER BY j.id DESC', ()
    ).fetchall()

    list = []
    for row in jobs:
        list.append( row_to_dict(row) )
    return jsonify(list)



@jobs_bp.route('/', methods=['POST'])
def create_job():
    generation_scheme_id = request.form['generation_scheme_id']
    db = get_db()
    cursor = db.cursor()
    error = None
    if not generation_scheme_id:
        error = 'generation_scheme_id is required.'

    if error is not None:
        return "error"

    try:
        cursor.execute(
            "INSERT INTO generation_jobs (scheme_id, state) VALUES (?, 'active')",
            (generation_scheme_id,),
        )
        db.commit()
    except db.IntegrityError:
        error = f"User {name} is already registered."
        return "error"
    except:
        return "error"


    new_id = cursor.lastrowid
    new_job_row = db.execute(
        'SELECT j.id as id, j.scheme_id, j.creation_date, j.state, s.name as scheme_name, s.module_name FROM generation_jobs j JOIN generation_schemes s on j.scheme_id = s.id WHERE j.id = ?', (new_id,)
    ).fetchall()[0]


    print("SDGen: Starting blenderproc")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path) 
    # os.system("blenderproc run bproc_area/__main__.py")
    subprocess.run(["blenderproc", "run", "bproc_area/__main__.py"], cwd=dir_path)
    print("SDGen: Finished with starting blenderproc")

    return jsonify( row_to_dict(new_job_row) )









































