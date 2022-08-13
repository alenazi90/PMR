from webapp import app
from flask import g
import psycopg2, psycopg2.extras, psycopg2.pool
from webapp import users, systems ,assets, engagements, reports,  user, settings

@app.before_request
def before_request():
  if not hasattr(g, 'db'):
    g.db = psycopg2.connect(app.config['webapp_database_uri'])
    g.users 		= users.Users(g.db)
    g.systems  		= systems.Systems(g.db)
    g.assets  		= assets.Assets(g.db)
    g.engagements 	= engagements.Engagements(g.db)
    g.reports 		= reports.Reports(g.db)
    g.settings		= settings.Settings(g.db)

@app.teardown_request
def teardown_request(exception):
  pass

@app.teardown_appcontext
def teardown_app(error):
    if hasattr(g, 'db'):
        g.db.close()
