import psycopg2
import psycopg2.extras
from datetime import datetime

class Systems(object):

  def __init__(self, db):
    self.db = db
    self._db = db
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)


  def delete(self, id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("DELETE from systems WHERE id = %s", (id,))
      self.cur.execute("DELETE from web_assets WHERE  system_id = %s", (id,))
      self.cur.execute("DELETE from network_assets WHERE system_id = %s", (id,))
      self.db.commit()
    except IndexError:
      return None
    finally:
      self.cur.close()



  def isConfirmed(self,id, user_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select confirmed from systems where id=%s AND user_id=%s",(id, user_id))
      rows = self.cur.fetchall()
      return rows[0][0]
    finally:
      self.cur.close()


  def count(self,user_id,cid=None):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      if cid:
        self.cur.execute("select count(id) from systems where user_id=%s AND customer_id=%s",(user_id,cid))
      else:
        self.cur.execute("select count(id) from systems where user_id=%s",(user_id,))
      rows = self.cur.fetchall()
      return rows[0][0]
    finally:
      self.cur.close()

  def get_systems(self):
    try:
      self.cur.execute("SELECT * FROM systems")
      rows = self.cur.fetchall()
      return rows
    finally:
      self.cur.close()

  def get_system(self,id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT * FROM systems where id = %s ", (id,))
      rows = self.cur.fetchall()
      return dict(rows[0])
    except IndexError:
      return None
    except Exception:
      return None
    finally:
      self.cur.close()

  def create(self, name, severity, contact_name, contact_email,department):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("INSERT INTO systems (name, severity, contact_name, contact_email,department) VALUES (%s, %s, %s, %s, %s) RETURNING ID" ,  ( name, severity, contact_name, contact_email,department ))
      id = self.cur.fetchone()[0]
      self.db.commit()
      return {"status":"success", "id":id}
    except psycopg2.Error as e:
      self.db.rollback()
      print(e)
      return {"status":"faild", "id": "NA"}
    finally:
      self.cur.close()



  def edit(self, name, severity, contact_name, contact_email,department , id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("update systems  set name=%s, severity=%s, contact_name=%s, contact_email=%s , department=%s WHERE id = %s ", (name, severity, contact_name, contact_email,department , id))
      self.db.commit()
      return {"status":"success"}
    except psycopg2.Error as e:
      self.db.rollback()
      print(e)
      return {"status":"faild"}
    finally:
      self.cur.close()


