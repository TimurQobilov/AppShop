from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from app.models import db, User, Product
from app.forms import *



app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:timur910210@localhost/online_store'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'secret'
db = SQLAlchemy(app)



# Создание таблиц в базе данных
with app.app_context():
    db.create_all()

#главная страница
@app.route('/')
def index():
    return render_template('index.html')



#добавления товара
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')

        item = Product(title=title, price=price)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('/'))
        except:
            return "Error"
    return render_template('create.html')


# Регистрация пользователя
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username()
        email= form.email()
        password = form.password()
        if User.query.filter_by(username=username).first():
            flash("Пользователь с таким именем существует", "danger")
            return redirect(url_for('registration'))
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("Вы успешно зарегистрировались!", "success")
        return redirect(url_for('signin'))
    return render_template('registration.html', form=form)

#вход в магазин
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Вы успешно вошли", "success")
            return redirect(url_for('/'))
        else:
            flash("Неверное имя пользователя или пароль", "danger")
    return render_template('signin.html', form=form)


# Выход пользователя
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Вы вышли из системы", "info")
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)