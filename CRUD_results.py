"""
Project: class_order_management
Module: MA-DBPY
Date: 12.01.24
Author: Ryan Bersier
Version: 1.0
"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import database
from datetime import datetime


# Function for create the main window to manage result
def display_result(event, window):
    global frame3, entry_pseudo, entry_exercise, entry_startdate, entry_enddate, page, results_window, windows

    # Global variables for window management
    windows = window
    results_window = tk.Toplevel(window)
    results_window.title("Résultats")
    results_window.geometry("1200x600")
    rgb_color_result = (139, 201, 194)
    hex_color_result = '#%02x%02x%02x' % rgb_color_result
    results_window.configure(bg=hex_color_result)

    # create a style for a progressbar
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("red.Horizontal.TProgressbar", background='red')
    style.configure("yellow.Horizontal.TProgressbar", background='yellow')
    style.configure("green.Horizontal.TProgressbar", background='green')

    page = 0

    # Frames for layout
    frame1 = Frame(results_window, background="white")
    frame1.pack(side=TOP, pady=10)
    frame2 = Frame(results_window, background="white", width=900)
    frame2.pack(side=TOP, pady=10)
    frame3 = Frame(results_window, background="white", width=900)
    frame3.pack(side=TOP, pady=10)
    frame4 = Frame(results_window, background="white", width=900)
    frame4.pack(side=TOP, pady=10)

    # Title
    label_title = Label(frame1, text="ENTRAINEMENT : AFFICHAGE", font=("Arial", 18, "bold"))
    label_title.pack()

    # Filters Section
    label_pseudo = Label(frame2, text="Pseudo :", font=("Arial", 12))
    label_pseudo.grid(row=1, column=1, padx=31)
    entry_pseudo = Entry(frame2, font=("Arial", 12), width=10)
    entry_pseudo.grid(row=1, column=2)
    label_exercise = Label(frame2, text="Exercice :", font=("Arial", 12))
    label_exercise.grid(row=1, column=3, padx=31)

    # Combobox for exercise selection
    exercise_value = tk.StringVar(frame2)
    entry_exercise = ttk.Combobox(frame2, textvariable=exercise_value, font=("Arial", 10), width=10, background="white")
    entry_exercise.grid(row=1, column=4)
    entry_exercise['values'] = ('', 'GEO01', 'INFO02', 'INFO05')
    entry_exercise['state'] = 'readonly'

    # Date Entry Widgets
    start = tk.StringVar()
    start.set("")
    end = tk.StringVar()
    end.set("")
    label_startdate = Label(frame2, text="Date de début :", font=("Arial", 12))
    label_startdate.grid(row=1, column=5, padx=31)
    entry_startdate = DateEntry(frame2, font=("Arial", 12), width=10, date_pattern='yyyy-mm-dd', textvariable=start)
    entry_startdate.grid(row=1, column=6)
    label_enddate = Label(frame2, text="Date de fin :", font=("Arial", 12))
    label_enddate.grid(row=1, column=7, padx=31)
    entry_enddate = DateEntry(frame2, font=("Arial", 12), width=10, date_pattern='yyyy-mm-dd', textvariable=end)
    entry_enddate.grid(row=1, column=8)

    # Buttons
    button_show = Button(frame2, text="Afficher les résultats", font=("Arial", 12), background="lightgrey", command=filters)
    button_show.grid(row=2, column=1)
    button_create = Button(frame2, text="Créer un résultat", font=("Arial", 12), background="lightgrey", command=create)
    button_create.grid(row=2, column=2)

    button_previouspage = Button(frame4, text="Page précédente", font=("Arial", 12), background="lightgrey", command=previouspage)
    button_previouspage.pack(side=LEFT)
    button_nextpage = Button(frame4, text="Page suivante", font=("Arial", 12), background="lightgrey", command=nextpage)
    button_nextpage.pack(side=LEFT)

    # Column Headers
    headers = ["Élève", "Date et Heure", "Temps", "Exercice", "Nb OK", "Nb Total", "% Réussi"]
    for col, header in enumerate(headers):
        label = tk.Label(frame3, text=header, font=("Arial", 12, "bold"))
        label.grid(row=0, column=col, padx=35)


# Function to filter the result
def filters():
    global frame3, entry_pseudo, entry_exercise, entry_startdate, entry_enddate, page, data
    pseudo = entry_pseudo.get()
    exercise = entry_exercise.get()
    startdate = entry_startdate.get()
    enddate = entry_enddate.get()
    running = True

    # Check if stardate < enddate or equal in the temporality
    if not startdate == "" and not enddate == "":
        conv_startdate = datetime.strptime(startdate, "%Y-%m-%d")
        conv_enddate = datetime.strptime(enddate, "%Y-%m-%d")
        if not conv_startdate <= conv_enddate:
            messagebox.showerror(parent=results_window, title="Erreur", message="Attention la date de début doit se situer avant la date de fin dans la chronologie temporelle")
            running = False

    # Retrieve data from the database
    try:
        data = database.read_result(pseudo, exercise, startdate, enddate)[page]
    except:
        running = False

    if running:
        # Clear existing widgets in frame3
        for widget in frame3.winfo_children():
            widget.destroy()

        # Add headers to frame3
        headers = ["Élève", "Date et Heure", "Temps", "Exercice", "Nb OK", "Nb Total", "% Réussi"]
        for col, header in enumerate(headers):
            label = tk.Label(frame3, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=col, padx=35)

        # Iterate through results and display them
        for i, result in enumerate(data):
            percent = (result[4] / result[5]) * 100
            progress_value = int(percent)
            # Determine progress bar style based on percentage
            if progress_value <= 33:
                progress_bar = ttk.Progressbar(frame3, orient="horizontal", length=100, mode="determinate",
                                               value=progress_value, style="red.Horizontal.TProgressbar")
            elif 34 <= progress_value <= 66:
                progress_bar = ttk.Progressbar(frame3, orient="horizontal", length=100, mode="determinate",
                                               value=progress_value, style="yellow.Horizontal.TProgressbar")
            else:
                progress_bar = ttk.Progressbar(frame3, orient="horizontal", length=100, mode="determinate",
                                               value=progress_value, style="green.Horizontal.TProgressbar")
            progress_bar.grid(row=i + 1, column=6)

            # Display result data
            for col, value in enumerate(result):
                label = tk.Label(frame3, text=value, font=("Arial", 10))
                label.grid(row=i + 1, column=col, padx=30)
                # Add buttons for delete and update operations
                button_delete = Button(frame3, text="supprimer", font=("Arial", 12), background="lightgrey",
                                       command=lambda row=i + 1: delete(row, 0, 1))
                button_delete.grid(row=i + 1, column=7)
                button_update = Button(frame3, text="modifier", font=("Arial", 12), background="lightgrey",
                                       command=lambda row=i + 1: update(row, 0, 1))
                button_update.grid(row=i + 1, column=8)


# Function to create results
def create():
    global entry_Student, entry_Date, entry_Time, entry_Exercise, entry_Nbok, entry_Nbtot, create_window

    # Create a new window for data entry
    create_window = tk.Toplevel(results_window)
    create_window.title("Création d'un résultat")
    create_window.geometry("650x200")
    rgb_color_result = (139, 201, 194)
    hex_color_result = '#%02x%02x%02x' % rgb_color_result
    create_window.configure(bg=hex_color_result)

    # Frames for layout
    frame1 = Frame(create_window, background="white")
    frame1.pack(side=TOP, pady=10)
    frame2 = Frame(create_window, background="white", width=900)
    frame2.pack(side=TOP, pady=10)

    # Entry fields for user input
    label_Student = Label(frame1, text="Élève :", font=("Arial", 12))
    label_Student.grid(row=1, column=1)
    entry_Student = Entry(frame1, font=("Arial", 12), width=20)
    entry_Student.grid(row=2, column=1, padx=10)
    label_Date = Label(frame1, text="Date et Heure :", font=("Arial", 12))
    label_Date.grid(row=1, column=2)
    entry_Date = Entry(frame1, font=("Arial", 12), width=20)
    entry_Date.grid(row=2, column=2, padx=10)
    label_Time = Label(frame1, text="Temps :", font=("Arial", 12))
    label_Time.grid(row=1, column=3)
    entry_Time = Entry(frame1, font=("Arial", 12), width=20)
    entry_Time.grid(row=2, column=3, padx=10)

    label_Exercise = Label(frame1, text="Exercice :", font=("Arial", 12))
    label_Exercise.grid(row=3, column=1)
    entry_Exercise = Entry(frame1, font=("Arial", 12), width=20)
    entry_Exercise.grid(row=4, column=1, padx=10)
    label_Nbok = Label(frame1, text="Nb OK :", font=("Arial", 12))
    label_Nbok.grid(row=3, column=2)
    entry_Nbok = Entry(frame1, font=("Arial", 12), width=20)
    entry_Nbok.grid(row=4, column=2, padx=10)
    label_Nbtot = Label(frame1, text="Nb Total :", font=("Arial", 12))
    label_Nbtot.grid(row=3, column=3)
    entry_Nbtot = Entry(frame1, font=("Arial", 12), width=20)
    entry_Nbtot.grid(row=4, column=3, padx=10)

    # Button to submit data
    button = Button(frame2, text="Terminer", font=("Arial", 12), background="lightgrey", command=get_create)
    button.grid(row=1, column=2)


# Function to take the data for create row
def get_create():
    global entry_Student, entry_Date, entry_Time, entry_Exercise, entry_Nbok, entry_Nbtot, create_window

    # Retrieve user input from entry widgets
    student = entry_Student.get()
    date = entry_Date.get()
    time = entry_Time.get()
    exercise = entry_Exercise.get()
    nbok = entry_Nbok.get()
    nbtot = entry_Nbtot.get()
    running = True

    # Check if nbok < nbtot or equal
    if not nbok == "" and not nbtot == "":
        if not nbok <= nbtot:
            messagebox.showerror(parent=create_window, title="Erreur", message="Merci de bien remplir faire en sorte que nbok doit être inférieur à nbtot")
            running = False

    if running:
        # Check if any field is empty
        if student == "" or date == "" or time == "" or exercise == "" or nbok == "" or nbtot == "":
            messagebox.showerror(parent=create_window, title="Erreur", message="Merci de bien remplir tous les champs pour pouvoir insérer un nouveau résultat")
        else:
            try:
                # Insert data into the database
                database.create_result(student, date, time, exercise, nbok, nbtot)
                messagebox.showinfo(parent=create_window, title="Succès", message="Vos données ont bien été ajoutées à la base de données (la fenêtre s'est fermée)")
                create_window.destroy()
                filters()
            except ValueError as ve:
                messagebox.showerror(parent=create_window, title="Erreur", message=f"{ve}")


# Function for delete data
def delete(row, col_name, col_date):
    # Ask for confirmation before deleting
    result = messagebox.askquestion(parent=results_window, title="Question", message="Êtes-vous sûr de vouloir supprimer cette ligne ?")
    if result == 'no':
        messagebox.showinfo(parent=results_window, title="Info", message="Les données restent intactes")
    else:

        # Get name and date from the selected row
        name = frame3.grid_slaves(row=row, column=col_name)
        date = frame3.grid_slaves(row=row, column=col_date)
        if name and date:
            name_widget = name[0]
            date_widget = date[0]
        if isinstance(name_widget and date_widget, tk.Label):
            name_obj = name_widget.cget('text')
            date_obj = date_widget.cget('text')

        # Delete data from the database
        database.delete_result(name_obj, date_obj)
        messagebox.showinfo(parent=results_window, title="Info", message="Les données ont été supprimées. N'oubliez pas d'actualiser.")
        filters()


# Function for update data
def update(row, col_name, col_date):
    global entry_Time, entry_Nbok, entry_Nbtot, update_window

    # Create a new window for data update
    update_window = tk.Toplevel(results_window)
    update_window.title("Modification de données")
    update_window.geometry("700x200")
    rgb_color_update = (139, 201, 194)
    hex_color_update = '#%02x%02x%02x' % rgb_color_update
    update_window.configure(bg=hex_color_update)

    # Frames for layout
    frame1 = Frame(update_window, background="white")
    frame1.pack(side=TOP, pady=10)
    frame2 = Frame(update_window, background="white", width=900)
    frame2.pack(side=TOP, pady=10)

    # Entry fields for user input
    label_Time = Label(frame1, text="Temps :", font=("Arial", 12))
    label_Time.grid(row=1, column=1)
    entry_Time = Entry(frame1, font=("Arial", 12), width=20)
    entry_Time.grid(row=2, column=1, padx=10)
    label_Nbok = Label(frame1, text="Nb OK :", font=("Arial", 12))
    label_Nbok.grid(row=1, column=2)
    entry_Nbok = Entry(frame1, font=("Arial", 12), width=20)
    entry_Nbok.grid(row=2, column=2, padx=10)
    label_Nbtot = Label(frame1, text="Nb Total :", font=("Arial", 12))
    label_Nbtot.grid(row=1, column=3)
    entry_Nbtot = Entry(frame1, font=("Arial", 12), width=20)
    entry_Nbtot.grid(row=2, column=3, padx=10)

    # Buttons
    button = Button(frame2, text="Terminer", font=("Arial", 12), background="lightgrey", command=lambda: get_update(row, col_name, col_date, update_window))
    button.grid(row=1, column=2)


# Function to take the data for update row
def get_update(row, col_name, col_date, update_window):
    global entry_Time, entry_Nbok, entry_Nbtot

    # Retrieve updated data from entry widgets
    time = entry_Time.get()
    nbok = entry_Nbok.get()
    nbtot = entry_Nbtot.get()
    running = True

    # Check if nbok < nbtot or equal
    if not nbok == "" and not nbtot == "":
        if not nbok <= nbtot:
            messagebox.showerror(parent=update_window, title="Erreur", message="Merci de bien remplir faire en sorte que nbok doit être inférieur à nbtot")
            running = False

    if running:
        # Get name and date from the selected row
        name = frame3.grid_slaves(row=row, column=col_name)
        date = frame3.grid_slaves(row=row, column=col_date)

        if name and date:
            name_widget = name[0]
            date_widget = date[0]
        if isinstance(name_widget and date_widget, tk.Label):
            name_obj = name_widget.cget('text')
            date_obj = date_widget.cget('text')

        # Check if any field is empty
        if time == "" and nbok == "" and nbtot == "":
            messagebox.showerror(parent=update_window, title="Erreur", message="Aucun champ n'est rempli ou un ou plusieurs champs ne correspondent pas (nb ok et nb total doivent être des entiers, et le format de temps doit être hh:mm:ss)")
        else:
            # Update data in the database
            try:
                database.update_result(time, nbok, nbtot, name_obj, date_obj)
                messagebox.showinfo(parent=update_window, title="Succès", message="Les données ont bien été modifiées dans la base de données")
                update_window.destroy()
                filters()
            except ValueError as ve:
                messagebox.showerror(parent=update_window, title="Erreur", message=f"{ve}")

# Function for turn next page
def nextpage():
    global page, data

    if page <= (len(data) - 3):
        page += 1
        filters()
    else:
        messagebox.showinfo(parent=results_window, title="Info", message="Vous êtes arrivé à la page maximum il n y a pas de donnée après")


# Function for turn previous page
def previouspage():
    global page

    if page > 0:
        page -= 1
        filters()
    else:
        messagebox.showinfo(parent=results_window, title="Info", message="Vous êtes arrivé à la page minimum il n y a pas de donnée avant")
