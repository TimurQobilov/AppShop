from flask_login import login_required, login_user
from flask import render_template, redirect, url_for, session, flash
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.sql.functions import current_user
from flask_login import current_user
from app.models import User, Product, CartItem
from app import db
from app.forms import RegistrationForm, LoginForm, ProfileForm
import os
from werkzeug.utils import secure_filename




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
            if form.photo.data:
                filename = secure_filename(form.photo.data.filename)
                form.photo.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
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
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                login_user(user)
                session['user_id'] = user.id  # Записываем ID пользователя в сессию
                flash("Вы успешно вошли!", "success")
                return redirect(url_for('index'))
            else:
                flash("Неверные данные!", "danger")
        return render_template('signin.html', form=form)

#Выходи из магазина
    @app.route('/logout')
    def logout():
        session.pop('user_id', None)
        session.pop('username', None)
        flash("Вы вышли из системы", "info")
        return redirect(url_for('signin'))


# Добавление товара в корзину
    @app.route('/add_to_cart/<int:product_id>', methods=['POST', 'GET'])
    @login_required
    def add_to_cart(product_id):
        cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(user_id=current_user.id, product_id=product_id)
            db.session.add(cart_item)
        db.session.commit()
        flash('Товар добавлен в корзину', 'success')
        return redirect(url_for('cart'))

    # Страница корзины
    @app.route('/cart')
    @login_required
    def cart():
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        return render_template('cart.html', cart_items=cart_items)

    # Удаление товара из корзины
    @app.route('/remove_from_cart/<int:item_id>')
    @login_required
    def remove_from_cart(item_id):
        cart_item = CartItem.query.get(item_id)
        if cart_item and cart_item.user_id == current_user.id:
            db.session.delete(cart_item)
            db.session.commit()
            flash('Товар удалён из корзины', 'info')
        return redirect(url_for('cart'))








