import sqlite3


def check_file(filename):

    with open(filename) as file:
        irds_list = list()
        for items in file.read().split():
            irds_list.append(items)

        connection = sqlite3.connect('ua.db')
        cursor = connection.cursor()

        for item in irds_list:
            query = "select * from KATEL3 where ua = '{}'".format(item[:15])
            cursor.execute(query)
            connection.commit()
            text = cursor.fetchone()
            if text and text[0] == item[:15]:
                continue
            else:
                print(item, 'нет соответствия в базе данных')

        return ('...проверка файла {} окончена'.format(filename))


if __name__ == "__main__":
    print(check_file(filename='files/list_for_change.txt'))
