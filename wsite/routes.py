from flask import render_template, request, flash, redirect, url_for
from wsite import db, app, mail, Message
from wsite.forms import RegisterForm, LoginForm, ContactForm
from wsite.models import User
from flask_login import login_user, current_user, logout_user



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/user_settings')
def user_settings():
    return render_template('user_settings.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.email == form.email.data: #zaten kayit varsa
            flash(f'Kayitli e-posta!', 'danger')
        else:
            user = User(name=form.name.data, email=form.email.data, password=form.password.data)
            db.session.add(user) #kullaniciyi veri tabanına ekle
            db.session.commit() #veri tabanını güncelle
            flash(f"{form.name.data} hesap olusturuldu", 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form = form)


@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated: #login olunmussa index sayfasina yonlendir
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash(f'Giris basarisiz!', 'danger')
    return render_template('login.html', form = form)

@app.route('/logout')
def logout():
    logout_user()# cikis yap.
    return redirect(url_for('index'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            msg=Message(form.name.data, sender='proje Sitesi mesaji', recipients=['ozkan44celik@gmail.com']) #mail alma
            msg.body=f"Gönderen: {form.name.data} ({form.email.data})\n {form.message.data}"
            mail.send(msg)
            flash(f'Teşekkürler {form.name.data}, mesajını aldık.', 'success')
            return redirect(url_for('contact'))
        else:
            flash(f'OPS, bir problem oldu.', 'danger')
    elif request.method == 'GET':
        return render_template('contact.html', title= 'Contact', form = form)


@app.route('/addRegion', methods=['POST'])
def addRegion():
    aa = request.form['cevap']
    return render_template('index.html', aa = aa)