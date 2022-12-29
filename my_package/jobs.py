import importlib
import os
import subprocess
from unicodedata import name
from flask import Blueprint, render_template, abort, current_app, g, jsonify, request, flash, send_file, Response
from my_package.db import get_db
from owlready2 import *
from . import util
import json
import time
from io import BytesIO
import zipfile
import os
import shutil
import my_package
import secrets
import string


active_processes = {}


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
        'SELECT j.id as id, j.knowledge_base_id, j.creation_date, j.state as status, s.name as scheme_name, s.module_name, j.statistics as statistics FROM generation_jobs j JOIN generation_schemes s on j.knowledge_base_id = s.id ORDER BY j.id DESC', ()
    ).fetchall()

    list = []
    for row in jobs:
        as_dict = row_to_dict(row)

        as_dict["status"] = determine_active_job_status(as_dict["id"], as_dict["status"])

        list.append( as_dict )
    return jsonify(list)






update_counter = 0

def event_stream():
    update_counter_old = update_counter
    i = 0
    try:
        while True:
            if update_counter != update_counter_old or i % 60 == 0: # Sending data at least all 60 seconds to check that client is still listening
                yield 'data: %s\n\n' % update_counter
                update_counter_old = update_counter
            print("Stream starts sleeping")
            time.sleep(1)
            i += 1
    finally:
        return
        pass





@jobs_bp.route('/updates-stream')
def stream():
    print("Stream called")
    return Response(event_stream(), mimetype="text/event-stream")





@jobs_bp.route('/<int:job_id>', methods=['GET', 'DELETE'])
def single_job(job_id):
    if request.method == 'GET':
        db = get_db()
        jobs = db.execute(
            'SELECT j.id as id, j.knowledge_base_id, j.creation_date, j.state as status, s.name as scheme_name, s.module_name, j.statistics as statistics FROM generation_jobs j JOIN generation_schemes s on j.knowledge_base_id = s.id WHERE j.id = ? ORDER BY j.id DESC', (job_id,)
        ).fetchall()

        list = []
        for row in jobs:
            as_dict = row_to_dict(row)
            as_dict["status"] = determine_active_job_status(as_dict["id"], as_dict["status"])
            list.append( as_dict )

        if len(list) != 1:
            # Error
            return "error"

        return jsonify(list[0])


    if request.method == 'DELETE':
        delete_job(job_id)
        return jsonify( {} )



def get_job(job_id):
    db = get_db()
    jobs = db.execute(
        'SELECT j.id as id, j.knowledge_base_id, j.creation_date, j.state as status, s.name as scheme_name, s.module_name, j.statistics as statistics FROM generation_jobs j JOIN generation_schemes s on j.knowledge_base_id = s.id WHERE j.id = ? ORDER BY j.id DESC', (job_id,)
    ).fetchall()

    list = []
    for row in jobs:
        as_dict = row_to_dict(row)
        as_dict["status"] = determine_active_job_status(as_dict["id"], as_dict["status"])
        list.append( as_dict )

    if len(list) != 1:
        return "error"
    
    return list[0]




@jobs_bp.route('/<int:job_id>/abort', methods=['POST'])
def abort_job(job_id):
    job = get_job(job_id)

    if job == "error":
        return "error"

    if job["status"] == "generating":
        active_processes[job["id"]].terminate()
        update_job_state(job_id, "aborting")

    return jsonify(job)



@jobs_bp.route('/<int:job_id>/finished', methods=['POST'])
def finish_job(job_id):
    # job = get_job(job_id)

    error = None
    if ("passcode" not in request.json) or ("statistics" not in request.json):
        error = 'passcode and statistics are required.'
    if error is not None:
        return "error"

    passcode = request.json['passcode']
    statistics = request.json['statistics']

    # Connect to DB
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "UPDATE generation_jobs SET state = 'finished', statistics = ? WHERE id = ? and passcode = ?",
            (str(statistics), job_id, passcode),
        )
        db.commit()
    except db.IntegrityError:
        error = f"error"
        return "error"
    else:
        pass

    global update_counter
    update_counter += 1
    return jsonify({}) # TODO








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
    alphabet = string.ascii_letters + string.digits
    passcode = ''.join(secrets.choice(alphabet) for i in range(20))  

    # Connect to DB and insert new job
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO generation_jobs (knowledge_base_id, state, params, passcode, statistics) VALUES (?, 'generating', ?, ?, '')",
            (knowledge_base_id, params, passcode),
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

    start_json_to_onto(loaded_class, new_job_dict["id"], new_job_dict["json_data"], params)

    print("ADDRESS: :::::::::::::::")
    print(request.headers.get('Host'))


    start_onto_to_sd(new_job_dict["id"], passcode)

    return jsonify( row_to_dict(new_job_row) )






