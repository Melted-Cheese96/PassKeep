import pickle
import os
from time import sleep

def make_master_pass(user_password):
    with open('cfg', 'wb') as doc:
        pickle.dump(user_password, doc)
    print('Your password has been created!')
    print('')
    print('Returning to main menu')
    sleep(1)
    intro()

def verify_password(entered_password):
    with open('cfg', 'rb') as doc:
        pickled_password = pickle.load(doc)
        if entered_password == pickled_password:
            print('You got the correct password')
        else:
            print('You did not get the correct password!')

def create_new_password():
    print('It looks like this is your first time using this program!')
    print('')
    master_password = input('Enter a new master password')
    print(type(master_password))
    make_master_pass(master_password)



def intro():
    files = os.listdir()
    running = True
    print('Welcome to PassKeep')
    while True:
        if 'cfg' in files:
            password = input('Enter your master password')
            verify_password(password)
        else:
            create_new_password()
intro()