"""
Copy Rights, All Rights Reserved 2020
File name: access_shift_plan.py

Description: 
Model - Bridge between backend and frontend code that collects data from frontend, processes/parses 
        and utilize backend process like caching, retriving cache data, process cached data etc.

Code Changes:
Release Date    Revision Date   Changes By      Description
------------    -------------   -----------     ------------
                Sept 2020     Sabarish AC         Initial
                Sept 2020     Sayan H          Code Updation
"""
import uuid
import datetime
from backend import shift_load_excel
from util import util
from cache import CacheFile

config = util.get_conf()
shift_plan_cache = CacheFile(config['app']['shiftplan_cache_file'])
log = util.get_logger_obj()
const= util.excelConstants()

class accessShiftPlan(object):
  def __init__(self, roaster_dict, created_date=datetime.datetime.utcnow(), id=None):
    self.roaster_dict = roaster_dict 
    self.month = roaster_dict['month']
    self.year = roaster_dict['year']
    self.shore = roaster_dict['shore']
    self.team = roaster_dict['team']
    self.associates = roaster_dict['associates']
    self.associates_plan= roaster_dict['associates_plan']
    self.excel_file = '-'.join([self.team, 'ACC', 'SHIFT', 'PLAN.xlsx'])
    self.id = uuid.uuid4().hex if id is None else id    
    
  """
  Standard instance creation for backend shift_load_excel class.
  """
  def __createInstance__(self):
    _instance = shift_load_excel.ACCShiftPlan(self.associates, self.team, self.month, self.year, self.shore)
    return _instance
  
  """
  Generator Function: That yields shift plan categories for each associates. (ACC|NACC|EACC|OFF|LEAVE|TCS HOLIDAY Plan)
  """
  def key_generator(self):
    for _plan in self.associates_plan:
      yield _plan
      
  """
  Alter the UI Roaster dict in such a format that backend accepts.
  Example:
      Original dict from UI -> associates_plan: {'Sabs AC_AccPlan': '04-Sep-2020', '05-Sep-2020', 'Sabs AC_OffPlan': '06-Sep-2020', '07-Sep-2020' .... }
      Altered Dict for backend -> associates_plan: {'Sabs AC_AccPlan': {4:'A', 5:'A'}, 'Sabs AC_OffPlan': {6: 'O', 7: 'O'} .... }
  """
  def alter_roaster_plan_dict(self):
    # Sample Roaster Dict: { 'month': 'JULY', 'shore': 'OACC', 'year': '2020', 'team': 'CTPT',
    #   'associates': ['Sabarish AC', 'Sayan H', 'Ganapthy R'],
    #   'associates_plan': {'Sabs AC_AccPlan': '04-Sep-2020', '05-Sep-2020', 'Sabs AC_OffPlan': '06-Sep-2020', '07-Sep-2020' .... } }
    for _plan_key in self.key_generator():
      # ACC Plan
      if const.SHIFT_CATEGORY.ACC in _plan_key:
        _key = [int(shft_date.split('-')[0]) for shft_date in self.associates_plan[_plan_key].split(',') if shft_date.split('-')[0].isdigit()]
        self.associates_plan[_plan_key] = dict(zip(_key, ['A']*len(_key)))
        self.associates_plan[_plan_key]= {int(_k): _v for _k, _v in self.associates_plan[_plan_key].items() }
      # Night Shift ACC Plan
      elif const.SHIFT_CATEGORY.NACC in _plan_key:
        _key = [int(shft_date.split('-')[0]) for shft_date in self.associates_plan[_plan_key].split(',') if shft_date.split('-')[0].isdigit() ]
        self.associates_plan[_plan_key] = dict(zip(_key, ['N']*len(_key)))
        self.associates_plan[_plan_key] = { int(_k): _v for _k, _v in self.associates_plan[_plan_key].items() }
      # Evening Shift ACC Plan
      elif const.SHIFT_CATEGORY.EACC in _plan_key:
        _key = [int(shft_date.split('-')[0]) for shft_date in self.associates_plan[_plan_key].split(',') if shft_date.split('-')[0].isdigit()]        
        self.associates_plan[_plan_key] = dict(zip(_key, ['E']*len(_key)))
        self.associates_plan[_plan_key] = { int(_k): _v for _k, _v in self.associates_plan[_plan_key].items() }
      # Off Plan
      elif const.SHIFT_CATEGORY.OFF in _plan_key:
        _key = [int(shft_date.split('-')[0]) for shft_date in self.associates_plan[_plan_key].split(',') if shft.date.split('-')[0].isdigit()]
        self.associates_plan[_plan_key]= dict(zip(_key, ['O']*len(_key)))
        self.associates_plan[_plan_key]= {int(_k): _v for _k, _v in self.associates_plan[_plan_key].items() }        
      # LEAVE Plan
      elif const.SHIFT_CATEGORY.LEAVE in _plan_key:
        _key = [int(shft_date.split('-')[0]) for shft_date in self.associates_plan[_plan_key].split(',') if shft.date.split('-')[0].isdigit()]
        self.associates_plan[_plan_key]= dict(zip(_key, ['L']*len(_key)))
        self.associates_plan[_plan_key]= {int(_k): _v for _k, _v in self.associates_plan[_plan_key].items()}
      # TCS HOLIDAY Plan
      elif const.SHIFT_CATEGORY.TCS in _plan_key::
        _key = [int(shft_date.split('-')[0]) for shft_date in self.associates_plan[_plan_key].split(',') if shft.date.split('-')[0].isdigit()]
        self.associates_plan[_plan_key]= dict(zip(_key, ['H']*len(_key)))
        self.associates_plan[_plan_key]= {int(_k): _v for _k, _v in self.associates_plan[_plan_key].items() }
        
  """
  Fetch complete shift plan for the given team.
  """
  def get_shift_plan_team(self,teamName):
    _team_plan = shift_pln_cache.get_shift_plan_cache(teamName)
    if isinstance(_team_plan, list):
      log.debug("Overall cached shift plan for the team: " + self.team + ': ' + _team_plan)
      return _team_plan
  
  """
  Bridge Function: To cache team shift plan from UI to cache file (Backend)
  """
  def cache_roaster_plan(self):
    self.alter_roaster_plan_dict()
    # Restore the altered associates plan dict to main dict object.
    self.roaster_dict['associates_plan'] = self.associates_plan
    log.debug("Altered Roaster dict: " + self.roaster_dict)
    # After altering, cache the contents to cache file.
    shift_plan_cache.put_shift_plan_cache(self.roaster_dict, planID=self.id)                                      
    log.debug("Shift roaster plan for Team: " + self.roaster_dict['team'] + " has cached successfully")
            
  """
  Function for downloading contents to excel sheet.
  """
  def save_to_excel(self):
    _shiftPlan_inst= self.__createInstance__()
    if _shiftPlan_inst.check_excel_exists():
      from openpyxl import load_workbook
      import collections  # To Use Named Tuple :)
      _wb = load_workbook(self.excel_file)
      # Check if correct sheets exists else create new sheet.
      _shiftPlan_inst.check_excel_sheet_exists(wb_inst=_wb)
      _shiftPlan_inst.add_headers_to_sheet()
      for asso_id, asso in enumerate(self.associates):
        _shiftKeys= (
                asso_acc_key, asso_nacc_key, asso_eacc_key, asso_off_key, 
                asso_leave_key, asso_tcsh_key ) = (
                  '_'.join([asso, const.SHIFT_CATEGORY.ACC]),
                  '_'.join([asso, const.SHIFT_CATEGORY.NACC]),
                  '_'.join([asso, const.SHIFT_CATEGORY.EACC]),
                  '_'.join([asso, const.SHIFT_CATEGORY.OFF]),
                  '_'.join([asso, const.SHIFT_CATEGORY.LEAVE]),
                  '_'.join([asso, const.SHIFT_CATEGORY.TCS])
                )
        for _key in _shiftKeys:
          self.associates_plan[_key]= {int(_k): _v for _k, _v in self.associates_plan[_key].items() }
        print('Associate plan : -------- ' + {self.associate_plan}')
        _shiftPlan_inst.append_contents_to_excel(asso_id, 
                        self.associates_plan[asso_acc_key],
                        self.associates_plan[asso_nacc_key],
                        self.associates_plan[asso_eacc_key],
                        self.associates_plan[asso_off_key],
                        self.associates_plan[asso_leave_key],
                        self.associates_plan[asso_tcsh_key])
        
  @classmethod
  def from_shift_plan_cache(cls, shift_plan_id):
    shift_plan_data = shift_plan_cache.get_shift_plan_cache(shift_plan_id)
    return cls(**shift_plan_data)
