"""
File name: home.py
Changes by : Ganapathy R
"""

# built in Modules
from flask import render_template, abort, sesssion, flash, redirect, url_for
from flask_login import login_required

# User defined Modules

from . import home
import sys
sys.path.append('C://ctpt//app-shift-mgnt')
from util import util

conf = util.get_conf()

"""
Render to Home Page on / route
"""

@home.route('/home')
@home.route('/')

def homePage():
    if 'email' in session:
        email = session['email']
        return render_template(conf['templates']['home'], logged_in=session, is_home=True, title='Welcome to CTPT Shift Plan App')
    else:
        flash('You muste be logged in to use this app, please login!!', category='warning')
        return redirect(url_for('auth.user_login'))
        

