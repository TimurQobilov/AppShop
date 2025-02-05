from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from app.models import User



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:timur910210@localhost/online_store'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/item')
def item():
    return render_template('item-product.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

if __name__ == '__main__':
    app.run(debug=True)