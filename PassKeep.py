import pickle
import os
from time import sleep
from passlib.hash import pbkdf2_sha256
import sys
import string
import random
from cryptography.fernet import Fernet

current_dir = os.getcwd()

def save_pass(username, user_password, file_name):  # This saves a regular password
    
    if '.' in file_name:
        print('Here1')
        pass
    else:
        print('Here2')
        file_name = '.' + file_name
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted_username = f.encrypt(str.encode(username))
    encrypted_password = f.encrypt(str.encode(user_password))

    doc = open('.saved', 'a')
    doc.write(file_name)
    doc.write('\n')
    doc.close()
    os.chdir(file_name)
    with open('.username', 'wb') as doc:
        pickle.dump(encrypted_username, doc)
    
    with open(file_name, 'wb') as doc:
        pickle.dump(encrypted_password, doc)

    file_name = '{} key'.format(file_name)
    with open(file_name, 'wb') as doc:
        pickle.dump(key, doc)
    os.chdir(current_dir)
        
def save_master_pass(password):  # This saves the master password
    with open('.cfg', 'wb') as doc:
        pickle.dump(password, doc)
    print('Your password has been saved!')


def generate_password():
    alphabet = string.ascii_lowercase
    pWord = ''
    for letters in range(0, 28):
        random_letter = random.choice(alphabet)
        pWord = ''.join([random.choice(alphabet) + str(random.randint(1, 28)) for x in range(28)])
    return pWord


def verify_password(entered_password):  # Verifies if the master password is equal to what the user has enterted
    entered_password = str.encode(entered_password)
    print(type(entered_password))
    doc = open('.cfg', 'rb')
    content = pickle.load(doc)
    verification = pbkdf2_sha256.verify(entered_password, content)
    if verification:
        print('That was the correct password!')
        print('')
        print('Bringing you to main menu')
        print('')
        sleep(1)
        main()
    else:
        print('That was the wrong password!')
        sys.exit()

def delete_everything():  # Does a full wipe of everything in the directory
    try:
        with open('.saved', 'r') as doc:
            for line in doc:
                for word in line.split():
                    print(word)
                    os.system('rm -rf {}'.format(word))

    except FileNotFoundError:
        pass

    try:
        os.remove('.cfg')
        os.remove('.saved')
    except FileNotFoundError:
        pass
    print('Everything has been wiped')
    sleep(1)
    print('')
    print('Quitting')
    sys.exit()


def make_master_password(passw):  # The master password is hashed with sha256
    passw = passw.encode('utf-8')
    hash1 = pbkdf2_sha256.hash(passw)
    print(type(hash1))
    save_master_pass(hash1)
    print('Your password has been saved!')
    print('')
    print('Restarting program...')
    sleep(1)
    intro()


def read_password():
    account = input('Enter what account you want to search for!')
    if ' ' in account:
        account = account.replace(' ', '')
    account = '.' + account
    try:
        os.chdir(account)
        with open(account, 'rb') as doc:
            encrypted_password = pickle.load(doc)
        print(encrypted_password)
        file_name = '{} key'.format(account)
        with open(file_name, 'rb') as doc:
            key = pickle.load(doc)
        f = Fernet(key)
        decrypted_password = f.decrypt(encrypted_password)
        decrypted_password = decrypted_password.decode()
        print('Your password for {} is {}'.format(account, decrypted_password))
    except Exception as e:
        print('That account was either not found or you did not enter a valid directory')
    os.chdir(current_dir)
    
def delete_all_files():  # This function removes everything if the master key file is not in the directory.
    with open('.saved', 'r') as doc:
        for line in doc:
            for word in line.split():
                os.system('rm -rf {}'.format(word))
    os.remove('.saved')


def add_password():  # Lets the user add passwords
    all_files = os.listdir()
    new_password = {}
    account = input('Enter what this password is going to be used for!').lower()
    if ' ' in account:
        account = account.replace(' ', '')
    new_path = '.' + account
    os.mkdir(new_path)
    #os.chdir(account)
    username = input('Enter username for {}: '.format(account))    
    print('\n')
    password = input('Enter password!: ')
    print('\n')
    save_pass(username, password, account)
    print('Your new password has been saved \n')
    print('Returning...')
    sleep(2)
    print('')
    main()


def delete_password():  # This function is called when the user presses 3 in main()
    all_files = os.listdir()
    account_to_delete = input('Enter account that you want to delete')
    if ' ' in account_to_delete:
        account_to_delete = account_to_delete.replace(' ', '')
        print(account_to_delete)
    account_to_delete = '.' + account_to_delete
    words_to_re_add = []
    if account_to_delete in all_files:
        with open('.saved', 'r') as doc:
            for line in doc:
                for word in line.split():
                    if word == account_to_delete:
                        pass
                    else:
                        words_to_re_add.append(word)
        with open('.saved', 'w') as doc:
            for item in words_to_re_add:
                doc.write(item)
                doc.write('')
                doc.write(' ')
        os.system('rm -rf {}'.format(account_to_delete))
        print('Account details for {} has been deleted'.format(account_to_delete))
    else:
        print('That account was not found!')
        print('')
        sleep(1)
        main()


def see_all_saved_accounts():  # This shows the user all their saved accounts
    print('Here are all your saved passwords:')
    try:
        with open('.saved', 'r') as doc:
            for line in doc:
                for word in line.split():
                    print(word)
    except FileNotFoundError:
        print('You have no passwords saved!')


def main():  # Main function where you can choose your options
    while True:
        print('')
        print('Type in 1 to store a new password! \n')
        print('Type in 2 to retrieve one of your passwords \n')
        print('Type in 3 to delete one of your saved accounts \n')
        print('Type in 4 to quit the program \n')
        print('Type in 5 to see all saved accounts \n')
        print('Type in 6 to delete everything \n')

        option = input()
        if option == '1':
            add_password()
        elif option == '2':
            read_password()
        elif option == '3':
            delete_password()
        elif option == '4':
            print('Quitting...')
            quit()
        elif option == '5':
            see_all_saved_accounts()
        elif option == '6':
            delete_everything()
        else:
            print('Invalid command...')
            print('Restarting...')
            sleep(1)


def create_new_password():  # this is the function that prompts the user to enter a new master password if the file 'cfg' is not found
    print('No setup files found! \n')
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
    if '.cfg' in files:
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
