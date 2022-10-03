import importlib
import os
import pathlib
import subprocess
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
        "scheme_name" : row["scheme_name"],
        "module_name" : row["module_name"]
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
    # Read form data and check for problems
    generation_scheme_id = request.form['generation_scheme_id']
    error = None
    if not generation_scheme_id:
        error = 'generation_scheme_id is required.'
    if error is not None:
        return "error"

    # Connect to DB and insert new job
    db = get_db()
    cursor = db.cursor()
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

    # Query the just created job out of the DB
    new_id = cursor.lastrowid
    new_job_row = db.execute(
        'SELECT j.id as id, j.scheme_id, j.creation_date, j.state, s.module_name, s.name as scheme_name FROM generation_jobs j JOIN generation_schemes s on j.scheme_id = s.id WHERE j.id = ?',
        (new_id,)
    ).fetchall()[0]
    new_job_dict = row_to_dict(new_job_row)


    module_name = new_job_dict["module_name"]
    if not is_data_scientist_module(new_job_dict["module_name"]):
        return "error"
    job_id = new_job_dict["id"]

    path = pathlib.Path(os.path.dirname(os.path.realpath(__file__))) / "data_scientist_modules" / module_name / "__init__.py"

    spec = importlib.util.spec_from_file_location(new_job_dict["module_name"], path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


    loaded_class = getattr(module, "SDGenModule")
    loaded_class.json_to_onto("", "", "")

    print(loaded_class)

    return

    print("SDGen: Starting blenderproc")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path) 
    # os.system("blenderproc run bproc_area/__main__.py")
    # subprocess.run(["blenderproc", "debug", "bproc_area/__main__.py"], cwd=dir_path)
    pid = subprocess.Popen(["blenderproc", "debug", "bproc_area/__main__.py"], cwd=dir_path).pid
    print("SDGen: Finished with starting blenderproc")

    return jsonify( row_to_dict(new_job_row) )




def start_json_to_onto():
    # Define necessary paths
    path_to_ontology_input = f'{ get_path_to_package() / "data/ontologies/" / "sdgen_ontology_2_classes.owl" }'
    path_to_ontology_output = f'{ get_path_to_package() / "data/ontologies/" / "sdgen_ontology_2_individuals.owl" }'

    # Start json_to_onto
    sys_create_new_generation_scheme(path_to_ontology_input, path_to_ontology_output) # need also to specify which module is meant one day (e.g. unnamed_sd_package.addons.modules.example.SDGenExampleModule)




def sys_create_new_generation_scheme(path_to_ontology_classes, path_to_ontology_individuals):
    # Load settings (later global?)
    settings = """ { "next_id" : 1 } """
    parsed_settings = json.loads(settings)

    # Get ontologies
    onto_classes, onto_individuals = FutureUtilities.load_classes_and_individuals(path_to_ontology_classes, path_to_ontology_individuals)

    # Get new ontology name
    old_scheme_names = [ individual.name for individual in onto_individuals.search(type=onto_classes.GenerationScheme) ]
    new_id = parsed_settings["next_id"]
    while (new_name := f"EGS{new_id:03}") in old_scheme_names: # resulting name is saved in new_name
        new_id += 1

    # Create new nodes in the ontology
    SDGenModule.json_to_onto(onto_classes, onto_individuals, new_name)

    onto_individuals.save(file=path_to_ontology_individuals)
        
    
































