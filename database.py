"""
Project: class_order_management
Module: MA-DBPY
Date: 29.08.23
Author: Ryan Bersier
Version: 1.0
"""

import mysql.connector
from tkinter import messagebox
import datetime
from datetime import datetime


# Function for opening a session in MySQL
def open_dbconnection():
    global db_connection
    db_connection = mysql.connector.connect(host='127.0.0.1', port='3306', user='root', password='root',
                                            database='Braintrainning', buffered=True, autocommit=True)


# Save result in the database
def save_results(exercise, pseudo, duration, nbtrials, nbok):
    open_dbconnection()
    cursor = db_connection.cursor()

    # Check if the game exists
    query3 = "SELECT id FROM games WHERE exercise = %s"
    cursor.execute(query3, (exercise,))
    data1 = cursor.fetchone()

    # Check if the player exists
    query4 = "SELECT id FROM players WHERE pseudonym = %s"
    cursor.execute(query4, (pseudo,))
    data2 = cursor.fetchone()

    # If the game doesn't exist, insert it
    if data1 is None:
        query1 = "INSERT INTO games (exercise) values (%s)"
        cursor.execute(query1, (exercise,))
        query3 = "SELECT id FROM games WHERE exercise = %s"
        cursor.execute(query3, (exercise,))
        data1 = cursor.fetchone()
    # If the player doesn't exist, insert it
    elif data2 is None:
        query2 = "INSERT INTO players (pseudonym) values (%s)"
        cursor.execute(query2, (pseudo,))
        query4 = "SELECT id FROM players WHERE pseudonym = %s"
        cursor.execute(query4, (pseudo,))
        data2 = cursor.fetchone()

    x = datetime.datetime.now()
    date_hour = x.strftime("%Y-%m-%d %H:%M:%S")

    # Insert the result into the games_has_players table
    query5 = "INSERT INTO games_has_players (game_id, player_id, duration, startdate, nb_ok, nb_tot) values (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query5, (data1[0], data2[0], duration, date_hour, nbok, nbtrials))


# All data to show the results
def read_result(pseudo, exercise, startdate, enddate):
    open_dbconnection()
    cursor = db_connection.cursor()

    # Construct the base query
    query1 = "SELECT players.pseudonym, games_has_players.startdate, games_has_players.duration, games.exercise, games_has_players.nb_ok, games_has_players.nb_tot FROM games_has_players INNER JOIN players ON games_has_players.player_id = players.id INNER JOIN games ON games_has_players.game_id = games.id WHERE 1=1"

    # Add filters based on input parameters
    if not pseudo == "":
        query1 += f" AND players.pseudonym LIKE '{pseudo}%'"
    if not exercise == "":
        query1 += f" AND games.exercise LIKE '{exercise}%'"
    if not startdate == "":
        query1 += f" AND games_has_players.startdate >= '{startdate}'"
    if not enddate == "":
        query1 += f" AND games_has_players.startdate <= '{enddate}'"

    try:
        # Execute the query
        cursor.execute(query1)
        data = cursor.fetchall()
        query_data = []
        query_data.append([])
        actualN = 1
        for user in range(len(data)):
            query_data[actualN - 1].append(data[user])
            if user == (actualN * 9):
                query_data.append([])
                actualN += 1
    except:
        # Handle errors related to date format
        messagebox.showerror(title="Erreur", message="Il peut y avoir une erreur dans le format de la date de début ou de fin. Veuillez essayer le format suivant : AAAA-MM-JJ (Remarque : la fenêtre précédente n'est pas fermée)")
    return query_data


