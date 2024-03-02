
from werkzeug.security import generate_password_hash

class User():
    id = "test"
    username = "test"
    email = "test"
    password = "test"
    admin = "test"

def create_user_table():
  
    print('create_user_table')
    
def add_user(username, password, email, admin):
    
    hashed_password = generate_password_hash(password, method='sha256')
    
def update_password(username, password):
    
    hashed_password = generate_password_hash(password, method='sha256')

def show_users():

    users = []

    return users
