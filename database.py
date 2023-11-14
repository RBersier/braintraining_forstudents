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
    if data1[0] is None:
        query1 = "INSERT INTO games (exercise) values (%s,))"
        cursor = db_connection.cursor()
        cursor.execute(query1, (exercise,))
        query3 = "SELECT id FROM games WHERE exercise = %s"
        cursor.execute(query3, (exercise,))
        data1 = cursor.fetchone()
    elif data2[0] is None:
        query2 = "INSERT INTO players (pseudonym) values (%s,))"
        cursor = db_connection.cursor()
        cursor.execute(query2, (pseudo,))
        query4 = "SELECT id FROM players WHERE pseudonym = %s"
        cursor.execute(query4, (pseudo,))
        data2 = cursor.fetchone()

    x = datetime.datetime.now()
    date_hour = x.strftime("%Y-%m-%d %H:%M:%S")


    query8 = "INSERT INTO games_has_players (games_id, player_id, duration, start_date, nb_ok, nb_tot) values (%s, %s, %s, %s, %s, %s))"
    cursor = db_connection.cursor()
    cursor.execute(query8, (data1[0], data2[0], duration, date_hour, nbok, nbtrials))


def close_dbconnection():
    db_connection.close()
