from flask import Flask, request, render_template
from werkzeug.security import generate_password_hash

from db import User, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
db.init_app(app)


@app.route('/')
def index():
    return '<h1>My Site!</h1>'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            hash_psw = generate_password_hash(request.form.get('psw'))
            user = User(username=request.form.get('name'),
                        password=hash_psw,
                        lastname = request.form.get('lastname'),
                        email = request.form.get('email'))
            db.session.add(user)
            db.session.flush()
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print(err)
    return render_template('login.html')

@app.cli.command("init-db")
def init_db():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
