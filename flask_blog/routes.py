from __future__ import print_function
import sys
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, session, g
from flask_blog import app, db, bcrypt
from flask_blog.form import RetirerForm, VirementForm, VerserForm, RegistrationForm, LoginForm, UpdateAccountForm,  clientForm, CompteForm, UpdateClientForm, ChequierForm
from flask_blog.models import User, Compte, Chequier, Admin, Transaction
from flask_login import current_user, logout_user, login_required, login_user
import datetime
from datetime import timedelta
app.secret_key="yoursecrectkey"
app.permanent_session_lifetime=timedelta(minutes=15)

@app.route("/client")
def client_liste():
    if 'Admin' in session :
        form = RegistrationForm()
        users = User.query.all()
        return render_template('admin/client.html', users=users, form=form)
    else :
        return render_template('admin/access_denied.html')

@app.route("/compte")
def compte_liste():
    if 'Admin' in session :
        form = CompteForm()
        form1 = VerserForm()
        comptes = Compte.query.all()
        return render_template('admin/compte.html',form1=form1, comptes=comptes, form=form)
    else :
        return render_template('admin/access_denied.html')

@app.route("/chequier")
def chequier_liste():
    if 'Admin' in session:
        chequiers = Chequier.query.all()
        return render_template('admin/chequier.html', chequiers=chequiers)
    else :
        return render_template('admin/access_denied.html')

