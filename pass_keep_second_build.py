'''
Changelog
1:Changed the way that account information is stored. 
2:Did a complete overhaul of the delete_all_files() function. Still a WIP

'''

import pickle
import os
from time import sleep
from passlib.hash import pbkdf2_sha256
import sys

def save_pass(user_password, file_name): #This saves a regular password
    with open(file_name, 'wb') as doc:
        pickle.dump(user_password, doc)


def save_master_pass(password): #This saves the master password
    with open('cfg', 'wb') as doc:
        pickle.dump(password, doc)
    print('Your password has been saved!')

def verify_password(entered_password): #This function verifies the master password
    entered_password = str.encode(entered_password)
    print(type(entered_password))
    doc = open('cfg', 'rb')
    content = pickle.load(doc)
    verification = pbkdf2_sha256.verify(entered_password, content)
    if verification == True:
        print('That was the correct password!')
        print('')
        print('Bringing you to main menu')
        print('')
        sleep(1)
        main()
    else:
        print('That was the wrong password!')
        sys.exit()


def make_master_password(passw): #The master password is hashed with sha256
    passw = passw.encode('utf-8')
    hash1 = pbkdf2_sha256.hash(passw)
    print(type(hash1))
    save_pass(hash1, 'cfg')
    print('Your password has been saved!')
    print('Quitting program...')
    sleep(1)
    sys.exit()

def read_all_passwords(): #Shows the user all their saved passwords
    account = input('Enter what account you want to search for!')
    try:
        with open(account, 'rb') as doc:
            print('Your password for {} is {}'.format(account, pickle.load(doc)))
    except FileNotFoundError:
        print('We were not able to find the account that you specified!')

def delete_all_files(): #This function removes everything if the master key file is not in the directory.
    all_files = os.listdir()
    for single_file in all_files:
        if single_file.endswith('.py') or single_file.endswith('.git'):
            pass
        else:
            os.remove(single_file)



def add_password(): #Lets the user add passwords
    new_password = {}
    all_files = os.listdir()
    use_case = input('Enter what this password is going to be used for!')
    password = input('Enter password')
    new_password[use_case] = password
    if use_case in all_files:
        print('You already have a password for that account!')
    else:
        save_pass(password, use_case)
    print('Your new password has been saved')
    print('')
    print('Returning...')
    sleep(2)
    print('')
    main()

def main():
    while True:
        option = input('Type in 1 to store a new password and type in 2 to retrieve all your passwords')
        if option == '1':
            add_password()
        elif option == '2':
            read_all_passwords()

def create_new_password():
    print('It looks like this is your first time using this program!')
    print('')
    master_password = input('Enter a new master password')
    print(type(master_password))
    make_master_password(master_password)



def intro():
    files = os.listdir()

    print('Welcome to PassKeep')
    print('')
    if 'cfg' in files:
        password = input('Enter your master password')
        verify_password(password)
        main()
    else:
        delete_all_files()
        create_new_password()
intro()
