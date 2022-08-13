from flask import g
from flask_login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, AnonymousUserMixin,
                            confirm_login, fresh_login_required)
from flask import request
import psycopg2
import psycopg2.extras
from psycopg2 import IntegrityError

class User(UserMixin):
  def __init__(self, **kwargs):
      self.email = kwargs.get('email', None)
      self.name = kwargs.get('name', None)
      self.password = kwargs.get('password', None)
      self.phone = kwargs.get('phone', None)

      try:
        if request.headers.getlist("X-Forwarded-For"):
           self.ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
           self.ip = request.remote_addr
      except RuntimeError:
        self.ip = None

  def validate_password(self, password):
    v = g.bcrypt.check_password_hash(self.password, password)
    return v


  def save(self):
    cur = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
    try:
      pw_hash = g.bcrypt.generate_password_hash(self.password).decode('utf-8')
      cur.execute("INSERT INTO users (email, name, password, phone) VALUES (lower(%s), %s,%s,%s)", [self.email, self.name, pw_hash, self.phone])
      g.db.commit()
      return self.email
    except IntegrityError as e:
      if e.pgcode == '23505':
        return "Email address already exists"
      else:
        return "Integrity Error"

    except psycopg2.Error as e:
      g.db.rollback()
      return "rollback"

    finally:
      cur.close()



  def get_by_id(self, id):
    cur = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
    try:
      cur.execute("SELECT * FROM users WHERE id = %s", [id])
      row = cur.fetchone()
      if(row == None):
        return None

      self.email = row["email"]
      self.name = row["name"]
      self.password = row["password"]
      self.isAdmin = row['admin']
      self.id = row['id']
      self.active = True

      return self

    except psycopg2.Error as e:
      g.db.rollback()
      return None

    finally:
      cur.close()


  def get_by_email(self, email):
    cur = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)
    try:
      cur.execute("SELECT * FROM users WHERE lower(email)=lower(%s)", (email,))
      row = cur.fetchone()
      if(row == None):
        return None

      self.email = row["email"]
      self.name = row["name"]
      self.password = row["password"]
      self.isAdmin = row['admin']
      self.id = row['id']
      self.active = True

      return self

    except psycopg2.Error as e:
      g.db.rollback()
      return None

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

  def update(self, id, name, email, phone):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("UPDATE user_settings set name=%s, phone=%s, email=%s WHERE id = %s", (name, email, phone, id))
      self.db.commit()
      return {'status':'updated'}
    finally:
      self.cur.close()



