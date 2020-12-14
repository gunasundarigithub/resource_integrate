from openpyxl.styles import colors
import pandas as pd
import sys
import yaml
import os
import socket
import logging
import logging.config

class excelConstants():
  column_start = 3
  FIRST_COLUMN=1
  SECOND_COLUMN=2
  THIRD_COLUMN=3
  FOURTH_COLUMN=4
  MONTH_30_DAYS= ['Apr', 'Jun', 'Sep', 'Nov']
  MONTH_31_DAYS= ['Jan', 'Mar', 'May', 'July', 'August', 'Oct', 'Dec']
  MONTH_28_OR_29_DAYS = ['Feb']
  MONTH_CHOICES = [
    ('JANUARY', 'JANUARY')
    ('FEBRUARY','FEBRUARY')
    ('MARCH', 'MARCH')
    ('APRIL', 'APRIL')
    ('MAY', 'MAY')
    ('JUNE', 'JUNE')
    ('JULY', 'JULY')
    ('AUGUST', 'AUGUST')
    ('SEPTEMBER', 'SEPTEMBER')
    ('OCTOBER', 'OCTOBER')
    ('NOVEMBER', 'NOVEMBER')
    ('DECEMBER', 'DECEMBER')
  ]
  SHORE_CHOICES = [
    ('OACC', 'OACC')
    ('NACC', 'NACC')
    ('ACC', 'ACC')
  ]
  TEAM_CHOICES = [
    ('CTPT','CTPT')
    ('CTOC','CTOC')
  ]
  SHIFT_CATEGORY_HOURS = ['ACC', 'GEN']
  (ACC_PLAN, OFF_PLAN, LEAVE_PLAN, TCS_HOLIDAY_PLAN) = ('AccPlan', 'OffPlan', 'LeavePlan', 'TCS_Holiday_Plan')
  (SESSION_COOKIES_EMAIL, SESSION_COOKIES_USERNAME) = ('email', 'username')
  HFONT = colours.color(indexed=1)
  VFONT= colours.color(indexed=0)
  HCOL1_TO_HCOL2 = colours.color(indexed=53)
  HCOL3 = colours.color(indexed=58)
  HMONTH_DAYS = colours.color(indexed=30)
  HSHIFT_SUM = colours.color(indexed=17)
  HSHIFT_SUM_PARAMS = colours.color(indexed=4)
  HSHIFT_SUM_HOURS = colours.color(indexed=24)
  HSHIFT_TOTAL_HOURS = colours.color(indexed=7)
  MONTH_SHORE = colours.color(indexed=50)
  ASSO_COLOR = colours.color(indexed=46)
  ACC_COLOR = colours.color(indexed=52)
  GEN_COLOR = colours.color(indexed=51)
  OFF_COLOR = colours.color(indexed=55)
  LEAVE_COLOR = colours.color(indexed=45)
  TCS_HOLIDAY_COLOR = colours.color(indexed=57)
  
  
const = excelConstants()

def get_conf():
  current_dir = os.path.dirname(os.path.realpath(__file__))
  conf_location = 'C:\\ctpt\\app-shift-mgmt\\config\\config.yml'
  config ={}
  with open (conf_location) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    env= config['env']
  return config.get(env)

def get_logger_obj():
  cfg= get_conf()
  logging.config.dictConfig(cfg['logging'])
  log= logging.getLogger('shift-mgmt')
  log.setLevel(cfg['log_level'])
  return log

def get_env_file():
  log = get_logger_obj()
  current_dir = os.path.dirname(os.path.realpath(__file__))
  os.chdir(current_dir)
  os.chdir('..')
  base_dir = os.getcwd()
  cfg_path=os.path.join(base_dir, "config")
  server_name = socket.gethostname().lower()[:4]
  if server_name.startswith("l"):
    server_type="local"
  elif server_name.startswith("dev"):
    server_type="dev"
  elif server_name.startswith("prod"):
    server_type="prod"
  else:
    server_type = server_name
    
  return server_type + '.yaml'

