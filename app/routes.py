from flask import render_template, request, redirect, url_for, session, flash
from flask_bcrypt import check_password_hash, generate_password_hash
from app.models import User, Product
from app import db
from app.forms import RegistrationForm, LoginForm, ProfileForm

def register_routes(app):

    @app.route('/')
    def index():
        return render_template('index.html', products=Product.query.all())


#Добавления товара
    @app.route('/create', methods=['GET', 'POST'])
    def create():
        form = ProfileForm()
        if form.validate_on_submit():
            item = Product(
                title=form.title.data,
                price=form.price.data,
                description=form.description.data
            )
            db.session.add(item)
            db.session.commit()
            flash("Товар успешно добавлен!", "success")
            return redirect(url_for('index'))

        return render_template('create.html', form=form)
#Регистрация пользователя
    @app.route('/registration', methods=['GET', 'POST'])
    def registration():
        form = RegistrationForm()
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            if User.query.filter_by(username=username).first():
                flash("Пользователь с таким именем уже существует", "danger")
                return redirect(url_for('registration'))

            if User.query.filter_by(email=email).first():
                flash("Этот email уже зарегистрирован", "danger")
                return redirect(url_for('registration'))

            hashed_password = generate_password_hash(password).decode('utf-8')

            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash("Вы успешно зарегистрировались!", "success")
            return redirect(url_for('signin'))

        return render_template('registration.html', form=form)

#Вход в магазин
    @app.route('/signin', methods=['GET', 'POST'])
    def signin():
        print(1)
        form = LoginForm()
        if form.validate_on_submit():
            print(2)
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username, password=password).first()
            print(3)
            if user:
                session['user_id'] = user.id
                flash("Вы успешно вошли в систему", "success")

                return redirect(url_for('/'))
            else:
                flash("Неверное имя пользователя или пароль", "danger")

        return render_template('signin.html', form=form)

#Выходи из магазина
    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        flash("Вы вышли из системы", "info")
        return redirect(url_for('/'))
