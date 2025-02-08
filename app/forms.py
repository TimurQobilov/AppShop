from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, TextAreaField, SubmitField,EmailField
from wtforms.validators import DataRequired,Length

class RegistrationForm(FlaskForm):
    username = StringField(label='Имя', validators=[DataRequired('Заполните имя'), Length(min=2, max=20)])
    email = EmailField(label='Почта', validators=[DataRequired('Впишите почту')])
    password = PasswordField(label='Придумайте пароль', validators=[DataRequired('Придумайте пароль'), Length(min=2)])
    confirm_password = PasswordField(label='Повторите пароль', validators=[DataRequired('Повторите пароль'), Length(min=2)])
    submit = SubmitField(label='Зарегистрироваться')

class LoginForm(FlaskForm):
    username =StringField('Имя пользователя' , validators=[DataRequired('Ведите имя')])
    password = PasswordField('Пароль', validators=[DataRequired('Ведите пароль')])
    submit = SubmitField('Войти')

class ProfileForm(FlaskForm):
    title = StringField('Название товара', validators=[DataRequired()])
    price = FloatField('Цена', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    submit = SubmitField('Сохранить')