@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and 'Admin' in session:
        return redirect(url_for('client_liste'))
    elif current_user.is_authenticated and 'client' in session:
        return redirect(url_for('acount'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and admin.password == form.password.data:
            session["Admin"] = True
            login_user(admin, remember=form.remember.data)
            return redirect(url_for('client_liste'))
        else :
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.password == form.password.data:
                session["client"] = True
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('client_dashbord'))
            else:
                flash("s'ils vous plaît vérfier votre email ou mot de pass", 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    session.pop('Admin',None)
    session.pop('user',None)
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.num_tel = form.numero.data
        current_user.adresse = form.adresse.data
        current_user.etatCivil = form.etatCivil.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('client_liste'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.numero.data = current_user.num_tel
        form.adresse.data = current_user.adresse
        form.etatCivil.data = current_user.etatCivil
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('admin/edit_profile.html', title='Account',
                           image_file=image_file, form=form)



@app.route("/create_client", methods=['GET', 'POST'])
def new_client():
    if 'Admin' in session:
        form = clientForm()
        users = User.query.all()
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                cin = form.cin.data,
                email=form.email.data,
                naissance=form.date_naissance.data,
                num_tel = form.numero.data,
                adresse = form.adresse.data,
                sexe = form.sexe.data,
                etatCivil = form.etatCivil.data,
                num_carte = form.num_carte.data,
                code_confidentiel = form.code_conf.data,
                password=form.password.data,
            )
            db.session.add(user)
            db.session.commit()
            flash('Another customer has been added!', 'success')
            return redirect(url_for('client_liste'))
        return render_template('admin/create_client.html', title='New Client',
                            form=form, legend='New Client', user=users
                            )
    else :
        return render_template('admin/access_denied.html')


@app.route("/create_compte", methods=['GET', 'POST'])
@login_required
def new_compte():
    if 'Admin' in session:
        form = CompteForm()
        users = User.query.all()
        if form.validate_on_submit():
            user_idc = request.form.get("user")
            compte = Compte(type=form.type.data, RIB=form.numc.data, somme=form.somme.data, user_id=user_idc)
            db.session.add(compte)
            db.session.commit()
            flash('Another compte has been added!', 'success')
            return redirect(url_for('compte'))
        return render_template('admin/create_compte.html', title='New compte',
                            form=form, legend='New compte', users=users)
    else :
        return render_template('admin/access_denied.html')

@app.route("/client/<int:user_id>/compte", methods=['GET', 'POST'])
@login_required
def compte_user(user_id):
    if 'Admin' in session:
        client = User.query.get_or_404(user_id)
        form = CompteForm()
        if form.validate_on_submit():
            compte = Compte(type=form.type.data, RIB=form.RIB.data, somme=form.somme.data)
            compte.user_id= client.id
            db.session.add(compte)
            db.session.commit()
            flash('Another compte has been added!', 'success')
            return redirect(url_for('compte_liste'))

        return render_template('admin/create_compte.html',
                            form=form, legend='Ouvrir un compte', user_id=user_id)
    else :
        return render_template('admin/access_denied.html')


@app.route("/client/<int:user_id>/chequier", methods=['GET', 'POST'])
@login_required
def chequier_user(user_id):
        chequier = Chequier()
        chequier.user_id= user_id
        db.session.add(chequier)
        db.session.commit()
        flash('Une demande de chequier a été envoyée!', 'success')
        return redirect(url_for('client_dashbord'))



@app.route("/client/<int:user_id>")
def client(user_id):
    if 'Admin' in session:
        client = User.query.get_or_404(user_id)
        return render_template('admin/user_profile.html', title=client.username, client=client)
    else :
        render_template("admin/acess_denied.html")

@app.route("/client/<int:user_id>/update", methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    if 'Admin' in session:
        client = User.query.get_or_404(user_id)
        form = UpdateClientForm()
        if form.validate_on_submit():
            client.username = form.username.data
            client.email = form.email.data
            client.password = form.password.data
            db.session.commit()
            flash('Your client has been updated!', 'success')
            return redirect(url_for('client_liste'))
        elif request.method == 'GET':
            form.username.data = client.username
            form.email.data = client.email
        return render_template('admin/create_client.html', username='Update client',
                            form=form, legend='Update client')
    else :
        render_template('admin/access_denied.html')

@app.route("/client/<int:user_id>/delete", methods=['post'])
@login_required
def delete_user(user_id):
    if 'Admin' in session:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        flash('Your client has been deleted!', 'success')
        return redirect(url_for('client_liste'))
    else :
        render_template("admin/access_denied.html")


@app.route("/compte/<int:acc_id>/delete", methods=['post'])
@login_required
def delete_compte(acc_id):
    if 'Admin' in session:
        compte = Compte.query.filter_by(RIB=acc_id).first()
        db.session.delete(compte)
        db.session.commit()
        flash('Le compte a été radié', 'success')
        return redirect(url_for('compte_liste'))
    else :
        render_template("admin/access_denied.html")

@app.route('/verser/<int:acc_id>', methods=['post'])
@login_required
def verser(acc_id):
    if 'Admin' in session:
        compte = Compte.query.filter_by(RIB=acc_id).first()
        form1 = VerserForm()
        compte.somme = compte.somme + form1.montant.data
        Tx = Transaction()
        print(compte.user_id, file=sys.stderr)
        Tx.user_id = compte.user_id
        Tx.de = acc_id
        Tx.montant = form1.montant.data
        Tx.type = 'Depot'
        Tx.vers = 0
        db.session.add(Tx)
        db.session.commit()
        return redirect(url_for('compte_liste'))
    else :
        return render_template("admin/access_denied.html")

@app.route('/client_profil')
@login_required
def client_dashbord():
    form1 = RetirerForm()
    form = VirementForm()
    Tx = Transaction.query.filter_by(user_id=current_user.id)
    print(Tx[0].type,file=sys.stderr)
    return render_template("client/client_dashboard.html",form1=form1,Tx=Tx,form=form,user=current_user)

@app.route('/virement/<int:user_id>',methods=['POST'])
@login_required
def virement(user_id):
    client = User.query.filter_by(id = user_id).first()
    comptes = Compte.query.all()
    form = VirementForm()
    sender_RIB = form.De.data
    reciver_RIB = form.vers.data
    for compteA in current_user.comptes :
        if sender_RIB == compteA.RIB and compteA.somme > form.montant.data:
            print(compteA.somme,file=sys.stderr)
            compteA.somme = compteA.somme - form.montant.data
            Tx = Transaction()
            Tx.user_id= current_user.id
            Tx.de = sender_RIB
            Tx.vers = reciver_RIB
            Tx.montant = form.montant.data
            Tx.type = 'Virement'
            db.session.add(Tx)
            db.session.commit()
            print(compteA.somme,file=sys.stderr)

            flash("Votre virement est bien effectué",'success')
        else :
            flash("Vous n'avez pas le montant suffisant, Ou bien le RIB expéditeur est erroné",'danger')
    for compteB in comptes:
        if reciver_RIB == compteB.RIB:
            compteB.session.somme = compteB.somme + form.montant.data
            db.commit()

    return redirect(url_for('client_dashbord'))

@app.route('/Retirer/<int:user_id>',methods=['POST'])
@login_required
def Retirer(user_id):
    client = User.query.filter_by(id = user_id).first()
    comptes = Compte.query.all()
    form = RetirerForm()
    sender_RIB = form.RIB.data
    for compteA in current_user.comptes :
        if sender_RIB == compteA.RIB and compteA.somme > form.montant.data and client.num_carte == form.num_carte.data and client.code_confidentiel == form.code_conf.data:
            print(compteA.somme,file=sys.stderr)
            compteA.somme = compteA.somme - form.montant.data
            Tx = Transaction()
            Tx.user_id= current_user.id
            Tx.de = sender_RIB
            Tx.vers = 0
            Tx.montant = form.montant.data
            Tx.type = 'Retrait'
            db.session.add(Tx)
            db.session.commit()
            print(compteA.somme,file=sys.stderr)

            flash("Votre Retrait est bien effectué",'success')
        else :
            flash("Vous n'avez pas le montant suffisant, Ou bien le RIB expéditeur est erroné",'danger')
    return redirect(url_for('client_dashbord'))

@app.route('/transaction/<int:user_id>', methods=['GET'])
@login_required
def Transactions(user_id):
    if 'Admin in session':
        Tx = Transaction.query.filter_by(user_id=user_id).all()

        return render_template("admin/client_transaction.html",Tx=Tx)