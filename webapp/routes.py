from flask import Flask, request, session, redirect, url_for, abort, \
     render_template,render_template_string, flash, jsonify, g, send_file, make_response, jsonify
from smtplib import SMTPAuthenticationError, SMTPServerDisconnected, SMTPException 
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from webapp import app, bcrypt,  login_manager
from webapp.user import User
from webapp.forms import *
from datetime import datetime
import json, requests, ujson, hashlib, os, datetime, pygal
from PIL import Image
from io import BytesIO
from base64 import b64encode
from flask_weasyprint import HTML, render_pdf
from pygal.style import Style


def cal(result):
  return 1





@app.route('/upload', methods=['POST'])
@login_required
def upload():
  form = UploadForm()

  if form.validate_on_submit():
    fn = form.file.data
    if fn != '' and fn is not None:

      filename = secure_filename(form.file.data.filename)
      extn = filename.split('.')[-1]
      if extn not in app.config['UPLOAD_EXTENSIONS']:
        abort(400)

      # generate name for the image
      md5hash = hashlib.md5(os.urandom(64)).hexdigest() + "." + extn
      #form.file.data.save(os.path.join(app.config['UPLOAD_PATH'], md5hash))

      # resizing the uploaded image
      im = Image.open(form.file.data)
      output = BytesIO()
      im.thumbnail((900,600), Image.ANTIALIAS)
#      im = im.resize((150,150))

      # save new image
      im.save(os.path.join(app.config['SCREENSHOTS_UPLOAD_PATH'], md5hash ), quality=100)
      output.seek(0)


      # saving URL into logo var
      return md5hash
      return '<img src="/static/images/uploads/screenshots/'+md5hash+'">'




@app.route('/photos')
@login_required
def photos():
  import os
  files = [f for f in os.listdir(os.path.join(app.config['SCREENSHOTS_UPLOAD_PATH']) )]
  return ujson.dumps(files)




@app.route('/sla/data')
@login_required
def get_all_findings_data():
  result = g.reports.get_all_findings()
  resultz = [ {k:v for k, v in s.items()} for s in result ]
  findings = []
  for r in result:
    for f in r['findings']:
      findings.append( {'scope': r['scope'], 'title':f['title'] , 'severity':f['severity'], 'status':f['status'], 'recv_date':r['recv_date'] , 'name':r['name'], 'owner_name':r['owner_name']} )

  return json.dumps(findings, indent=4, sort_keys=True, default=str)




@app.route('/all_vulnerabilites')
@login_required
def get_all_findings():
  result = g.reports.get_all_findings()
  return render_template("reports/findings_list.html", result=result)
  return jsonify(g.reports.get_all_findings())




@app.route('/')
@login_required
def root():
  result = {
         "assets"		:   g.engagements.count_per_category('2022 Plan'),
         "active_engagements"	:   "#"
  }



  data = {'systems': [] }
  pendings = {
   'critical':   {'total':0, 'types':{'web':0,'network':0,'ios':0,'android':0}},
   'high':       {'total':0, 'types':{'web':0,'network':0,'ios':0,'android':0}},
   'medium':     {'total':0, 'types':{'web':0,'network':0,'ios':0,'android':0}},
   'low':        {'total':0, 'types':{'web':0,'network':0,'ios':0,'android':0}},
   'riskaccepted': {'total':0, 'types':{'web':0,'network':0,'ios':0,'android':0}},
   'identified':         {'total':0, 'types':{'web':0,'network':0,'ios':0 ,'android':0 }}
  }


  # for bar chart
  eng = g.engagements.get_pending_engagements()
  for e in eng:
    e_name = e['name']
    e_id  =  e['id']
    scopes = g.engagements.allowed_reports(e_id)
    t,c,h,m,l=0,0,0,0,0
    for scope in scopes:
      # for each scope (web, network.etc) in e_id .. count them
      re = g.reports.get_engagement_findings_by_type(scope,e_id) 
      if re:
        # sum totals for each type/scope
        c += re['c']
        h += re['h']
        m += re['m']
        l += re['l']
        t = c+h+m+l
    if t > 0:
      # append total numbers for each engagement here
      data['systems'].append( {'name':e_name  , 'c':c,'h':h,'m':m,'l':l })



  # for total pending vuln details totals by type
  for e in eng:
    e_id  =  e['id']
    for s in ['web','network','ios', 'android']:
      p  = g.reports.get_engagement_findings_by_type(s,e_id)
      if p:
        pendings['critical']['total'] += p['c']
        pendings['critical']['types'][s] += p['c']
        pendings['high']['total'] += p['h']
        pendings['high']['types'][s] += p['h']
        pendings['medium']['total'] += p['m']
        pendings['medium']['types'][s] += p['m']
        pendings['low']['total'] += p['l']
        pendings['low']['types'][s] += p['l']

        pendings['riskaccepted']['total'] += p['r']
        pendings['riskaccepted']['types'][s] += p['r']

        pendings['identified']['total']    += p['c'] + p['h'] + p['m'] + p['l']
        pendings['identified']['types'][s] += p['c'] + p['h'] + p['m'] + p['l']




  return render_template("index.html",r=result,pendings=pendings,data=data)







