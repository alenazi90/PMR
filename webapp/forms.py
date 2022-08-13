#forms
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, DateTimeField, BooleanField, SelectField, TextAreaField, HiddenField, IntegerField, FieldList
from wtforms.fields.html5 import DateField, DateTimeLocalField
from wtforms.validators  import InputRequired, Email, Length
from wtforms.widgets import HiddenInput
from flask_wtf.file import FileField, FileAllowed


class UploadForm(FlaskForm):
  file = FileField();

class SettingsForm(FlaskForm):
  title = StringField('Report Title')
  company_name = StringField('Company Name')
  logo = StringField('Report Cover Page')
  file  = FileField('Upload Report Cover Page')

class UserProfileForm(FlaskForm):
  name  = StringField('Name', validators=[InputRequired()])
  email  = StringField('Email', validators=[InputRequired()])
  password  = PasswordField('Password',validators=[InputRequired()])
  type  = StringField('Type')
  admin  = StringField('Admin ')
  phone  = StringField('Phone')
  status  = StringField('Status')
  job_title  = StringField('job_title')
  recaptcha = RecaptchaField()

class UserPasswordForm(FlaskForm):
  opwd  = PasswordField('Current Password', validators=[InputRequired()])
  npwd  = PasswordField('New Password', validators=[InputRequired()])
  cnpwd = PasswordField('New Password Confirmation', validators=[InputRequired()])


class SystemForm(FlaskForm):
  id  		= StringField('ID')
  name  	= StringField('System Name', validators=[InputRequired()])
  severity  	= StringField('Severity')
  contact_name  = StringField('Business Owner', validators=[InputRequired()])
  contact_email = StringField('Business Owner Email', validators=[InputRequired()])
  department  	= StringField('Department', validators=[InputRequired()])

class WebAssetForm(FlaskForm):
  system_id	= StringField('System_ID')
  fqdn 		= StringField('FQDN')

class NetworkAssetForm(FlaskForm):
  system_id	= StringField('System_ID')
  ip 		= StringField('IP')

class AssetForm(FlaskForm):
  system_id	= HiddenField()
  assets 	= TextAreaField('Assets')


class EngagementForm(FlaskForm):
  id  = StringField()
  name 	= StringField('Engagement Name ', validators=[InputRequired()])
  system_id  = SelectField("Systems")
  assigned_to  = SelectField('Assigned To', validators=[InputRequired()])
  tester  = SelectField('Tester', validators=[InputRequired()])
  start_date  = DateTimeLocalField('PT Start Date', format='%Y-%m-%dT%H:%M')
  end_date  = DateTimeLocalField('PT End Date', format='%Y-%m-%dT%H:%M')
  type  = SelectField('PT Type', choices = [('network','Network'), ('web','Web Application'),('ios','Mobile iOS'), ('android','Mobile Android') ], validators=[InputRequired()])
  category  = StringField('Category', validators=[InputRequired()])
  status  = SelectField('Status', choices = [('waiting_owner','Waiting Client'), ('in_progress','In Progress'),('completed','Completed') ], validators=[InputRequired()])
  src_ip  = StringField('SRC IP', validators=[InputRequired()])
  soc_notification  = BooleanField("SOC")

class ReportForm(FlaskForm):
  id  = StringField()
  e_id  = HiddenField()
  r_id  = HiddenField()
  report_name 	= StringField('Report Name ', validators=[InputRequired()])
  report_id  = StringField("Report ID")
  tester  = SelectField('Tester', validators=[InputRequired()])
  recv_date  = DateTimeLocalField('Report Received On', format='%Y-%m-%dT%H:%M')
  type  = StringField("Report Type")
  scope  = SelectField('Report Scope', choices = [], validators=[InputRequired()])
  third_party  = BooleanField("Third Party Report?" )
