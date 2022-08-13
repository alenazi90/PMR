from flask import Flask, request, session, redirect, url_for, abort, \
     render_template, flash, jsonify, g, Blueprint

from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

import json, ujson
from webapp.forms import *
from webapp  import app

import json, requests, ujson, hashlib, os, datetime, pygal
from PIL import Image
from io import BytesIO
from base64 import b64encode


admin = Blueprint('admin', __name__,
                        template_folder='templates')

@admin.before_request
def restrict_to_admins():
  try:
    if not current_user.isAdmin == True:
      abort(404)
  except:
    abort(404)

@admin.route('/')
@login_required
def admin_index():
  users = g.users.get_all()
  return render_template("admin/users_list.html", users=users)




@admin.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
  form = SettingsForm()
  result = g.settings.get()
  if result:
    form.logo.data        = result['logo']
    form.title.data   = result['title']
    form.company_name.data   = result['company_name']
  return render_template('/admin/settings/settings.html', form=form)


@admin.route('/settings/edit', methods=['GET','POST'])
@login_required
def edit_settings():
  form = SettingsForm()
  result = g.settings.get()
  if result:
    form.logo.data        = result['logo']

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
#      im.thumbnail((200,200), Image.ANTIALIAS)
#      im = im.resize((150,150))

      # save new image
      im.save(os.path.join(app.config['UPLOAD_LOGO_PATH'], md5hash ), quality=100)
      output.seek(0)

      try:
        # remove old image from disk
        r = g.settings.get_logo()
        if r['logo']:
          os.remove(os.path.join(app.config['UPLOAD_LOGO_PATH'],r['logo']))
      except OSError as e:
        print("File Not Found")
        pass
      # saving URL into logo var
      form.logo.data = md5hash

    title         = request.form.getlist('title[]')
    content       = request.form.getlist('content[]')
    order         = request.form.getlist('order[]')
    sections = []
    for i in range(len(title)):
      sections.append( {'order':  0 if order == '' else order,
                     'order': order[i],
                     'title': title[i],
                     'content':content[i] } )

    result      = g.settings.update(form.logo.data, form.title.data, form.company_name.data, ujson.dumps(sections))
    return redirect("/admin/settings/edit")

  result = g.settings.get()
  if result:
    form.logo.data        = result['logo']
    form.title.data   = result['title']
    form.company_name.data   = result['company_name']
  return render_template("/admin/settings/settings.html", form=form)








@admin.route('/systems/delete/<id>/', methods=['GET'])
@login_required
def delete_sys(id):
    g.systems.delete(id)
    return redirect('/systems')

@admin.route('/engagements/delete_eng/<id>/', methods=['GET'])
@login_required
def delete_eng(id):
    g.engagements.delete(id)
    return redirect('/engagements')


@admin.route('/user/<id>', methods=['GET','POST'])
@login_required
def edit_user(id):
  form = UserProfileForm()
  if request.method == 'POST':
    result      = g.users.update_all(id, form.name.data, form.email.data, form.phone.data, form.job_title.data, form.type.data)
    return redirect("/admin/")
  result = g.users.get(id)
  form.name.data        = result['name']
  form.phone.data       = result['phone']
  form.email.data       = result['email']
  form.status.data      = result['status']
  form.type.data        = result['type']
  form.job_title.data        = result['job_title']
  return render_template("admin/edit_user_profile.html", form=form)



@admin.route('/users/add', methods=['POST', 'GET'])
@login_required
def admin_add_new_user():

  form = UserProfileForm()
  if request.method == 'POST':
    pwd = g.users.add_new_user(form.email.data,form.name.data,form.job_title.data,form.phone.data,current_user.email, False, form.type.data, False )
    print(pwd)
#    return render_template("admin/users_list.html", form=form, pwd=pwd)
    return redirect("/admin/")
  result = g.users.get(current_user.id)
  return render_template("admin/add_user.html", form=form)


@admin.route('/delete_user/<id>')
@login_required
def admindelete_user(id):
  user = g.users.get(id)
  if user['email'] != app.config['ADMIN_EMAIL']:
    g.users.delete_user(id)
  return redirect('/admin/')

@admin.route('/activate_user/<id>')
@login_required
def admin_activate_user(id):
  user = g.users.get(id)
  if user['email'] != app.config['ADMIN_EMAIL']:
    g.users.activate_user(id)
  return redirect('/admin/')

@admin.route('/suspend_user/<id>')
@login_required
def admin_suspend_user(id):
  user = g.users.get(id)
  if user['email'] != app.config['ADMIN_EMAIL']:
    g.users.suspend_user(id)
  return redirect('/admin/')




@admin.route('/deactivate_user', methods=['POST'])
@login_required
def admin_delete_user():
  email    =  request.form['email'];
  g.users.delete_user(email)
  return json.dumps({'status':'user account is inactive'})

@admin.route('/activate_user', methods=['POST'])
@login_required
def aaadmin_activate_user():
  email    =  request.form['email'];
  g.users.activate_user(email)
  return json.dumps({'status':'user account is active'})

@admin.route('/change_user_password', methods=['POST'])
@login_required
def admin_change_user_password():
  email    =  request.form['email'];
  pwd = g.users.change_user_password(email)
  return json.dumps({'status':'User password has been changed','pwd':pwd})
