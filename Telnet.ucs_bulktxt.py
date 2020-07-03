
def telnet_ucs_bulktxt_ucs_offbulk(host, name_of_ird):
    """
    Telnet operation ucs_bulktxt and ucs_offbulk
    """

    # print ('\nhost: \n', host)
    if host == '172.31.176.4':
        print('\n на KATEL2')
    if host == '172.31.177.4':
        print('\n на KATEL3')
    else:
        print('\n не задан хост, исправьте\n')

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
    print('=>{} 22. $'.format(host))
    telnet.read_until(b'$')
    print('=>{} 23. ucs_bulktxt'.format(host))
    telnet.write(b'ucs_bulktxt\r\n')
    print('=>{} 24. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Log message contents (y or n)? y
    print('=>{} 10. Log message contents (y or n)?'.format(host))
    t10 = telnet.read_until(b'?')
    print(t10)
    print('=>{} 11. y'.format(host))
    telnet.write(b'y\r\n')
    print('=>{} 12. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Enter bulk file specification:
    print('=>{} 13. Enter bulk file specification:'.format(host))
    t13 = telnet.read_until(b'specification:')
    print(t13)
    print('=>{} 14. {}'.format(host, rmt_blk_file))
    telnet.write(rmt_blk_file + b'\r\n')
    print('=>{} 15. time.sleep(3)'.format(host))
    time.sleep(3)

    # -- Enter text file specification:
    print('=>{} 16. Enter text file specification:'.format(host))
    # telnet.read_until(b'specification:')
    print('=>{} 17. {}'.format(host, rmt_scr_file))
    telnet.write(rmt_scr_file + b'\r\n')
    print('=>{} 18. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Another file (y or n)? n
    print('=>{} 19. Another file (y or n)?'.format(host))
    t19 = telnet.read_until(b'?')
    print(t19)
    print('=>{} 20. n'.format(host))
    telnet.write(b'n\r\n')
    print('=>{} 21. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- ucs_offbulk
    print('=>{} 22. $'.format(host))
    t22 = telnet.read_until(b'$')
    print(t22)
    print('=>{} 23. ucs_offbulk'.format(host))
    telnet.write(b'ucs_offbulk\r\n')
    print('=>{} 24. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- bulk-файл для обрабокти
    print('=>{} 25. File name (64 char max) :'.format(host))
    t25 = telnet.read_until(b':')
    print(t25)
    print('=>{} 26. {}'.format(host, rmt_blk_file))
    telnet.write(rmt_blk_file + b'\r\n')
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
    telnet.write(rmt_log_file + b'\r\n')
    print('=>{} 32. time.sleep(3)'.format(host))
    time.sleep(3)

    print('=>{} 33. ...проверка... \n'.format(host))
    check_log = telnet.read_until(b'(UCSMANAGER)$')
    print(check_log, '\n')
    print(check_log.split()[-4] + b' ' + check_log.split()[-3], '\n', '`' * 20)
    if check_log.split()[-4] == b'0':
        print('\n', ' (', host, ')\n', 'БЕЗ ОШИБОК!!! \n ВСЁ ОТЛИЧНО!!! \n ЗАПИШИТЕ ВСЁ В ЖУРНАЛ!!!\n')
    else:
        print('ЕСТЬ ОШИБКИ!!! \n НУЖНА ДОПОЛНИТЕЛЬНАЯ ПРОВЕРКА!!!\n')

    return {host: check_log.split()[-4] + b' ' + check_log.split()[-3]}


"""
# -- Разделение на потоки (2)
def thread_execution(function, host_dic):
    with ThreadPoolExecutor(max_workers=2) as executor:
        # print('ThreadPoolExecutor works with function: {} and host_dic: {}'.format(function, host_dic))
        th_exe_res = executor.map(function, host_dic)
    return list(th_exe_res)


print('\n', 'УДАЛЕННО ПО ТЕЛНЕТ ЗАПУСКАЕМ СКРИПТЫ В ДВА ПОТОКА:', '\n')
host_dic = {KATEL2: 'KATEL2', KATEL3: 'KATEL3'}
results = thread_execution(telnet_ucs_audit, host_dic)
print('\nлог-файлы транзакций скриптов: \n (если размер 0 блоков, значит без ошибок)')
pprint(results)
"""

if __name__ == "__main__":

    # -- из текстового файла со списком номеров приемников формируем рабочий список ird_name_list
    ird_name_list = list()
    with open('files/list_for_change.txt') as listfile:
        for ird_name in listfile:
            ird_name_list.append(ird_name.rstrip())

    pprint(ird_name_list)

    print('\n', '- -'*20, '\n')

    # -- для полученного списка приемников из внутрнней БД UCS получаем скрипты-описания приемника.
    # -- он будет храниться на удаленном хосте.
    # -- потом его нужно скачивать и править вручную, если нужны какие-либо изменения.
    # print(telnet_ucs_audit(KATEL2, ird_name_list))
    print(telnet_ucs_audit(KATEL2, ['000-03454-60108-063']))
