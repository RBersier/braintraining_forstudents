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
import re
import bcrypt


def administration(window):
    global frame3, admin_window, windows

    windows = window
    admin_window = tk.Toplevel(windows)
    admin_window.title("adminsistration")
    admin_window.geometry("800x600")
    rgb_color_admin = (139, 201, 194)
    hex_color_admin = '#%02x%02x%02x' % rgb_color_admin
    admin_window.configure(bg=hex_color_admin)

    # Frames for layout
    frame1 = Frame(admin_window, background="white")
    frame1.pack(side=TOP, pady=10)
    frame2 = Frame(admin_window, background="white", width=900)
    frame2.pack(side=TOP, pady=10)
    frame3 = Frame(admin_window, background="white", width=900)
    frame3.pack(side=TOP, pady=10)

    # Title
    label_title = Label(frame1, text="ADMINISTRATION : Utilisateur", font=("Arial", 18, "bold"))
    label_title.pack()

    # Buttons
    button_show = Button(frame2, text="Afficher les utilisateurs", font=("Arial", 12), background="lightgrey", command=show_user)
    button_show.grid(row=2, column=1)
    button_create = Button(frame2, text="Créer un utilisateurs", font=("Arial", 12), background="lightgrey", command=create_user)
    button_create.grid(row=2, column=2)

    # Column Headers
    headers = ["Utilisateurs", "Niveau d'accès"]
    for col, header in enumerate(headers):
        label = tk.Label(frame3, text=header, font=("Arial", 12, "bold"))
        label.grid(row=0, column=col, padx=35)


def show_user():
    global frame3
    running = True

    # Retrieve data from the database
    try:
        data = database.read_user()
    except:
        running = False

    if running:
        # Clear existing widgets in frame3
        for widget in frame3.winfo_children():
            widget.destroy()

        # Add headers to frame3
        headers = ["Utilisateurs", "Niveau d'accès"]
        for col, header in enumerate(headers):
            label = tk.Label(frame3, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=col, padx=35)

        for i, result in enumerate(data):
            # Display result data
            for col, value in enumerate(result):
                label = tk.Label(frame3, text=value, font=("Arial", 10))
                label.grid(row=i + 1, column=col, padx=30)
                # Add buttons for delete and update operations
                button_delete = Button(frame3, text="supprimer", font=("Arial", 12), background="lightgrey",
                                       command=lambda row=i + 1: delete_user(row, 0))
                button_delete.grid(row=i + 1, column=7)
                button_update = Button(frame3, text="modifier", font=("Arial", 12), background="lightgrey",
                                       command=lambda row=i + 1: update_user(row, 0))
                button_update.grid(row=i + 1, column=8)


def create_user():
    global entry_user, entry_access, entry_password, entry_confpassword, create_user_window, windows

    # Create a new window for data entry
    create_user_window = tk.Toplevel(windows)
    create_user_window.title("Création d'un utilisateur")
    create_user_window.geometry("850x200")
    rgb_color_create_user = (139, 201, 194)
    hex_color_create_user = '#%02x%02x%02x' % rgb_color_create_user
    create_user_window.configure(bg=hex_color_create_user)

    frame1 = Frame(create_user_window, background="white")
    frame1.pack(side=TOP, pady=10)
    frame2 = Frame(create_user_window, background="white", width=900)
    frame2.pack(side=TOP, pady=10)

    # Entry fields for user input
    label_user = Label(frame1, text="Utilisateurs :", font=("Arial", 12))
    label_user.grid(row=1, column=1)
    entry_user = Entry(frame1, font=("Arial", 12), width=20)
    entry_user.grid(row=2, column=1, padx=10)
    label_access = Label(frame1, text="Niveau d'accès :", font=("Arial", 12))
    label_access.grid(row=1, column=2)
    entry_access = Entry(frame1, font=("Arial", 12), width=20)
    entry_access.grid(row=2, column=2, padx=10)
    label_password = Label(frame1, text="mot de passe :", font=("Arial", 12))
    label_password.grid(row=1, column=3)
    entry_password = Entry(frame1, font=("Arial", 12), width=20, show="●")
    entry_password.grid(row=2, column=3, padx=10)
    label_confpassword = Label(frame1, text="confirmation MDP :", font=("Arial", 12))
    label_confpassword.grid(row=1, column=4)
    entry_confpassword = Entry(frame1, font=("Arial", 12), width=20, show="●")
    entry_confpassword.grid(row=2, column=4, padx=10)

    # Button to submit data
    button = Button(frame2, text="Terminer", font=("Arial", 12), background="lightgrey", command=get_create_user)
    button.grid(row=1, column=2)


