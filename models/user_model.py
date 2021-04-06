from sql_alchemy import database
import random
import string


class UserModel(database.Model):
    __tablename__ = 'users'

    user_id = database.Column(database.String, primary_key=True)
    username = database.Column(database.String)
    email = database.Column(database.String(40))
    password = database.Column(database.String(20))

    def __init__(self, user_id, username, email, password):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password

    def createUser(self):
        database.session.add(self)
        database.session.commit()

    @classmethod
    def findByEmail(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None
