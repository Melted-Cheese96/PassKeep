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
    print('Closing program...')
    sleep(1)


def read_all_passwords(): #Shows the user all their saved passwords
    account = input('Enter what account you want to search for!')
    try:
        with open(account, 'rb') as doc:
            print('Your password for {} is {}'.format(account, pickle.load(doc)))
    except FileNotFoundError:
        print('We were not able to find the account that you specified!')


def delete_all_files(): #This function removes everything if the master key file is not in the directory.
    all_files = os.listdir()
    doc = open('.saved', 'r')
    content = doc.readlines()
    for item in content:
        os.remove(item)
    doc.close()
    os.remove('.saved')



def add_password(): #Lets the user add passwords
    new_password = {}
    all_files = os.listdir()
    account = input('Enter what this password is going to be used for!')
    password = input('Enter password')
    new_password[account] = password
    if account in all_files:
        print('You already have a password for that account!')
    else:
        with open('.saved', 'a') as doc:
            doc.write(account)
            print(doc)

        save_pass(password, account)
    print('Your new password has been saved')
    print('')
    print('Returning...')
    sleep(2)
    print('')
    main()

def delete_password():
    all_files = os.listdir()
    account_to_delete = input('Enter account that you want to delete')
    if account_to_delete in all_files:
        doc = open('.saved', 'r')
        content = doc.readlines()
        doc.close()
        doc = open('.saved', 'w')
        for line in content:
            if line == account_to_delete:
                pass
            else:
                doc.write(line)
        os.remove(account_to_delete)
    else:
        print('That account was not found!')
        print('')
        sleep(1)
        main()

def main():
    while True:
        option = input('Type in 1 to store a new password and type in 2 to retrieve all your passwords. Or type in 3 to delete one of your saved passwords. Or 4 to quit the program')
        if option == '1':
            add_password()
        elif option == '2':
            read_all_passwords()
        elif option == '3':
            delete_password()
        elif option == '4':
            print('Quitting...')
            sys.exit()

def create_new_password(): #this is the function that prompts the user to enter a new master password if the file 'cfg' is not found
    print('It looks like this is your first time using this program!')
    print('')
    master_password = input('Enter a new master password')
    print(type(master_password))
    make_master_password(master_password)

def create_saved_account_list():
    with open('.saved', 'x') as doc:
        pass


def intro():
    files = os.listdir()
    print('Welcome to PassKeep')
    print('')
    if 'cfg' in files:
        password = input('Enter your master password')
        verify_password(password)
        main()
    else:
        if '.saved' in files:
            delete_all_files()
        create_new_password()
        create_saved_account_list()
        sys.exit()

intro()