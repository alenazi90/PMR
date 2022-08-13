from flask import Flask, request, session, redirect, url_for, abort, \
     render_template, flash, jsonify, g
from webapp import app
from webapp import login_manager
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from flask_bcrypt import Bcrypt
from webapp.user import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators  import InputRequired, Email, Length


@login_manager.unauthorized_handler
def unauthorized_callback():
  return redirect('/login')

@login_manager.user_loader
def load_user(user_id):
  user = User()
  return user.get_by_id(user_id)


class LoginForm(FlaskForm):
  email = StringField('Email Address', validators=[InputRequired()])
  password = PasswordField('Password',validators=[InputRequired(), Length(min=3,max=80)])
  remember = BooleanField('Remember me')


@app.route("/login", methods=["GET", "POST"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User()
    user = user.get_by_email(form.email.data)
    if user is not  None:
      g.bcrypt = Bcrypt(app)
      password_valid = user.validate_password(form.password.data)
      if password_valid == True:
        login_user(user)
        return redirect("/")
      print("pass wrong")
    print("Wrong User")
  return render_template("login.html", form=form)






@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("Logged out.")
    return redirect('/login')
