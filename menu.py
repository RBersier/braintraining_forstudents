############################
# Training (Menu)
# JCY oct 23
# PRO DB PY
############################
import mysql.connector
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import geo01
import info02
import info05
import database

# exercises array
a_exercise = ["geo01", "info02", "info05"]
albl_image = [None, None, None]  # label (with images) array
a_image = [None, None, None]  # images array
a_title = [None, None, None]  # array of title (ex: GEO01)

dict_games = {"geo01": geo01.open_window_geo_01, "info02": info02.open_window_info_02,
              "info05": info05.open_window_info_05}


# call other windows (exercises)
def exercise(event, exer):
    dict_games[exer](window)


# call display_results
def display_result(event):
    global frame3, entry_pseudo, entry_exercise, entry_startdate, entry_enddate
    results_window = tk.Toplevel(window)
    results_window.title("Résultats")
    results_window.geometry("1200x500")
    rgb_color_result = (139, 201, 194)
    hex_color_result = '#%02x%02x%02x' % rgb_color_result
    results_window.configure(bg=hex_color_result)
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("red.Horizontal.TProgressbar", background='red')
    style.configure("yellow.Horizontal.TProgressbar", background='yellow')
    style.configure("green.Horizontal.TProgressbar", background='green')
    frame1 = Frame(results_window, background="white")
    frame1.pack(side=TOP, pady=10)
    frame2 = Frame(results_window, background="white", width=900)
    frame2.pack(side=TOP, pady=10)
    frame3 = Frame(results_window, background="white", width=900)
    frame3.pack(side=TOP, pady=10)

    # Title
    label_title = Label(frame1, text="TRAINING : AFFICHAGE", font=("Arial", 18, "bold"))
    label_title.pack()

    # Filter
    label_pseudo = Label(frame2, text="Pseudo :", font=("Arial", 12))
    label_pseudo.grid(row=1, column=1, padx=31)
    entry_pseudo = Entry(frame2, font=("Arial", 12), width=10)
    entry_pseudo.grid(row=1, column=2)
    label_exercise = Label(frame2, text="Exercice :", font=("Arial", 12))
    label_exercise.grid(row=1, column=3, padx=31)
    entry_exercise = Entry(frame2, font=("Arial", 12), width=10)
    entry_exercise.grid(row=1, column=4)
    label_startdate = Label(frame2, text="Date de début :", font=("Arial", 12))
    label_startdate.grid(row=1, column=5, padx=31)
    entry_startdate = Entry(frame2, font=("Arial", 12), width=10)
    entry_startdate.grid(row=1, column=6)
    label_enddate = Label(frame2, text="Date de fin :", font=("Arial", 12))
    label_enddate.grid(row=1, column=7, padx=31)
    entry_enddate = Entry(frame2, font=("Arial", 12), width=10)
    entry_enddate.grid(row=1, column=8)

    # Button
    button_show = Button(frame2, text="Afficher les résultat", font=("Arial", 12), background="lightgrey", command=filters)
    button_show.grid(row=2, column=1)
    button_create = Button(frame2, text="Créer un résultat", font=("Arial", 12), background="lightgrey", command=create)
    button_create.grid(row=2, column=2)

    # Name of column
    headers = ["Élève", "Date et Heure", "Temps", "Exercice", "Nb OK", "Nb Total", "% Réussi"]
    for col, header in enumerate(headers):
        label = tk.Label(frame3, text=header, font=("Arial", 12, "bold"))
        label.grid(row=0, column=col, padx=35)


