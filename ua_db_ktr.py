import sqlite3
import parser_txt

# connect to ua.db - database with unit addresses
connection = sqlite3.connect('ua.db')
cursor = connection.cursor()

cursor.execute("CREATE TABLE if not exists ktr (ua text not null primary key, name text, odrt text, region text, city text, program text, obltv text);")
connection.commit()


def sql_queries(db_table, somedata):
    """
    function takes data and put it into database
    """

    query = "REPLACE into ktr (ua, name, odrt, region, city, program, obltv) values ('{}','{}','{}','{}','{}','{}','{}');".format(
        somedata.split(',')[0], somedata.split(',')[1], somedata.split(',')[2], somedata.split(',')[3],
        somedata.split(',')[4], somedata.split(',')[5], somedata.split(',')[6])
    print(query)

    cursor.execute(query)
    connection.commit()

    return 'data was inserted into DB'


data, wrong_data = parser_txt.parse_txt('files/PRM.txt')

# pprint(data)
if wrong_data:
    print('следующие данные нужно исправить: ', wrong_data)

# разбираем данные, добытые из скрипта,
# для формирования стоки для записи в БД.

data_str = ''

for unit_info in data.items():

    unit_address = unit_info[0][0:15]
    # print(unit_address)
    sums = ''
    for unit_discr in unit_info[1].items():
        sums = sums + str(unit_discr[1]) + ','
    data_str = (unit_address + ',' + sums)

    data_string = data_str[0:len(data_str) - 1]

    print(data_string)
    # получилась строка следующего вида:
    # 000-03454-59966,000-03454-59966-026,Акмолинская ОДРТ,Зерендинский,Айдабул,Казахстан,ОБЛ_ТВ
    # передаём её для записи в БД:
    print(sql_queries('ktr', data_string))

connection.close()
