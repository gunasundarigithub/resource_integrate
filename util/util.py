from openpyxl.styles import colors
import pandas as pd
import sys
import yaml
import collections
import os
import socket
import logging
import logging.config

class excelConstants():
  column_start = 3
  FIRST_COLUMN = 1
  SECOND_COLUMN = 2
  THIRD_COLUMN = 3
  FOURTH_COLUMN = 4
  MONTH_30_DAYS = ['Apr', 'Jun', 'Sep', 'Nov']
  MONTH_31_DAYS = ['Jan', 'Mar', 'May', 'July', 'August', 'Oct', 'Dec']
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
  SHIFT_PLAN = collections.namedtuple('SHIFT_PLAN', 'ACC OFF LEAVE TCS NACC EACC')
  COOKIES = collections.namedtuple('COOKIES', 'EMAIL USERNAME TEAM MONTH EXCELFILE')
  SHIFT_CATEGORY = SHIFT_PLAN(ACC='AccPlan', OFF='OffPlan', LEAVE='LeavePlan', TCS='TCS_Holiday_Plan', \
      NACC='NIGHT_SHIFT', EACC='EVENING_SHIFT')
  SESSION_COOKIES = COOKIES(EMAIL='email', USERNAME='username', TEAM='team', MONTH='month', EXCELFILE='excel_file')
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

"""
Get YAML configuration file based on ENV.
"""
def get_conf():
  current_dir = os.path.dirname(os.path.realpath(__file__))
  conf_location = 'C:\\Sabs Learning\\Python Learning\\resource_integrate\\config\\config.yml'
  config ={}
  with open (conf_location) as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    env= config['env']
  return config.get(env)


"""
Get host based on environment.
"""
def fetch_host_on_env():
  import socket
  get_host = lambda: ('localhost' if socket.gethostname().startswith('L') else socket.gethostname()) 
  return get_host()

"""
Set up logger object for logging.
"""
def get_logger_obj():
  cfg= get_conf()
  logging.config.dictConfig(cfg['logging'])
  log = logging.getLogger('shift-mgmt')
  log.setLevel(cfg['log_level'])
  return log

"""
Get Env that you are working on....
"""
def get_env_file():
  log = get_logger_obj()
  current_dir = os.path.dirname(os.path.realpath(__file__))
  os.chdir(current_dir)
  os.chdir('..')
  base_dir = os.getcwd()
  # Set config location based on environment running on.
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

"""
Automate function to generate number of days for a given month by the user.
"""
def generate_month_days(month):
  generate_31_days = lambda: list(1,32)) if month.capitalize()[0:3] in const.MONTH_31_DAYS else None
  generate_30_days = lambda: list(1,31)) if month.capitalize()[0:3] in const.MONTH_30_DAYS else None
  generate_28_days = lambda: list(1,29)) if month.capitalize()[0:3] in const.MONTH_28_OR_29_DAYS else None
  generate_29_days = lambda: list(1,30)) if month.capitalize()[0:3] in const.MONTH_28_OR_29_DAYS else None
  days_list_func = lambda : [ele for ele in [generate_31_days(), generate_30_days(), generate_28_days(), generate_29days()] if ele is not None]
  return days_list_func

"""
Function to generate weekdays for a given month.
Second Header --> [ Team Member, list of weekdays like Mon Tue Wed Thu Fri Sat Sun....]
"""
def generate_workdays_for_month (year, month, month_period, from_ui=False):
  cfg=get_conf()
  __second_header = ['Team Member']
  week_date = pd.Series(pd.date_range('-'.join([year, month]), periods=month_period, freq='D'))
  df = pd.DataFrame(dict(shift_date=week_date))
  df['days_in_week'] = df['shift_date'].dt.day_name()
  for day_row in df['days_in_week']:
    __second_header.append(day_row[0:3])
  if from_ui:
    return __second_header[1:]
  else:
    __second_header.extend(cfg.get('shift_category'))
    __second_header.extend(cfg.get('shift_category_hours'))
    return __second_header
  
