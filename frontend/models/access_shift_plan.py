__author__ = 'Sabarish AC'
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
    self.id = uuid.uuid4().hex if id is None else id
    
    
    
  def __createInstance__(self):
    _instance = shift_load_excel.ACCShiftPlan(self.associates, self.team, self.month, self.year, self.shore)
    return _instance
  
  def key_generator(self):
    for _plan in self.associates_plan:
      yield _plan
      
      
  def alter_roaster_plan_dict(self):
    for _plan_key in self.key_generator():
      if const.SHIFT_CATEGORY.ACC in _plan_key:
        _key = [int(shft_date.split('-')[0]) for shft_date in self.associates_plan[_plan_key].split(',') if shft.date.split('-')[0].isdigit()]
        self.associates_plan[_plan_key]= dict(zip(_key, ['A']*len(_key)))
        self.associates_plan[_plan_key]= {int(_k): _v for _k, _v in self.associates_plan[_plan_key].items() }
        
      elif const.SHIFT_CATEGORY.OFF in _plan_key:
        _key = [int(shft_date.split('-')[0]) for shft_date in self.associates_plan[_plan_key].split(',') if shft.date.split('-')[0].isdigit()]
        self.associates_plan[_plan_key]= dict(zip(_key, ['O']*len(_key)))
        self.associates_plan[_plan_key]= {int(_k): _v for _k, _v in self.associates_plan[_plan_key].items() }
        
      elif const.SHIFT_CATEGORY.LEAVE in _plan_key:
        _key = [int(shft_date.split('-')[0]) for shft_date in self.associates_plan[_plan_key].split(',') if shft.date.split('-')[0].isdigit()]
        self.associates_plan[_plan_key]= dict(zip(_key, ['L']*len(_key)))
        self.associates_plan[_plan_key]= {int(_k): _v for _k, _v in self.associates_plan[_plan_key].items()}
      
      elif const.SHIFT_CATEGORY.TCS in _plan_key::
        _key = [int(shft_date.split('-')[0]) for shft_date in self.associates_plan[_plan_key].split(',') if shft.date.split('-')[0].isdigit()]
        self.associates_plan[_plan_key]= dict(zip(_key, ['H']*len(_key)))
        self.associates_plan[_plan_key]= {int(_k): _v for _k, _v in self.associates_plan[_plan_key].items() }
        
def get_shift_plan_team(self,teamName):
  _team_plan = shift_pln_cache.get_shift_plan_cache(teamName)
  if isinstance(_team_plan, list):
    log.debug(f"Overall cached shift plan for the team : {self.team} - {_team_plan}")
    return _team_plan
  
def cache_roaster_plan(self):
  self.alter_roaster_plan_dict()
  self.roaster_dict['associates_plan'] = self.associates_plan
  log.debug(f"Altered Roaster dict: {self.roaster_dict}")
  shift_plan_cache.put_shift_plan_cache(self.roaster_dict, planID=self.id)                                      
  #log.debug(f"Shift roaster plan for Team:{self.roaster_dict['team']} has cached successfully")
            
def save_to_excel(self):
  _shiftPlan_inst= self.__createInstance__()
  if _shiftPlan_inst.check_excel_exists():
    _shiftPlan_inst.add_headers_to_sheet()
    for asso_id, asso in enumerate(self.associates):
      _shiftKeys= (asso_acc_key, asso_off_key, asso_leave_key, asso_tcsh_key) = ('_'.join([asso, const.SHIFT_CATEGORY.ACC]),
                                                                                 '_'.join([asso, const.SHIFT_CATEGORY.OFF]),
                                                                                 '_'.join([asso, const.SHIFT_CATEGORY.LEAVE]),
                                                                                 '_'.join([asso, const.SHIFT_CATEGORY.TCS]))
      for _key in _shiftKeys:
        self.associates_plan[_key]= {int(_k): _v for _k, _v in self.associates_plan[_key].items() }
      print(f'Associate plan : --------{self.associate_plan}')
      _shiftPlan_inst.append_contents_to_excel(asso_id, self.associates_plan[asso_acc_key],
                                               self.associates_plan[asso_off_key],
                                               self.associates_plan[asso_leave_key],
                                               self.associates_plan[asso_tcsh_key])
      

      
@classmethod
def from_shift_plan_cache(cls, shift_plan_id):
  shift_plan_data = shift_plan_cache.get_shift_plan_cache(shift_plan_id)
  return cls(**shift_plan_data)
