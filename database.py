"""
Projet : class_order_managment
Module : MA-DBPY
Date : 29.08.23
Autheur : Ryan Bersier
Version : 1.0
"""

import mysql.connector
from tkinter import messagebox
import datetime


# Function for Open session in Mysql
def open_dbconnection():
    global db_connection
    db_connection = mysql.connector.connect(host='127.0.0.1', port='3306', user='root', password='root',
                                            database='Braintrainning', buffered=True, autocommit=True)


# Save result in database
def save_results(exercise, pseudo, duration, nbtrials, nbok):
    open_dbconnection()
    cursor = db_connection.cursor()
    query3 = "SELECT id FROM games WHERE exercise = %s"
    cursor.execute(query3, (exercise,))
    data1 = cursor.fetchone()
    query4 = "SELECT id FROM players WHERE pseudonym = %s"
    cursor.execute(query4, (pseudo,))
    data2 = cursor.fetchone()
    if data1 is None:
        query1 = "INSERT INTO games (exercise) values (%s)"
        cursor.execute(query1, (exercise,))
        query3 = "SELECT id FROM games WHERE exercise = %s"
        cursor.execute(query3, (exercise,))
        data1 = cursor.fetchone()
    elif data2 is None:
        query2 = "INSERT INTO players (pseudonym) values (%s)"
        cursor.execute(query2, (pseudo,))
        query4 = "SELECT id FROM players WHERE pseudonym = %s"
        cursor.execute(query4, (pseudo,))
        data2 = cursor.fetchone()

    x = datetime.datetime.now()
    date_hour = x.strftime("%Y-%m-%d %H:%M:%S")

    query5 = "INSERT INTO games_has_players (game_id, player_id, duration, startdate, nb_ok, nb_tot) values (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query5, (data1[0], data2[0], duration, date_hour, nbok, nbtrials))


# All data for show the results
def read_result(pseudo, exercise, startdate, enddate):
    open_dbconnection()
    cursor = db_connection.cursor()
    query1 = "SELECT players.pseudonym, games_has_players.startdate, games_has_players.duration, games.exercise, games_has_players.nb_ok, games_has_players.nb_tot FROM games_has_players INNER JOIN players ON games_has_players.player_id = players.id INNER JOIN games ON games_has_players.game_id = games.id WHERE 1=1"
    if not pseudo == "":
        query1 += f" AND players.pseudonym LIKE '{pseudo}%'"
    if not exercise == "":
        query1 += f" AND games.exercise LIKE '{exercise}%'"
    if not startdate == "":
        query1 += f" AND games_has_players.startdate >= '{startdate}'"
    if not enddate == "":
        query1 += f" AND games_has_players.startdate <= '{enddate}'"
    try:
        cursor.execute(query1)
        data = cursor.fetchall()
    except:
        messagebox.showerror(title="Erreur",
                             message="Il y a peut être une erreur dans date de début ou de fin veuillez essayez le format suivant : AAAA-MM-JJ (Attention la précédente fenêtre n'est pas fermé)")
    return data


def close_dbconnection():
    db_connection.close()
