# import the Flask class from the flask module
from flask import Flask, request, render_template, redirect, session, flash, url_for
from flask_bootstrap import Bootstrap
from database import DatabaseAPI
from payment import PaymentAPI
from query import QueryAPI
import os

from forms import LoginForm, RegisterForm, ChangePasswordForm, PaymentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    # check if user is logged in
    if 'user_id' not in session:
        # if not, redirect to login page
        return redirect('/login')
    else:
        user_id = session['user_id']
        return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle requests to login url
    form = LoginForm()
    if form.validate_on_submit():
        # check if user exists in database and password matches
        database_api = DatabaseAPI()
        user = database_api.verify_user(form.email.data, form.password.data)
        if user is not None:
            # log the user in
            session['user_id'] = user.id
            session['user_email'] = user.email

            # redirect to the dashboard page
            if user.is_admin or user.id == 1:
                session['is_admin'] = True
            else:
                session['is_admin'] = False

            return redirect('/')

        # if login is incorrect
        else:
            flash('Username or password is not correct!')

    # Load login template
    return render_template('login.html', form=form, title='Login')


@app.route('/account')
def account():
    # get the user ID from the session
    user_id = session['user_id']
    # get the user's account information and payment status
    database_api = DatabaseAPI()
    user = database_api.get_user(user_id)
    # render the "My Account" page with the user's information and payment status
    return render_template('account.html', user_email=user.email, payment_status=user.payment_status, num_prompts=user.prompts)


@app.route('/change_password', methods=['POST'])
def change_password():
    # get the user ID from the session
    user_id = session['user_id']
    # get the new password from the request
    new_password = request.form['new_password']
    # update the user's password
    database_api = DatabaseAPI()
    database_api.change_user_password(user_id, new_password)
    # render the "My Account" page with a success message
    flash("Password changed successfully.")
    return render_template('account.html')


@app.route('/process_payment', methods=['POST'])
def process_payment():
    # get the user ID from the session
    user_id = session['user_id']
    database_api = DatabaseAPI()
    user_email = database_api.get_user(user_id).email
    # get the payment amount and payment method from the request
    tier = request.form['tier']

    # create an instance of the PaymentAPI class
    payment_api = PaymentAPI()

    # try to process the payment
    try:
        payment_confirmation = payment_api.process(
            tier, user_email)
    except Exception as e:
        # if payment fails, render the "My Account" page with an error message
        flash(str(e))
        return render_template('account.html')

    # if payment succeeds, update the user's payment status and render the "My Account" page
    # with a success message
    database_api = DatabaseAPI()
    database_api.update_payment_status(user_id, True)
    flash('Payment successful!')
    return render_template('account.html')


@app.route('/query', methods=['POST'])
def query():
    # get the user ID from the session
    user_id = session['user_id']
    # get the user's prompt from the request
    prompt = request.form['prompt']

    # create an instance of the QueryAPI class
    query = QueryAPI()

    # try to get the answer from the OpenAI API
    try:
        answer = query.generate_text(prompt)
        database_api = DatabaseAPI()
        database_api.update_prompt_count(user_id)
    except Exception as e:
        # if the API call fails, render the main page with an error message
        flash(str(e))
        return render_template('index.html')

    # if the API call succeeds, render the main page with the answer
    return render_template('index.html', answer=answer)


@app.route('/logout')
def logout():
    # remove the user ID from the session
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('is_admin', None)
    # redirect to the login page
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Handle requests to register url
    form = RegisterForm()
    if form.validate_on_submit():
        # create a new user with the form data
        database = DatabaseAPI()
        database.create_user(email=form.email.data,
                             password=form.password.data)
        # add user to database
        flash('The user have been created successfully!')

        # redirect to login page
        return redirect(url_for('login'))

    # load registration template
    return render_template('register.html', form=form, title='Register')


@app.route('/admin')
def admin():
    # check if user is logged in and is an admin
    if 'user_id' not in session:
        # if not, redirect to login page
        return redirect('/login')
    else:
        # if user is logged in, render the main page
        database_api = DatabaseAPI()
        user = database_api.get_user(session['user_id'])
        if user.is_admin == False and user.id != 1:
            return redirect('/')
        elif user.is_admin == True or user.id == 1:
            # if user is an admin, render the admin page
            users = database_api.get_users()
            return render_template('admin.html', users=users)


# start the Flask app
if __name__ == '__main__':
    app.run()
