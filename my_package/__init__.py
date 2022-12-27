import random
import os
import shutil
import string
import subprocess
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import pathlib
from datetime import datetime
from my_package.generationschemes import generationschemes_bp
from my_package.modules import modules_bp
from my_package.jobs import jobs_bp
from my_package.files import files_bp
from . import util
import pathlib


UPLOAD_FOLDER = pathlib.Path(__file__).parent.resolve() / 'uploads'



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
        return send_from_directory('client/public', 'index.html')




    # Path for all the static files (compiled JS/CSS, etc.)
    @app.route("/<path:path>")
    def home(path):
        return send_from_directory('client/public', path)


    app.register_blueprint(files_bp, url_prefix='/files')

    app.register_blueprint(generationschemes_bp, url_prefix='/generation-schemes')

    app.register_blueprint(modules_bp, url_prefix='/modules')

    app.register_blueprint(jobs_bp, url_prefix='/jobs')

    if True: # TODO: In production user modules should be loaded on every startup
        prepare_custom_code()



    return app






def prepare_custom_code():

    # 1. Module-Forms
    # 1.1 Delete existing forms
    path_client_forms = util.get_path_to_package() / "client" / "forms"
    for f in os.listdir( path_client_forms ):
        if not f.endswith(".svelte"):
            continue
        os.remove(os.path.join(path_client_forms, f))


    # 1.2 Copy 
    files = util.get_datascientist_modules_files()
    for el in files:
        path_to_svelte_form = pathlib.Path(el.path) / "Form.svelte"
        shutil.copyfile(path_to_svelte_form, path_client_forms / (el.name + ".svelte") )


    # 2. Form-elements (TODO, currently the form elements are directly placed into the target folder)


    # 3. Call "npm run" to compile svelte-forms
    subprocess.run(["npm", "run", "build"], cwd=util.get_path_to_package() / "client/", shell=True )