def filters():
    global frame3, entry_pseudo, entry_exercise, entry_startdate, entry_enddate
    pseudo = entry_pseudo.get()
    exercise = entry_exercise.get()
    startdate = entry_startdate.get()
    enddate = entry_enddate.get()
    running = True
    # Données
    try:
        data = database.read_result(pseudo, exercise, startdate, enddate)
    except:
        running = False
    if running:
        for widget in frame3.winfo_children():
            widget.destroy()
        headers = ["Élève", "Date et Heure", "Temps", "Exercice", "Nb OK", "Nb Total", "% Réussi"]
        for col, header in enumerate(headers):
            label = tk.Label(frame3, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=col, padx=35)

        for i, result in enumerate(data):
            percent = (result[4] / result[5]) * 100
            progress_value = int(percent)
            if progress_value <= 33:
                progress_bar = ttk.Progressbar(frame3, orient="horizontal", length=100, mode="determinate", value=progress_value, style="red.Horizontal.TProgressbar")
            elif 34 <= progress_value <= 66:
                progress_bar = ttk.Progressbar(frame3, orient="horizontal", length=100, mode="determinate", value=progress_value, style="yellow.Horizontal.TProgressbar")
            else:
                progress_bar = ttk.Progressbar(frame3, orient="horizontal", length=100, mode="determinate", value=progress_value, style="green.Horizontal.TProgressbar")
            progress_bar.grid(row=i + 1, column=6)

            # Show data
            for col, value in enumerate(result):
                label = tk.Label(frame3, text=value, font=("Arial", 10))
                label.grid(row=i + 1, column=col, padx=30)
                button_delete = Button(frame3, text="delete", font=("Arial", 12), background="lightgrey", command=lambda row=i + 1: delete(row, 0, 1))
                button_delete.grid(row=i + 1, column= 7)
                button_update = Button(frame3, text="update", font=("Arial", 12), background="lightgrey", command=lambda row=i + 1: update(row, 0, 1))
                button_update.grid(row=i + 1, column= 8)


def create():
    global entry_Student, entry_Date, entry_Time, entry_Exercise, entry_Nbok, entry_Nbtot, create_window

    create_window = tk.Toplevel(window)
    create_window.title("Création d'un utilisateurs")
    create_window.geometry("650x200")
    rgb_color_result = (139, 201, 194)
    hex_color_result = '#%02x%02x%02x' % rgb_color_result
    create_window.configure(bg=hex_color_result)

    frame1 = Frame(create_window, background="white")
    frame1.pack(side=TOP, pady=10)
    frame2 = Frame(create_window, background="white", width=900)
    frame2.pack(side=TOP, pady=10)

    # Columns
    label_Student = Label(frame1, text="Eleve :", font=("Arial", 12))
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

    # Button
    button = Button(frame2, text="Terminer", font=("Arial", 12), background="lightgrey", command=get_create)
    button.grid(row=1, column=2)


def get_create():
    global entry_Student, entry_Date, entry_Time, entry_Exercise, entry_Nbok, entry_Nbtot, create_window

    student = entry_Student.get()
    date = entry_Date.get()
    time = entry_Time.get()
    exercise = entry_Exercise.get()
    nbok = entry_Nbok.get()
    nbtot = entry_Nbtot.get()

    if student == "" or date == "" or time == "" or exercise == "" or nbok == "" or nbtot == "":
        messagebox.showerror(title="Erreur", message="Merci de bien remplire tout les champs pour pouvoir insérer de nouveau résultat (Attention la précédente fenêtre n'est pas fermé)")
    else:
        database.create_result(student, date, time, exercise, nbok, nbtot)
        create_window.destroy()
        messagebox.showinfo(title="Succès", message="vos données ont belle est bien été ajouté a la base de donnée (la fenêtre s'est fermé")


def delete(row, col_name, col_date):
    result = messagebox.askquestion("Question", "Êtes-vous sûr de vouloir supprimer cette ligne ?")
    if result == 'no':
        messagebox.showinfo(title="Info", message="les données reste intacte")
    else:
        name = frame3.grid_slaves(row=row, column=col_name)
        date = frame3.grid_slaves(row=row, column=col_date)
        if name and date:
            name_widget = name[0]
            date_widget = date[0]
        if isinstance(name_widget and date_widget, tk.Label):
            name_obj = name_widget.cget('text')
            date_obj = date_widget.cget('text')
        database.delete_result(name_obj, date_obj)
        messagebox.showinfo(title="Info", message="les données ont été suprimées n'oubliez pas d'actualiser")


