"""
Программа берёт из текстового файла list_for_change.txt список номеров приёсников,
для них по Телнет выполняет утилиту ucs_audit,
получившиеся .scr файлы скачивает в files/temp/ и объединяет их в один файл files/temp/result_file.SCR;1,
в него записывает изменения (добавить/убрать тиер-бит, изменить описательное поле)

... грузит итоговый скрипт на сервер и выполняет его
"""
import sqlite3
import ftplib
import telnetlib
import time
import os
import check_file
from glob import glob
from pprint import pprint
from progress.bar import IncrementalBar
from script_changing import script_file_changing
from SetUnitInformation import get_info_from_db


KATEL2 = '172.31.176.4'
KATEL3 = '172.31.177.4'




def sql_query(db, query):
    """
     из базы данных (ua.db) из одной из таблиц (ktr, ucs)
     достаётся информация по конкретному запросу.
     """

    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    query_str = query if query else "SELECT * FROM ucs;"
    cursor.execute(query_str)
    ird_data = cursor.fetchone()

    connection.close()

    return ird_data


def telnet_ucs_audit(host, ird_names_list):
    """
    TELNET operation ucs_audit
    """

    if host == '172.31.176.4':
        hostname = 'KATEL2'
    elif host == '172.31.177.4':
        hostname = 'KATEL3'
    else:
        print('\n не задан хост, исправьте\n')

    print('логинимся по telnet на', host, ' - ', hostname, '\n')

    telnet = telnetlib.Telnet(host)
    telnet.read_until(b'Username:')
    telnet.write(b'ucsmanager\r\n')
    telnet.read_until(b'Password:')
    telnet.write(b'gotalife\r\n')
    time.sleep(2)
    t7 = telnet.read_until(b'(UCSMANAGER)$').decode()
    # print(t7)

    for name_of_ird in ird_names_list:

        print('для приемника ', name_of_ird, 'выполняется утилита ucs_audit:')

        mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        bar = IncrementalBar(' ucs_audit_utility ', max=len(mylist))
        bar.next()

        # -- ucs_audit
        telnet.write(b'ucs_audit\r\n')
        time.sleep(1)

        # -- Please enter operator group to audit [0-15/ALL]:
        telnet.write(b'0\r\n')
        time.sleep(1)

        bar.next()

        # -- Do you want to create a report file [YES/NO]?:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Do you want to create a script file [YES/NO]?:
        telnet.write(b'YES\r\n')
        time.sleep(1)

        # --  Enter the script file specification (UCS$SCRIPT:UCSAUDITALL.SCR):
        time.sleep(1)

        if sql_query('ua.db', 'select * from ucs where name="{}";'.format(name_of_ird)):
            name_for_filename = sql_query('ua.db', 'select * from ucs where name="{}";'.format(name_of_ird))[0]
        else:
            name_for_filename = name_of_ird

        string_script_filename = 'ucs$script:' + name_for_filename + '.scr\r\n'
        telnet.write(string_script_filename.encode())
        time.sleep(1)

        bar.next()

        # -- Do you want to create a bulk file [YES/NO]?:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Do you wish filter on transaction data [YES/NO]?:
        telnet.write(b'YES\r\n')
        time.sleep(1)

        # -- Last channel IPG entry [0-1/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        bar.next()

        # -- IPG enable [0-1/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Adjust for daylight savings [0-1/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Release to EMM Provider ID [0x0-0xFFFF/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        bar.next()

        # -- MD Subtype [0-1/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Single VCM ID [1-65535/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Home VCM ID [1-65535/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Home virtual channel [1-4095/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Time zone [(-780)-(780)/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        bar.next()

        # -- Ratings region [0-255/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Enable blackouts [0-1/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Region code [0-255/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Postal code [NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Tier (one at a time) [0-2047/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Unit Group [0-255/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- IPG Svc Num Index [0-1/NONE]:
        telnet.write(b'\r\n')
        time.sleep(3)

        bar.next()

        # -- For the following fields: '?' is a single character wild card,
        #         '*' is a multi-character wildcard.
        # Name [NONE]:
        telnet.write((name_of_ird + '\r\n').encode())
        time.sleep(2)

        # -- Miscellaneous field 0 [NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Miscellaneous field 1 [NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Miscellaneous field 2 [NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        bar.next()

        # -- Miscellaneous field 3 [NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Miscellaneous field 4 [NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Miscellaneous field 5 [NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Multiport Update Enabled [0-1/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Virtual Network [0-500/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- HWC Profile Enabled [0-1/NONE]:
        telnet.write(b'\r\n')
        time.sleep(2)

        bar.next()

        # -- Select unit types (separate by comma, if more than one)
        #                 [1=DC1, 2=DC2, 3=IRT]:
        telnet.write(b'2\r\n')
        time.sleep(32)

        # -- Wish to audit the authorization file for operator group 0 again [YES/NO]?
        telnet.write(b'\r\n')
        time.sleep(2)
        telnet.read_until(b'$').decode()

        bar.next()

        bar.finish()

    telnet.close()

    return "\n.SCR-файлы подготовлены для редактирования \nв директории UCS$SCRIPT: хоста " + host + '\n'


