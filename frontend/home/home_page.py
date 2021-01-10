"""
File name: cache.py
Description: Home page API route

Change Log:
Release Date    Revision Date   Changes By      Description
------------    -------------   ----------      -----------
                July 2020       Sabarish AC     Initial
                August 2020     Ganapathy R     Code Updation & Refraction
"""
# Built in Modules
from flask import render_template, abort, session, flash, redirect, url_for

# Customized Modules
from . import home
import sys
sys.path.append('E:\\Sabs Learning\\resource_integrate')
from util import util

conf = util.get_conf()
const = util.excelConstants()

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