from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from replit import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'vaccessuserinfo.database.windows.net'
bootstrap = Bootstrap(app)
dab = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, dab.Model):
    id = dab.Column(dab.Integer, primary_key=True)
    username = dab.Column(dab.String(15), unique=True)
    email = dab.Column(dab.String(50), unique=True)
    password = dab.Column(dab.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/home/')
def homePage():
  return render_template('home.html')
  
@app.route('/')
def index():
    return render_template('home.html')

#about the Vaccess 
@app.route('/about/')
def about():
  return render_template("about.html")

#go to stats page
@app.route('/statistics/')
def statistics():
  return render_template("statistics.html")

# data pertaining to *insert types of data* 
@app.route('/data/')
def data():
  return render_template("data.html")

# go to self assessment/profile ? 
@app.route('/login/', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  return render_template('login.html', form=form)

  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
  #     if user:
  #         if check_password_hash(user.password, form.password.data):
  #             login_user(user, remember=form.remember.data)
    return redirect('/dash/')
  return render_template('login.html', form=form)

        # return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

   # return render_template('login.html', form=form)

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
    #     hashed_password = generate_password_hash(form.password.data, method='sha256')
    #     new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    #     db.session.add(new_user)
    #     db.session.commit()
      return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

# start with self assessment
@app.route('/start/')
def start():
  return render_template("start.html")

# # # # # assessments page listing the different ones 
#general assessment page
@app.route('/asmts/')
def asmts():
  return render_template("asmts.html")

# # # # # # # # # # # # # # # # # # # # # # # # # 

@app.route('/dash/')
def dashboard():
    return render_template('dash.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.errorhandler(404)
def page_not_found(e):
  return "ERROR. PAGE NOT FOUND.", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)