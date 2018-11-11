import tkinter as tk
from passlib.hash import pbkdf2_sha256
import sys
import random
import os
import pickle
from cryptography.fernet import Fernet
from tkinter import messagebox


class PassKeep:

    def __init__(self):  # Log in screen for PassKeep
        self.log_in_screen = tk.Tk()
        self.log_in_screen.title('PassKeep - Log In')
        self.log_in_screen.configure(height=False, width=False)
        self.password_label = tk.Label(text='Password:')
        self.password_label.grid(row=0)
        self.password_entry = tk.Entry()
        self.password_entry.grid(row=0, column=1)
        self.enter_button = tk.Button(text='Log in', command=self.verify_password)
        self.enter_button.grid(row=1, column=1)
        self.check_for_setup_files()
        self.log_in_screen.mainloop()

    def verify_password(self):  # Verifies the password that the user has entered
        entered_password = self.password_entry.get()
        with open('.cfg', 'rb') as doc:
            password_hash = pickle.load(doc)

        verification = pbkdf2_sha256.verify(entered_password, password_hash)
        if verification:
            messagebox.showinfo('Success', 'Correct password has been entered!')
            self.options()
        else:
            messagebox.showerror('Error', 'You did not enter the correct password')

    def options(self):  # Main Window
        self.log_in_screen.withdraw()
        self.options_window = tk.Toplevel()
        self.options_window.title('PassKeep')
        enter_new_password_button = tk.Button(self.options_window, text='Add account', command=self.store_new_password_gui)
        enter_new_password_button.grid(row=0)
        read_password_button = tk.Button(self.options_window, text='Retrieve password', command=self.read_password_gui)
        read_password_button.grid(row=1)
        remove_account_button = tk.Button(self.options_window, text='Remove account', command=self.remove_account_gui)
        remove_account_button.grid(row=2)
        full_wipe_button = tk.Button(self.options_window, text='Remove all saved info', command=self.remove_all_passwords)
        full_wipe_button.grid(row=3)
        quit_button = tk.Button(self.options_window, text='Quit', command=self.quit_program)
        quit_button.grid(row=4)

    def remove_all_passwords(self):
        with open('.saved', 'r') as doc:
            for line in doc:
                for word in line.split():
                    try:
                        key_file = '{} key'.format(word)
                        os.remove(key_file)
                        os.remove(word)

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
        account_label = tk.Label(self.new_password_window, text='Account:')
        account_label.grid(row=0)
        self.account_entry = tk.Entry(self.new_password_window)
        self.account_entry.grid(row=0, column=1)
        new_password_label = tk.Label(self.new_password_window, text='Password:')
        new_password_label.grid(row=1)
        self.new_password_entry = tk.Entry(self.new_password_window)
        self.new_password_entry.grid(row=1, column=1)
        create_button = tk.Button(self.new_password_window, text='Store details', command=self.store_password)
        create_button.grid(row=2, column=1)
        back_button = tk.Button(self.new_password_window, text='Back', command=self.store_new_password_back_button)
        back_button.grid(row=2, column=0)

    def store_new_password_back_button(self):
        self.new_password_window.destroy()
        self.options_window.deiconify()

    def store_password(self):  # Stores the password that has been entered in self.new_password_window()
        all_files = os.listdir()
        account = '.' + self.account_entry.get().lower()
        if ' ' in account:
            account = account.replace(' ', '')
            print(account)
        if account in all_files:
            messagebox.showerror('Error', 'You have already saved a password for that account!')
        password = self.new_password_entry.get()
        if len(password) < 3:
            messagebox.showerror('Error', 'Your password cannot be less than 3 letters')
        else:
            gen = Fernet.generate_key()
            f = Fernet(gen)
            password = f.encrypt(str.encode(password))
            doc = open('.saved', 'a')
            doc.write(account)
            doc.write('\n')
            doc.close()
            with open(account, 'wb') as doc:
                pickle.dump(password, doc)

            messagebox.showinfo('Success!', 'Account details for {} has been saved'.format(account))
            self.new_password_window.destroy()

            file_name = '{} key'.format(account)
            with open(file_name, 'wb') as doc:
                pickle.dump(gen, doc)

    def read_password_gui(self):
        self.options_window.withdraw()
        self.read_password_window = tk.Toplevel()
        account_label = tk.Label(self.read_password_window, text='Account:')
        account_label.grid(row=0)
        self.account_entry = tk.Entry(self.read_password_window)
        self.account_entry.grid(row=0, column=1)
        check_button = tk.Button(self.read_password_window, text='Retrieve', command=self.read_password)
        check_button.grid(row=1, column=1)
        back_button = tk.Button(self.read_password_window, text='Back', command=self.read_password_back_button)
        back_button.grid(row=1)

    def read_password_back_button(self):
        self.read_password_window.destroy()
        self.options_window.deiconify()

    def remove_account_gui(self):
        self.options_window.withdraw()
        self.remove_account_window = tk.Toplevel()
        account_label = tk.Label(self.remove_account_window, text='Account:')
        account_label.grid(row=0)
        self.account_entry = tk.Entry(self.remove_account_window)
        self.account_entry.grid(row=0, column=1)
        delete_button = tk.Button(self.remove_account_window, text='Delete Account', command=self.remove_account)
        delete_button.grid(row=1, column=1)
        back_button = tk.Button(self.remove_account_window, text='Back', command=self.remove_window_back_button)
        back_button.grid(row=1)

    def remove_window_back_button(self):
        self.remove_account_window.destroy()
        self.options_window.deiconify()

    def remove_account(self):
        account_to_remove = self.account_entry.get().lower()
        if ' ' in account_to_remove:
            account_to_remove = account_to_remove.replace(' ', '')
        account_to_remove = '.' + account_to_remove
        key_file = '{} key'.format(account_to_remove)
        words = []
        try:
            with open('.saved', 'r') as doc:
                for line in doc:
                    for word in line.split():
                        if word == account_to_remove:
                            pass
                        else:
                            words.append(word)
            with open('.saved', 'w') as doc:
                for item in words:
                    doc.write(item)

            os.remove(account_to_remove)
            os.remove(key_file)
            messagebox.showinfo('Success!', '{} has been removed!'.format(account_to_remove))
        except FileNotFoundError:
            messagebox.showerror('Error', 'The account that you entered was not found!')

    def read_password(self):
        account = '.' + self.account_entry.get().lower()
        if ' ' in account:
            account = account.replace(' ', '')
        account_key = '{} key'.format(account)
        print(account)
        print(account_key)
        try:
            with open(account, 'rb') as doc:
                encrypted_password = pickle.load(doc)

            with open(account_key, 'rb') as doc:
                key = pickle.load(doc)

            f = Fernet(key)
            decrypted_password = f.decrypt(encrypted_password)
            decrypted_password = decrypted_password.decode()
            messagebox.showinfo('Result', 'Your password for {} is {}'.format(account, decrypted_password))
        except FileNotFoundError:
            messagebox.showerror('Error', '{} was not found!'.format(account))

    def check_for_setup_files(self):  # Checks for setup files
        all_files = os.listdir()
        if '.saved' in all_files:
            if '.cfg' in all_files:
                pass
            else:
                with open('.saved', 'r') as doc:
                    for line in doc:
                        for word in line.split():
                            try:
                                os.remove(word)
                                key = '{} key'.format(word)
                                os.remove(key)
                            except FileNotFoundError:
                                pass
                os.remove('.saved')
        else:
            with open('.saved', 'x') as doc:
                pass

        if '.cfg' in all_files:
            pass
        else:
            self.log_in_screen.withdraw()
            self.new_window = tk.Toplevel()
            self.new_window.title('Password creation - PassKeep')
            new_window_label = tk.Label(self.new_window, text='Create master password!')
            new_window_label.grid(row=0)
            self.new_password_entry = tk.Entry(self.new_window)
            self.new_password_entry.grid(row=0, column=1)
            create_button = tk.Button(self.new_window, text='Create', command=self.create_master_password)
            create_button.grid(row=1, column=1)

    def create_master_password(self):  # Prompts user to create master password
        master_password = self.new_password_entry.get()
        if len(master_password) < 5:
            messagebox.showerror('Error', 'You cannot have a password that has less than 5 characters')
        else:
            master_password_hash = pbkdf2_sha256.hash(master_password)
            with open('.cfg', 'wb') as doc:
                pickle.dump(master_password_hash, doc)
                messagebox.showinfo('Success!', 'You have created a new master password, make sure that you remember it')
                self.new_window.destroy()
                self.log_in_screen.deiconify()




PassKeep = PassKeep()
