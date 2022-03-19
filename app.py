# flask imports
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid  # for public id
from werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps
from DbRepo import DbRepo
from Db_config import local_session, Base
from Logger import Logger
from sqlalchemy import Column, Integer,BigInteger, String, DateTime, ForeignKey, UniqueConstraint



app = Flask(__name__)
dao = DbRepo('postgresql+psycopg2://postgres:admin@localhost/flask_proj_db.db')
logger = Logger.get_instance()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# creates SQLALCHEMY object
db = sqlalchemy(app)
repo=DbRepo(local_session)


# Database ORMs
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))

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

    # gets name, email and password
    name = form_data.get('name')
    email = form_data.get('email')
    password = form_data.get('password')

    # check if user exists
    #userex = User.query \
    #    .filter_by(email=email) \
     #   .first()
    userex=User.query.filter_by(email)

    if userex:
        return make_response('User already exists. Please Log in.', 202)

    else:

        userex = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(userex)
        db.session.commit()

        return make_response('Successfully registered.', 201)


app.run()