# Create a new result
def create_result(student, date, time, exercise, nbok, nbtot):
    open_dbconnection()
    cursor = db_connection.cursor()

    # Check if the game exists
    query3 = "SELECT id FROM games WHERE exercise = %s"
    cursor.execute(query3, (exercise,))
    data1 = cursor.fetchone()

    # Check if the player exists
    query4 = "SELECT id FROM players WHERE pseudonym = %s"
    cursor.execute(query4, (student,))
    data2 = cursor.fetchone()

    # If the game doesn't exist, show an error message
    if data1 is None:
        messagebox.showerror(title="Erreur", message="Le champ Exercice ne peut contenir que GEO01, INFO02 ou INFO0 (Remarque : la fenêtre précédente n'est pas fermée)")
    else:
        # If the player doesn't exist, insert it
        if data2 is None:
            query2 = "INSERT INTO players (pseudonym) values (%s)"
            cursor.execute(query2, (student,))
            query4 = "SELECT id FROM players WHERE pseudonym = %s"
            cursor.execute(query4, (student,))
            data2 = cursor.fetchone()

        format_date = "%Y-%m-%d %H:%M:%S"
        format_time = "%H:%M:%S"
        date_test = False
        time_test = False
        nbok_test = False
        nbtot_test = False

        try:
            # Check if the date is in the correct format
            date_checked = datetime.strptime(date, format_date)
            date_test = True
        except:
            messagebox.showerror(title="Erreur", message="Le format du champ Date et Heure ne correspond pas à la base de données. Veuillez utiliser : AAAA-MM-JJ hh:mm:ss (Remarque : la fenêtre précédente n'est pas fermée)")

        try:
            # Check if the time is in the correct format
            time_checked = datetime.strptime(time, format_time)
            time_test = True
        except:
            messagebox.showerror(title="Erreur", message="Le format du champ Heure ne correspond pas à la base de données. Veuillez utiliser : hh:mm:ss (Remarque : la fenêtre précédente n'est pas fermée)")

        try:
            # Check if nbok is an integer
            nbok_checked = int(nbok)
            nbok_test = True
        except:
            messagebox.showerror(title="Erreur", message="Le format du champ Nb OK ne correspond pas à la base de données. Veuillez entrer un nombre (Remarque : la fenêtre précédente n'est pas fermée)")

        try:
            # Check if nbtot is an integer
            nbtot_checked = int(nbtot)
            nbtot_test = True
        except:
            messagebox.showerror(title="Erreur", message="Le format du champ Nb Total ne correspond pas à la base de données. Veuillez entrer un nombre (Remarque : la fenêtre précédente n'est pas fermée)")

        # If all checks pass, insert the result
        if date_test and time_test and nbok_test and nbtot_test:
            query1 = "INSERT INTO games_has_players (game_id, player_id, duration, startdate, nb_ok, nb_tot) values (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query1, (data1[0], data2[0], time_checked, date_checked, nbok_checked, nbtot_checked))


# Delete a result
def delete_result(name, date):
    open_dbconnection()
    cursor = db_connection.cursor()

    # Get the player's ID
    query1 = "SELECT id FROM players WHERE pseudonym = %s"
    cursor.execute(query1, (name,))
    data = cursor.fetchone()

    # Delete the result based on player ID and start date
    query2 = "DELETE FROM games_has_players WHERE player_id = %s AND startdate = %s"
    cursor.execute(query2, (data[0], date))


# Update a result
def update_result(time, nbok, nbtot, name, date):
    open_dbconnection()
    cursor = db_connection.cursor()

    # Get the player's ID
    query1 = "SELECT id FROM players WHERE pseudonym = %s"
    cursor.execute(query1, (name,))
    data = cursor.fetchone()

    format_time = "%H:%M:%S"
    time_test = False
    nbok_test = False
    nbtot_test = False

    try:
        # Check if the time is in the correct format
        time_checked = datetime.strptime(time, format_time)
        time_test = True
    except:
        time_test = False

    try:
        # Check if nbok is an integer
        nbok_checked = int(nbok)
        nbok_test = True
    except:
        nbok_test = False

    try:
        # Check if nbtot is an integer
        nbtot_checked = int(nbtot)
        nbtot_test = True
    except:
        nbtot_test = False

    update_params = {}

    # If time is valid, add it to the update parameters
    if time_test:
        update_params["duration"] = time_checked

    # If nbok is valid, add it to the update parameters
    if nbok_test:
        update_params["nb_ok"] = nbok_checked

    # If nbtot is valid, add it to the update parameters
    if nbtot_test:
        update_params["nb_tot"] = nbtot_checked

    # If there are update parameters, update the database
    if update_params:
        set_clause = ", ".join([f"{key} = %s" for key in update_params.keys()])
        query2 = f"UPDATE games_has_players SET {set_clause} WHERE player_id = %s and startdate = %s"
        cursor.execute(query2, (*update_params.values(), data[0], date))


# Close the database connection
def close_dbconnection():
    db_connection.close()