@app.route('/user/profile')
@login_required
def view_user_profile():
  form = UserProfileForm()
  result = g.users.get(current_user.id)
  form.name.data	= result['name']
  form.phone.data	= result['phone']
  form.email.data 	= result['email']
  form.status.data   	= result['status']
  form.password.data    = "*****************"
  form.type.data    	= result['type']

  return render_template("user/view_user.html", form=form)

@app.route('/user/profile/edit', methods=['GET','POST'])
@login_required
def edit_user_profile():
  form = UserProfileForm()
  if request.method == 'POST':
    result 	= g.users.update(current_user.id, form.name.data, form.email.data, form.phone.data)
    return redirect("/user/profile")
  result = g.users.get(current_user.id)
  form.name.data	= result['name']
  form.phone.data	= result['phone']
  form.email.data 	= result['email']
  form.status.data   	= result['status']
  form.type.data    	= result['type']
  return render_template("user/edit_user_profile.html", form=form)




@app.route('/user/password/edit', methods=['GET','POST'])
@login_required
def edit_user_password():
  form = UserPasswordForm()
  error = None
  if form.validate_on_submit():
    password_valid = bcrypt.check_password_hash(current_user.password, form.opwd.data)
    if password_valid == True:
      if form.npwd.data == form.cnpwd.data:
        result 	= g.users.update_password(current_user.id, form.npwd.data)
        return redirect("/user/profile")
      else:
        error = "Password Do not match"
    else:
      error = "Current Password is not correct"
  return render_template("user/edit_user_password.html", form=form, error=error)







@app.route('/engagements')
@login_required
def engagements():
    result = g.engagements.get_engagements()
    resultz = [ {k:v for k, v in s.items()} for s in result ]

    for i in resultz:

      if i['status'] == "waiting_owner":
        status = {"status":"Pending with Client", "bar":"30"}
      elif  i['status'] == "in_progress":
        status = {"status":"In Progress", "bar":"60"}
      elif  i['status'] == "nsp":
        status = {"status":"Firewall Request", "bar":"20"}
      elif  i['status'] == "completed":
        status = {"status":"Completed", "bar":"100"}
      elif  i['status'] == "late":
        status = {"status":"Engagement overdue ", "bar":"80"}
      else:
        status = {"status":"NA ", "bar":"0"}

      i['e'] = status
    return render_template("engagements/engagements_list.html", result=resultz)

