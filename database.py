from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from werkzeug.security import generate_password_hash, check_password_hash

import os

database_url = os.environ.get('DATABASE_URL')

# create the base class for our models
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    password_hash = Column(String(128), nullable=False)
    email = Column(String, nullable=False, unique=True)
    payment_status = Column(Boolean, default=False)
    prompts = Column(Integer, default=0)
    is_admin = Column(Boolean, default=False)

    def __init__(self, email, password, is_admin=False):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.payment_status = False
        self.prompts = 0
        self.is_admin = is_admin

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.email)


class DatabaseAPI:
    def __init__(self):
        # create a connection to the database
        self.engine = create_engine(database_url)

        # create all tables if they don't exist
        Base.metadata.create_all(self.engine)

        # create a session to interact with the database
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_user(self, email, password, is_admin=False):
        # create a new user
        user = User(email, password, is_admin)

        # add the user to the database
        self.session.add(user)

        # save the changes to the database
        self.session.commit()

    def verify_user(self, email, password):
        # query the database for a user with the given username and password
        user = self.session.query(User).filter_by(email=email).first()
        if user is not None and user.verify_password(password):
            return user
        else:
            return None

    def verify_email(self, email):
        # query the database for a user with the given username and password
        user = self.session.query(User).filter_by(email=email).first()
        if user is not None:
            return user
        else:
            return None

    def get_user(self, user_id):
        # query the database for the user with the given ID
        user = self.session.query(User).filter_by(id=user_id).first()

        # return the user's email address
        return user

    def get_users(self):
        # query the database for all users
        users = self.session.query(User).all()

        # return the user's email address
        return users

    def change_user_password(self, user_id, new_password):
        # query the database for the user with the given ID
        user = self.session.query(User).filter_by(id=user_id).first()

        # update the user's password
        user.password = new_password

        # save the changes to the database
        self.session.commit()

    def get_payment_status(self, user_id):
        # query the database for the user with the given ID
        user = self.session.query(User).filter_by(id=user_id).first()

        # return the user's payment status
        return user.payment_status

    def update_payment_status(self, user_id, status):
        # query the database for the user with the given ID
        user = self.session.query(User).filter_by(id=user_id).first()

        # update the user's payment status
        user.payment_status = status

        # save the changes to the database
        self.session.commit()

    def update_prompt_count(self, user_id):
        # query the database for the user with the given ID
        user = self.session.query(User).filter_by(id=user_id).first()

        # update the user's payment status
        user.prompts += 1

        # save the changes to the database
        self.session.commit()

    def get_prompt_count(self, user_id):
        # query the database for the user with the given ID
        user = self.session.query(User).filter_by(id=user_id).first()

        # return the user's payment status
        return user.prompts
