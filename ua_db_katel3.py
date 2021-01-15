import sqlite3
import parser_script
from pprint import pprint

# connect to ua.db - database with unit addresses
connection = sqlite3.connect('ua.db')
cursor = connection.cursor()

print('создаётся таблица KATEL3 , если её нет')
cursor.execute("CREATE TABLE if not exists KATEL3 (ua text not null primary key, name text, tiers text, misc1 text, misc2 text, misc3 text, misc4 text, misc5 text, misc6 text);")
connection.commit()


def sql_queries(db_table, somedata):
    """
    функция берёт данные и записывает из в базу данных
    """

    print(somedata.split(','))

    query = "REPLACE into KATEL3 (ua, tiers, name, misc1, misc2, misc3, misc4, misc5, misc6) values ('{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(
        somedata.split(',')[0], somedata.split(',')[1], somedata.split(',')[2], somedata.split(',')[3],
        somedata.split(',')[4], somedata.split(',')[5], somedata.split(',')[6], somedata.split(',')[7],
        somedata.split(',')[8])
    print(query)

    cursor.execute(query)
    connection.commit()

    return 'data was inserted into DB:\n{}'.format(query)


data = parser_script.parse_script('../KATEL3.SCR')

pprint(data, sort_dicts=False)

# разбираем данные, добытые из скрипта,
# для формирования стоки для записи в БД.

data_str = ''

for unit_info in data.items():

    unit_address = unit_info[0][0:15]
    # print(unit_address)
    sums = ''
    for unit_discr in unit_info[1].items():
        sums = sums + (str(unit_discr[1])).replace('[', '').replace(',', '').replace(']', '') + ','
    data_str = (unit_address + ',' + sums)

    data_string = data_str[0:len(data_str) - 1]
    # - 2 уберёт две последних лишних запятых

    print(data_string)
    # получилась строка следующего вида:
    # 000-03086-26596,1 211 213 303,000-03086-26596-214,KATELCO,Almaty,DNST,Rezerv Control,KATELCO              Control

    # передаём её для записи в БД:
    print(sql_queries('KATEL2', data_string))

connection.close()
