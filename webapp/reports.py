import psycopg2
import psycopg2.extras
from datetime import datetime

class Reports(object):

  def __init__(self, db):
    self.db = db
    self._db = db
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

  def get_count_by_tester(self, tester):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select count(tester) from reports where tester = %s", (tester, ))
      rows = self.cur.fetchall()
      return rows[0][0]
    finally:
      self.cur.close()

  def get_all_findings(self):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select reports.recv_date, reports.scope , engagements.id ,  findings, reports.e_id, systems.name as name , systems.contact_name as owner_name from reports join engagements on engagements.id = reports.e_id  join systems on systems.id = engagements.system_id")
      rows = self.cur.fetchall()
      return rows
    except IndexError:
      return None
    finally:
      self.cur.close()

  def get_total_findings_by_type(self, scope):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select c,h,m,l,r from reports where type = 'initial' AND scope = %s order by ts DESC LIMIT 1", (scope,))
      rows = self.cur.fetchall()
      return dict(rows[0])
    except IndexError:
      return None
    finally:
      self.cur.close()



  def get_engagement_findings_by_type(self, scope, e_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select c,h,m,l,r from reports where scope = %s AND e_id = %s order by ts DESC LIMIT 1", (scope,e_id))
      rows = self.cur.fetchall()
      return dict(rows[0])
    except IndexError:
      return None
    finally:
      self.cur.close()



  # deprcecated .. not used
  def _get_pending_findings_by_type(self,scope):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select c,h,m,l,r from reports where scope = %s order by ts DESC LIMIT 1", (scope,))
      rows = self.cur.fetchall()
      return dict(rows[0])
    except IndexError:
      return None
    finally:
      self.cur.close()


  def get_total_findings(self,e_id, scope):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select c,h,m,l,r from reports where e_id = %s AND type = 'initial' AND scope = %s order by ts DESC LIMIT 1", (e_id,scope))
      rows = self.cur.fetchall()
      return dict(rows[0])
    except IndexError:
      return None
    finally:
      self.cur.close()

  def get_pending_findings(self,e_id, scope):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select c,h,m,l,r from reports where e_id = %s AND scope = %s order by ts DESC LIMIT 1", (e_id,scope))
      rows = self.cur.fetchall()
      return dict(rows[0])
    except IndexError:
      return None
    finally:
      self.cur.close()


  def get_new_report_id(self):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT count(id) FROM reports where type != 'verification' AND third_party = false ")
      rows = self.cur.fetchall()
      return rows[0][0] + 1
    finally:
      self.cur.close()


  def get_reports(self):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT * FROM reports")
      rows = self.cur.fetchall()
      return rows
    finally:
      self.cur.close()

  def get_findings(self, id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("select engagements.id ,  findings, reports.e_id, systems.name as name , systems.contact_name as owner_name from reports join engagements on engagements.id = reports.e_id  join systems on systems.id = engagements.system_id WHERE reports.id=%s", (id,))
      rows = self.cur.fetchall()
      return rows #[dict(rows[i]) for i, x in enumerate(rows) ]
    except IndexError:
      return None
    finally:
      self.cur.close()


  def get_engagement_reports(self,e_id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT * FROM reports where e_id = %s ", (e_id,))
      rows = self.cur.fetchall()
      return rows
    except IndexError:
      return None
    finally:
      self.cur.close()

  def get_report(self,id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("SELECT * FROM reports where id = %s ", (id,))
      rows = self.cur.fetchall()
      return dict(rows[0])
    except IndexError:
      return None
    finally:
      self.cur.close()



  def create(self, e_id,report_name,report_id,type,findings,tester, recv_date,c,h,m,l,r, scope,third_party,r_id=None):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      self.cur.execute("INSERT INTO reports (e_id,r_id,report_name,report_id,type,findings,tester, recv_date,c,h,m,l,r, scope, third_party) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING ID" ,  ( e_id,r_id, report_name,report_id,type,findings,tester, recv_date,c,h,m,l,r ,scope,third_party ))
      id = self.cur.fetchone()[0]
      self.db.commit()
      return {"status":"success", "id":id}
    except psycopg2.Error as e:
      self.db.rollback()
      print(e)
      return {"status":"faild", "id": "NA"}
    finally:
      self.cur.close()



  def update(self, e_id,report_name,report_id,type, findings ,tester, recv_date, c,h,m,l,r, scope, third_party,r_id, id):
    self.cur = self.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
      if r_id:
        self.cur.execute("update reports set e_id=%s,report_name=%s,report_id=%s,type=%s, findings=%s ,tester=%s, recv_date=%s, c=%s,h=%s,m=%s,l=%s,r=%s, scope=%s, third_party=%s, r_id=%s   WHERE id = %s ", (e_id,report_name,report_id,type, findings ,tester, recv_date, c,h,m,l,r, scope, third_party,r_id, id ))
      else:
        self.cur.execute("update reports set e_id=%s,report_name=%s,report_id=%s,type=%s, findings=%s ,tester=%s, recv_date=%s, c=%s,h=%s,m=%s,l=%s,r=%s, scope=%s, third_party=%s  WHERE id = %s ", (e_id,report_name,report_id,type, findings ,tester, recv_date, c,h,m,l,r, scope, third_party, id ))
      self.db.commit()
      return {"status":"success"}
    except psycopg2.Error as e:
      self.db.rollback()
      print(e)
      return {"status":"faild"}
    finally:
      self.cur.close()


