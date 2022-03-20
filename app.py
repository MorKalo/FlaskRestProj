from DbRepo import DbRepo
from Db_config import local_session, Base
from Logger import Logger
from Customer import Customer
from User import User
from flask import Flask, request, jsonify, make_response, Response
from flask_sqlalchemy import SQLAlchemy
import uuid  # for public id
from werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
import jwt
from datetime import datetime, timedelta
from functools import wraps


app = Flask(__name__)
repo = DbRepo(local_session)
logger = Logger.get_instance()
app.config['SECRET_KEY'] = 'my secret key'

def convert_to_json(_list: list):
    json_list = []
    for i in _list:
        _dict = i.__dict__
        _dict.pop('_sa_instance_state', None)
        json_list.append(_dict)
    return json_list


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
            logger.logger.info('error 401, someone try to use function that needs token but token is missing')
            return jsonify({'message': 'Token is missing'}), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user =repo.update_by_column_value(User, User.public_id, data['public_id'],
                                                      data['public_id']).first()
        except:
            logger.logger.warning('error 401, someone try to use function that needs token but token is invaild')
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # passes the current logged in user into the endpoint so
        # you have access to them
        # (you also just pass the data of the token, or whatever
        #  you want)
        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/customers', methods=['GET', 'POST'])
def get_or_post_customers():
    if request.method == 'GET':
        return jsonify(convert_to_json(repo.get_all_customers()))
    if request.method =='POST':
        customer_data= request.get_json()
        new_customer = Customer(id=None, fullname=customer_data["fullname"], address=customer_data["address"])
        repo.post(new_customer)
        logger.logger.info(f' new customer created.{new_customer} {request.base_url}, ')
        return make_response('Customer Created!', 201)


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
