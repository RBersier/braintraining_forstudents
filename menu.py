#############################
# Training (Menu)
# JCY oct 23
# PRO DB PY
#############################
import mysql.connector
import tkinter as tk
from tkinter import *
from tkinter import ttk
import geo01
import info02
import info05
import database

# exercises array
a_exercise=["geo01", "info02", "info05"]
albl_image=[None, None, None] # label (with images) array
a_image=[None, None, None] # images array
a_title=[None, None, None] # array of title (ex: GEO01)

dict_games = {"geo01": geo01.open_window_geo_01, "info02": info02.open_window_info_02, "info05": info05.open_window_info_05}

# call other windows (exercices)
def exercise(event,exer):
    dict_games[exer](window)


#call display_results
def display_result(event):
    # Créer une nouvelle fenêtre pour afficher les résultats
    results_window = tk.Toplevel(window)
    results_window.title("Résultats")
    style = ttk.Style()

    # Définission du Tableau
    result_table = ttk.Treeview(results_window)
    result_table["columns"] = ("Élève", "Date Heure", "Temps", "Exercice", "Nb OK", "Nb Total", "% Réussi")
    result_table.column("#0", width=0, stretch=NO)
    result_table.column("Élève", anchor=CENTER, width=200)
    result_table.column("Date Heure", anchor=CENTER, width=200)
    result_table.column("Temps", anchor=CENTER, width=200)
    result_table.column("Exercice", anchor=CENTER, width=200)
    result_table.column("Nb OK", anchor=CENTER, width=200)
    result_table.column("Nb Total", anchor=CENTER, width=200)
    result_table.column("% Réussi", anchor=CENTER, width=200)

    result_table.heading("#0", text="", anchor=CENTER)
    result_table.heading("Élève", anchor=CENTER, text="Élève")
    result_table.heading("Date Heure", anchor=CENTER, text="Date Heure")
    result_table.heading("Temps", anchor=CENTER, text="Temps")
    result_table.heading("Exercice", anchor=CENTER, text="Exercice")
    result_table.heading("Nb OK", anchor=CENTER, text="Nb OK")
    result_table.heading("Nb Total", anchor=CENTER, text="Nb Total")
    result_table.heading("% Réussi", anchor=CENTER, text="% Réussi")

    #affichage des donnée
    data = database.read_result()
    for i, result in enumerate(data):
        percent = (result[4]/result[5]) * 100
        progress_value = int(percent)
        if percent <= 33:
            style.configure("Custom.Horizontal.TProgressbar", background="red")
        elif 34 <= percent <= 67:
            style.configure("Custom.Horizontal.TProgressbar", background="orange")
        else:
            style.configure("Custom.Horizontal.TProgressbar", background="green")

        progress_bar = ttk.Progressbar(result_table, orient="horizontal", length=100, mode="determinate", value=progress_value, style="Custom.Horizontal.TProgressbar")
        result_table.insert(parent='', index='end', iid=i, values=(result[0], result[1], result[2], result[3], result[4], result[5], progress_bar))

    result_table.pack()


# Main window
window = tk.Tk()
window.title("Training, entrainement cérébral")
window.geometry("1100x900")

# color définition
rgb_color = (139, 201, 194)
hex_color = '#%02x%02x%02x' % rgb_color # translation in hexa
window.configure(bg=hex_color)
window.grid_columnconfigure((0,1,2), minsize=300, weight=1)

# Title création
lbl_title = tk.Label(window, text="TRAINING MENU", font=("Arial", 15))
lbl_title.grid(row=0, column=1,ipady=5, padx=40,pady=40)

# labels creation and positioning
for ex in range(len(a_exercise)):
    a_title[ex]=tk.Label(window, text=a_exercise[ex], font=("Arial", 15))
    a_title[ex].grid(row=1+2*(ex//3),column=ex % 3 , padx=40,pady=10) # 3 label per row

    a_image[ex] = tk.PhotoImage(file="img/" + a_exercise[ex] + ".gif") # image name
    albl_image[ex] = tk.Label(window, image=a_image[ex]) # put image on label
    albl_image[ex].grid(row=2 + 2*(ex // 3), column=ex % 3, padx=40, pady=10) # 3 label per row
    albl_image[ex].bind("<Button-1>", lambda event, ex = ex :exercise(event=None, exer=a_exercise[ex])) #link to others .py
    print(a_exercise[ex])

# Buttons, display results & quit
btn_display = tk.Button(window, text="Display results", font=("Arial", 15))
btn_display.grid(row=1+ 2*len(a_exercise)//3 , column=1)
btn_display.bind("<Button-1>",lambda e: display_result(e))

btn_finish = tk.Button(window, text="Quitter", font=("Arial", 15))
btn_finish.grid(row=2+ 2*len(a_exercise)//3 , column=1)
btn_finish.bind("<Button-1>", quit)

# main loop
window.mainloop()