@app.route('/engagements/view/<id>')
@login_required
def view_engagement(id):
  form = EngagementForm()
  result                = g.engagements.get_engagement(id)
  if result == None:
    return redirect("/engagements")
  scope 		= g.engagements.allowed_reports(id)

  ##### NEW PENDINGS SUMMRY ######
  pendings = {
   'critical': 	 {'total':0, 'types':[]},
   'high': 	 {'total':0, 'types':[]},
   'medium': 	 {'total':0, 'types':[]},
   'low':	 {'total':0, 'types':[]},
   'riskaccepted': {'total':0, 'types':[]},
   'identified': 	 {'total':0, 'types':[]}
  }

  for s in scope:
    p  = g.reports.get_pending_findings(id, s)
    if p:

      pendings['critical']['total'] += p['c']
      pendings['critical']['types'].append( {'title':s,'count':p['c']} )
      pendings['high']['total'] += p['h']
      pendings['high']['types'].append( {'title':s,'count':p['h']} )
      pendings['medium']['total'] += p['m']
      pendings['medium']['types'].append( {'title':s,'count':p['m']} )
      pendings['low']['total'] += p['l']
      pendings['low']['types'].append( {'title':s,'count':p['l']} )
      pendings['riskaccepted']['total'] += p['r']
      pendings['riskaccepted']['types'].append( {'title':s,'count':p['r']} )

      k = g.reports.get_total_findings(id,s)
      if k:
        pendings['identified']['total'] += k['c']+k['h']+k['m']+k['l']
        pendings['identified']['types'].append( {'title':s,'count': k['c']+k['h']+k['m']+k['l'] } )




  reports                = g.reports.get_engagement_reports(id)
  if reports == None:
    reports  = []

  if result == None:
    abort(404)

  form.id.data		= result['id']
  form.status.data	= result['status']
  form.name.data	= result['name']
  form.tester.data      = result['tester']
  form.assigned_to.data	= result['assigned_to']
  form.start_date.data	= result['start_date']
  form.end_date.data	= result['end_date']
  form.type.data	= result['type']
  form.src_ip.data	= result['src_ip']
  form.soc_notification.data =  result['soc_notification']

  if form.status.data == "waiting_owner":
    status = {"status":"Pending with Client", "bar":"30"}
  elif form.status.data == "in_progress":
    status = {"status":"In Progress", "bar":"60"}
  elif form.status.data == "nsp":
    status = {"status":"Firewall Request", "bar":"20"}
  elif form.status.data == "completed":
    status = {"status":"Completed", "bar":"100"}
  elif form.status.data == "late":
    status = {"status":"Engagement overdue ", "bar":"80"}
  else:
    status = {"status":"NA ", "bar":"0"}

  return render_template("/engagements/view_engagement.html", form=form, scope=result['assets'], reports=reports, pendings=pendings,e=status)





@app.route('/reports/print/<id>')
@login_required
def print_report(id):

  form = EngagementForm()
  report = g.reports.get_report(id)
  e_id = report['e_id']
  result = g.engagements.get_engagement(e_id)


  form.id.data          = result['id']
  form.status.data      = result['status']
  form.name.data        = result['name']
  form.tester.data      = result['tester']
  form.assigned_to.data = result['assigned_to']
  form.start_date.data  = result['start_date']
  form.end_date.data    = result['end_date']
  form.type.data        = result['type']
  form.src_ip.data      = result['src_ip']
  form.soc_notification.data =  result['soc_notification']


  data = [{
    "Severity": 'Critical',
    "total": 2
  }, {
    "Severity": 'High',
    "total": 1
  }, {
    "Severity": 'Medium',
    "total": 3
  }, {
    "Severity": 'Low',
    "total": 4
  }]


  custom_style = Style(
    background='transparent',
    plot_background='transparent'

  )


  chart = pygal.Bar(width=450, height=250, style=custom_style)
  c_list = [x['total'] for x in data if x['Severity'] == 'Critical' ]
  h_list = [x['total'] for x in data if x['Severity'] == 'High' ]
  m_list = [x['total'] for x in data if x['Severity'] == 'Medium' ]
  l_list = [x['total'] for x in data if x['Severity'] == 'Low' ]

  chart.add('Critical',4)
  chart.add('High',6)
  chart.add('Medium',5)
  chart.add('Low',4)

  chart.x_labels = [x['Severity'] for x in data]

  settings = g.settings.get()
  html = render_template("reports/report.html", form=form, scope=result['assets'], report=report, base_url=app.config['app_base_url'],   chart_summary = chart.render_data_uri() , settings=settings)
  return render_pdf(HTML(string=html))





@app.route('/engagements/add', methods=['GET','POST'])
@login_required
def add_engagement():
  form = EngagementForm()
  systems = g.systems.get_systems()
  if request.method == 'POST':
    system_id		= request.form['system_id']
    name		= form.name.data
    tester		= request.form.getlist('tester[]')
    tester		= ','.join(tester)
    assigned_to		= form.assigned_to.data
    start_date		= form.start_date.data
    end_date		= form.end_date.data
    type		= request.form.getlist('type[]')
    type		= ','.join(type)
    src_ip		= form.src_ip.data
    category		= form.category.data
    status		= form.status.data
    soc_notification	= form.soc_notification.data

    r = g.assets.get_all(system_id)


    assets = ujson.dumps(r)
    result 	= g.engagements.create(name,system_id,assigned_to,tester,assets,src_ip,start_date,end_date,soc_notification,type, status, category)
    if result['status'] == "success":
      return  redirect("/engagements/view/%s" % result['id'])
    else:
      return  redirect("/engagements")

  form.system_id.choices = [(i['id'],i['name']) for i in systems]
  users = [ {"id":x['email'], "name":x['name']} for x in g.users.get_all()  ]
  form.assigned_to.choices = [(i['id'],i['name']) for i in  users]
  return render_template("engagements/add_engagement.html", form=form,systems=systems,users=users)









