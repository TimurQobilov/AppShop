from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:timur910210@localhost/online_store'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)




@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/item')
# def item():
#     return render_template('item-product.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/create')
def register():
    return render_template('create.html')

if __name__ == '__main__':
    app.run(debug=True)