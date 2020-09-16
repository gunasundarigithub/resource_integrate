class MultiCheckboxField(SelectMultipleField):
  widget = widgets. ListWidget(prefix_label=False)
  option_widget = widgets. CheckboxInput()
  
class AssociateShiftForm(FlaskForm):
  month= SelectField('Month', choices = const.MONTH_CHOICES)
  shore = RadioField('Shore', choices= const.SHORE_CHOICES, validators =[DataRequired()])
  year = StringField('Year', validators=[DataRequired(), Regexp(r'^([0-9]){4}$', message= "Year must be 4 digits")], 
                     render_kw={"placeholder" : "Year (YYYY)"} )
  teamName = SelectField ('Team', choices = const.TEAM_CHOICES, validators= [DataRequired()])
  submit = SubmitField ("Generate Month plan")
  
def __formInstance__():
  asso_shift_form = AssociateShiftForm()
  return asso_shift_form

@shift_dashboard.route('/shiftdashboard', methods=[GET, POST])
def dashboard(shift_plan_id=''):
  _roasterExists= False
  if const.SESSION_COOKIES.EMAIL in session and const.SESSION_COOKIES.USERNAME in session :
    team_members = team_members_cache.get_team_members_cache(session['team'])
    if team_members:
      _roasterExists = True
      if __formInstance__().validate_on_submit():
        _team_month_plan = shift_plan_cache.get_shift_plan_cache(__formInstance__().teamName.data, shift_month = __formInstance__().month.data)
        if _team_month_plan is not None and isinstance(_team_month_plan. dict):
          log.debug(f"Shift plan for Month : {__formInstance__().month.data} is already cached!" )
          log.debug(f"{__formInstance__().month.data} Plan for month: {__formInstance__().month.data}  - {_team_month_plan}" )
          session[const.SESSION_COOKIES.MONTH] = __formInstance__().month.data
          return render_template(conf['templates']['shift_roaster'], form= __formInstance__(), logged_in=session(), 
                                 _is_dash=True, _shift_id=team_month_plan['planId'] )
        else:
          log.debug(f"No Caching done for the month : {__formInstance__().month.data}, so processing to cache it!" )
          roaster_dict.update({
            'month': __formInstance__().month.data,
            'shore' : __formInstance__().shore.data,
            'year': __formInstance__().year.data
            'team': __formInstance__().teamName.data
            'associates': team_members
          })
          return render_template(conf['templates']['submit_roaster'], form= __formInstance__(), logged_in=session(), 
                                 _is_dash=True, month=roaster_dict['month'], team_members= team_members )
        
    elif team_members is None:
      flash(f"No team: in cache file!", category="error")
      
    else:
      flash(f"No team members available for the team : in cache file : ", category="error" )
    return render_template(conf['templates']['shift_roaster'], form= __formInstance__(), logged_in=session(), 
                                 _is_dash=True, _team_plan_exists= _roasterExists, hostname=host, _is_download=True )
  
  else:
    flash('You must log in to use the app, please login!', category='warning')
    return redirect(url_for('auth.user_login'))
  
@shift_dashboard.route('/teamdashboard', methods=['GET', 'POST'])
def generateDashboard():
  _roaster_status=_month_plan_exists=False
  if request.method == "POST":
    roaster_dict.update({
      'associates_plan': request.form.to_dict()
    })
    log.debug(f'Final Roaster Dict: {roaster_dict}')
    roaster_model = access_shift_plan.accessShiftPlan(roaster_dict)
    roaster_model.cache_roaster_plan()
    flash(f'Shift plan updated successfully for team : {session[const.SESSION_COOKIES.TEAM]}!', category='success')
    return redirect(url_for('shiftDashboard.generateDashboard'))
  else:
    _roaster_status =True
    return render_template(conf['templates']['roaster_modal'], logged_in=session(), 
                                 is_roaster_submitted=True, roaster_status=roaster_status, onth = roaster_dict['month'] )
  
@shift_dashboard.route('/download/<teamName>')
def load_to_excel(teamName):
  try:
    _roasterExists=False
    filename= '-'.join([session[const.SESSION_COOKIES.TEAM], 'ACC', 'SHIFT', 'PLAN.xlsx'])
    filepath = util.find_file(filename, os.getcwd())
    log.debug(f'filepath:------{filepath}')
    _team_plan = shift_plan_cache.get_shift_plan_cache(teamName)
    if _team_plan:
      log.debug(f"{teamName} Team plan : {_team_plan}")
      for each_team_plan in _team_plan:
        _df_month_exists= util.check_month_exists_excel(each_tem_plan['month'], filename(), os.gwtcwd())
        if not _df_month_exists:
          roaster_model = access_shift_plan.accessShiftPlan(each_team_plan)
          roaster_model.save_to_excel()
        else:
          log.debug("{each_team_plan['month'] already exists, processing for other months!")
          
    else:
      _roasterExists=True
      log.error(f"No roaster plan created for team: {session[const.SESSION_COOKIES.TEAM]}" )
    if filepath is not None:
      session[const.SESSION_COOKIES.EXCELFILE] =filepath[0]
      log.info("Downloading file...")
      log.info(f"returning from Request..")
      return send_file(filepath[0], as_attachment=filename)
    else:
      log.error(f"404 error, returning from request")
      return render_template(conf['templates'][''page_not_found], title='page_not_found'), 404
    
  except Exception as exp:
    log.error(f"Exception occured while downloading the shift roaster to excel")
    log.error(exp)
    log.error(tracebask.format_exc())
              
