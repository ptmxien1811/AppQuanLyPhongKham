from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
import cloudinary

app = Flask(__name__)

app.secret_key = "asbvasdasmdasm$#!"
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:Abc123@localhost/clinicdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"]=3

cloudinary.config(cloud_name='dokabu3ng',
                  api_key='577294329223111',
                  api_secret='FR262rDX7cNVj64RyjoKc-kdZx8')


db = SQLAlchemy(app)

login = LoginManager(app)