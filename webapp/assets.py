import psycopg2
import psycopg2.extras
from datetime import datetime

class Assets(object):

  def __init__(self, db):
    self.db = db
    self._db = db
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)


  def delete_asset(self,  system_id, asset, type):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      if type == 'web':
        self.cur.execute("DELETE from web_assets WHERE fqdn = %s AND system_id = %s", (asset,system_id))
      elif type == 'network':
        self.cur.execute("DELETE from network_assets WHERE ip = %s AND system_id = %s", (asset,system_id))
      self.db.commit()
    except IndexError:
      return None
    finally:
      self.cur.close()

  def get_web_count(self,system_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select count(system_id) from web_assets where system_id=%s",(system_id,))
      rows = self.cur.fetchall()
      return rows[0][0]
    finally:
      self.cur.close()


  def get_network_count(self,system_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select count(system_id) from network_assets where system_id=%s",(system_id,))
      rows = self.cur.fetchall()
      return rows[0][0]
    finally:
      self.cur.close()



  def get_all(self,system_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT fqdn FROM web_assets where system_id = %s ", (system_id,))
      web = self.cur.fetchall()
      self.cur.execute("SELECT ip FROM network_assets where system_id = %s ", (system_id,))
      network = self.cur.fetchall()
      return {"urls": [x['fqdn'] for x in web ] , "ips": [ x['ip'] for x in network] }
    finally:
      self.cur.close()




  def get_web_assets(self,system_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT * FROM web_assets where system_id = %s ", (system_id,))
      rows = self.cur.fetchall()
      return rows
    finally:
      self.cur.close()


  def get_network_assets(self,system_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT * FROM network_assets where system_id = %s ", (system_id,))
      rows = self.cur.fetchall()
      return rows
    finally:
      self.cur.close()

  def add_fqdn(self, fqdn, system_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("INSERT INTO web_assets (fqdn,system_id) VALUES ( %s, %s) " ,  (fqdn,system_id))
      self.db.commit()
      return {"status":"success"}
    except psycopg2.Error as e:
      self.db.rollback()
      print(e)
      return {"status":"faild"}
    finally:
      self.cur.close()


  def add_ip(self, ip, system_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("INSERT INTO network_assets (ip, system_id) VALUES ( %s, %s) " ,  (ip,system_id))
      self.db.commit()
      return {"status":"success"}
    except psycopg2.Error as e:
      self.db.rollback()
      print(e)
      return {"status":"faild"}
    finally:
      self.cur.close()



  def update(self):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("update systems  set name=%s, severity=%s, contact_name=%s, contact_email=%s , department=%s WHERE id = %s AND user_id=%s", (name, severity, contact_name, contact_email,department , id))
      self.db.commit()
      return {"status":"success"}
    except psycopg2.Error as e:
      self.db.rollback()
      print(e)
      return {"status":"faild"}
    finally:
      self.cur.close()


