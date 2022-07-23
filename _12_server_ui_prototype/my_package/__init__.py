#from flask import Flask, send_from_directory
#from flask import Flask, flash, request, redirect, url_for
import random

import os
import string
from flask import Flask, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import pathlib
from datetime import datetime
from my_package.generationschemes import simple_page








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

    # @app.route('/generation-schemes', methods=['GET'])
    # def get_generation_schemes():

    app.register_blueprint(simple_page, url_prefix='/generation-schemes')


















    from my_package import db
    db.init_app(app)
    return app











UPLOAD_FOLDER = pathlib.Path(__file__).parent.resolve() / 'beta_uploads'
ALLOWED_EXTENSIONS = {'obj'}

#app = Flask(__name__)
#app.config.from_object(__name__)










# return app




















# if __name__ == "__main__":
#     app.run(debug=True)