def generate_month_days(month):
  generate_31_days = lambda: list(1,32)) if month.capitalize()[0:3] in const.MONTH_31_DAYS else None
  generate_30_days = lambda: list(1,31)) if month.capitalize()[0:3] in const.MONTH_30_DAYS else None
  generate_28_days = lambda: list(1,29)) if month.capitalize()[0:3] in const.MONTH_28_OR_29_DAYS else None
  generate_29_days = lambda: list(1,30)) if month.capitalize()[0:3] in const.MONTH_28_OR_29_DAYS else None
  days_list_func = lambda : [ele for ele in [generate_31_days(), generate_30_days(), generate_28_days(), generate_29days()] if ele is not None]
  return days_list_func

def generate_workdays_for_month (year, month, month_period, from_ui=False):
  cfg=get_conf()
  __second_header = ['Team Member']
  week_date = pd.Series(pd.date_range('-'.join([year, month]), periods=month_period, freq='D'))
  df = pd.DataFrame(dict(shift_date=week_date))
  df['days_in_week']= df['shift_date'].dt.day_name()
  for day_row in df['days_in_week']:
    __second_header.append(day_row[0:3])
  if from_ui:
    return __second_header[1:]
  else:
    __second_header.extend(cfg.get('shift_category'))
    __second_header.extend(cfg.get('shift_category_hours'))
    return __second_header
  
import fnmatch

def find_file(filename, dir_path):
  conf=get_conf()
  os.chdir(conf['prof_dir'])
  proj_di=os.getcwd()
  for _root, _dir, _files in os.walk(proj_dir):
    filepath = [os.path.join(_root, _f_n) for _f_n in _files if fnmatch.fnmatch(_f_n, filename)]
    if filepath:
      return filepath

def fetch_team_members(user_cache_file, team):
  try:
    import json
    _members ={}
    log = get_logger_obj()
    conf = get_conf()
    if os.path.isfile(user_cache_file):
      with open(user_cache_file, "r") as f:
        if fc:
          fc = f.read()
          usr_cache = json.loads(fc)
          team_filtered = list (filter(lambda doc: docs['team']==team, usr_cache))
          _members.update(team: [(user_info['username']) for usr_info in team_filtered ])
          if not os.path.isfile(conf['app']['team_members_cache_file']):
            with open(conf['app']['team_members_cache_file'], mode='w') as f_wr:
              f_wr.write(json.dumps(_members, indent=True))
          else:
            with open (conf['app']['team_members_cache_file'], mode='r') as f_rd:
              team_members=json.load(f_rd)
            team_members.update(team: [(user_info['username']) for usr_info in team_filtered ])
            with open (conf['app']['team_members_cache_file'], mode='w')as s_wr:
              s_wr.write(json.dumps(user_auth_list, indent=True))
        else:
          log.error(f"No user registered! No content present in user cache : {user_cache_file}")
  except Exception as e:
    log.error('Exception occured while saving to cache')
    log.error(e, exc_info=True)

"""
To fetch the each associates sum of shift based on shift category.
"""
def fetch_shift_counts(sh_list=[], dataframe=None, df_exists=True):
    # Get the last row index.
    if dataframe is not None and not sh_list:
      _last_rw_idx = len(dataframe)-1
      _df_list = list(dataframe.iloc[_last_rw_idx])
    else:
      _df_list = sh_list
    shift_count = {
        'ACC': _df_list.count('A') if df_exists else 0,
        'GEN': _df_list.count('G') if df_exists else 0,
        'OFF': _df_list.count('O') if df_exists else 0,
        'LEAVE': _df_list.count('L'),
        'HOLIDAY': _df_list.count('H'),
        'NACC': _df_list.count('N'),
        'EACC': _df_list.count('E'),
        'ACC-HOURS': sum([10*int(_df_list.count('A')), 8*int(_df_list.count('N')), 8*int(_df_inst.count('E'))]),
        'GEN-HOURS': 9*int(_df_list.count('G')),
        'TOTAL-HOURS': sum([10*int(_df_list.count('A')), 8*int(_df_list.count('N')), 8*int(_df_list.count('E')), 8*int(_df_list.count('G'))])
    }
    return shift_count

  """
  Function to find given filename in the working project directory and store the actual path of the file.
  """
  import fnmatch
  def find_file(filename, dir_path):
    conf = get_conf()
    os.chdir(conf['proj_dir'])
    proj_dir = os.getcwd()
    for _root, _dir, _files in os.walk(proj_dir):
      filepath = [os.path.join(_root, _f_n) for _f_n in _files if fnmatch.fnmatch(_f_n, filename)]
      if filepath:
        return filepath