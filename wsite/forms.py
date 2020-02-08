from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=3, max=15, message=f"Kullanıcı adı en az %(min)s, en fazla %(max)s karakter uzunluğunda olabilir.")])
    email = StringField('Email', validators=[DataRequired(), Email(message="Geçerli bir e-posta adresi girilmedi.")])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message=f"Şifre en az %(min)s karakter uzunluğunda olabilir.")])
    confirm_password = PasswordField('Password', validators=[DataRequired(), EqualTo("password", message="Şifreler eşleşmiyor.")])
    checked = BooleanField("Checked", validators=[DataRequired()])
    submit = SubmitField('Kaydol')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # remember = BooleanField("Remember")
    submit = SubmitField('Giriş')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Gönder')