"""
Function to add General shifts for remaining days dynamically (Apart from ACC, OFF, LEAVE, TCS, HOLIDAY)
"""
def add_general_shifts(altered_dict, associate, month):
  month_days = generate_month_days(month)
  for _key in altered_dict.keys():
    _AOLHList = list(altered_dict[_key].keys())
    _gen_k = list(set(month_days[0]).difference(_AOLHList)))
    _gen_v = [ 'G' for _k in _gen_k ]
    shift_dict = dict(zip(_gen_k, _gen_v))
    # Update the remaining values with General shifts.
    altered_dict[associate].update(shift_dict)
    altered_dict[associate] = {
      _k: _v for _k, _v in sorted(altered_dict[associate].items(), key=lambda d: d[0])
    }

"""
Function to alter the roaster dict from cache as centralized dict based on associates.
"""
def alter_roaster_cached_dict(_mr):
  _alter_d = {}
  _tmp_d = {}
  for asso in _mr['associates']:
    for k in _mr['associates_plan'].keys():
      if asso in k:
        _int_k = { int(_k): _v for _k, _v in _mr['associates_plan'][k].items() }
        _alter_d.update({ asso : _int_k })
        _tmp_d.update(_int_k)
        _alter_d[asso].update(_tmp_d)
    _tmp_d = {}
    add_general_shifts(_alter_d, asso, _mr['month'])
    _alter_d[asso].update(fetch_shift_counts([ _v for _v in _alter_d[asso].values()]))
  return _alter_d

"""
To fetch the each associates sum of shift based on shift category.
"""
def fetch_shift_counts(sh_list=[], dataframe=None, df_exists=True):
  # Get the last tow index.
  if dataframe is not None and not sh_list:
    _last_rw_idx = len(dataframe) - 1
    _df_list = list(dataframe.iloc[_last_rw_idx])
  else:
    _df_list = sh_list
  shift_count = (
    'ACC': _df_list.count('A') if df_exists else 0,
    'GEN': _df_list.count('G') if df_exists else 0,
    'OFF': _df_list.count('O') if df_exists else 0,
    'NACC': _df_list.count('N'),
    'EACC': _df_list.count('E'),
    'LEAVE': _df_list.count('L'),
    'HOLIDAY': _df_list.count('H'),
    'ACC-HOURS': sum(
      [
        10*int(_df_list.count('A')), 8*int(_df_list.count('N')), 8*int(_df_list.count('E'))
      ]
    ),
    'GEN-HOURS': 9*int(_df_list.count('G')),
    'TOTAL-HOURS': sum(
      [
        10*int(_df_list.count('A')), 8*int(_df_list.count('N')), 8*int(_df_list.count('E')), 9*int(_df_list.count('G'))
      ]
    )
  )
  
"""
Function to find the given filename in the working project directory and store the actual path of the file.
"""
import fnmatch
def find_file(filename, dir_path):
  conf = get_conf()
  os.chdir(conf['prod_dir'])
  proj_di=os.getcwd()
  for _root, _dir, _files in os.walk(dir_path):
    filepath = [os.path.join(_root, _f_n) for _f_n in _files if fnmatch.fnmatch(_f_n, filename)]
    if filepath:
      return filepath

"""
Function to check if a specific month exists in the shift plan exists, if exists return True else False.
"""
def check_month_exists_excel(month, filename, dir_path):
  _monthExists = False
  _filePath = find_file(filename, dir_path)
  import pandas as pd
  if os.path.isfile(filename):
    # Concat the difference to one object, hence we can collect all excel sheets at one place. (use pandas concat())
    df = pd.concat(pd.read_excel(_filePath[0], sheet_name=None), ignore_index=True)
    df_m = df[df["Month"]==month] # OR use loc/iloc to fetch the month values.
    # df_m = df.loc[(df.Month == month)]
    # df_m = df.iloc[(df.Month == month).values]
    if not df_m.empty:
      _monthExists = True
      return _monthExists
  return _monthExists

"""
Function to fetch list of months been cached for a team.
"""
def get_cached_month_roaster(teamRoasterPlan):
  month_list = [ _t["month"] for _t in teamRoasterPlan ]
  return month_list