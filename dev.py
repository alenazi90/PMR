from webapp import app
from webapp.admin import admin as admin_routes
import sys
import logging

from psycogreen.gevent import patch_psycopg
patch_psycopg()
app.register_blueprint(admin_routes, url_prefix="/admin")




if __name__ == '__main__':

  port = int(sys.argv[1])
  app.config['app_base_url'] = "http://192.168.235.138:%s" % port
  app.config['webapp_database_uri'] = "dbname=ptdb host=127.0.0.1  user=pt"

  app.config["DEVELOPMENT"] = True
  logging.basicConfig(level=logging.DEBUG)

  # Run a local debug version
  app.run(host='0.0.0.0', debug=True, threaded=True, port=port)
