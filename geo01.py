# Training (GEO01)
# JCY oct 23
# PRO DB PY

import tkinter as tk
from tkinter import messagebox
import random
from math import sqrt
import time
import database
import datetime

# Main window
# graphical variables
l = 1000 # canvas length
h = 500 # canvas height
target_x = 10 # x & y to find
target_y = 10
scale = 47.5 #100 pixels for x=1
mycircle= None #objet utilisé pour le cercle rouge


#important data (to save)
entry_pseudo=None
pseudo=""
exercise="GEO01"
nbtrials=0 #number of total trial
nbsuccess=0 #number of successfull trials


# on canvas click, check if succeded or failed
def canvas_click(event):
    global mycircle, nbtrials, nbsuccess
    # x et y clicked
    click_x = (event.x - l/2) / scale
    click_y = -(event.y - h/2) / scale

    # distance between clicked and (x,y)
    dx = abs(click_x - target_x)
    dy = abs(click_y - target_y)
    d = sqrt((dx)**2 + (dy)**2) # Pythagore

    # display a red circle where clicked (global variable mycircle)
    mycircle = circle(target_x,target_y,0.5,"red")

    # check succeeded or failed
    nbtrials+=1
    if d > 0.5:
        window_geo01.configure(bg="red")
    else:
        window_geo01.configure(bg="green")
        nbsuccess += 1
    lbl_result.configure(text=f"{pseudo} Essais réussis : {nbsuccess} / {nbtrials}")
    window_geo01.update()
    time.sleep(1) # delai 1s
    next_point(event=None)


def circle(x,y,r,color):
    #circle, center x & y, r radius, color
    mycircle=canvas.create_oval((x - r) * scale + l/2, -(y-r) * scale + h/2, (x + r) * scale + l/2, -(y + r)* scale + h/2, fill=color)
    return mycircle


def next_point(event):
    global target_x, target_y, mycircle
    window_geo01.configure(bg=hex_color)#remettre couleur normale
    print("next_point " + str(event))
    #Clearing the canvas
    canvas.delete('all')

    # x & y axis
    canvas.create_line(0, h/2, l, h/2, fill="black")  # x
    canvas.create_line(l/2, 0, l/2, h, fill="black")  # y
    # graduation -10 +10
    for i in range(-10,11,5):
        canvas.create_line(l/2+i*scale, h/2-10,l/2+i*scale, h/2+10, fill="black")  # on x
        canvas.create_text(l/2+i*scale, h/2+20, text=i, fill="black", font=("Helvetica 15"))
    for i in range(-5,6,5):
        canvas.create_line(l/2-10, h/2-i*scale,l/2+10, h/2-i*scale, fill="black")  # y
        canvas.create_text(l/2-20, h/2-i*scale, text=i, fill="black", font=("Helvetica 15"))

    # x & y random
    target_x = round(random.uniform(-10, 10),0)
    target_y = round(random.uniform(-5, 5),0)

    # display x & y, 1 decimal
    lbl_target.configure(text=f"Cliquez sur le point ({round(target_x, 1)}, {round(target_y, 1)}). Echelle x -10 à +10, y-5 à +5")


def display_timer():
    duration=datetime.datetime.now()-start_date #elapsed time since beginning, in time with decimals
    duration_s=int(duration.total_seconds()) #idem but in seconds (integer)
    #display min:sec (00:13)
    lbl_duration.configure(text="{:02d}".format(int(duration_s /60)) + ":" + "{:02d}".format(duration_s %60))
    window_geo01.after(1000, display_timer) #recommencer après 15 ms


def finish():
    global exercise, nbtrials, nbsuccess, pseudo, entry_pseudo

    # Obtenir la valeur de l'entrée pour pseudo
    pseudo = entry_pseudo.get()

    # condition pour pas de division par 0
    if nbtrials == 0:
        messagebox.showerror(title="Erreur", message="Vous devez faire au moin 1 essai avant de terminer la partie")
    else:
        # Calculer le temps écoulé
        end_date = datetime.datetime.now()
        elapsed_time = end_date - start_date
        total_seconds = elapsed_time.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

        # Enregistrer les valeurs dans la base de données
        database.save_results(exercise, pseudo, duration, nbtrials, nbsuccess)

        # Fermer la fenêtre et la base de donnée
        database.close_dbconnection()
        nbtrials = 0
        nbsuccess = 0
        window_geo01.destroy()


def open_window_geo_01(window):
    # window = tk.Tk()
    global window_geo01, hex_color, lbl_title, lbl_duration, lbl_result, lbl_target, canvas, start_date, pseudo, entry_pseudo
    window_geo01 = tk.Toplevel(window)

    window_geo01.title("Exercice de géométrie")
    window_geo01.geometry("1100x900")

    # colors définition
    rgb_color = (139, 201, 194)
    hex_color = '#%02x%02x%02x' % rgb_color # translation in hexa
    window_geo01.configure(bg=hex_color)

    # Canvas creation
    lbl_title = tk.Label(window_geo01, text=f"{exercise}", font=("Arial", 15))
    lbl_title.grid(row=0, column=1, padx=5, pady=5)

    lbl_duration = tk.Label(window_geo01, text="0:00", font=("Arial", 15))
    lbl_duration.grid(row=0,column=2, ipady=5, padx=10,pady=10)

    tk.Label(window_geo01, text='Pseudo:', font=("Arial", 15)).grid(row=1, column=0, padx=5, pady=5)
    entry_pseudo = tk.Entry(window_geo01, font=("Arial", 15))
    entry_pseudo.grid(row=1, column=1)

    lbl_result = tk.Label(window_geo01, text=f"Essais réussis : 0/0", font=("Arial", 15))
    lbl_result.grid(row=1, column=3, padx=5, pady=5, columnspan=4)

    lbl_target = tk.Label(window_geo01, text="", font=("Arial", 15))
    lbl_target.grid(row=2, column=0, padx=5, pady=5, columnspan=6)

    canvas = tk.Canvas(window_geo01, width=l, height=h, bg="#f9d893")
    canvas.grid(row=4, column=0, padx=5, pady=5, columnspan=6)
    btn_next = tk.Button(window_geo01, text="Suivant", font=("Arial", 15))
    btn_next.grid(row=5, column=0, padx=5, pady=5, columnspan=6)

    btn_finish = tk.Button(window_geo01, text="Terminer", font=("Arial", 15))
    btn_finish.grid(row=6, column=0, columnspan=6)

    # first call of next_point
    next_point(event=None)
    start_date = datetime.datetime.now()
    display_timer()

    # first call of next_point
    # binding actions (canvas & buttons)
    canvas.bind("<Button-1>", canvas_click)
    btn_next.bind("<Button-1>", next_point)
    btn_finish.bind("<ButtonRelease-1>",lambda event=None: finish())

    # main loop
    window_geo01.mainloop()