@jobs_bp.route('/<int:job_id>/result', methods=['GET'])
def download_result(job_id):
    # Check that job exists and is finished
    job = get_job(job_id)
    if job == "error" or job["status"] != "finished":
        return "error"

    # Create zip file
    memory_file = BytesIO() # create file only in memory
    path_to_dataset = util.get_path_to_package() / "data" / "generated_datasets" / str(job_id)
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk over all subfolders of dataset folder
        for root, dirs, files in os.walk(path_to_dataset):
            relative_path = os.path.relpath(root, path_to_dataset) # Extract relative path from dataset folder so that same relative path from root is used in zip
            for file in files:
                zipf.write(os.path.join(root, file), arcname = os.path.join(relative_path, file))
    memory_file.seek(0)

    # Send zip file
    return send_file(memory_file,
                     download_name="result_" + str(job_id) + ".zip",
                     as_attachment=True)








def delete_job(job_id):
    # Check that job exists and is finished/unknown/... (only non-active jobs should be deleted)
    job = get_job(job_id)
    if job == "error" or job["status"] not in ["finished", "aborted", "unknown"]:
        return "error"

    # Path to folder that should be deleted
    path_to_dataset = util.get_path_to_package() / "data" / "generated_datasets" / str(job_id)

    # Delete from file system
    print("Try deleting " + str(path_to_dataset))
    try:
        shutil.rmtree(path_to_dataset)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        return

    # Delete from database
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "DELETE FROM generation_jobs WHERE id = ?",
            (job_id,),
        )
        db.commit()
    except:
        print("ERROR when writing in DB")
        # print(e)
    # Need to close cursor in sqlite3?








def determine_active_job_status(job_id, stated_status):
    new_status = stated_status

    if not stated_status in ["generating", "aborting"]:
        return stated_status

    if stated_status == "generating":
        if not job_id in active_processes:
            new_status = "unknown"
        else:
            process_state = active_processes[job_id].poll()
            if (process_state is not None) and process_state == 0:
                new_status = "finished"
            if (process_state is not None) and process_state != 0:
                new_status = "error"

    if stated_status == "aborting":
        if job_id not in active_processes:
            new_status = "unknown"
        else:
            process_state = active_processes[job_id].poll()
            if not (process_state is None): # Windows puts process directly to terminated state (no longer None), even if it actually keeps running
                print("aborted with code " + str(process_state))
                new_status = "aborted (" + str(process_state) + ")"

    if new_status != stated_status:
        update_job_state(job_id, new_status)

    return new_status





def update_job_state(job_id, new_state):
    if new_state not in ["generating", "aborting", "finished", "unknown", "error", "aborted"]:
        print("WATCH OUT: unknown new_state was saved for a job")
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            "UPDATE generation_jobs SET state = ? WHERE id = ?",
            (new_state, job_id),
        )
        db.commit()
    except e:
        print("ERROR when writing in DB")
        print(e)
    # Need to close cursor in sqlite3?




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
    job_path = util.get_path_to_package() / "data" / "generated_datasets" / str(job_id)
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

        # Start json_to_onto:
        loaded_class.json_to_onto(onto_classes, parsed_data, parsed_ml_system_params)

    onto_individuals.save(file=path_to_ontology_individuals)



def start_onto_to_sd(job_id, passcode):
    print("SDGen: Starting blenderproc")
    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(request.headers.get('Host')) 
    print(request.headers.get('host_url')) 
    print(request.headers.get('scheme')) 
    print(request.host_url) 
    # pid = subprocess.Popen(["blenderproc", "run", "bproc_area/__main__.py", util.get_path_to_package(), str(job_id)], cwd=dir_path).pid
    process = None
    if not my_package.get_settings_debug_mode():
        process = subprocess.Popen(["blenderproc", "run", "bproc_area/__main__.py", util.get_path_to_package(), str(job_id), str(passcode), request.host_url], cwd=dir_path)
    else:
        process = subprocess.Popen(["blenderproc", "debug", "bproc_area/__main__.py", util.get_path_to_package(), str(job_id), str(passcode), request.host_url], cwd=dir_path)
    active_processes[job_id] = process
    print("SDGen: Finished with starting blenderproc")
        
    




















def load_classes_and_individuals(path_to_ontology_classes, path_to_ontology_individuals):
    w = World()
    onto_classes = w.get_ontology("file://" + path_to_ontology_classes).load() # w.
    # onto_individuals = get_ontology("http://test.org/onto.owl") # "file://" + path_to_ontology_individuals).load() # w.
    # onto_individuals = get_ontology("http://www.semanticweb.org/david/ontologies/2022/6/synthetic-data-generation/onto.owl") # "file://" + path_to_ontology_individuals).load() # w.
    onto_individuals = w.get_ontology("http://www.semanticweb.org/david/ontologies/2022/6/synthetic-data-generation-individuals") #.load() # "file://" + path_to_ontology_individuals).load() # w.
    onto_individuals.imported_ontologies.append(onto_classes)
    #onto_individuals = onto_individuals.load()
    return onto_classes, onto_individuals












