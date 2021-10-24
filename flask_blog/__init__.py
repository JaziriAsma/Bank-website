from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b1322f152ba116c500abb606ec6a3d2a'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.sqlite'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
from flask_blog import routes