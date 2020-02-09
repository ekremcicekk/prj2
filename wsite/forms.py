from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from wsite.models import User
from flask_login import current_user


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=3, max=15, message=f"Kullanıcı adı en az %(min)s, en fazla %(max)s karakter uzunluğunda olabilir.")])
    email = StringField('Email', validators=[DataRequired(), Email(message="Geçerli bir e-posta adresi girilmedi.")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message=f"Şifre en az %(min)s karakter uzunluğunda olabilir.")])
    confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo("password", message="Şifreler eşleşmiyor.")])
    checked = BooleanField("Checked", validators=[DataRequired()])
    submit = SubmitField('Kaydol')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Bu e-posta adresi ile daha önce kayıt yapılmış, lütfen farklı bir e-posta adresi girin.')



class UpdateAccountForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(), Length(min=3, max=15, message=f"Kullanıcı adı en az %(min)s, en fazla %(max)s karakter uzunluğunda olabilir.")])
    email = StringField('Email',
                        validators=[DataRequired(), Email(message="Geçerli bir e-posta adresi girilmedi.")])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'], "Desteklenmeyen format! Sadece jpg ve png dosya formatı desteklenmektedir.")])
    submit = SubmitField('Güncelle')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Bu e-posta adresi ile daha önce kayıt yapılmış, lütfen farklı bir e-posta adresi girin.')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField("Remember")
    submit = SubmitField('Giriş')



class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email(message="Geçerli bir e-posta adresi girilmedi.")])
    submit = SubmitField('Şifre sıfırlama isteği')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Bu e-postaya sahip hesap yok. Önce kayıt olmalısınız.')



class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message=f"Şifre en az %(min)s karakter uzunluğunda olabilir.")])
    confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo("password", message="Şifreler eşleşmiyor.")])
    submit = SubmitField('Şifreyi Değiştir')



class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Gönder')
