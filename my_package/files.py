import importlib
import os
import subprocess
from unicodedata import name
from flask import Blueprint, render_template, abort, current_app, g, jsonify, request, flash, current_app
from my_package.db import get_db
from owlready2 import *
from . import util
import json
import pathlib
from werkzeug.utils import secure_filename
from datetime import datetime
import random
import string



# VALUES


# UPLOAD_FOLDER = pathlib.Path(__file__).parent.resolve() / 'suploads'
ALLOWED_EXTENSIONS = {'obj'}


# Create Blueprint
files_bp = Blueprint('files_bp', __name__, template_folder='templates')


# ROUTES


@files_bp.route('/', methods=['POST'])
def upload_file():
    print("ajax reached")

    # check if the post request has the file part
    if 'file' not in request.files:
        #flash('No file part')
        #return redirect(request.url)
        return "Error"
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        # flash('No selected file')
        # return redirect(request.url)
        return ""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add date to filename to make it more unique
        filename = datetime.today().strftime('%Y-%m-%d--%H-%M-%S') + "--" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + '--' + filename


        # Save file on server
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        # Send the created filename to the client
        return filename
        #return redirect(url_for('download_file', name=filename))
    return ""












def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS













