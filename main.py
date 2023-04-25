import copy
import datetime
import hashlib
import os

from flask import Flask, redirect, render_template, request, session, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from additional import provinces, cities


app = Flask(__name__)
app.config['SECRET_KEY'] = <SECRET_KEY>
Bootstrap(app)

# Create database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///instance/data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Create table
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    type_of_fuel = db.Column(db.String(25), nullable=True)
    province = db.Column(db.String(25), nullable=True)
    city = db.Column(db.String(25), nullable=True)
    frequency = db.Column(db.String(25), nullable=True)
    next_date = db.Column(db.Date, nullable=True)
    code = db.Column(db.Integer, nullable=True)


with app.app_context():
    db.create_all()


# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user_id' in session:
        user = User.query.get(int(session['user_id']))
        typesoffuel = ['Regular gas', 'Premium gas', 'Diesel']
        frequency = ['Every day', 'Once a week', 'Twice a month', 'Once a month']
        provinces_ = copy.deepcopy(provinces)
        if request.method == 'GET' and user.province:
            # url = "https://countriesnow.space/api/v0.1/countries/state/cities"
            # payload = {'country': "Canada", 'state': user.province}
            # response = requests.request("POST", url, data=payload)
            # cities = json.loads(response.text)['data']
            cities_ = cities[user.province]
            return render_template('home.html',
                                   fuel=user.type_of_fuel, typesoffuel=typesoffuel,
                                   freq=user.frequency, frequency=frequency,
                                   prov=user.province, provinces=provinces_,
                                   city=user.city, cities=cities_, user_name=user.name, next_date=user.next_date)
        elif request.method == 'GET':
            return render_template('home.html',
                                   fuel='', typesoffuel=typesoffuel,
                                   freq='', frequency=frequency,
                                   prov='', provinces=provinces_,
                                   city='', user_name=user.name if user.name else '')

        if request.method == 'POST':
            typesoffuel = ['Regular gas', 'Premium gas', 'Diesel']
            frequency = ['Every day', 'Once a week', 'Twice a month', 'Once a month']
            provinces_ = copy.deepcopy(provinces)

            user.type_of_fuel = request.form['typeoffuel']
            user.frequency = request.form['frequency']
            user.province = request.form['province']
            user.city = request.form['city']

            if user.frequency == 'Every day':
                user.next_date = datetime.date.today()
            elif user.frequency == 'Once a week':
                user.next_date = datetime.date.today() + datetime.timedelta(weeks=1)
            elif user.frequency == 'Twice a month':
                user.next_date = datetime.date.today() + datetime.timedelta(weeks=2)
            elif user.frequency == 'Once a month':
                user.next_date = datetime.date.today() + datetime.timedelta(weeks=4)
            db.session.commit()

            typesoffuel.remove(user.type_of_fuel)
            frequency.remove(user.frequency)
            provinces_.remove(user.province)

            return render_template('home.html',
                                   fuel=user.type_of_fuel, typesoffuel=typesoffuel,
                                   freq=user.frequency, frequency=frequency,
                                   prov=user.province, provinces=provinces_,
                                   city=user.city, user_name=user.name, next_date=user.next_date)

    else:
        return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        # Create a new user
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        salt = 'ho64dv4512hgfjuul'
        password_salt = password.encode('utf-8') + salt.encode('utf-8')
        hash_object = hashlib.sha256(password_salt)
        password_hash = hash_object.hexdigest()

        new_user = User(
            name=name,
            email=email,
            password=password_hash,
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            message = 'This email already exists!'
            return render_template('register.html', message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        salt = 'ho64dv4512hgfjuul'
        password_salt = password.encode('utf-8') + salt.encode('utf-8')
        hash_object = hashlib.sha256(password_salt)
        password_hash = hash_object.hexdigest()
        if user is not None and user.password == password_hash:
            session['user_id'] = user.user_id
            return redirect(url_for('home'))
        else:
            message = 'Invalid email or password'
            return render_template('login.html', message=message)


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == 'GET':
        # verification_code = [randint(0, 9) for _ in range(4)]
        return render_template('forget_password.html', message='Verification number sent to your address!')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


@app.route('/unsubscribe')
def unsubscribe():
    user = User.query.get(int(session['user_id']))
    user.type_of_fuel = None
    user.frequency = None
    user.province = None
    user.city = None
    user.next_date = None
    db.session.commit()
    return redirect(url_for('home'))


# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
