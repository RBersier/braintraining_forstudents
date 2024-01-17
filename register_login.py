"""
Project: class_order_management
Module: MA-DBPY
Date: 12.01.24
Author: Ryan Bersier
Version: 1.0
"""

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import database
import bcrypt
import re
import menu
import CRUD_users


# Function for create window where user can be authenticated
def login():
    global entry_pseudo, entry_pw, login_window
    # Create a new window for login
    login_window = tk.Tk()
    login_window.title("Connexion utilisateurs")
    login_window.geometry("500x400")
    rgb_color_login = (139, 201, 194)
    hex_color_login = '#%02x%02x%02x' % rgb_color_login
    login_window.configure(bg=hex_color_login)

    # Frames for layout
    frame1 = Frame(login_window, background=hex_color_login)
    frame1.pack(side=TOP, pady=10)
    frame2 = Frame(login_window, background="white", width=900)
    frame2.pack(side=TOP, pady=10)
    frame3 = Frame(login_window, background="white", width=900)
    frame3.pack(side=TOP, pady=10)
    frame4 = Frame(login_window, background="white", width=900)
    frame4.pack(side=TOP, pady=10)

    # Title
    lbl_title = tk.Label(frame1, text="CONNEXION", font=("Arial", 15))
    lbl_title.grid(row=0, column=1, ipady=5, padx=40, pady=40)

    # Entry fields for user input
    label_pseudo = Label(frame2, text="Pseudonyme :", font=("Arial", 12))
    label_pseudo.grid(row=1, column=1)
    entry_pseudo = Entry(frame2, font=("Arial", 12), width=20)
    entry_pseudo.grid(row=1, column=2, padx=10)
    label_pw = Label(frame2, text="Mot de passe :", font=("Arial", 12))
    label_pw.grid(row=2, column=1)
    entry_pw = Entry(frame2, font=("Arial", 12), width=20, show="●")
    entry_pw.grid(row=2, column=2, padx=10)

    # Buttons
    button_login = Button(frame3, text="Connexion", font=("Arial", 12), background="lightgrey", command=check_login)
    button_login.grid(row=1, column=1)

    # Label and button if user want create account
    label_pseudo = Label(frame4, text="Inscrivez-vous :", font=("Arial", 12))
    label_pseudo.grid(row=1, column=1)
    button_register = Button(frame4, text="Inscription", font=("Arial", 12), background="lightgrey", command=register)
    button_register.grid(row=1, column=2)

    login_window.mainloop()


# Function for test if the user write in field exist
def check_login():
    global entry_pseudo, entry_pw, window, login_window, levelofaccess

    # Retrieve user input from entry widgets
    pseudo = entry_pseudo.get()
    password = entry_pw.get()

    try:
        passaccess = database.check_user(pseudo, login_window)
        hashpw = passaccess[0].encode("utf-8")
        levelofaccess = passaccess[1]
        password = password.encode("utf-8")

        # Check if the password are correct
        if bcrypt.checkpw(password, hashpw):
                messagebox.showinfo(parent=login_window, title="info", message="Vous vous êtes connecté avec succès")
                login_window.destroy()
                menu.main(levelofaccess)
        else:
            messagebox.showerror(parent=login_window, title="info", message="Vous vous êtes trompé de mot de passe")
    except ValueError as ve:
        messagebox.showerror(parent=login_window, title="Erreur", message=f"{ve}")


# Function for create window where user can be create an account
def register():
    global login_window, entry_pseudo, entry_pw, entry_confpw, register_window
    login_window.destroy()

    # Create a new window for register
    register_window = tk.Tk()
    register_window.title("Inscription utilisateur")
    register_window.geometry("500x400")
    rgb_color_register = (139, 201, 194)
    rgb_color_register = '#%02x%02x%02x' % rgb_color_register
    register_window.configure(bg=rgb_color_register)

    # Frames for layout
    frame1 = Frame(register_window, background=rgb_color_register)
    frame1.pack(side=TOP, pady=10)
    frame2 = Frame(register_window, background="white", width=900)
    frame2.pack(side=TOP, pady=10)
    frame3 = Frame(register_window, background="white", width=900)
    frame3.pack(side=TOP, pady=10)

    # Title
    lbl_title = tk.Label(frame1, text="INSCRIPTION", font=("Arial", 15))
    lbl_title.grid(row=0, column=1, ipady=5, padx=40, pady=40)

    # Entry fields for user input
    label_pseudo = Label(frame2, text="Pseudonyme :", font=("Arial", 12))
    label_pseudo.grid(row=1, column=1)
    entry_pseudo = Entry(frame2, font=("Arial", 12), width=20)
    entry_pseudo.grid(row=1, column=2, padx=10)
    label_pw = Label(frame2, text="Mot de passe :", font=("Arial", 12))
    label_pw.grid(row=2, column=1)
    entry_pw = Entry(frame2, font=("Arial", 12), width=20, show="●")
    entry_pw.grid(row=2, column=2, padx=10)
    label_confpw = Label(frame2, text="Confirmation mot de passe :", font=("Arial", 12))
    label_confpw.grid(row=3, column=1)
    entry_confpw = Entry(frame2, font=("Arial", 12), width=20, show="●")
    entry_confpw.grid(row=3, column=2, padx=10)

    # Buttons
    button_login = Button(frame3, text="Inscription", font=("Arial", 12), background="lightgrey", command=check_register)
    button_login.grid(row=1, column=1)

    register_window.mainloop()


# Function for check and register user in the DB
def check_register():
    global entry_pseudo, entry_pw, entry_confpw, register_window, window, levelofaccess, pseudo

    # This is the password pattern
    password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"

    # Retrieve user input from entry widgets
    pseudo = entry_pseudo.get()
    password = entry_pw.get()
    confpassword = entry_confpw.get()

    # Check if any entry are empty and check if password is same at confpassword and check if password respect the password pattern
    if pseudo == "" or password == "" or confpassword == "":
        messagebox.showerror(parent=register_window, title="Erreur", message="Il semblerait que vous n'avez pas rempli tous les champs")
    elif password != confpassword:
        messagebox.showerror(parent=register_window, title="Erreur", message="Le mot de passe et la confirmation du mot de passe ne sont pas identique")
    elif not re.match(password_pattern, password):
        messagebox.showerror(parent=register_window, title="Erreur", message="Votre mot de passe n'est pas assez fort il doit comprendre une majuscule, une minuscule, un chiffre, un caractère spéciale et 8 caractère minimum")
    else:
        # Try to add user on DB
        try:
            hashpw = CRUD_users.hash_password(password)
            levelofaccess = database.new_user(pseudo, hashpw, register_window)
            levelofaccess = levelofaccess[0]
            messagebox.showinfo(parent=register_window, title="Info", message="Félicitation vous faites partie de nos utilisateurs.")
            register_window.destroy()
            menu.main(levelofaccess)
        except ValueError as ve:
            messagebox.showerror(parent=register_window, title="Erreur", message=f"{ve}")


# This the start for all program
login()
