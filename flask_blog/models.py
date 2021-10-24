from datetime import datetime
from flask_blog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    cin = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    naissance = db.Column(db.String(20), unique=True, nullable=False)
    num_tel = db.Column(db.Integer,unique=True)
    etatCivil = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    adresse = db.Column(db.String(120), unique=True, nullable=False)
    sexe = db.Column(db.String(10), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    num_carte =  db.Column(db.Integer,unique=True)
    code_confidentiel = db.Column(db.Integer,unique=True)

    comptes = db.relationship('Compte', backref='client', lazy=True)
    chequiers = db.relationship('Chequier', backref='client', lazy=True)

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False);
    de = db.Column(db.Integer, nullable=False)
    vers = db.Column(db.Integer, nullable=False)
    montant = db.Column(db.Integer, nullable=False);

class Compte(db.Model):
    RIB = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    somme = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Compte('{self.type}', '{self.RIB}', '{self.date_creation}','{self.somme}')"

class Chequier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_demande = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)