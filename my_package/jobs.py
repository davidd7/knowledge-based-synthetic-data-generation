import importlib
import os
import subprocess
from unicodedata import name
from flask import Blueprint, render_template, abort, current_app, g, jsonify, request, flash
from my_package.db import get_db
from owlready2 import *
from . import util
import json


# Create Blueprint
jobs_bp = Blueprint('jobs_bp', __name__, template_folder='templates')


# Helper functions
def row_to_dict(row):
    res = {}
    for key in row.keys():
        res[key] = row[key]
    return res


# ROUTES


@jobs_bp.route('/', methods=['GET'])
def list_jobs():
    db = get_db()
    jobs = db.execute(
        'SELECT j.id as id, j.knowledge_base_id, j.creation_date, j.state as status, s.name as scheme_name, s.module_name FROM generation_jobs j JOIN generation_schemes s on j.knowledge_base_id = s.id ORDER BY j.id DESC', ()
    ).fetchall()

    list = []
    for row in jobs:
        list.append( row_to_dict(row) )
    return jsonify(list)


@jobs_bp.route('/', methods=['POST'])
def create_job():
    # Read form data and check for problems
    knowledge_base_id = request.form['knowledge_base_id']
    params = request.form['params']
    error = None
    if not knowledge_base_id:
        error = 'knowledge_base_id is required.'
    if not params:
        error = 'params is required.'
    if error is not None:
        return "error"

    # Connect to DB and insert new job
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO generation_jobs (knowledge_base_id, state, params) VALUES (?, 'active', ?)",
            (knowledge_base_id, params),
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
        'SELECT j.id as id, j.knowledge_base_id, j.creation_date, j.state, j.params, s.module_name, s.name as scheme_name, s.data as json_data FROM generation_jobs j JOIN generation_schemes s on j.knowledge_base_id = s.id WHERE j.id = ?',
        (new_id,)
    ).fetchall()[0]
    new_job_dict = row_to_dict(new_job_row)

    loaded_class = load_data_scientist_module_by_name(new_job_dict["module_name"])

    print("SOOOOOOOOO: ")
    print(params)
    # return
    start_json_to_onto(loaded_class, new_job_dict["id"], new_job_dict["json_data"], params)
    start_onto_to_sd(new_job_dict["id"])

    return jsonify( row_to_dict(new_job_row) )






def load_data_scientist_module_by_name(module_name):
    # Check that parameter really references a module
    if not module_name in util.get_data_scientist_module_filenames():
        return "error"

    # Import the module
    path = util.get_path_to_package() / "custom_code" / "modules" / module_name / "__init__.py"
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Return the class in the loaded module
    return getattr(module, "SDGenModule")




def start_json_to_onto(loaded_class, job_id, json_data, ml_system_params):
    # 1. Create directory
    job_path = util.get_path_to_package() / "generated_datasets" / str(job_id)
    job_path.mkdir(parents=True, exist_ok=True)

    # Define necessary paths
    path_to_ontology_classes = f'{ util.get_path_to_package() / "ontology_classes" / "main.owl" }'
    path_to_ontology_individuals = f'{ job_path / "individuals.owl" }'

    # Get ontologies
    onto_classes, onto_individuals = load_classes_and_individuals(path_to_ontology_classes, path_to_ontology_individuals)

    # Create new nodes in the ontology
    with onto_individuals:
        parsed_data = json.loads(json_data)
        parsed_ml_system_params = json.loads(ml_system_params)
        print("WOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        print(ml_system_params)
        print(parsed_ml_system_params)
        # Start json_to_onto:
        loaded_class.json_to_onto(onto_classes, parsed_data, parsed_ml_system_params)

    onto_individuals.save(file=path_to_ontology_individuals)



def start_onto_to_sd(job_id):
    print("SDGen: Starting blenderproc")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(dir_path) 
    pid = subprocess.Popen(["blenderproc", "run", "bproc_area/__main__.py", util.get_path_to_package(), str(job_id)], cwd=dir_path).pid
    print("SDGen: Finished with starting blenderproc")
        
    


















# def load_classes_and_individuals(path_to_ontology_classes, path_to_ontology_individuals):
#     #w = World()
#     onto_classes = get_ontology("file://" + path_to_ontology_classes).load() # w.
#     # onto_individuals = get_ontology("http://test.org/onto.owl") # "file://" + path_to_ontology_individuals).load() # w.
#     # onto_individuals = get_ontology("http://www.semanticweb.org/david/ontologies/2022/6/synthetic-data-generation/onto.owl") # "file://" + path_to_ontology_individuals).load() # w.
#     onto_individuals = get_ontology("http://www.semanticweb.org/david/ontologies/2022/6/synthetic-data-generation-individuals") #.load() # "file://" + path_to_ontology_individuals).load() # w.
#     onto_individuals.imported_ontologies.append(onto_classes)
#     #onto_individuals = onto_individuals.load()
#     return onto_classes, onto_individuals


def load_classes_and_individuals(path_to_ontology_classes, path_to_ontology_individuals):
    w = World()
    onto_classes = w.get_ontology("file://" + path_to_ontology_classes).load() # w.
    # onto_individuals = get_ontology("http://test.org/onto.owl") # "file://" + path_to_ontology_individuals).load() # w.
    # onto_individuals = get_ontology("http://www.semanticweb.org/david/ontologies/2022/6/synthetic-data-generation/onto.owl") # "file://" + path_to_ontology_individuals).load() # w.
    onto_individuals = w.get_ontology("http://www.semanticweb.org/david/ontologies/2022/6/synthetic-data-generation-individuals") #.load() # "file://" + path_to_ontology_individuals).load() # w.
    onto_individuals.imported_ontologies.append(onto_classes)
    #onto_individuals = onto_individuals.load()
    return onto_classes, onto_individuals












