"""
Copy Rights, All Rights Reserved 2020
File name: shiftDashboard.py

Description: 
Flask FrameWork API Routes For UI.

Code Changes:
Release Date    Revision Date   Changes By      Description
------------    -------------   -----------     ------------
                Sept 2020     Sabarish AC         Initial
                Sept 2020     Sayan H          Code Updation
"""
# ------------------------------------------- Built-in Modules ------------------------------------------------------------------------
from flask import flash, redirect, url_for, render_template, session, request, send_file
from flask_wtf import FlaskForm
from wtforms import widgets, PasswordField, StringField, SubmitField, SelectField, SelectMultipleField, RadioField, ValidationError, IntegerField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, AnyOf, Regexp
from openpyxl import load_workbook
import traceback
import os
import sys
#sys.path.append('E:\\Sabs Learning\\resource_integrate\\')
#sys.path.append('E:\\Sabs Learning\\resource_integrate\\frontend')

# ------------------------------------------- User-defined Modules --------------------------------------------------------------------
from . import shift_dashboard
from util import util, teamMembers
from models import access_shift_plan
import cache

# ------------------------------------------- Global Objects Var ----------------------------------------------------------------------
const = util.excelConstants()
conf = util.get_conf()
log = util.get_logger_obj()
host = util.fetch_host_on_env()   # Get Host based on env your working!
print(f'host: ----- ---- ---- ---- ---- {host}')
user_cache = cache.CacheFile(conf['app']['user_cache_file'])
shift_plan_cache = cache.CacheFile(conf['app']['shiftplan_cache_file'])
team_members_cache = cache.CacheFile(conf['app']['team_members_cache_file'])
team_years_cache = cache.CacheFile(conf['app']['team_years_cache_file'])
team_const = teamMembers.TEAM
roaster_dict = {}

class MultiCheckboxField(SelectMultipleField):
  widget = widgets.ListWidget(prefix_label=False)
  option_widget = widgets.CheckboxInput()

"""
Class to register the new user to create a new account shift plan app.
"""
class AssociateShiftForm(FlaskForm):
  month= SelectField('Month', choices = const.MONTH_CHOICES)
  shore = RadioField('Shore', choices= const.SHORE_CHOICES, validators =[DataRequired()])
  year = StringField('Year', validators=[DataRequired(), Regexp(r'^([0-9]){4}$', message= "Year must be 4 digits")], 
                     render_kw={"placeholder" : "Year (YYYY)"} )
  teamName = SelectField('Team', choices=const.TEAM_CHOICES, validators=[DataRequired()])
  submit = SubmitField('Generate Month plan')

"""
Class to choose shift year plan and fetch it in UI.
"""
class TeamYearForm(FlaskForm):
  year = SelectField('Choose Shift Plan Year', choices=['2020', '2021'])
  submit = SubmitField('Fetch Year Plan')

"""
Form Instance for Associate Shift Plan Form.
"""
def __formInstance__():
  asso_shift_form = AssociateShiftForm()
  return asso_shift_form

"""
Form Instance for Year Selection To Fetch Year Shift Plan.
"""
def __yearFormInstance__():
  year_shift_form = TeamYearForm()
  return year_shift_form

"""
Render to Shift Plan Page on /shiftdashboard route
"""
@shift_dashboard.route('/shiftdashboard', methods=['GET', 'POST'])
def dashboard(shift_plan_id=''):
  _roasterExists= False
  if const.SESSION_COOKIES.EMAIL in session and const.SESSION_COOKIES.USERNAME in session:
    # Automate Here! To Auto fetch the team members using cache file.
    team_members = team_members_cache.get_team_members_cache(session['team'])
    if team_members:
      _roasterExists = True
      _is_roaster = True # Set Create Roaster Flag to True Initially.
      if __formInstance__().validate_on_submit():
        team_years_cache.cache_shift_plan_year(__formInstance__().year.data, __formInstance__().teamName.data)
        _team_month_plan = shift_plan_cache.get_shift_plan_cache(__formInstance__().teamName.data, 
                shift_year=__formInstance__().year.data, shift_month=__formInstance__().month.data)
        if _team_month_plan is not None and isinstance(_team_month_plan, dict):
          log.debug("Shift plan for Month : " + __formInstance__().month.data + " is already cached!" )
          log.debug(__formInstance__().month.data + " Plan for month: " + __formInstance__().month.data + " - " + _team_month_plan)
          session[const.SESSION_COOKIES.MONTH] = __formInstance__().month.data
          return render_template(conf['templates']['shift_roaster'], form=__formInstance__(), logged_in=session(), 
                      _is_roaster=_is_roaster, _shift_id=team_month_plan['planId'], _validation=True)
        elif session['team']!=__formInstance__().teamName.data:
          flash('You belong to Team ' + session['team'] + ' and not ' + __formInstance__().teamName.data + ', \
                  please select your team as ' + session['team'] + '!', category='warning')
        else:
          _is_roaster = False   # Set Create Roaster Flag to False, if team Month does not exists.
          log.debug("No Caching done for the month : " + __formInstance__().month.data + ", so processing to cache it!" )
          roaster_dict.update({
            'month': __formInstance__().month.data,
            'shore' : __formInstance__().shore.data,
            'year': __formInstance__().year.data,
            'team': __formInstance__().teamName.data,
            'associates': team_members
          })
          return render_template(conf['templates']['submit_roaster'], form=__formInstance__(), logged_in=session, \
                                  _is_roaster=_is_roaster, month=roaster_dict['month'], team_members=team_members,\
                                 _validation=True, _team_plan_exists=_roasterExists, hostname=host, _is_download=True)
      else:
        return render_template(conf['templates']['shift_roaster'], form=__formInstance__(), logged_in=session, _is_roaster=_is_roaster, \
                              _validationFailed=True, _team_plan_exists=_roasterExists, hostname=host, _is_download=True)
    elif team_members is None:
      flash("No team: " + __formInstance__().teamName.data + " in cache file: " + conf['app']['team_members_cache_file'] + "!", category="error")
    else:
      flash("No team members available for the team : " + str(__formInstance__().teamName.data) + " in cache file: " + conf['app']['team_members_cache_file'] + "!", category="error" )
    return render_template(conf['templates']['shift_roaster'], form=__formInstance__(), logged_in=session, _is_roaster=True, 
                                _team_plan_exists=_roasterExists, hostname=host, _is_download=True )  
  else:
    flash('You must log in to use the app, please login!!', category='warning')
    return redirect(url_for('auth.user_login'))
  