def telnet_ucs_bulktxt_ucs_offbulk(host, filename):
    """
    Telnet operation ucs_bulktxt and ucs_offbulk
    """

    # print ('\nhost: \n', host)
    if host == '172.31.176.4':
        print('\n на KATEL2')
    elif host == '172.31.177.4':
        print('\n на KATEL3')
    else:
        print('\n не задан хост, исправьте\n')

    name_of_ird = filename[:-6]
    rmt_blk_file = 'ucs$bulk:' + name_of_ird + '.blk'
    rmt_scr_file = 'ucs$script:' + name_of_ird + '.scr'
    rmt_log_file = 'ucs$bulk:' + name_of_ird + '.log'

    print('=>{} 1. telnet({})'.format(host, host))
    telnet = telnetlib.Telnet(host)

    print('=>{} 2. Username:'.format(host))
    telnet.read_until(b'Username:')

    print('=>{} 3. ucsmanager'.format(host))
    telnet.write(b'ucsmanager\r\n')

    print('=>{} 4. Password:'.format(host))
    telnet.read_until(b'Password:')

    print('=>{} 5. gotalife'.format(host))
    telnet.write(b'gotalife\r\n')

    print('=>{} 6. time.sleep(3)'.format(host))
    time.sleep(3)

    print('=>{} 7. (UCSMANAGER)$'.format(host))
    telnet.read_until(b'(UCSMANAGER)$')

    # -- ucs_bulktxt
    # print('=>{} 22. $'.format(host))
    # telnet.read_until(b'$')
    print('=>{} 8. ucs_bulktxt'.format(host))
    telnet.write(b'ucs_bulktxt\r\n')
    print('=>{} 9. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Log message contents (y or n)? y
    print('=>{} 10. Log message contents (y or n)?'.format(host))
    t10 = telnet.read_until(b'?')
    print(t10.decode())
    print('=>{} 11. y'.format(host))
    telnet.write(b'y\r\n')
    print('=>{} 12. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Enter bulk file specification:
    print('=>{} 13. Enter bulk file specification:'.format(host))
    t13 = telnet.read_until(b'specification:')
    print(t13.decode())
    print('=>{} 14. {}'.format(host, rmt_blk_file))
    telnet.write((rmt_blk_file + '\r\n').encode())
    print('=>{} 15. time.sleep(3)'.format(host))
    time.sleep(3)

    # -- Enter text file specification:
    print('=>{} 16. Enter text file specification:'.format(host))
    # telnet.read_until(b'specification:')
    print('=>{} 17. {}'.format(host, rmt_scr_file))
    telnet.write((rmt_scr_file + '\r\n').encode())
    print('=>{} 18. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Another file (y or n)? n
    print('=>{} 19. Another file (y or n)?'.format(host))
    t19 = telnet.read_until(b'?')
    print(t19.decode())
    print('=>{} 20. n'.format(host))
    telnet.write(b'n\r\n')
    print('=>{} 21. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- ucs_offbulk
    print('=>{} 22. $'.format(host))
    t22 = telnet.read_until(b'$')
    print(t22.decode())
    print('=>{} 23. ucs_offbulk'.format(host))
    telnet.write(b'ucs_offbulk\r\n')
    print('=>{} 24. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- bulk-файл для обрабокти
    print('=>{} 25. File name (64 char max) :'.format(host))
    t25 = telnet.read_until(b':')
    print(t25.decode())
    print('=>{} 26. {}'.format(host, rmt_blk_file))
    telnet.write((rmt_blk_file + '\r\n').encode())
    print('=>{} 27. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Y - для подтверждения
    print('=>{} 28. Y'.format(host))
    telnet.write(b'Y\r\n')
    print('=>{} 29. (UCSMANAGER)$'.format(host))
    telnet.read_until(b'(UCSMANAGER)$')
    print('=>{} 30. time.sleep(3)'.format(host))
    time.sleep(3)

    # -- проверка лог-файла на ошибки (если 0 - нет ошибок)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    print('=>{} 31. {}'.format(host, rmt_log_file))
    telnet.write(('dir ' + rmt_log_file + '/size\r\n').encode())
    print('=>{} 32. time.sleep(3)'.format(host))
    time.sleep(3)

    print('=>{} 33. ...проверка... \n'.format(host))
    check_log = telnet.read_until(b'(UCSMANAGER)$')
    print(check_log.decode(), '\n')
    print(check_log.split()[-4] + b' ' + check_log.split()[-3], '\n', '`' * 20)
    if check_log.split()[-4] == b'0':
        print('\n', ' (', host, ')\n', 'ТРАНЗАКЦИЯ ПРОШЛА БЕЗ ОШИБОК!!! \n')
    else:
        print('ЕСТЬ ОШИБКИ!!! \n НУЖНА ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА!!!\n')

    telnet.close()

    return {host: check_log.split()[-4] + b' ' + check_log.split()[-3]}


def ftp_download(host):
    print('соединение по FTP с сервером ', host)
    ftp = ftplib.FTP(host, 'ucsmanager', 'gotalife')
    ftp.cwd('ucs$script')

    listing = []

    ftp.retrlines('LIST', listing.append)  # список из листинга файлов

    list_of_files = []

    for lines in listing:
        if lines.startswith('000-'):  # критерий отбора файлов.
            list_of_files.append(lines.split()[0])

    for filename in list_of_files:
        print('скачиваем файл {}'.format(filename))
        local_filename = os.path.join(r'files/temp/', filename)
        local_file = open(local_filename, 'wb')
        ftp.retrbinary('RETR ' + filename, local_file.write)
        local_file.close()

        ftp.delete(filename)  # тут же удаляем файлы, что-б не засорять директорию.

    ftp.close()

    print('в директорию files/temp/ скачаны файлы:')
    spisok = os.listdir('files/temp/')

    return spisok


def ftp_upload(host, file_list):
    print('соединение по FTP с сервером ', host)
    ftp = ftplib.FTP(host, 'ucsmanager', 'gotalife')
    time.sleep(5)
    path = 'sys$sysdevice:[dc2.ucs.script]'
    ftp.cwd(path)

    for file_for_upload in file_list:
        print('по FTP грузим файл {} на хост {}'.format(file_for_upload, host))
        with open(file_for_upload, 'rb') as file:
            ftp.storbinary('STOR ' + file_for_upload.split('/')[-1], file)
    time.sleep(15)
    ftp.close()
    print('...done')


def sql_name_compare(name):
    """

    :param name: имя приемника
    :return: real_name: реальное имя приемника
    """


    ua = name[:-4]
    real_name = get_info_from_db(ua, 'ucs')

    # real_name:
    # ('000-03454-60108', '000-03454-60108-063', '312', 'KezTeleRadio', 'KYZYLORDA', 'Kamystybas', 'Kazakhstan',
    # 'KazTeleRadio                   KYZYLORDA', '')

    return real_name[1] if real_name else name

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":

    # перед началом работы очищаем предыдущие временные файлы
    # print('перед началом работы очищаем предыдущие временные файлы')
    files_for_del = glob('files/temp/*.SCR;1')
    for file in files_for_del:
        # delete local files
        print('...deleting old .scr files in parent dir {}'.format(file))
        os.remove(file)

    print('...поехали...\n')

    # -- проверка номеров приёмников в файле на соответствие в БД ua.db
    print(check_file.check_file('files/list_for_change.txt'))

    # -- из текстового файла со списком номеров приемников формируем рабочий список ird_name_list
    ird_name_list = list()
    with open('files/list_for_change.txt') as listfile:
        for ird_name in listfile:
            if ird_name.startswith('000-'):
                ird_name_list.append(ird_name.rstrip())

    print('будем работать с приемниками:')
    pprint(ird_name_list)
    print('\n{} приёмников'.format(len(ird_name_list)))

    # -- проверка имён в списке на соответствие именам во внутрнней БД UCS,
    # заполненой из актуального файла UA_DB.SCR;1.
    actual_ird_name_list = list()
    for point in ird_name_list:
        if point:
            actual_ird_name_list.append(sql_name_compare(point))
    #   print(actual_ird_name_list)

    print('\n', '- -'*20, '\n')

    # -- для списка приемников, из внутрнней БД UCS получаем скрипты-описания (.SCR-файлы) каждого приемника.
    # -- они будут храниться на удаленном хосте (в директории ucs$script).

    '''
    почему-то, при работе функции сразу со всем списком, скрипт-файлы создаются через раз,
    поэтому пока вместо отправки для функции сразу всего списка,
    будем отправлять отдельно для каждого приемника. 
    Это гораздо дольше :-( но работает.
       Вобщем, задание на потом - разобраться почему через раз работает
    
    print(telnet_ucs_audit(KATEL2, actual_ird_name_list))
    '''

    for irds in actual_ird_name_list:
        print(telnet_ucs_audit(KATEL3, [irds]))

    # -- полученные файлы скриптов .scr по FTP скачиваются с удаённого сервера на локальный для редактирования.

    # -- предварительно удаляем старый файл
    if os.path.exists('files/temp/result_file.SCR;1'):
        os.remove('files/temp/result_file.SCR;1')
    list_for_change = ftp_download(KATEL3)
    print(list_for_change)  # -- составляется список скачанных файлов.

    # из этих файлов создается единый файл, в который будут внесены изменения.
    with open('files/temp/result_file.SCR;1', 'w') as file:
        for files in list_for_change:
            with open('files/temp/' + files, 'r') as src_files:
                for lines in src_files:
                    file.write(lines)

    print('создан объединенный файл files/temp/result_file.SCR;1 ')

    # -- КАКИЕ ИЗМЕНЕНИЯ НУЖНО ВНЕСТИ --
    print('вносим изменения:')
    print(script_file_changing('files/temp/result_file.SCR;1', '+9'))
    print(script_file_changing('files/temp/result_file.SCR;1', 'm1 U'))

    # -- отредактированный скрипт нужно сконвертировать в исполняемый файл и выполнить его удалённо:
    print('отредактированный скрипт нужно конвертируем в исполняемый файл и выполняем его удалённо\n'
          'с помощью утилит ucs_bulktxt и ucs_offbulk, предварительно загрузив на сервер по FTp.')
    print(ftp_upload(KATEL3, ['files/temp/result_file.SCR;1']))
    print(telnet_ucs_bulktxt_ucs_offbulk(KATEL3, 'result_file.SCR;1'))
    print('\nну вот и всё - программа отработала!!!')
    time.sleep(20)
