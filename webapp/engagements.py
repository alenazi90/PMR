import psycopg2
import psycopg2.extras
from datetime import datetime

class Engagements(object):

  def __init__(self, db):
    self.db = db
    self._db = db
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

  def delete(self,  id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("DELETE from engagements WHERE id = %s", (id,))
      self.cur.execute("DELETE from reports WHERE e_id = %s", (id,))
      self.db.commit()
    except IndexError:
      return None
    finally:
      self.cur.close()

  def count_per_category(self, category):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select count(category) from engagements where category =%s",(category,))
      rows = self.cur.fetchall()
      return rows[0][0]
    finally:
      self.cur.close()

  def get_pending_engagements(self):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT * FROM engagements where status != 'completeda' order by ts DESC")
      rows = self.cur.fetchall()
      return rows
    finally:
      self.cur.close()



  def get_engagements(self):
    try:
      self.cur.execute("SELECT * FROM engagements order by ts DESC")
      rows = self.cur.fetchall()
      return rows
    finally:
      self.cur.close()



  def can_add_report(self,e_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select ( select cardinality(regexp_split_to_array(type,',')) from engagements where id = %s ) > ( select count(id) from reports where type != 'verification' AND e_id = %s )",(e_id,e_id))
      rows = self.cur.fetchall()
      return rows[0][0]
    finally:
      self.cur.close()


  def allowed_reports(self,e_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select regexp_split_to_array(type,',') from engagements where id=%s",(e_id,))
      rows = self.cur.fetchall()
      return rows[0][0]
    except IndexError:
      return None
    finally:
      self.cur.close()



  def remaining_allowed_reports(self,e_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute(" select array_agg(e) from ( select unnest(  ARRAY(select regexp_split_to_array(type,',') from engagements where id=%s ) ) except select unnest(  ARRAY(select scope from reports where e_id = %s ) ) ) as dt(e) ",(e_id,e_id))
      rows = self.cur.fetchall()
      return rows[0][0]
    except IndexError:
      return None
    finally:
      self.cur.close()



  def get_engagement(self,id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT * FROM engagements where id = %s ", (id,))
      rows = self.cur.fetchall()
      return dict(rows[0])
    except IndexError:
      return None
    except Exception:
      return None
    finally:
      self.cur.close()



  def create(self, name,system_id,assigned_to,tester,assets,src_ip,start_date,end_date,soc_notification,type,status, category):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("INSERT INTO engagements (name,system_id,assigned_to,tester,assets,src_ip,start_date,end_date,soc_notification,type, status, category) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s) RETURNING ID" ,  ( name,system_id,assigned_to,tester,assets,src_ip,start_date,end_date,soc_notification,type, status , category))
      id = self.cur.fetchone()[0]
      self.db.commit()
      return {"status":"success", "id":id}
    except psycopg2.Error as e:
      self.db.rollback()
      print(e)
      return {"status":"faild", "id": "NA"}
    finally:
      self.cur.close()



  def edit(self, name,assigned_to,tester,src_ip,start_date,end_date,soc_notification,type,status, category, id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("update engagements  set name=%s,assigned_to=%s,tester=%s,src_ip=%s,start_date=%s,end_date=%s,soc_notification=%s,type=%s,status=%s, category=%s  WHERE id = %s", ( name,assigned_to,tester,src_ip,start_date,end_date,soc_notification,type,status,category, id))
      self.db.commit()
      return {"status":"success"}
    except psycopg2.Error as e:
      self.db.rollback()
      print(e)
      return {"status":"faild"}
    finally:
      self.cur.close()


