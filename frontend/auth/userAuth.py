"""
File name: userAuth.py
Description: User Authentication/Registration (login/register) Form and API Routes, cache the user creds to cache file.

Change Log:
Release Date    Revision Date   Changes By      Description
------------    -------------   ----------      -----------
                July 2020       Sabarish AC     Initial
                August 2020     Ganapathy R     Code Updation & Refraction
"""
# Built in modules
from flask import Flask, redirect, render_template, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, AnyOf
import sys

# User-defined modules
from . import auth 
from models import user 
sys.path.append('C:\\ctpt\\ctpt-backup\\resource_integrate\\cache')
import cache
from util import util

user_model = user.User
conf = util.get_conf()
const = util.excelConstants()
log = util.get_logger_obj()
user_cache = cache.CacheFile(conf['app']['user_cache_file'])

"""
Class to register the new user to create a new account shift plan app.
"""
class UserRegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email ID"})
    username = StringField('Associate Name' , validators=[DataRequired()], render_kw={"placeholder": "Associate Name"})
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirmPassword')], render_kw={"placeholder": "Password"})
    confirmPassword = PasswordField('Confirm Password', render_kw={"placeholder": "Confirm Password"})
    team = SelectField('Team', choices=const.TEAM_CHOICES)
    submit = SubmitField('Register')

"""
Class to login users who have already ref=gister to shift plan app.
"""
class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Registered Email ID"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Valid Password"})
    submit = SubmitField('Login')

@auth.route('/register', methods=['GET', 'POST'])
def user_register():
    reg_form = UserRegistrationForm()
    print(reg_form)
    if reg_form.validate_on_submit():
        _is_reg = user_model.register(reg_form.email.data, reg_form.username.data, reg_form.team.data, reg_form.password.data)
        if _is_reg:
            flash('Thanks for registering Shift Plan App! You have successfuly registered! Please log-in', category='info')
            return redirect(url_for('auth.user_login'))
        else:
            flash('User: ' + reg_form.email.data + ' already exists for Shift Plan App!! Please register with different user!', category='warning') 
    return render_template(conf['templates']['register'], form=reg_form, is_register=True, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def user_login():
    login_form = UserLoginForm()
    if login_form.validate_on_submit():
        user_login_data = user_model.validate_user_login(login_form.email.data, login_form.password.data)
        if user_login_data:
            log.info('User login data: ' + str(user_login_data))
            # If both email and password are valid redirect to home page.
            if user_login_data['verify_username'] and user_login_data['verify_pass']:
                log.debug('session cookie: ' + str(session))
                return redirect(url_for('home.homePage'))
            # if not alert user for invvalid 'user or passsword'
            elif not user_login_data['verify_username']:
                flash('EmailId: ' + login_form.email.data + ' is not a  Registered User!! Please register and Login!!', category='error')
            else:
                flash('Invalid Password, Please Enter An Valid Password!!', category='error')
    return render_template(conf['templates']['login'], form=login_form, logged_in=session, is_login=True, title='Login')

@auth.route('/logout')
def user_logout():
    user_model.logout()
    flash('You have successfuly logged out!!', category='info')
    return redirect(url_for('auth.user_login'))
