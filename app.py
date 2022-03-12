from flask import Flask, request, jsonify, make_response
import uuid  # for public id
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps
from RestDataAccess import RestDataAccess
from Logger import Logger
from User import User
from Customer import Customer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my secret key'
dao=RestDataAccess('flaskRestProj_db.db')
logger=Logger.get_instance()


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


@app.route('/customers', methods=['GET','POST'])
#@token_required
def get_or_post_customer(user):
    if request.method=='GET':
        get_cust=request.args.to_dict()
        customers=dao.get_all_customers(get_cust)
        return jsonify(customers)
    if request.method == 'POST':
        customer_details=request.get_json()
        post_customer=Customer(id=customer_details['id'], name=customer_details['name'], city=customer_details['city'])
        ans=dao.add_new_customer(post_customer)
        if ans:
            logger.logger.info(f'customer: "{post_customer}" has been created by user: "{user}"')
            return make_response(('Customer created succesfully', 201))
        else:
            logger.logger.error(f'user:"{user}" tried to creat new customer but faild because he didnt insert name or city or both. ')
            return jsonify({'answer': 'failed'})






        return jsonify(customers)

    users = User.query.all()

    print(current_user.name)
    print(current_user.email)
    print(current_user.password)
    # convert to json
    output = []
    for user in users:
        output.append({
            'public_id': user.public_id,
            'name': user.name,
            'email': user.email
        })

    return jsonify({'users': output})




@app.route('/signup', methods=['POST'])
def signup():
    form_data = request.form

    # gets name, email and password
    name = form_data.get('name')
    email = form_data.get('email')
    password = form_data.get('password')

    # check if user exists
    user = User.query \
        .filter_by(email=email) \
        .first()

    if user:
        return make_response('User already exists. Please Log in.', 202)

    else:

        user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

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