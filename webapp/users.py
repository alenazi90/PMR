import psycopg2
import psycopg2.extras
from flask import g
from webapp import app
from flask_bcrypt import Bcrypt
from psycopg2 import IntegrityError
import random, string
import hashlib, json
from os import urandom


class Users(object):
  def __init__(self, db):
    self.db = db
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)


  def is_active(self,user_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select status from users where id=%s",(user_id,))
      rows = self.cur.fetchall()
      return rows[0][0]
    finally:
      self.cur.close()


  def add_new_user(self, email, name,  job_title, phone, created_by, admin, type, change_password):
    cur = self.db.cursor()
    g.bcrypt = Bcrypt(app)
    randpwd1 = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(5))
    randpwd2 = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(8))
    ranpwd = randpwd1 + "@Default!" + randpwd2
    ranpwd = 'D3fault'
    password = g.bcrypt.generate_password_hash(ranpwd).decode('utf-8')
    try:
      cur.execute("INSERT INTO users (email, name, phone, job_title,password,created_by,admin,type,change_password) VALUES (lower(%s),%s,%s,%s,%s,%s,%s,%s,%s)", (email, name,  phone, job_title,password,created_by,admin, type, change_password))
      self.db.commit()
      return {"status":"User has been added","pwd":ranpwd}
    except IntegrityError as e:
      if e.pgcode == '23505':
        return {"status":"Email address already exists"}
      else:
        return {"status":"Integrity Error"}

    finally:
      cur.close()



  def get(self, id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT * FROM users where id = %s", (id,))
      rows = self.cur.fetchall()
      return dict(rows[0])
    finally:
      self.cur.close()


  def update_all(self, id, name, email, phone,title,type):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("UPDATE users set name=%s, phone=%s, email=%s,job_title=%s, type=%s WHERE id = %s", (name, phone, email,title,type, id))
      self.db.commit()
      return {'status':'updated'}
    finally:
      self.cur.close()

  def update(self, id, name, email, phone,title=None,type=None):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      if title:
        self.cur.execute("UPDATE users set name=%s, phone=%s, email=%s,job_title=%s, type=%s WHERE id = %s", (name, phone, email,title,type, id))
      else:
        self.cur.execute("UPDATE users set name=%s, phone=%s, email=%s WHERE id = %s", (name, phone, email, id))
      self.db.commit()
      return {'status':'updated'}
    finally:
      self.cur.close()



  def get_all(self):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT * FROM users order by created_at DESC")
      rows = self.cur.fetchall()
      return rows
    finally:
      self.cur.close()




  def update_password(self, id, pwd):
    cur = self.db.cursor()
    g.bcrypt = Bcrypt(app)
    password = g.bcrypt.generate_password_hash(pwd).decode('utf-8')

    try:
      cur.execute("UPDATE users set password = %s WHERE id = %s", (password,id))
      self.db.commit()
      return
    finally:
      cur.close()



  def change_user_password(self, email, pwd):
    cur = self.db.cursor()
    g.bcrypt = Bcrypt(app)
    password = g.bcrypt.generate_password_hash(pwd).decode('utf-8')

    try:
      cur.execute("UPDATE users set password = %s WHERE email = %s", (password,email))
      self.db.commit()
      return
    finally:
      cur.close()



  def activate_user(self, id):
    cur = self.db.cursor()
    try:
      cur.execute("UPDATE users set status = 'active' WHERE id = %s", (id,))
      self.db.commit()
    finally:
      cur.close()

  def suspend_user(self, id):
    cur = self.db.cursor()
    try:
      cur.execute("UPDATE users set status = 'inactive' WHERE id = %s", (id,))
      self.db.commit()
    finally:
      cur.close()



  def delete_user(self, id):
    cur = self.db.cursor()
    try:
      cur.execute("DELETE from users WHERE id = %s", (id,))
      self.db.commit()
    finally:
      cur.close()

  def deactivate_user(self, id):
    cur = self.db.cursor()
    try:
      cur.execute("UPDATE users set status = 'inactive' WHERE email = %s", (email,))
      self.db.commit()
    finally:
      cur.close()

  def _activate_user(self, email):
    cur = self.db.cursor()
    try:
      cur.execute("UPDATE users set status = 'active' WHERE email = %s", (email,))
      self.db.commit()
    finally:
      cur.close()

