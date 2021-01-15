"""
File name: user.py
Description: User backend functionality to cache user details on the cache json file as DB.

Change Log:
Release Date    Revision Date   Changes By      Description
------------    -------------   ----------      -----------
                July 2020       Sabarish AC     Initial
"""
# ------------------------------------------- Built-In Modules --------------------------------------------------------------------
from flask import session, redirect, url_for
import uuid
import sys
from datetime import datetime

# ------------------------------------------- Customized Modules --------------------------------------------------------------------
sys.path.append('E:\\Sabs Learning\\resource_integrate\\cache')
sys.path.append('E:\\Sabs Learning\\resource_integrate\\util')
from crypto_parser import ShiftPlanCrypto
from cache import CacheFile
import util

const = util.util.excelConstants
config = util.util.get_conf()
log = util.util.get_logger_obj()
user_cache_inst = CacheFile(config['app']['user_cache_file'])
crypto = ShiftPlanCrypto()
now = datetime.now()

class User(object):
  def __init__(self, email, password, username=None, team='CSE', date=now.strftime('%Y-%M-%d'), userID=None):
    self.email = email
    self.password = password
    self.username = username
    self.team = team
    self.date = date
    self.userID = uuid.uuid4().hex if userID is None else userID
    
  """
  Classmethod: Fetch user auth details by email.
  """
  @classmethod  
  def get_by_emailID(cls, emailID):
    user_auth = user_cache_inst.get_user_cache(emailID)
    log.info('user_auth: ' + str(user_auth))
    if not isinstance(user_auth, (list)) and user_auth is not None:
      return cls(**user_auth)
    return None
  
  """
  Classmethod: Fetch user auth details by user-id.
  """
  @classmethod
  def get_by_userID(cls, userID):
    user_auth = user_cache_inst.get_user_cache(userID)
    if not user_auth:
      return cls(**user_auth)
  
  """
  Classmethod: Validate user by emailId and password.
  """
  @classmethod
  def validate_user_login(cls, emailID, pwd):
    user = cls.get_by_emailID(emailID)
    if user is not None:
      # Validate User Password.
      _dc_pwd = crypto.get_credentials(user.password, appname=config['app_name'])
      if _dc_pwd['pass']==pwd:
        # Once Authentication is validated, Add session cookie to the user.
        cls.login(emailID, user.username, user.team)
        return {'verify_username': True, 'verify_pass': True}
      else:
        return {'verify_username': True, 'verify_pass': False}
    else:
      # Validate Username.
      return {'verify_username': False, 'verify_pass': False}
    
  """
  Classmethod: Register user if not exists.
  """
  @classmethod
  def register(cls, emailId, username, team, pwd):
    user = cls.get_by_emailID(emailId)
    if user is not None or not user:
      # If user doesn't exist, add it to cache to register new user.
      new_reg_user = cls(emailId, pwd, username=username, team=team)
      # Get the encrypted password from Cryto Script (Secret-Key Encryption)
      _enc_pwd = crypto.do_encrypt(str(pwd))
      print('-------' + str(new_reg_user) + '-----------')
      user_cache_inst.put_user_cache(new_reg_user.date, emailId, username, _enc_pwd, team, new_reg_user.userID)
      session[const.SESSION_COOKIES.EMAIL] = emailId
      return True
    else:
      # User exists!!
      return False    
    
  # Note: In Flask, user need not handle cookies, its handled by flask by default.
  #       Flask sends cookies to the session that is secure and unique when the user 
  #       logs in to the app. User just needs to add session-id while logging in.

  """
  Staticmethod: Check if user is logged in based on flask.session param.
  """
  @staticmethod
  def login(emailID, username, team):
    # Session can be noted or set only if user auth validation is success. (validate_user_login)
    session[const.SESSION_COOKIES.EMAIL]= emailID
    session[const.SESSION_COOKIES.USERNAME]= username
    session[const. SESSION_COOKIES.TEAM]= team
    
  """
  Staticmethod: Logs out the user from the app.
  """
  @staticmethod
  def logout():
    session.pop(const.SESSION_COOKIES.EMAIL, None)
    session.pop(const.SESSION_COOKIES.USERNAME, None)
    session.pop(const. SESSION_COOKIES.TEAM, None)
    session.pop(const. SESSION_COOKIES.MONTH, None)
    session.pop(const. SESSION_COOKIES.EXCELFILE, None)
    return redirect(url_for('auth.user_login'))