@app.route('/engagements/edit/<e_id>', methods=['GET','POST'])
@login_required
def edit_engagement(e_id):
  form = EngagementForm()
  systems = g.systems.get_systems()

  if request.method == 'GET':
    result = g.engagements.get_engagement(e_id)
    form.id.data          = result['id']
    form.status.data      = result['status']
    form.name.data        = result['name']
    form.category.data        = result['category']
    form.assigned_to.data = result['assigned_to']
    form.start_date.data  = result['start_date']
    form.end_date.data    = result['end_date']
    form.src_ip.data      = result['src_ip']

    form.soc_notification.data =  result['soc_notification']

    testers = [ {"id":x['email'], "name":x['name']} for x in g.users.get_all()  ]
    form.assigned_to.choices = [(i['id'],i['name']) for i in  testers]
    return render_template("engagements/edit_engagement.html", form=form, testers=testers , cur_testers=result['tester'], cur_type=result['type'])

  if request.method == 'POST':
    name		= form.name.data
    assigned_to		= form.assigned_to.data
    start_date		= form.start_date.data
    end_date		= form.end_date.data
    category		= form.category.data
    tester		= request.form.getlist('tester[]')
    tester		= ','.join(tester)
    type		= request.form.getlist('type[]')
    type		= ','.join(type)
    src_ip		= form.src_ip.data
    status		= form.status.data
    soc_notification	= form.soc_notification.data

    result 	= g.engagements.edit(name,assigned_to,tester,src_ip,start_date,end_date,soc_notification,type,status, category, e_id)
    if result['status'] == "success":
      return  redirect("/engagements/view/%s" % e_id)
    else:
      return  redirect("/engagements")

  form.system_id.choices = [(i['id'],i['name']) for i in systems]
  form.assigned_to.choices = [(i['id'],i['name']) for i in  testers]
  return render_template("engagements/add_engagement.html", form=form,systems=systems)





@app.route('/reports/view/<id>')
@login_required
def view_report(id):
  result                = g.reports.get_findings(id)
  if result == None:
    abort(404)
  return render_template("/reports/findings_list.html", result=result)




@app.route('/reports/add/<e_id>', methods=['GET','POST'])
@login_required
def add_report(e_id):
  form = ReportForm()
  upform = UploadForm()


  if form.type.data != "verification":
    if g.engagements.can_add_report(e_id) == False:
      return  redirect("/engagements/view/%s" % e_id)

  allowed_reports = g.engagements.allowed_reports(e_id)
  rem_allowed_reports = g.engagements.remaining_allowed_reports(e_id)

  if request.method == 'POST':
    report_name		= form.report_name.data
    report_id		= form.report_id.data
    tester              = request.form.getlist('tester[]')
    tester              = ','.join(tester)

    type		= form.type.data
    scope		= form.scope.data
    third_party		= form.third_party.data
    recv_date		= form.recv_date.data

    desc         = request.form.getlist('desc[]')
    status         = request.form.getlist('status[]')
    title                 = request.form.getlist('title[]')
    soln            = request.form.getlist('soln[]')
    impact 	         = request.form.getlist('impact[]')
    poc	             = request.form.getlist('poc[]')
    vuln_targets               = request.form.getlist('vuln_targets[]')
    severity           = request.form.getlist('severity[]')

    findings = []
    for i in range(len(title)):
      findings.append( {'desc':  '' if len(desc) == 0 else desc[i],
                     'title': title[i],
                     'soln': soln[i],
                     'impact': impact[i],
                     'status':status[i],
                     'poc':poc[i],
                     'vuln_targets':vuln_targets[i],
                     'severity':severity[i] } )


    high        = 0
    medium      = 0
    low         = 0
    critical    = 0
    riskaccepted = 0
    for j in findings:
      if j['status'] == "Risk Accepted":
        riskaccepted += 1
      if j['status'] == 'Open' or  j['status'] == "Partially Remidated":
        if j['severity'] == 'critical':
          critical +=1
        if j['severity'] == 'high':
          high +=1
        if j['severity'] == 'medium':
          medium +=1
        if j['severity'] == 'low':
          low += 1



    if type == "verification":
      r_id		= form.r_id.data
      result 	= g.reports.create(e_id,report_name,report_id,type,ujson.dumps(findings),tester, recv_date, critical,high,medium,low,riskaccepted, scope, third_party,r_id)
    else:
      result 	= g.reports.create(e_id,report_name,report_id,type,ujson.dumps(findings),tester, recv_date, critical,high,medium,low,riskaccepted, scope, third_party)
    if result['status'] == "success":
      return  redirect("/engagements/view/%s" % e_id)


  # GET
  form.e_id.data=e_id
  form.type.data = 'initial'
  form.scope.choices = rem_allowed_reports
  form.report_id.data = "REPORT-" + '{:03}'.format(g.reports.get_new_report_id()) + "-2022"


  testers = [ {"id":x['email'], "name":x['name']} for x in g.users.get_all()  ]
  return render_template("reports/add2_report.html", form=form, upform=upform, findings=None, testers=testers )

