def update(row, col_name, col_date):
    global entry_Time, entry_Nbok, entry_Nbtot, update_window

    update_window = tk.Toplevel(window)
    update_window.title("Modification de données")
    update_window.geometry("700x200")
    rgb_color_result = (139, 201, 194)
    hex_color_result = '#%02x%02x%02x' % rgb_color_result
    update_window.configure(bg=hex_color_result)

    frame1 = Frame(update_window, background="white")
    frame1.pack(side=TOP, pady=10)
    frame2 = Frame(update_window, background="white", width=900)
    frame2.pack(side=TOP, pady=10)

    # Columns
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

    button = Button(frame2, text="Terminer", font=("Arial", 12), background="lightgrey", command=lambda: get_update(row, col_name, col_date))
    button.grid(row=1, column=2)


def get_update(row, col_name, col_date):
    global entry_Time, entry_Nbok, entry_Nbtot, update_window

    time = entry_Time.get()
    nbok = entry_Nbok.get()
    nbtot = entry_Nbtot.get()

    name = frame3.grid_slaves(row=row, column=col_name)
    date = frame3.grid_slaves(row=row, column=col_date)

    if name and date:
        name_widget = name[0]
        date_widget = date[0]
    if isinstance(name_widget and date_widget, tk.Label):
        name_obj = name_widget.cget('text')
        date_obj = date_widget.cget('text')

    if time == "" and nbok == "" and nbtot == "":
        messagebox.showerror(title="Erreur", message="Aucun champ n'est rempli ou un ou plusieurs champs ne correspondent pas (nb ok et nb totale doivent être des entiers, et le format de temps doit être hh:mm:ss) (Attention, la précédente fenêtre n'est pas fermée)")
    else:
        database.update_result(time, nbok, nbtot, name_obj, date_obj)
        update_window.destroy()
        messagebox.showinfo(title="Succès", message="les données ont belle est bien été modifié a la base de donnée (la fenêtre s'est fermé")


# Main windows
window = tk.Tk()
window.title("Training, entrainement cérébral")
window.geometry("1100x900")

# color définition
rgb_color = (139, 201, 194)
hex_color = '#%02x%02x%02x' % rgb_color  # translation in hexa
window.configure(bg=hex_color)
window.grid_columnconfigure((0, 1, 2), minsize=300, weight=1)

# Title création
lbl_title = tk.Label(window, text="TRAINING MENU", font=("Arial", 15))
lbl_title.grid(row=0, column=1, ipady=5, padx=40, pady=40)

# labels creation and positioning
for ex in range(len(a_exercise)):
    a_title[ex] = tk.Label(window, text=a_exercise[ex], font=("Arial", 15))
    a_title[ex].grid(row=1 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)  # 3 label per row

    a_image[ex] = tk.PhotoImage(file="img/" + a_exercise[ex] + ".gif")  # image name
    albl_image[ex] = tk.Label(window, image=a_image[ex])  # put image on label
    albl_image[ex].grid(row=2 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)  # 3 label per row
    albl_image[ex].bind("<Button-1>",
                        lambda event, ex=ex: exercise(event=None, exer=a_exercise[ex]))  # link to others .py
    print(a_exercise[ex])

# Buttons, display results & quit
btn_display = tk.Button(window, text="Display results", font=("Arial", 15))
btn_display.grid(row=1 + 2 * len(a_exercise) // 3, column=1)
btn_display.bind("<Button-1>", lambda e: display_result(e))

btn_finish = tk.Button(window, text="Quitter", font=("Arial", 15))
btn_finish.grid(row=2 + 2 * len(a_exercise) // 3, column=1)
btn_finish.bind("<Button-1>", quit)

# main loop
window.mainloop()
