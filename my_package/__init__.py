import random
import os
import shutil
import string
import subprocess
from flask import Flask, flash, request, redirect, url_for, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import pathlib
from datetime import datetime
from my_package.generationschemes import generationschemes_bp
from my_package.modules import modules_bp
from my_package.jobs import jobs_bp
from my_package.jobs import is_job_running
from my_package.files import files_bp
from . import util
import pathlib
import json


UPLOAD_FOLDER = pathlib.Path(__file__).parent.resolve() / 'data' / 'uploads'



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # Connect to database (use single object for all requests, via factory pattern)
    from my_package import db
    db.init_app(app)



    # ROUTES


    # Path for our main Svelte page
    @app.route("/")
    def base():
        return send_from_directory('frontend/public', 'index.html')




    # Path for all the static files (compiled JS/CSS, etc.)
    @app.route("/<path:path>")
    def home(path):
        return send_from_directory('frontend/public', path)


    @app.route('/settings/debug-mode/', methods=['GET', 'PUT'])
    def settings_debug_mode():
        # if PUT:
        if request.method == 'PUT':
            debug_mode_value = request.json['value']
            error = None
            if not ("value" in request.json):
                error = 'debug_mode_value is required.'
            elif debug_mode_value not in [True, False]:
                error = "value must be true or false"
            if error is not None:
                return "error is: " + error

            print(debug_mode_value)
            with open( util.get_path_to_package() / 'data/settings.json', 'w') as f:
                json.dump({"debug_mode" : debug_mode_value}, f)

        # if PUT or GET:
        value = "false"
        with open( util.get_path_to_package() / 'data/settings.json', 'r') as f:
            value = json.load(f)["debug_mode"]

        return jsonify({"value":value})


    @app.route('/settings/reload-custom-code/', methods=['POST'])
    def settings_reload_custom_code():
        # if PUT:
        if request.method == 'POST':
            if is_job_running():
                return "ERROR" # TODO
            else:
                prepare_custom_code()

        return jsonify({})


    app.register_blueprint(files_bp, url_prefix='/files')

    app.register_blueprint(generationschemes_bp, url_prefix='/generation-schemes')

    app.register_blueprint(modules_bp, url_prefix='/modules')

    app.register_blueprint(jobs_bp, url_prefix='/jobs')

    if True: # TODO: In production user modules should be loaded on every startup
        prepare_custom_code()



    return app



def get_settings_debug_mode():
    value = False
    with open( util.get_path_to_package() / 'data/settings.json', 'r') as f:
        value = json.load(f)["debug_mode"]
    return value




def prepare_custom_code():

    # 1. Forms from modules
    # 1.1 Delete existing forms
    path_client_forms = util.get_path_to_package() / "frontend" / "src" / "forms"
    for f in os.listdir( path_client_forms ):
        if not f.endswith(".svelte"):
            continue
        os.remove(os.path.join(path_client_forms, f))

    # 1.2 Copy 
    files = util.get_datascientist_modules_files()
    for el in files:
        path_to_svelte_form = pathlib.Path(el.path) / "Form.svelte"
        shutil.copyfile(path_to_svelte_form, path_client_forms / (el.name + ".svelte") )


    # 2. Form-elements
    # 2.1 Delete existing forms
    path_client_forms = util.get_path_to_package() / "frontend" / "src" / "form_components"
    for f in os.listdir( path_client_forms ):
        if not f.endswith(".svelte"):
            continue
        os.remove(os.path.join(path_client_forms, f))

    # 2.2 Copy 
    files = util.get_datascientist_formcomponents_files()
    for el in files:
        if not el.name.endswith(".svelte"):
            continue
        shutil.copyfile(el, path_client_forms / el.name )




    # 3. Call "npm run" to compile svelte-forms
    subprocess.run(["npm", "run", "build"], cwd=util.get_path_to_package() / "frontend/", shell=True )