@app.route('/reports/verify/<id>', methods=['GET','POST'])
@login_required
def verify_report(id):
  form = ReportForm()
  result = g.reports.get_report(id)
  form.report_name.data = "verification_"+result['report_name']
  form.report_id.data 	= result['report_id']
  form.tester.data	= result['tester']
  form.type.data 	= "verification"
  form.scope.choices 	= [result["scope"]]
  findings  		= result['findings']
  form.recv_date.data	= datetime.datetime.now()
  form.e_id.data	= result['e_id']
  form.r_id.data 	= id

  testers = [ {"id":x['email'], "name":x['name']} for x in g.users.get_all()  ]
  return render_template("reports/add_report.html", form=form, findings=findings, testers=testers)


@app.route('/reports/edit/<id>', methods=['GET','POST'])
@login_required
def edit_report(id):
  form = ReportForm()


  if request.method == 'POST':
    report_name		= form.report_name.data
    report_id		= form.report_id.data
    tester              = request.form.getlist('tester[]')
    tester              = ','.join(tester)
    r_id		= form.r_id.data
    e_id		= form.e_id.data
    type		= form.type.data
    scope		= form.scope.data
    third_party		= form.third_party.data
    recv_date		= form.recv_date.data



    # ++++++++++++++ parsing vulnerabilites ++++++++++++++++++
    #desc         = request.form.getlist('desc[]')
    status         = request.form.getlist('status[]')
    title                 = request.form.getlist('title[]')
    #soln                = request.form.getlist('soln[]')
    severity           = request.form.getlist('severity[]')

    findings = []
    for i in range(len(title)):
      findings.append( {'desc': '', #desc[i],
                     'title':title[i],
                     'soln': '', #soln[i],
                     'status':status[i],
                     'severity':severity[i] } )

    high        = 0
    medium      = 0
    low         = 0
    critical    = 0
    riskaccepted = 0
    for j in findings:
      if j['status'] == "Risk Accepted":
        riskaccepted += 1
      if j['status'] == 'Open' or  j['status'] == "Partially Remidated":
        if j['severity'] == 'critical':
          critical +=1
        if j['severity'] == 'high':
          high +=1
        if j['severity'] == 'medium':
          medium +=1
        if j['severity'] == 'low':
          low += 1
    # ++++++++++++++ parsing vulnerabilites ++++++++++++++++++



    result 	= g.reports.update(e_id,report_name,report_id,type,ujson.dumps(findings),tester, recv_date, critical,high,medium,low,riskaccepted, scope, third_party,r_id, id)
    if result['status'] == "success":
      return  redirect("/engagements/view/%s" % e_id)




  result = g.reports.get_report(id)
  form.report_name.data = result['report_name']
  form.report_id.data 	= result['report_id']
  form.type.data 	= result['type']
  form.scope.choices 	= [result["scope"]]
  findings  		= result['findings']
  form.recv_date.data	= datetime.datetime.now()
  form.e_id.data	= result['e_id']
  form.r_id.data 	= result['r_id']
  form.id.data 		= id

  testers = [ {"id":x['email'], "name":x['name']} for x in g.users.get_all()  ]
  return render_template("reports/edit_report.html", form=form, findings=findings, testers=testers , cur_testers=result['tester'])













@app.route('/systems')
@login_required
def systems():
    systems = g.systems.get_systems()
    systemz = [ {k:v for k, v in s.items()} for s in systems ]
    for i in systemz:
      i['urls_count'] = g.assets.get_web_count(i['id'])
      i['ips_count'] = g.assets.get_network_count(i['id'])
    return render_template("systems/systems_list.html", systems=systemz)





