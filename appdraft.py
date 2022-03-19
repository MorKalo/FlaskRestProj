from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid  # for public id
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from RestDataAccess import RestDataAccess
from Logger import Logger
from Customer import Customer
from DbRepo import DbRepo
from Db_config import local_session, Base
from sqlalchemy import Column, Integer,BigInteger, String, DateTime, ForeignKey, UniqueConstraint



app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:admin@localhost/flask_proj_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
logger=Logger.get_instance()

db = SQLAlchemy(app)
repo=DbRepo(local_session)

class User(Base):
    __tablename__ = 'users'

    id=Column(BigInteger(), primary_key=True, autoincrement=True)
    public_id=Column(String(50),unique=True )
    name=Column(String(50))
    username=Column(String(100), unique=True)
    password=Column(String(100))

@app.route("/")
def homepage():
    return '''
        <html>
            Hey! nice to see you :)
        </html>
        '''

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.removeprefix('Bearer ')
        # return 401 if token is not passed
        if not token:
            logger.logger.info('someone try to use function that needs token but token is missing')
            return jsonify({'message': 'Token is missing'}), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user =dao.get_user_by_public_id('public_id')
                #User.query \
                #.filter_by(public_id=data['public_id']) \
                #.first()
        except:
            logger.logger.warning('someone try to use function that needs token but token is invaild')
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/signup', methods=['POST'])
def signup():
    form_data = request.form

    # gets username and password
    username = form_data.get('username')
    password = form_data.get('password')

    # check if user exists
    user = User.query \
        .filter_by(username=username) \
        .first()

    if user:
        return make_response('User already exists. Please Log in.', 202)

    else:

        user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            username=username,
            password=generate_password_hash(password)
        )

        repo.add(user)
        repo.commit()

        return make_response('Successfully registered.', 201)


@app.route('/login', methods=['POST'])
def login():
    form_data = request.form

    # check that no field is missing
    if not form_data or not form_data.get('email') or not form_data.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required!"'}
        )

    # check if user exists
    user = User.query \
        .filter_by(email=form_data.get('email')) \
        .first()

    if not user:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist!"'}
        )

    # check password
    if not check_password_hash(user.password, form_data.get('password')):
        return make_response(
            'Could not verify',
            403,
            {'WWW-Authenticate': 'Basic realm ="Wrong Password!"'}
        )

    # generates the JWT Token
    token = jwt.encode({
        'public_id': user.public_id,
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }, app.config['SECRET_KEY'])

    return make_response(jsonify({'token': token.decode('UTF-8')}), 201)



# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            token = token.removeprefix('Bearer ')
            #eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJhMjA3MWU0Ny0xMTM5LTQ4MGItODhhZi03YjM4MzMyY2UxNWYiLCJleHAiOjE2NDYyNDkzMzF9.vcODiNWOd2VLzbwduTRk-1y1R11gBF_ktjRjA5kgHgU
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query \
                .filter_by(public_id=data['public_id']) \
                .first()
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401

        # passes the current logged in user into the endpoint so you have access to them
        # (you also just pass the data of the token, or whatever you want)
        return f(current_user, *args, **kwargs)

    return decorated



if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debuger shell
    # if you hit an error while running the server
    app.run(debug=True)