from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import DateField,StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_blog.models import User, Compte


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Valider')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()], render_kw={"placeholder": "Adresse Email..."})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Mot de passe..."})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Mettre à jour votre photo de profil', validators=[FileAllowed(['jpg', 'png'])])
    adresse = StringField('Adresse',validators=[DataRequired()])
    numero = StringField('Numéro de téléphone',validators=[DataRequired(), Length(min=8,max=8,message="Vérifier le numéro de téléphone")])
    etatCivil = StringField('Etat Civil',validators=[DataRequired()])
    submit = SubmitField('Modifier')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class clientForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    cin = StringField('CIN',validators=[DataRequired(),Length(min=8,max=8,message="Numéro du CIN doit contenir 8 chiffres")])
    date_naissance = DateField('Date de naissance',format='%d/%m/%Y')
    email = TextAreaField('Email', validators=[DataRequired(), Email("Vérifier l'adresse Email")])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6,max=20,message="La langeur minimale est 6 caractére")])
    sexe = StringField('Sex',validators=[DataRequired()])
    adresse = StringField('Adresse',validators=[DataRequired()])
    numero = StringField('Numéro de téléphone',validators=[DataRequired(), Length(min=8,max=8,message="Vérifier le numéro de téléphone")])
    etatCivil = StringField('Etat Civil',validators=[DataRequired()])
    num_carte = StringField('Numéro carte', validators=[DataRequired(), Length(min=8,max=8,message="Numéro de la carte doit contenir 8 chiffre")])
    code_conf = PasswordField('code confidentiel', validators=[DataRequired(), Length(min=4,max=4,message="Code confi doit contenir 4 chiffre")])
    submit = SubmitField('Valider')


class UpdateClientForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Confirm Password',
                                     validators=[DataRequired()])
    submit = SubmitField('Modifier')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')



class CompteForm(FlaskForm):
    type = StringField('Type', validators=[DataRequired()])
    RIB = StringField('RIB', validators=[DataRequired()])
    somme = FloatField('Somme', validators=[DataRequired()])
    submit = SubmitField('Valider')


class ChequierForm(FlaskForm):
    submit = SubmitField('Oui')

class VerserForm(FlaskForm):
    montant = FloatField('Somme', validators=[DataRequired()], render_kw={"placeholder": "Montant..."})
    submit = SubmitField('Verser')

class VirementForm(FlaskForm):
    De = IntegerField('Envoyeur (RIB) ', validators=[DataRequired()])
    vers = IntegerField('Destinataire (RIB) ', validators=[DataRequired()])
    montant = FloatField('Montant', validators=[DataRequired()])
    submit = SubmitField('Envoyer')

class RetirerForm(FlaskForm):
    num_carte = IntegerField('numéro de la carte ', validators=[DataRequired()])
    code_conf = IntegerField('code confidentiel ', validators=[DataRequired()])
    montant = FloatField('Montant', validators=[DataRequired()])
    RIB = IntegerField('RIB du compte ', validators=[DataRequired()])
    submit = SubmitField('Retirer')