@app.route('/systems/add', methods=['GET','POST'])
@login_required
def add_system():
  form = SystemForm()
  if request.method == 'POST':
    department		= form.department.data
    name     		= form.name.data
    severity     		= form.severity.data
    contact_name     	= form.contact_name.data
    contact_email     	= form.contact_email.data

    result 	= g.systems.create(name, severity, contact_name, contact_email,department)
    if result['status'] == "success":
      return  redirect("/systems/view/%s" % result['id'])
    else:
      return  redirect("/systems")

  return render_template("systems/add_system.html", form=form)



@app.route('/system/edit/<id>', methods=['GET','POST'])
@login_required
def edit_system(id):
  form = SystemForm()
  if request.method == 'POST':
    department		= form.department.data
    name     		= form.name.data
    severity     	= form.severity.data
    contact_name     	= form.contact_name.data
    contact_email     	= form.contact_email.data

    result 	= g.systems.edit(name, severity, contact_name, contact_email,department, id)
    if result['status'] == "success":
      return  redirect("/systems/view/%s" % id)
    else:
      return  redirect("/systems")

  result      = g.systems.get_system(id)
  form.name.data = result['name']
  form.department.data = result['department']
  form.severity.data = result['severity']
  form.contact_name.data = result['contact_name']
  form.contact_email.data = result['contact_email']
  return render_template("systems/edit_system.html", form=form)





@app.route('/systems/view/<id>')
@login_required
def view_system(id):
  form = SystemForm()
  result                = g.systems.get_system(id)
  if result == None:
    return redirect("/systems")
  web_count                = g.assets.get_web_count(id)
  network_count                = g.assets.get_network_count(id)
  if result == None:
    abort(404)
  form.name.data = result['name']
  form.department.data = result['department']
  form.severity.data = result['severity']
  form.contact_name.data = result['contact_name']
  form.contact_email.data = result['contact_email']
  form.id.data = result['id']

  return render_template("/systems/view_system.html", form=form, web_count=web_count, network_count=network_count)


@app.route('/assets/web/view/<id>')
@login_required
def view_system_web_assets(id):
  system =  g.systems.get_system(id)
  if system == None:
    return redirect("/systems")
  result =  g.assets.get_web_assets(id)
  return render_template("/assets/view_assets.html", assets=result, system=system)



@app.route('/assets/web/add/<system_id>', methods=['GET','POST'])
@login_required
def add_assets(system_id):
  form = WebAssetForm()
  if request.method == 'POST':
    fqdn		= form.fqdn.data
    result 	= g.assets.add_fqdn(fqdn,system_id)
    return  redirect("/assets/web/view/%s" % system_id)
  return render_template("/assets/add_assets.html", form=form)


@app.route('/assets/network/add/<system_id>', methods=['GET','POST'])
@login_required
def add_network_assets(system_id):
  form = NetworkAssetForm()
  form = AssetForm()
  if request.method == 'POST':

    import sys, re
    import ipaddress
    import iptools


    text = form.assets.data
    ips = []
    bad_ips = []
    for new_line in text.split('\n'):
      regex = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?:/\d{1,2}|)', new_line)

      if regex is not None:
        for match in regex:
          if iptools.ipv4.validate_ip(match):
            for x in iptools.IpRangeList(match):
              if x not in ips:
                ips.append(x)
          elif iptools.ipv4.validate_cidr(match):
            for x in iptools.IpRangeList(match):
              if x not in ips:
                ips.append(x)
          else:
            bad_ips.append(match)

      else:
        bad_ips.append(regex)
        bad_ips.append(new_line)


      if len(bad_ips) > 0:
        form.assets.data = text
        return render_template("/assets/add_network_assets.html", form=form, bad_ips=bad_ips, good_ips=ips)

    for ip in ips:
      g.assets.add_ip(ip,system_id)
    return  redirect("/assets/network/view/%s" % system_id)

  return render_template("/assets/add_network_assets.html", form=form)



@app.route('/assets/network/view/<id>')
@login_required
def view_system_network_assets(id):
  system =  g.systems.get_system(id)
  if system == None:
    return redirect("/systems")

  result =  g.assets.get_network_assets(id)
  return render_template("/assets/view_assets.html", assets=result, system=system)






@app.route('/assets/delete_asset/<system_id>/', methods=['GET'])
@login_required
def delete_asset(system_id):
    asset = request.args.get('asset')
    type = request.args.get('type')
    ruuid = g.assets.delete_asset(system_id, asset, type)

    return redirect('/systems/view/%s' % system_id)








