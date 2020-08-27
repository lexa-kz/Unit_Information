import re
import sqlite3

with open('files/list_for_change.txt') as file:
    irds_list = list()
    for items in file.read().split():
        irds_list.append(items)

    connection = sqlite3.connect('ua.db')
    cursor = connection.cursor()
    
    for item in irds_list:
        query = "select * from ucs where ua = '{}'".format(item[:15])
        cursor.execute(query)
        connection.commit()
        text = cursor.fetchone()
        if text and text[0] == item[:15]:
            continue
        else:
            print(item, 'нет соответствия в базе данных')
   
    print('...проверка окончена')
