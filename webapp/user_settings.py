from flask import g
from webapp import app
import psycopg2
import psycopg2.extras


class UserSettings(object):
  def __init__(self, db):
    self.db = db
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

  def get(self, id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT * FROM user_settings where customer_id = %s", (id,))
      rows = self.cur.fetchall()
      return dict(rows[0])
    finally:
      self.cur.close()


  def get_logo(self, id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT logo FROM user_settings where customer_id = %s", (id,))
      rows = self.cur.fetchall()
      return dict(rows[0])
    finally:
      self.cur.close()


  def update(self, cr, logo, vat_no, branch_name, address, phone, email, customer_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("UPDATE user_settings set cr=%s, logo=%s, vat_no=%s, branch_name=%s, address=%s, phone=%s, email = %s WHERE customer_id = %s", (cr, logo, vat_no, branch_name, address, phone, email, customer_id))
      self.db.commit()
      return {'status':'updated'}
    finally:
      self.cur.close()


  def create(self, user_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("INSERT INTO user_settings (customer_id) VALUES (%s)" ,  ( user_id,))
      self.db.commit()
      return {"status":"success"}
    except psycopg2.Error as e:
      self.db.rollback()
      print(e)
      return {"status":"faild"}
    finally:
      self.cur.close()


