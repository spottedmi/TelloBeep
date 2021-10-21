from flask import (
    Flask, 
    render_template, 
    request, 
    redirect,
    session,
    )
import logging
from queue import Queue
from db_connector import Db_connector
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import sys, datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../db.sqlite"
app.config["SECRET_KEY"] = "SECRET"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    added = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())

class Posts(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    added_date = db.Column(db.DateTime(timezone=True), default=datetime.datetime.now())
    content = db.Column(db.String(5000), nullable=False)
    title = db.Column(db.String(100), nullable=False, unique=True)
    approved = db.Column(db.Boolean(), nullable=False, default=False)
    approved_by = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    approved_date = db.Column(db.DateTime(timezone=True), nullable=True)
    

# db.create_all()
# sys.exit()

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Password"})
    password2 = PasswordField(validators=[InputRequired(), Length(min=0, max=100)], render_kw={"placeholder":"Password"})
    submit = SubmitField("Login")
    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("user already exists")


@app.route("/")
@login_required
def hello_world():
    print(queue_list)
    username = current_user.username

    return f"<p>Hello, World! ---> {username}</p>"


@app.route("/restricted")
@login_required
def restricted():
    return "<p>restricted area!</p>"

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                print(request.args)
                return redirect("/")

        return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
   
    return render_template("register.html", form=form)


def back_server(q_list, host="0.0.0.0", port=12345):
    global queue_list
    queue_list = q_list

    app.run(host=host, port=port)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=12345)

#todo 
# clean up this shitty code