"""
Copy Rights, All Rights Reserved 2020
File name: run.py

Description : Excecutes the shft-load script based on associates shift pla given by user.

Code Changes:
Modified by: Ganapathy R 

"""

import sys
import datetime
import argparse
import os
from shift_load_excel import ACCShiftPlan
sys.path.appened('C://ctpt//app-shift-mgnt')
import util

log = utill.get_logger_obj()
proj_dir = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]
script_params = ['CTPT','CTOC']

def main():
    asso_list = []
    asso_acc_list = []
    asso_off_list = []
    #Required shift plan params.
    month = input('Enter The month:(As month name')')
    year = input('Enter The Year')
    shore = input('Enter the Shore : (OACC/NACC/ACC): ')
    asso_num = int(input(f'Enter the number of associates in your team'))

    # Do Args parsing
    opr_param = "".join(script_params)
    scipt_usage = "usage pythonshift_run.py --teamName=" = +opr_param
    # This tiny function will return the respective module's Load function
    
    # if matching job module not found  then returns None
    get_script_dict = lamda teamName: ACCShiftPlan(asso_list, asso_acc_list,asso_off_list,teamName,month,year,shore,asso_num) if teamName else None
    
    parser = argparse.ArgumentParser(prog=__file__,description="scripts collects associate shift plan from user and loads onto excel",usage=script_usage)
    parser.add_argument("--teamName", required=True, help= "For Instance, You can give team name:%s."%(opr_param))
    
    args = parser.parse_args()
    load_script_fn = get_script_dict(args.teamName)
    for _n in range(1, asso_num+1):
        associate_name= input(f'ASSOCIATE NUM: {_n},ASSOCIATE NAME: ')
        print('*'*100)
        asso_plan = input('Enter the shift plan for ACC Coverage: \n' + 'Usage <day>:0/<day>:L \n')
        print('*'*100)
        asso_list.append(associate_name)
        log,debug('associates : ' + str(asso_list))
        asso_acc_list.appened(acc_plan)
        asso_off_list.append(off_plan)
    #  Validate if function call is correct
    if not load_script_fn:
        log.error(f'Invalid jobtype. given jobtype is {args.teamName}')
        sys.exit(1)

    if args.teamName:
        # check if the excel sheet already exists. if not create new one.
        if load_script_fn.check_excel_exists():
            load_script_fn.add_headers_to_sheet()
            for asso_id, asso in enumerate(asso_list):
                load_script_fn.append_contents_to_excel(asso_id)



if __name__ == '__main__':
    main