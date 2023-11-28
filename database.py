"""
Projet : class_order_managment
Module : MA-DBPY
Date : 29.08.23
Autheur : Ryan Bersier
Version : 1.0
"""

import mysql.connector
import datetime

#fonction pour ouverture d'une session Mysql
def open_dbconnection():
    global db_connection
    db_connection = mysql.connector.connect(host='127.0.0.1', port='3306', user='root', password='root', database='Braintrainning', buffered=True, autocommit=True)

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

# all data for show the result
def read_result():
    open_dbconnection()
    cursor = db_connection.cursor()
    query1 = "SELECT players.pseudonym, games_has_players.startdate, games_has_players.duration, games.exercise, games_has_players.nb_ok, games_has_players.nb_tot FROM games_has_players INNER JOIN players ON games_has_players.player_id = players.id INNER JOIN games ON games_has_players.game_id = games.id"
    cursor.execute(query1,)
    data = cursor.fetchall()
    return data

def close_dbconnection():
    db_connection.close()
