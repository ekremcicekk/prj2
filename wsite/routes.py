from flask import render_template, request, flash, redirect, url_for
from wsite import db, app, mail, Message, bcrypt
from wsite.forms import RegisterForm, LoginForm, ContactForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from wsite.models import User, turkis_date
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import os
import secrets
from datetime import datetime, timedelta
from flask_admin.contrib import sqla
from flask_admin import AdminIndexView, helpers, Admin, expose



@app.errorhandler(404)
def page_not_found(e):
    erorr_404 = "404 Bulunamadı: İstenen URL sunucuda bulunamadı. URL'yi manuel olarak girdiyseniz, lütfen yazımınızı kontrol edin ve tekrar deneyin."
    return render_template('404.html', error_=erorr_404), 404



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/user')
@login_required
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"{form.name.data} hesap olusturuldu", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)



@app.route('/login', methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Giriş başarısız. Lütfen e-postayı ve şifreyi kontrol edin', 'danger')
    return render_template('login.html',  form=form)




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





def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    #eski profil resmini sil
    if not current_user.image_file == "default.png":
        old_picture_path = os.path.join(app.root_path, 'static','profile_pics', current_user.image_file)
        os.remove(old_picture_path)
    return picture_fn



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Hesabın güncellendi!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)





def send_reset_email(user):
    now = turkis_date()
    expires_time = now + timedelta(seconds=900)
    expires_time = expires_time.strftime("%d.%m.%Y  %X")
    now = now.strftime("%d.%m.%Y  %X")

    token = user.get_reset_token()
    msg = Message('Şifre Yenileme',
                  sender='proje Sitesi mesaji',
                  recipients=[user.email])
    msg.html = f'''<div style='margin: 10px;padding: 15px 25px;border: 5px solid #f1f1f1;border-radius: 25px; color:#fff;background-color:#2791b7;'>
  <img src="{ url_for('static', filename='img/logo.png', _external=True) }/" alt=' '  height='50'>
  <p><strong>Merhaba {user.name},</strong><br>
Birisi <abbr title='{now}'>kısa süre önce</abbr> hesabınız için şifre değişikliği istedi. Bu sizseniz aşağıdaki bağlantıyı tıklayarak yeni bir şifre oluşturabilirsiniz.</p>
  <p style='margin-bottom: 15px;padding: 15px 25px;border: 2px solid #f1f1f1;border-radius: 5px; color:#000; background-color:#fff;'> <strong>Bağlantı: </strong>{url_for('reset_token', token=token, _external=True)}</p>
  <hr style='border: 1px solid #fff;'>
  <li><small>Bağlantının son geçerlilik süresi: {expires_time}</small></li>
  <li><small>Şifrenizi değiştirmek istemiyorsanız veya bunu istemediyseniz, bu mesajı yok sayın ve silin.</small></li>
  <ul>
</div>'''

    mail.send(msg)



@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('E-posta adresinizi kontrol edin. Şifrenizi sıfırlama talimatlarını içeren bir e-posta gönderildi (15dk geçerlidir)', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Şifre Yenileme', form=form)




@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Bu bağlantı geçersiz veya süresi dolmuş.', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Şifreniz güncellendi! Artık giriş yapabilirsiniz', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


# yönetici paneli ---
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin
    def on_model_change(self, form, User, is_created=False):
        User.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    


class MyIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login_view'))
        return super(MyIndexView, self).index()
    @expose('/login/', methods=('GET', 'POST'))
    def login_view(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
            else:
                flash('Giriş başarısız. Lütfen e-postayı ve şifreyi kontrol edin', 'danger')

        if current_user.is_authenticated :
            return redirect(url_for('.index'))
        self._template_args['form'] = form
        return super(MyIndexView, self).index()


app.config['FLASK_ADMIN_SWATCH'] = 'Slate' #'Flatly'#'Superhero'
admin = Admin(app, name='KODLA', template_mode='bootstrap3',
                  index_view=MyIndexView())


admin.add_view(MyModelView(User, db.session, name='Users'))

#yönetici paneli --