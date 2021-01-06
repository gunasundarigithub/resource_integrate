"""
File name: app.py
Description: Execution start of App. That routes to flask APIs through blueprints (just like components)

Change Log:
Release Date    Revision Date   Changes By      Description
------------    -------------   ----------      -----------
                July 2020       Sabarish AC     Initial
                August 2020     Ganapathy R     Code Updation & Refraction
"""
# External Modules.
from flask import Flask, render_template, abort, request
from flask_login import LoginManager
from flask_bootstrap import Bootstrap 
import sys
sys.path.append('E:\\Sabs Learning\\resource_integrate')
# Internal Modules.
from util import util
from backend import shift_load_excel

ap_config = util.get_conf()

#Initiate flask framework Internal DB
# db = SQLALchemy()
login_manager = LoginManager()

def create_app(env):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'SABARISHAC'
    #app.config.from_object(app_config['app'])

    Bootstrap(app)
    # Implement Error Handling pages here while accessing the pages.
    # 403 - Forbidden.

    """
    @app.errorhandler(403)
    def throw_forbidden(error):
        return render_template(app_config['templates']['forbidden'], title='Forbidden Access'), 403
    """
    # 404 - Page Not Found 
    @app.errorhandler(404)
    def throw_page_not_found(error):
        return render_template(app_config['templates']['page_not_found'], title='page_not_found'), 404

    """
    500 Internal Server Erro.
    @app.errorhandler(500)
    def throw_server_error(error):
        return render_template(app_config['templates']['internal_server_error'], title='internal_server_error'), 500
    """
    @app.route('/home')    # www.appshiftmgnt.com/home
    def home_page():
        return render_template('login.html')

    # Import all necessary blueprints.
    # Blueprint for short, can help you structure your flask application by grouping its functionality into reusable components.
    import models 
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from shiftDashboard import shift_dashboard as shiftDashboard_blueprint
    app.register_blueprint(shiftDashboard_blueprint)

    # Intialize authentication setup for this app.
    login_manager.init_app(app)
    #Login_manager.Login_message = "Sorry!!" You must be. Logged into access this page!!"
    #Login_manager.Login_view = "auth."

    @app.route('shift_plan/<month>', methods=['GET', 'POST'])
    def process_excel_contents(month):
        pass

    return app

if __name__ == '__main__':
    import os
    env = os.getenv('FLASK_CONFIG')
    app = create_app(env)
    app.run(port=1793)