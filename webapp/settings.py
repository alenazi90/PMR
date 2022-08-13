from flask import g
from webapp import app
import psycopg2
import psycopg2.extras


class Settings(object):
  def __init__(self, db):
    self.db = db
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

  def get(self):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT * FROM report_format")
      rows = self.cur.fetchall()
      return dict(rows[0])
    except IndexError:
      return None
    finally:
      self.cur.close()


  def get_logo(self):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT logo FROM report_format")
      rows = self.cur.fetchall()
      return dict(rows[0])
    except IndexError:
      return None
    finally:
      self.cur.close()

  def get_title(self):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT title FROM report_format")
      rows = self.cur.fetchall()
      return dict(rows[0])
    except IndexError:
      return None
    finally:
      self.cur.close()



  def update(self, logo, title, company_name, sections):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("UPDATE report_format set  logo=%s, title=%s, company_name=%s, sections=%s", (logo,title,company_name, sections))
      self.db.commit()
      return {'status':'updated'}
    except IndexError:
      return None
    finally:
      self.cur.close()






