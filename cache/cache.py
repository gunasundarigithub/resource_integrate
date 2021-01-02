"""
File name: cache.py
Description: Handles Caching . Caches user Auth Details, shift plan details to cache file( instead of DB)

Change Log:
Release Date    Revision Date   Changes By      Description
------------    -------------   ----------      -----------
                July 2020       Sabarish AC     Initial
                August 2020     Ganapathy R     Code Updation & Refraction
"""
import datetime
import json
import logging
import os
import sys
#sys.path.append('E:\\Sabs Learning\\resource_integrate') # Note: Please specify your local/server path when working/deploying respectively.
from util import util

log = util.get_logger_obj()
conf = util.get_conf()

class CacheFile:    
    now = datetime.datetime.now()
    cache = {}
    user_auth = []
    shift_plan = []
    team_year_list = []

    def __init__(self, location):
        self.location = location

    def put_user_cache(self, create_date, email, username, pwd, team, userid):
        """
        Appends a user authentication details to the cache file
        :param key:    
        :param document:
        :return:
        """
        try:
            # Perform Concatenation with parent directory with cache file.
            user_cache_file = ''.join([conf['app']['cache_location'], self.location])
            self.cache['date'] = create_date
            self.cache['email'] = email
            self.cache['username'] = username
            self.cache['password'] = pwd.decode('UTF-8') # password encrypted
            self.cache['email'] = email
            self.cache['team'] = team.upper()
            self.cache['userid'] = userid
            if not os.path.isfile(user_cache_file):
                self.user_auth.append(self.cache)
                with open(user_cache_file, mode='w') as f_wr:
                    f_wr.write(json.dumps(self.user_auth, indent=True))
            else:
                with open(user_cache_file, mode='r') as f_rd:   
                    user_auth_list = json.load(f_rd)
            user_auth_list.append(self.cache)
            with open(user_cache_file, mode='w') as s_wr:
                s_wr.write(json.dumps(user_auth_list, indent=True))
            # Now Cache the Team Members to Team-Members.json file to save the each team members.
        except Exception as e:
            log.error('Exception occured while saving to User Auth cache')
            log.error(e, exc_info=True)
 
    def get_user_cache(self, emailId):
        """
        Get user authenticate from cache file. Each line in a JSON document which gets 
        unmarshalled to python dictionary
        :retun: Return the list of dict
        """
        try:
            docs = []
            # Perform Concatenation to parent directory with cache file.
            user_cache_file = ''.join([conf['app']['cache_location'], self.location])
            if os.path.isfile(user_cache_file):
                with open(user_cache_file, "r") as f:
                    fc= f.read()
                    if fc:
                        docs = json.loads(fc)
                        log.debug("Fetching details from cache....")
                        fetch_user = list(filter(lambda doc: doc['email']==emailId, docs))
                        if fetch_user:
                            return fetch_user[0]
                        return fetch_user
                    else:
                        log.error("No registered users found in user cache! Empty file....")
            else:
                log.error("Error 404, User Auth Cache file: " + self.location + " not found")        

        except Exception as e :
            log.error('Exception occured while reading from User Auth Cache.')
            log.error(e, exc_info=True)
        return docs

    def put_shift_plan_cache(self, roaster_dict, planId=''):
        """
        Appends a Team shift roaster plan to the cache file
        :param key:
        :param document:
        :return:
        """
        try:
            # Perform Concatenation on cache file with correct team name.
            team_cache_file = '-'.join([roaster_dict['team'], self.location])
            self.cache['date'] = self.now.strftime('%y-%m-%d') 
            self.cache['planId'] = planId
            self.cache['month'] = roaster_dict['month']
            self.cache['shore'] = roaster_dict['shore']
            self.cache['year'] = roaster_dict['year']
            self.cache['team'] = roaster_dict['team']
            self.cache['associates'] = roaster_dict['associates']
            self.cache['associates_plan'] = roaster_dict['associates_plan']
            # Find the cache file by concatenating the parent directory with cache file.
            if not os.path.isfile(''.join([conf['app']['cache_location'], team_cache_file])):
                self.shift_plan.append(self.cache)
                with open(''.join([conf['app']['cache_location'], team_cache_file]), mode='w') as f_wr:
                    f_wr.write(json.dumps(self.shift_plan, indent=True))

            else:
                # if cache file exists with contents then append it.
                with open(''.join([conf['app']['cache_location'], team_cache_file]), mode='r') as f_rd:
                    shift_plan_list = json.load(f_rd)
                shift_plan_list.append(self.cache) 
                with open(''.join([conf['app']['cache_location'], team_cache_file]), mode ='w') as s_wr:
                    s_wr.write(json.dumps(shift_plan_list, indent=True)) 

        except Exception as e :
            log.error('Exception occured while saving to Roaster Cache')
            log.error(e, exc_info=True)

    """
    Function to remove month shift plan from the cached file.
    """
    def deleteMonthPlan(self, month, teamName):
        try:
            docs = []
            # Perform concatenation on cache file with correct team name.
            team_cache_file = '-'.join([teamName, self.location])
            # Find the cache file by concatenation the parent directory with cache file.
            if os.path.isfile(''.join([conf['app']['cache_location'], team_cache_file])):
                with open(''.join([conf['app']['cache_location'], team_cache_file])) as fread:
                    fc = fread.read()
                    if fc:
                        docs = json.loads(fc)
                        if docs:
                            # Using list comprehension to remove required shift month plan.
                            docs_updated = [ tp for tp in docs if tp['month']!=month.upper() ]
                            with open(''.join([conf['app']['cache_location'], team_cache_file]), mode='w') as f_wr:
                                f_wr.write(json.dumps(docs_updated, indent=True))
                    else:
                        log.debug("No contents are present in cache: " + team_cache_file)
        except Exception as ex:
            log.error("Exception occured while deleting " + month + " month plan for the team " + teamName)
            log.error(ex, exc_info=True)

    def get_shift_plan_cache(self, teamName, shift_month='', shift_year=''):
        """
        Gets Associated shift plan        
        from cache file. Each line is a JSON document, which gets
        unmarshalled to python dictionary.

        :return: Returns a list of dict
        """
        try:
            docs =[]
            # Perform concatenation on cache file with correct team name.
            team_cache_file = '_'.join([teamName, self.location])
            # Find the cache file by concatenating the parent directory with cache file.
            if os.path.isfile(''.join([conf['app']['cache_location'], team_cache_file]), "r"):
                with open(''.join([conf['app']['cache_location'], team_cache_file]), "r") as f_rd:
                    fc = f_rd.read()
                    if fc:
                        docs = json.loads(fc)
                        log.debug("Fetching details from cache... " + docs)
                        print('month: ----------------------', shift_month)
                        if docs:
                            for team_plan in docs:
                                if team_plan['team']==teamName:
                                    if shift_month:
                                        fetch_shift_roaster_month = list(filter(lambda doc: doc['month']==shift_month, docs))
                                        if fetch_shift_roaster_month:
                                        # Fetch shift roaster plan for a particular month if shift_month is set
                                            return fetch_shift_roaster_month[0]
                                        else:
                                            return None
                            # If 'shift_month' is not set, return all the shift roaster records of the team.
                            else:
                                fetch_shift_roaster_month = list(filter(lambda doc: doc['team']==teamName, docs))
                                return fetch_shift_roaster_month
                        else:
                            log.debug('Team ' + teamName + ' roaster plan is not present in cache.')
                    else:
                        log.debug('No contents are present in cache ' + team_cache_file)
            else:
                log.error('Error 404, shift roaster cache file: ' + self.location + ' not found')
            return docs

        except Exception as e:
            log.error('Exception occured while reading from roaster cache.') 
            log.error(e, exc_info=True)                       

    """
    Function to fetch team members dynamically based on users registration.
    """
    def cache_team_members(self, user_cache_file, team):
        try:
            import json
            _members = {}
            # Perform concatenation on parent directory with cache file.
            team_members_cache_file = ''.join([conf['app']['cache_location'], conf['app']['team_members_cache_file']])
            if os.path.isfile(user_cache_file):
                with open(user_cache_file, "r") as f_rd:
                    fc = f_rd.read()
                    if fc:
                        usr_cache = json.loads(fc)
                        team_filtered = list(filter(lambda soc: doc['team']==team, usr_cache))
                        # Filter out Team Members based on teamself.
                        _members.update({team: [(usr_info['username']) for usr_info in team_filtered ]})
                        # Now Add the contents to the Team-Members JSON file.
                        if not os.path.isfile(team_members_cache_file):
                            with open(team_members_cache_file, mode='w') as f_wr:
                                f_wr.write(json.dumps(_members, indent=True))
                        else:
                            with open(team_members_cache_file, mode='r') as f_rd:
                                team_members = json.load(f_rd)
                            team_members.update({
                                team: [usr_info['username'] for usr_info in team_filtered ]
                            })
                            with open(team_members_cache_file, mode='w') as s_wr:
                                s_wr.write(json.dumps(team_members, indent=True))
                    else:
                        log.error("No user registered!, No contents present in the user cache " + user_cache_file)
        except Exception as e:
            log.error('Exception occurred while saving to Team-Members cache.')
            log.error(e, exc_info=True)

    """
    Function to get the Team-Members cache contents.
    """
    def get_team_members_cache(self, teamName):
        try:
            docs = []
            # Perform concatenation on parent directory with cache file.
            team_cache_file = ''.join([conf['app']['cache_location'], conf['app']['team_members_cache_file']])
            if os.path.isfile(team_cache_file, "r"):
                with open(team_cache_file, 'r') as f_rd:
                    fc = f_rd.read()
                    if fc:
                        docs = json.loads(fc)
                        log.debug('docs of team members ' + docs)
                        log.debug('Fetching details from Team-Members Cache.... ' + docs)
                        fetch_team_members = [
                            docs[team] for team in docs if teamName in team
                        ]
                        if fetch_team_members:
                            return fetch_team_members[0]
                        else:
                            log.debug('Team ' + teamName + ' is not found in Team-Members Cache..')
                            return None
                    else:
                        log.error('Empty Team-Members cache file')
            else:
                log.error('Error 404, User Auth Cache file ' + team_cache_file + ' not found')
        except Exception as e:
            log.error('Exception occurred while reading from Team-Members cache.')
            log.error(e, exc_info=True)