# Function to take the data for create row
def get_create_user():
    global entry_user, entry_access, entry_password, entry_confpassword, create_user_window

    password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    # Retrieve user input from entry widgets
    user = entry_user.get()
    access = entry_access.get()
    password = entry_password.get()
    conf_pw = entry_confpassword.get()

    # Check if any field is empty
    if user == "" or access == "" or password == "" or conf_pw == "":
        messagebox.showerror(parent=create_user_window, title="Erreur", message="Merci de bien remplir tous les champs pour pouvoir insérer un nouvel utilisateur")
    else:
        if password == conf_pw:
            if re.match(password_pattern, password):
                try:
                    hashpw = hash_password(password)
                    messagebox.showinfo(parent=create_user_window, title="Succès", message="Vos données ont bien été ajoutées à la base de données")
                    database.create_user_db(user, hashpw, access, create_user_window)
                    show_user()
                except ValueError as ve:
                    messagebox.showerror(parent=create_user_window, title="Erreur", message=f"{ve}")
            else:
                messagebox.showerror(parent=create_user_window, title="Erreur", message="Votre mot de passe n'est pas assez fort il doit comprendre une majuscule, une minuscule, un chiffre, un caractère spéciale et 8 caractère minimum")
        else:
            messagebox.showerror(parent=create_user_window, title="Erreur", message="le mot de passe n'est pas écivalent à sa confirmation")


# Function for delete data
def delete_user(row, col_name):
    global admin_window
    # Ask for confirmation before deleting
    result = messagebox.askquestion(parent=admin_window, title="Question", message="Êtes-vous sûr de vouloir supprimer cette ligne ?")
    if result == 'no':
        messagebox.showinfo(parent=admin_window, title="Info", message="Les données restent intactes")
    else:
        # Get name and date from the selected row
        name = frame3.grid_slaves(row=row, column=col_name)
        if name:
            name_widget = name[0]
        if isinstance(name_widget, tk.Label):
            name_obj = name_widget.cget('text')
        # Delete data from the database
        database.delete_user(name_obj)
        messagebox.showinfo(parent=admin_window, title="Info", message="Les données ont été supprimées. N'oubliez pas d'actualiser.")
        show_user()


# Function for update data
def update_user(row, col_name):
    global entry_pseudo, entry_password, entry_confpw, entry_access,  update_user_window, windows

    # Create a new window for data update
    update_user_window = tk.Toplevel(windows)
    update_user_window.title("Modification d'utilisateurs")
    update_user_window.geometry("850x200")
    rgb_color_update_user = (139, 201, 194)
    hex_color_update_user = '#%02x%02x%02x' % rgb_color_update_user
    update_user_window.configure(bg=hex_color_update_user)

    frame1 = Frame(update_user_window, background="white")
    frame1.pack(side=TOP, pady=10)
    frame2 = Frame(update_user_window, background="white", width=900)
    frame2.pack(side=TOP, pady=10)

    # Entry fields for user input
    label_pseudo = Label(frame1, text="Utilisateur :", font=("Arial", 12))
    label_pseudo.grid(row=1, column=1)
    entry_pseudo = Entry(frame1, font=("Arial", 12), width=20)
    entry_pseudo.grid(row=2, column=1, padx=10)
    label_password = Label(frame1, text="Mot de passe :", font=("Arial", 12))
    label_password.grid(row=1, column=2)
    entry_password = Entry(frame1, font=("Arial", 12), width=20, show="●")
    entry_password.grid(row=2, column=2, padx=10)
    label_confpw = Label(frame1, text="Confirmation MDP :", font=("Arial", 12))
    label_confpw.grid(row=1, column=3)
    entry_confpw = Entry(frame1, font=("Arial", 12), width=20, show="●")
    entry_confpw.grid(row=2, column=3, padx=10)
    label_access = Label(frame1, text="Niveau d'accès :", font=("Arial", 12))
    label_access.grid(row=1, column=4)
    entry_access = Entry(frame1, font=("Arial", 12), width=20)
    entry_access.grid(row=2, column=4, padx=10)

    button = Button(frame2, text="Terminer", font=("Arial", 12), background="lightgrey", command=lambda: get_update_user(row, col_name))
    button.grid(row=1, column=2)


# Function to take the data for update row
def get_update_user(row, col_name):
    global entry_pseudo, entry_password, entry_confpw, entry_access,  update_user_window

    hashpw = ""
    password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    # Retrieve updated data from entry widgets
    user = entry_pseudo.get()
    password = entry_password.get()
    confpw = entry_confpw.get()
    access = entry_access.get()

    # Get name from the selected row
    name = frame3.grid_slaves(row=row, column=col_name)

    if name:
        name_widget = name[0]
    if isinstance(name_widget, tk.Label):
        name_obj = name_widget.cget('text')

    # Check if any field is empty
    if user == "" and password == "" and confpw == "" and access == "":
        messagebox.showerror(parent=update_user_window, title="Erreur", message="Aucun champ n'est rempli")
    else:
        if password == confpw:
            if not password == "":
                if re.match(password_pattern, password):
                    hashpw = hash_password(password)
                else:
                    messagebox.showerror(parent=update_user_window, title="Erreur", message="Votre mot de passe n'est pas assez fort il doit comprendre une majuscule, une minuscule, un chiffre, un caractère spéciale et 8 caractère minimum")
                    return
            try:
                database.update_user(user, hashpw, access, name_obj, update_user_window)
            except ValueError as ve:
                messagebox.showerror(parent=update_user_window, title="Erreur", message=f"{ve}")
            else:
                messagebox.showinfo(parent=update_user_window, title="Succès", message="Les données ont bien été modifiées dans la base de données (la fenêtre s'est fermée)")
                update_user_window.destroy()
                show_user()
        else:
            messagebox.showerror(parent=update_user_window, title="Erreur", message="le mot de passe n'est pas écivalent à sa confirmation")


def hash_password(password):
    password = password
    password_bytes = password.encode('utf-8')
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')
