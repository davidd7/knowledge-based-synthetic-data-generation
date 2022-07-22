#from flask import Flask, send_from_directory
#from flask import Flask, flash, request, redirect, url_for
import random

import os
import string
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import pathlib
from datetime import datetime

UPLOAD_FOLDER = pathlib.Path(__file__).parent.resolve() / 'beta_uploads'
ALLOWED_EXTENSIONS = {'obj'}





app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
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
        filename = filename.split(".")
        filename[-2] += "-" + datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + "_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        filename = ".".join(filename)

        # Save file on server
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Send the created filename to the client
        return filename
        #return redirect(url_for('download_file', name=filename))
    return ""





# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)


# @app.route("/upload")
# def hello():
#     return str(random.randint(0, 100))


if __name__ == "__main__":
    app.run(debug=True)
