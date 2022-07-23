from flask import Blueprint, render_template, abort, current_app, g
from flask.cli import with_appcontext
import click

import sqlite3

















simple_page = Blueprint('simple_page', __name__, template_folder='templates')


@simple_page.route('/', methods=['GET'])
def show():
    return "ssasd"