"""
Render Page/API to generate team dashboard after user submits the data.
"""
@shift_dashboard.route('/teamdashboard', methods=['GET', 'POST'])
def generateDashboard():
  # Set flag to check if the roaster has been created! Set to False Initially.
  _roaster_status = _month_plan_exists = False
  if request.method == "POST":
    roaster_dict.update({
      'associates_plan': request.form.to_dict()
    })
    log.debug('Final Roaster Dict: ' + str(roaster_dict))
    # DB Cache Shift Plan Roaster For Your Team.
    roaster_model = access_shift_plan.accessShiftPlan(roaster_dict)
    roaster_model.cache_roaster_plan()
    flash('Shift plan updated successfully for team : ' + str(session[const.SESSION_COOKIES.TEAM])+ '!', category='success')
    return redirect(url_for('shiftDashboard.generateDashboard'))
  return render_template(conf['templates']['roaster_modal'], logged_in=session, _is_dash=True, hostname=host, form=__yearFormInstance__())

"""
Router to render team shift plan dashboard based on year.
"""
@shift_dashboard.route('/yeardashboard', methods=['GET', 'POST'])
def yearTeamDashboard():
  dash_status = True    # Set Dashboard existing flag to True (Assumption).
  _alter_dict = {}
  if request.method == 'POST':
    if __yearFormInstance__().validate_on_submit:
      _user_choosed_year = __yearFormInstance__().year.data
      _team_year_plan = shift_plan_cache.get_shift_plan_cache(session['team'], shift_year=_user_choosed_year)

      if _team_year_plan:
        _roaster_month_list = util.get_cached_month_roaster(_team_year_plan)
        for idx, month in enumerate(_roaster_month_list):
          _month_num = util.generate_month_days(month)[0]
          _month_days = util.generate_workdays_for_month(_team_year_plan[idx]['year'], month, len(util.generate_month_days(month)[0]), from_ui=True)
          # Converting to dictionary object for month having its days and numbers.
          _month_in_num_days = dict(zip(_month_num, _month_days))
          _new_dict = util.alter_roaster_cached_dict(_team_year_plan[idx])
          _alter_dict.update({month: _new_dict})
          _alter_dict[month]['month_in_num_days'] = _month_in_num_days
          _alter_dict[month]['shore'] = _team_year_plan[idx]['shore']
          _alter_dict[month]['associates'] = _team_year_plan[idx]['associates']
      else:
        log.error('Team Roaster Plan Not Found, Creating it....')
        dash_status = False   # Set Dashboard existing to False. (No Team Dashboard, Creating first time)
  else:
    dash_status = False
  return render_template(conf['templates']['roaster_modal'], logged_in=session, _is_dash=True, dash_status=dash_status, \
                          roaster=_alter_dict, hostname=host, form=__yearFormInstance__(), yearPlanDash=True)

"""
Router API to delete a month shift plan.
"""
@shift_dashboard.route('/deleteMonthPlan/<month>')
def deleteMonthPlan(month):
  if month:
    shift_plan_cache.deleteMonthPlan(month, session['team'])
    return redirect(url_for('shiftDashboard.yearTeamDashboard'))
  else:
    log.error('No month plan available for the team ' + session['team'])

"""
Router API to download Team shift plan to excel.
"""
@shift_dashboard.route('/download/<teamName>')
def load_to_excel(teamName):
  try:
    _roasterExists = False    # Set this flag initially to False (no roaster exists)
    filename = '-'.join([session[const.SESSION_COOKIES.TEAM], 'ACC', 'SHIFT', 'PLAN.xlsx'])
    filepath = util.find_file(filename, os.getcwd())
    log.debug('filepath: ------ ' + str(filepath))
    _team_plan = shift_plan_cache.get_shift_plan_cache(teamName)
    if _team_plan:
      log.debug(teamName + ' Team plan : ' + _team_plan)
      for each_team_plan in _team_plan:
        _df_month_exists= util.check_month_exists_excel(each_tem_plan['month'], filename, os.gwtcwd())
        if not _df_month_exists:
          roaster_model = access_shift_plan.accessShiftPlan(each_team_plan)
          sheet_name = '-'.join([teamName, each_team_plan['year']])
          roaster_model.save_to_excel(teamName, sheet_name)
          log.info('Downloading file..')
          log.info('Returning from request..')
        else:
          log.debug(each_team_plan['month'] + ' already exists, processing for other months!')
    if filepath is not None:
      log.error(f"404 error, returning from request")
      return render_template(conf['templates']['page_not_found'], title='page_not_found'), 404
    else:
      _roasterExists=True
      log.error("No roaster plan created for team: " + session[const.SESSION_COOKIES.TEAM])
      return render_template(conf['templates']['page_not_found'], title='page_not_found'), 404
    return send_file(filepath[0], as_attachment=filename)
    
  except Exception as exp:
    log.error("Exception occured while downloading the shift roaster to excel")
    log.error(exp)
    log.error(traceback.format_exc())