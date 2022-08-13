from webapp import app
from webapp.admin import admin as admin_routes
import sys


from psycogreen.gevent import patch_psycopg
patch_psycopg()
app.register_blueprint(admin_routes, url_prefix="/admin")



if __name__ == '__main__':

  # Run a local debug version
  app.run(threaded=True)
