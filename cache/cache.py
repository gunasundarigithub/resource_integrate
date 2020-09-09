"""
File name: cache.py
Description: Handles Caching . Caches user Auth Details , shift plan details to cache file( instead of DB)

Changes by : Ganapathy R
"""
import datetime
import json
import logging
import os
import sys
sys.path.append('C://ctpt//app-shift-mgnt')
from util import util

log = utill.get_logger_obj()

class CacheFile:
    
    now = datetime.datetime.now()
    cache = {}
    user_auth = []
    shift_plan = []

    def __init__(self, location):
        self.location = location

    def put user_cache(self, create_date, email, username, pwd, team, userid):
        """
        Appends a user authentication details to the cache file
        :param key:    
        :param document:
        :return:
        """

        try:
            self.cache['date'] = create_date
            self.cache['email'] = email
            self.cache['username'] = username
            self.cache['password'] = pwd.decode('UTF-8') # password encrypted
            self.cache['email'] = email
            self.cache['team'] = team.upper()
            self.cache['userid'] = userid
            if not os.path.isfile(self.location):
                self.user_auth.append(self.cache)
                with open(self.location, mode='w') as f_wr:
                    f_wr.write(json.dumps(self.user_auth, indent=True))
            else:
                with open(self.location, mode='r') as f_rd:   
                    user_auth_list = json.load(f_rd)
            user_auth_list.append(self.cache)
            with open(self.location, mode='w') as s_wr:
                s_wr.write(json.dumps(user_auth_list, indent=True))

        except Exception as e:
            log.error('Exception occured while saving into cache')
            log.error(e, exc_info=True)
 
    def get_user_cache(self, emailId):
        """
        Get user authenticate from cache file. each lne in a JSON document which gets 
        unmarshalled to python dictionary
        :retun: Return the list of dict
        """

        try:
            docs = []
            if os.path.isfile(self.location):
                with open(self.location, "r") as f:
                    fc= f.read()
                    if fc:
                        docs = json.loads(fc)
                        logs.debug("Fetching details from cahce")
                        fetch_user = list(filter(lambda doc: doc['email']==emaiId),docs))
                        if fetch_user:
                            return fetch_user[0]
                        return fetch_user
                    else:
                        log.error(f"Error 404, User Auth Cache file: {self.location} not found")        

        except Exception as e :
            log.error('Exception occured while reading from cache file')
            log.error(e, exc_info=True)

    def put_shift_plan_cache(self, roaster_dict, planId=''):
        """
        Appends a Team shift roaster plan to the cache file
        :param key:
        :param document:
        :return:
        """
        try:
            self.cache['date'] = self.now.strftime('%y-%m-%d') 
            self.cache['planId'] = planId
            self.cache['month'] = roaster_dict['month']
            self.cache['shore'] = roaster_dict['shore']
            self.cache['year'] = roaster_dict['year']
            self.cache['team'] = roaster_dict['team']
            self.cache['associates'] = roaster_dict['associates']
            self.cache['associates_plan'] = roaster_dict['associates_plan']

            if not os.path.isfile(self.location):
                self.shift_plan.append(self.cache)
                with open(self.location, mode='w') as f_wr:
                    f_wr.write(json.dumps(self.shift_plan, indent=True))

            else:
                # if cache file exists with contents then append it.

                with open(self.location, mode='r') as f_wd:
                    shift_plan_list = json.load(f_rd)
                shift_plan_list.append(self.cache) 
                with open(self.location, mode ='w') as s_wr:
                    s_wr.write(json.dumps(shift_plan_list, indent=True)) 

        except Exception as e :
            log.error('Exception occured while saving to cache')
            log.error(e, exc_info=True)

    def get_shift_plan_cache(self, shift_month=''):

        """
        Gets Associated shift plan        
        from cache file. Each line is a JSON document, which gets
        unmarshalled to python dictionary.

        :return: Returns a list of dict
        """

        try:
            docs =[]
            if os.path.isfile(self.location):
                with open(self.location,"r") as f:
                    fc = f.read()
                    if fc:
                        docs = json.loads(fc)
                        log.debug(f"Fetching details from cache...{docs}")
                        print('month: ----------------------', shift_month)
                        if shift_month and docs:
                            fetch_shift_roaster_month = list(filter(lambda doc: doc['month']==shift_month,docs))
                            # fetch shift roaster plan for a particular month if shift_month is set
                            return fetch_shift_roaster_month[0]
                            # If 'shift_month' is not set, return all the shift roaster records of the team.

                        else:
                            log.error(f'Error 404, shift roaster cache file: {self.location} not found ')
                        return docs

        except Exception as e:
            log.error('Exception occured while reading from cache file .') 
            log.error(e,exc_info=True)                       











            



                           















