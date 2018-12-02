import tkinter as tk
from passlib.hash import pbkdf2_sha256
import sys
import os
import pickle
from cryptography.fernet import Fernet
from tkinter import messagebox
import string
import random
import pyperclip


class PassKeep:

    def __init__(self):  # Log in screen for PassKeep
        self.log_in_screen = tk.Tk()
        self.log_in_screen.title('PassKeep - Log In')
        self.log_in_screen.resizable(height=False, width=False)
        self.user_handle = tk.Label(text='Username:')
        self.user_handle.grid(row=0)
        self.user_handle_entry = tk.Entry()
        self.user_handle_entry.grid(row=0, column=1)
        self.password_label = tk.Label(text='Password:')
        self.password_label.grid(row=1)
        self.password_entry = tk.Entry(show='*')
        self.password_entry.grid(row=1, column=1)
        self.enter_button = tk.Button(text='Log in', command=self.verify_password)
        self.enter_button.grid(row=2, column=1)
        self.log_in_state = tk.IntVar()
        self.show_password_check_box_log_in_screen = tk.Checkbutton(text='Show password', variable=self.log_in_state,
                                                                          command=lambda: self.check_state(self.password_entry, self.log_in_state))
        self.show_password_check_box_log_in_screen.grid(row=2)
        self.check_for_setup_files()
        self.log_in_screen.mainloop()

    def check_state(self, password_var, state_var):  # Checks the state of self.log_in_state checkbox.
        state = state_var.get()
        print(state)
        if state == 0:
            password_var.configure(show='*')
        else:
            password_var.configure(show='')

    def verify_password(self):  # Verifies the password that the user has entered
        starting_dir = os.getcwd()
        username = self.user_handle_entry.get()
        password = self.password_entry.get()
        username = '.' + username
        print(os.listdir())
        if username not in os.listdir():
            messagebox.showerror('User not found', 'User was not found!')
        else:
            os.chdir(username)
            with open('.cfg', 'rb') as password_config_file:
                p_hash = pickle.load(password_config_file)

            verification = pbkdf2_sha256.verify(password, p_hash)
            if verification:
                self.options()
            else:
                messagebox.showerror('Wrong password!', 'You have not entered the correct password!')
                self.password_entry.delete(0, 'end')
                self.user_handle_entry.delete(0, 'end')
                os.chdir(starting_dir)

    def options(self):  # Main Window
        self.log_in_screen.withdraw()
        self.options_window = tk.Toplevel()
        self.options_window.resizable(height=False, width=False)
        self.options_window.title('PassKeep')
        logged_in_label = tk.Label(self.options_window, text='Logged in as {}'.format(self.user_handle_entry.get()))
        logged_in_label.grid(row=0)
        enter_new_password_button = tk.Button(self.options_window, text='Add account',
                                              command=self.store_new_password_gui)
        enter_new_password_button.grid(row=1)
        read_password_button = tk.Button(self.options_window, text='Retrieve account details ',
                                         command=self.read_password_gui)
        read_password_button.grid(row=2)
        remove_account_button = tk.Button(self.options_window, text='Remove account',
                                          command=self.remove_account_gui)
        remove_account_button.grid(row=3)
        full_wipe_button = tk.Button(self.options_window, text='Remove all saved info',
                                     command=self.remove_all_passwords)
        full_wipe_button.grid(row=4)
        quit_button = tk.Button(self.options_window, text='Quit',
                                command=self.quit_program)
        quit_button.grid(row=5)

    def remove_all_passwords(self):
        with open('.saved', 'r') as doc:
            for line in doc:
                for word in line.split():
                    try:
                        print(word)
                        # key_file = '{} key'.format(word)
                        # os.remove(key_file)
                        print(word)
                        os.system('rm -rf {}'.format(word))

                    except FileNotFoundError:
                        pass
        try:
            os.remove('.cfg')
            os.remove('.saved')
        except FileNotFoundError:
            pass

        messagebox.showinfo('Success', 'All info has been removed!')
        self.log_in_screen.destroy()

    def quit_program(self):
        self.log_in_screen.destroy()
        sys.exit()

    def store_new_password_gui(self):  # Stores new account details
        self.options_window.withdraw()
        self.new_password_window = tk.Toplevel()
        self.new_password_window.title('PassKeep')
        self.new_password_window.resizable(height=False, width=False)
        # button_frame = tk.Frame(self.new_password_window)
        # button_frame.grid(row=0)
        account_label = tk.Label(self.new_password_window, text='Account:')
        account_label.grid(row=0)
        self.account_entry = tk.Entry(self.new_password_window)
        self.account_entry.grid(row=0, column=1)
        self.username_label = tk.Label(self.new_password_window, text='Username:')
        self.username_label.grid(row=1)
        self.username_entry = tk.Entry(self.new_password_window)
        self.username_entry.grid(row=1, column=1)
        new_password_label = tk.Label(self.new_password_window, text='Password:')
        new_password_label.grid(row=2)
        self.new_password_entry = tk.Entry(self.new_password_window, show='*')
        self.new_password_entry.grid(row=2, column=1)
        create_button = tk.Button(self.new_password_window, text='Store details', command=self.store_password)
        create_button.grid(row=3, column=1)
        back_button = tk.Button(self.new_password_window, text='Back', command=self.store_new_password_back_button)
        back_button.grid(row=3, column=0)
        self.show_state = tk.IntVar()
        self.chk_box = tk.Checkbutton(self.new_password_window, text='Show password', variable=self.show_state,
                                      command=self.check_chk_box)
        self.chk_box.grid(row=5, column=1)
        generate_password_button = tk.Button(self.new_password_window, text='Generate password', command=self.generate_password)
        generate_password_button.grid(row=4, column=1)

    def generate_password(self):
        alphabet = string.ascii_lowercase
        numbers = [x for x in range(21)]
        generated_password = ''
        print(numbers)
        for x in range(0, 24):
            generated_password += random.choice(alphabet)
            generated_password += str(random.choice(numbers))

        prompt = messagebox.askyesno('Copy?', 'Do you want to copy the new password to your clipboard?')
        if prompt == True:
            pyperclip.copy(generated_password)
        else:
            pass

        self.new_password_entry.insert(0, generated_password)

    def check_chk_box(self):  # Controls the check box located in store_new_password_gui()
        chk_box_state = self.show_state.get()
        if chk_box_state == 0:
            self.new_password_entry.configure(show='*')
        elif chk_box_state == 1:
            self.new_password_entry.configure(show='')

    def store_new_password_back_button(self):  # Controls the back button for the 'store_new_password_gui()'
        self.new_password_window.destroy()
        self.options_window.deiconify()

    def store_password(self):  # Stores the password that has been entered in self.new_password_window()
        all_files = os.listdir()
        current_dir = os.getcwd()
        account = '.' + self.account_entry.get().lower()
        username = self.username_entry.get().lower()
        print(username)
        #if ' ' in username:
         #   username = username.replace(' ', '')
          #  print(username)
        if ' ' in account:
            account = account.replace(' ', '')
            print(account)
        if account in all_files:
            messagebox.showerror('Error', 'You have already saved a password for that account!')
        else:
            password = self.new_password_entry.get()
            if len(password) < 3:
                messagebox.showerror('Error', 'Your password cannot be less than 3 letters')
            else:
                gen = Fernet.generate_key()
                f = Fernet(gen)
                password = f.encrypt(str.encode(password))
                username = f.encrypt(str.encode(username))
                doc = open('.saved', 'a')
                doc.write('\n')
                doc.write(account)
                doc.write('\n')
                doc.close()
                os.mkdir(account)
                os.chdir(account)
                print(os.getcwd())
                with open(account, 'wb') as doc:
                    pickle.dump(password, doc)

                messagebox.showinfo('Success!', 'Account details for {} has been saved'.format(account))

                file_name = '{} key'.format(account)
                with open(file_name, 'wb') as doc:
                    pickle.dump(gen, doc)

                if len(username) > 2:
                    with open('username', 'wb') as doc1:
                        pickle.dump(username, doc1)

            os.chdir(current_dir)
            print(os.getcwd())
            self.account_entry.delete(0, 'end')
            self.username_entry.delete(0, 'end')
            self.new_password_entry.delete(0, 'end')

    def read_password_gui(self):  # Setup widgets for the read_password_gui()
        self.options_window.withdraw()
        self.read_password_window = tk.Toplevel()
        self.read_password_window.title('PassKeep')
        self.read_password_window.resizable(height=False, width=False)
        account_label = tk.Label(self.read_password_window, text='Account:')
        account_label.grid(row=0)
        self.account_entry = tk.Entry(self.read_password_window)
        self.account_entry.grid(row=0, column=1)
        check_button = tk.Button(self.read_password_window, text='Retrieve', command=self.read_password)
        check_button.grid(row=1, column=1)
        back_button = tk.Button(self.read_password_window, text='Back', command=self.read_password_back_button)
        back_button.grid(row=1)

    def read_password_back_button(self):  # Controls the back button for read_password_gui()
        self.read_password_window.destroy()
        self.options_window.deiconify()

    def remove_account_gui(self):  # Interface for removing accounts
        self.options_window.withdraw()
        self.remove_account_window = tk.Toplevel()
        self.remove_account_window.resizable(height=False, width=False)
        account_label = tk.Label(self.remove_account_window, text='Account:')
        account_label.grid(row=0)
        self.account_entry = tk.Entry(self.remove_account_window)
        self.account_entry.grid(row=0, column=1)
        delete_button = tk.Button(self.remove_account_window, text='Delete Account', command=self.remove_account)
        delete_button.grid(row=1, column=1)
        back_button = tk.Button(self.remove_account_window, text='Back', command=self.remove_window_back_button)
        back_button.grid(row=1)

    def remove_window_back_button(self):  # Back button for remove_window_back_button()
        self.remove_account_window.destroy()
        self.options_window.deiconify()

    def remove_account(self):  # Removes the account that the user specified in the GUI entry box
        all_files = os.listdir()
        account_to_remove = self.account_entry.get().lower()
        if account_to_remove == '.cfg' or account_to_remove == '.saved':
            messagebox.showerror('Nice try', 'Nice try')
        else:
            if ' ' in account_to_remove:
                account_to_remove = account_to_remove.replace(' ', '')
            account_to_remove = '.' + account_to_remove
            words = []
            try:
                with open('.saved', 'r') as doc:
                    for line in doc:
                        for word in line.split():
                            if word == account_to_remove:
                                print('Account to remove found in .saved!')
                                print(word)
                            else:
                                words.append(word)

                with open('.saved', 'w') as doc:
                    for item in words:
                        doc.write(item)
                current_dir = os.getcwd()
                if account_to_remove in all_files:
                    print('Here')
                    os.system('rm -rf {}'.format(account_to_remove))
                    messagebox.showinfo('Success!', '{} has been removed!'.format(account_to_remove))
                else:
                    messagebox.showerror('Error', 'That account was not found!')
            except FileNotFoundError:
                messagebox.showerror('Error', 'The account that you entered was not found!')

            self.account_entry.delete(0, 'end')

    def read_password(self):  # responsible for reading saved accounts
        to_decrypt = []
        current_directory = os.getcwd()
        account = '.' + self.account_entry.get().lower()
        if ' ' in account:
            account = account.replace(' ', '')
        account_key = '{} key'.format(account)
        try:
            os.chdir(account)
            all_files = os.listdir()
            with open(account_key, 'rb') as doc2:  # Gets the fernet key to decrypt the encrypted information
                key = pickle.load(doc2)
            f = Fernet(key)

            with open(account, 'rb') as doc:
                encrypted_password = pickle.load(doc)

            if 'username' in all_files:
                with open('username', 'rb') as doc1:
                    encrypted_username = pickle.load(doc1)

                decrypted_username = f.decrypt(encrypted_username)
                decrypted_username = decrypted_username.decode()
                decrypted_password = f.decrypt(encrypted_password)
                decrypted_password = decrypted_password.decode()
                account = account.strip('.')
                messagebox.showinfo('Result', 'Your username for {} is {}, your password is {}'.format(
                                                                                                    account,
                                                                                                    decrypted_username,
                                                                                                    decrypted_password))
            else:
                decrypted_password = f.decrypt(encrypted_password)
                decrypted_password = decrypted_password.decode()
                messagebox.showinfo('Result', 'Your password is {}'.format(decrypted_password))

            self.account_entry.delete(0, 'end')

        except Exception as e: # The only exceptions that can really happen here are NotADirectoryError or FileNotFound
            messagebox.showerror('Error', '{} was not found or could not be opened'.format(account))
            self.account_entry.delete(0, 'end')
        os.chdir(current_directory)

    def check_for_setup_files(self):  # Checks for setup files on startup
        all_files = os.listdir()
        if '.users' in all_files:
            starting_dir = os.getcwd()
            os.chdir('.users')
            if len(os.listdir()) == 0:
                os.chdir(starting_dir)
                self.new_account_creation()
            else:
                pass
        else:
            os.mkdir('.users')
            self.new_account_creation()

    def new_account_creation(self):
        self.log_in_screen.withdraw()
        create_account_window = tk.Toplevel()
        username_label = tk.Label(create_account_window, text='Username:')
        username_label.grid(row=0)
        username_entry = tk.Entry(create_account_window)
        username_entry.grid(row=0, column=1)
        password_label = tk.Label(create_account_window, text='New master password:')
        password_label.grid(row=1)
        new_master_password_entry = tk.Entry(create_account_window)
        new_master_password_entry.grid(row=1, column=1)
        new_master_password_entry.configure(show='*')
        checkbutton_status = tk.IntVar()
        show_password_button = tk.Checkbutton(create_account_window, text='Show password', variable=checkbutton_status,
                                              command=lambda: self.check_state(new_master_password_entry, checkbutton_status))
        show_password_button.grid(row=2)
        create_account_button = tk.Button(create_account_window, text='Create account',
                                          command=lambda: self.create_master_password(new_master_password_entry.get(),
                                                                                      username_entry.get(), create_account_window))
        create_account_button.grid(row=2, column=1)

    def create_master_password(self, password, username, window):
        # Prompts user to create master password if '.cfg' is not found in user's current directory.
        if ' ' in username:
            username = username.replace(' ', '')
        starting_dir = os.getcwd()
        os.chdir('.users')
        username = '.' + username
        os.mkdir(username)
        os.chdir(username)
        password_hash = pbkdf2_sha256.hash(password)
        with open('.cfg', 'wb') as config_file:
            pickle.dump(password_hash, config_file)
        messagebox.showinfo('New Account Created', 'You have created your new account!')
        window.destroy()
        print(os.getcwd())
        os.chdir(starting_dir)
        os.chdir('.users')
        self.log_in_screen.deiconify()


PassKeep = PassKeep()  # Initializes PassKeep class.
