# Built-In Modules.
from flask import Blueprint
shift_dashboard = Blueprint('shiftDashboard', __name__)
from . import shiftDashboard