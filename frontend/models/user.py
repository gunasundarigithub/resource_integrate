from flask import session, redirect, url_for
import uuid
import sys
from datetime import datetime
sys.path.append('C:\\ctpt\\app-shift-mgmt\\cache')
sys.path.append('Ç:\\ctpt\\app-shift-mgmt\\util')
from crypto import CacheFile
from cache import CacheFile
import util

const = util.util.excelConstats
config= util.util.get_conf()
log = util.util.get_logger_obj()
user_cache_inst = CacheFile(config['app']['user_cache_file'])
crypto= ShiftPlanCrypto()
now = datetime.now()

class User(object):
  def __init__(self, email, password, username=None, team='CSE', date=now.strftime('%Y-%M-%d'), userID=None):
    self.email=email
    self.password= password
    self.username = username
    self.team = team
    self.date= date
    self.userID= uuid.uuid4().hex if userID is None else userID
    
  @classmethod  
  def get_by_emailID(cls, emailID):
    user_auth = user_cache_inst.get_user_cache(emailID)
    log.info(f'user_auth:{user_auth}')
    if not isinstance(user_auth, (list)) and user_auth is not None:
      return cls(**user_auth)
    return None
  
  @classmethod
  def get_by_userID(cls, userID):
    user_auth= user_cache_inst.get_user_cache(userID)
    if not user_auth:
      return cls(**user_auth)
    
  
  @classmethod
  def validate_user_login(cls, emailID, pwd):
    user = cls.get_by_emailID(emailID)
    if user is not None:
      _dc_pwd = crypto.get_credentials(user.password, appname= config['app-name'])
      if _dc_pwd['pass']==pwd:
        cls.login(emailID, user.username, user.team)
        return {'verify_username': True, 'verify_pass': True}
      else:
        return {'verify_username': True, 'verify_pass': False}
    else:
      return {'verify_username': False, 'verify_pass': False}
    
  @classmethod
  def register(cls, emailID, username, team, pwd):
    user = cls.get_by_emailID(emailID)
    if user is not None or not user:
      new_reg_user = cls(emailID, pwd, username=username, team=team)
      _enc_pwd = crypto.do_encrypt(str(pwd))
      user_cache_inst.put_user_cache(new_reg_user.date, emailID, username, _enc_pwd, team, new_reg_user.userID)
      session[const.SESSION_COOKIES.EMAIL] =emailID
      return True
    else:
      return False
    
    
@staticmethod
def login(emailID, username, team):
  session[const.SESSION_COOKIES_EMAIL]= emailID
  session[const.SESSION_COOKIES.USERNAME]= username
  session[const. SESSION_COOKIES_TEAM]= team
  
@staticmethod
def logout():
  session.pop(const.SESSION_COOKIES_EMAIL, None)
  session.pop(const.SESSION_COOKIES.USERNAME, None)
  session.pop(const. SESSION_COOKIES_TEAM, None)
  session.pop(const. SESSION_COOKIES_MONTH, None)
  session.pop(const. SESSION_COOKIES_EXCELLIFE, None)
  return redirect(url_for('auth.user_login'))
