from unicodedata import name
from flask import Blueprint, render_template, abort, current_app, g, jsonify, request, flash
from flask.cli import with_appcontext
import click
import json
import sqlite3
from my_package.db import get_db



jobs_bp = Blueprint('jobs_bp', __name__, template_folder='templates')

@jobs_bp.route('/', methods=['GET', 'POST'])
def list_jobs():

    if request.method == 'GET':
        db = get_db()
        jobs = db.execute(
            'SELECT j.id as id, j.scheme_id, j.creation_date, j.state, s.name as scheme_name, s.module_name FROM generation_jobs j JOIN generation_schemes s on j.scheme_id = s.id ORDER BY j.id DESC', ()
        ).fetchall()

        list = []
        for row in jobs:
            list.append( row_to_dict(row) )
        return jsonify(list)

    if request.method == 'POST':
        generation_scheme_id = request.form['generation_scheme_id']
        db = get_db()
        cursor = db.cursor()
        error = None
        if not generation_scheme_id:
            error = 'generation_scheme_id is required.'

        if error is None:
            try:
                cursor.execute(
                    "INSERT INTO generation_jobs (scheme_id, state) VALUES (?, 'active')",
                    (generation_scheme_id,),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {name} is already registered."
            else:
                new_id = cursor.lastrowid
                new_job_row = db.execute(
                    'SELECT j.id as id, j.scheme_id, j.creation_date, j.state, s.name as scheme_name, s.module_name FROM generation_jobs j JOIN generation_schemes s on j.scheme_id = s.id WHERE j.id = ?', (new_id,)
                ).fetchall()[0]
            return jsonify( row_to_dict(new_job_row) )

        return "error"






def row_to_dict(row):
    return {
        "id" : row["id"],
        "scheme_id" : row["scheme_id"],
        "creation_date" : row["creation_date"],
        "status" : row["state"],
        "scheme_name" : row["scheme_name"]
    }

































