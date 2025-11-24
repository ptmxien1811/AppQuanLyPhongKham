from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

app = Flask(__name__)

app.secret_key = "asbvasdasmdasm$#!"
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:Abc123@localhost/clinicdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"]=3


db = SQLAlchemy(app)

login = LoginManager(app)