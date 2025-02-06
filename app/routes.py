from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.models import Product, db

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    products = Product.query.all()
    return render_template('products.html', products=products)

@main_routes.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        product = Product(name=name, price=price, description=description)
        db.session.add(product)
        db.session.commit()
        flash('Товар добавлен!')
        return redirect(url_for('main.index'))
    return render_template('add_product.html')

@main_routes.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

@main_routes.route('/delete_product/<int:id>')
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Товар удален!')
    return redirect(url_for('main.index'))