############################
# Training (Menu)
# JCY oct 23
# PRO DB PY
############################
import tkinter as tk
import geo01
import info02
import info05
import CRUD_results
import CRUD_users

# Arrays for exercise data
a_exercise = ["geo01", "info02", "info05"]
albl_image = [None, None, None]  # Label (with images) array
a_image = [None, None, None]  # Images array
a_title = [None, None, None]  # Array of titles (e.g., GEO01)

# Dictionary to map exercise names to their corresponding functions
dict_games = {"geo01": geo01.open_window_geo_01, "info02": info02.open_window_info_02,"info05": info05.open_window_info_05}


# Function to open other windows (exercises)
def exercise(event, exer):
    dict_games[exer](window)


def return_login():
    from register_login import login


# Main part of your code
# Main window creation
def main(levelofaccess):
    global window
    window = tk.Tk()
    window.title("Training, entraînement cérébral")
    window.geometry("1100x900")

    # Color definition
    rgb_color = (139, 201, 194)
    hex_color = '#%02x%02x%02x' % rgb_color
    window.configure(bg=hex_color)
    window.grid_columnconfigure((0, 1, 2), minsize=300, weight=1)

    # Title creation
    lbl_title = tk.Label(window, text="TRAINING MENU", font=("Arial", 15))
    lbl_title.grid(row=0, column=1, ipady=5, padx=40, pady=40)

    # Labels creation and positioning for exercises
    for ex in range(len(a_exercise)):
        a_title[ex] = tk.Label(window, text=a_exercise[ex], font=("Arial", 15))
        a_title[ex].grid(row=1 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)

        a_image[ex] = tk.PhotoImage(file="img/" + a_exercise[ex] + ".gif")
        albl_image[ex] = tk.Label(window, image=a_image[ex])
        albl_image[ex].grid(row=2 + 2 * (ex // 3), column=ex % 3, padx=40, pady=10)
        albl_image[ex].bind("<Button-1>", lambda event, ex=ex: exercise(event=None, exer=a_exercise[ex]))

    # Buttons for displaying results and quitting
    if levelofaccess > 1:
        btn_display = tk.Button(window, text="Display results", font=("Arial", 15))
        btn_display.grid(row=1 + 2 * len(a_exercise) // 3, column=1)
        btn_display.bind("<Button-1>", lambda e: CRUD_results.display_result(e, window))

    btn_finish = tk.Button(window, text="Quitter", font=("Arial", 15))
    btn_finish.grid(row=4 + 2 * len(a_exercise) // 3, column=1)
    btn_finish.bind("<Button-1>", quit)

    if levelofaccess > 2:
        btn_admin = tk.Button(window, text="Administration", font=("Arial", 15), command=lambda : CRUD_users.administration(window))
        btn_admin.grid(row=2 + 2 * len(a_exercise) // 3, column=1)

    btn_logout = tk.Button(window, text="Logout", font=("Arial", 15), command=lambda: [window.destroy(), return_login()])
    btn_logout.grid(row=3 + 2 * len(a_exercise) // 3, column=1)

    # Main loop
    window.mainloop()
