import ftplib
import telnetlib
import time
from pprint import pprint
# from concurrent.futures import ThreadPoolExecutor


KATEL2 = '172.31.176.4'
KATEL3 = '172.31.177.4'


# FTP - - - - - - - - - - - - - - - - - - - -
def put_file_by_ftp(node, scr_file):
    """
    загрузка файлов по FTP
    """

    print('ГРУЗИМ ФАЙЛ: ', scr_file, ' по FTP на KATEL2 и KATEL3', '\n')

    path = 'sys$sysdevice:[dc2.ucs.script]'

    ftp = ftplib.FTP(node, 'ucsmanager', 'gotalife')

    ftp.cwd(path)

    with open(scr_file, 'rb') as file:
        ftp.storbinary('STOR ' + scr_file, file)
    ftp.close()

    print('for ', node, '... DONE!\n')


# TELNET - - - - - - - - - - - - - - - - - - - -
def telnet_ucs_audit(host, name_of_ird):
    """
    TELNET operation ucs_audit
    """

    # print ('\nhost: \n', host)
    if host == '172.31.176.4':
        print('\n на KATEL2')
    if host == '172.31.177.4':
        print('\n на KATEL3')
    else:
        print('\n не задан хост, исправьте\n')

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

    # -- ucs_audit
    print('=>{} 8. ucs_bulktxt'.format(host))
    telnet.write(b'ucs_audit\r\n')
    print('=>{} 9. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Please enter operator group to audit [0-15/ALL]:
    print('=>{} 10. Please enter operator group to audit [0-15/ALL]:'.format(host))
    telnet.read_until(b'ALL]:')
    print('=>{} 11. ALL'.format(host))
    telnet.write(b'ALL\r\n')
    print('=>{} 12. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Do you want to create a report file [YES/NO]?:
    print('=>{} 13. Do you want to create a report file [YES/NO]?:'.format(host))
    telnet.read_until(b'?')
    print('=>{} 14. NO')
    telnet.write(b'NO\r\n')
    print('=>{} 15. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Do you want to create a script file [YES/NO]?:
    print('=>{} 16. Do you want to create a script file [YES/NO]?:'.format(host))
    telnet.read_until(b'?')
    print('=>{} 17. YES'.format(host))
    telnet.write(b'YES\r\n')
    print('=>{} 18. time.sleep(1)'.format(host))
    time.sleep(1)

    # --  Enter the script file specification (UCS$SCRIPT:UCSAUDITALL.SCR):
    print('=>{} 19.  Enter the script file specification (UCS$SCRIPT:UCSAUDITALL.SCR):'.format(host))
    # telnet.read_until(b'?')
    print('=>{} 20. time.sleep(1)'.format(host))
    time.sleep(1)
    print('=>{} 21. ucs$script:'.format(host) + name_of_ird + '.scr')
    telnet.write(b'ucs$script:' + name_of_ird + b'.scr\r\n')
    print('=>{} 22. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Do you want to create a bulk file [YES/NO]?:
    print('=>{} 23. Do you want to create a bulk file [YES/NO]?:'.format(host))
    telnet.read_until(b'?')
    print('=>{} 24. NO'.format(host))
    telnet.write(b'NO\r\n')
    print('=>{} 25. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Do you wish filter on transaction data [YES/NO]?:
    print('=>{} 26. Do you wish filter on transaction data [YES/NO]?:'.format(host))
    telnet.read_until(b'?')
    print('=>{} 27. YES'.format(host))
    telnet.write(b'YES\r\n')
    print('=>{} 28. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Last channel IPG entry [0-1/NONE]:
    print('=>{} 29. Last channel IPG entry [0-1/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 30. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 31. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- IPG enable [0-1/NONE]:
    print('=>{} 29. IPG enable [0-1/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 30. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 31. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Adjust for daylight savings [0-1/NONE]:
    print('=>{} 32. Adjust for daylight savings [0-1/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 33. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 34. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Release to EMM Provider ID [0x0-0xFFFF/NONE]:
    print('=>{} 35. Release to EMM Provider ID [0x0-0xFFFF/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 36. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 37. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- MD Subtype [0-1/NONE]:
    print('=>{} 35. MD Subtype [0-1/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 36. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 37. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Single VCM ID [1-65535/NONE]:
    print('=>{} 38. Single VCM ID [1-65535/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 39. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 40. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Home VCM ID [1-65535/NONE]:
    print('=>{} 41. Home VCM ID [1-65535/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 42. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 43. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Home virtual channel [1-4095/NONE]:
    print('=>{} 44. Home virtual channel [1-4095/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 45. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 46. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Time zone [(-780)-(780)/NONE]:
    print('=>{} 47. Time zone [(-780)-(780)/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 48. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 49. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Ratings region [0-255/NONE]:
    print('=>{} 47. Ratings region [0-255/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 48. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 49. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Enable blackouts [0-1/NONE]:
    print('=>{} 50. Enable blackouts [0-1/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 51. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 52. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Region code [0-255/NONE]:
    print('=>{} 53. Region code [0-255/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 54. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 55. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Postal code [NONE]:
    print('=>{} 53. Postal code [NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 54. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 55. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Tier (one at a time) [0-2047/NONE]:
    print('=>{} 56. Tier (one at a time) [0-2047/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 57. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 58. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Unit Group [0-255/NONE]:
    print('=>{} 59. Unit Group [0-255/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 60. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 61. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- IPG Svc Num Index [0-1/NONE]:
    print('=>{} 62. IPG Svc Num Index [0-1/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 63. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 64. time.sleep(2)'.format(host))
    time.sleep(2)

    # -- For the following fields: '?' is a single character wild card,
    #         '*' is a multi-character wildcard.
    # Name [NONE]:
    print('=>{} 65. Name [NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 66. '.format(host) + name_of_ird)
    telnet.write(name_of_ird + b'\r\n')
    print('=>{} 67. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Miscellaneous field 0 [NONE]:
    print('=>{} 68. Miscellaneous field 0 [NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 69. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 70. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Miscellaneous field 1 [NONE]:
    print('=>{} 71. Miscellaneous field 1 [NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 72. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 73. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Miscellaneous field 2 [NONE]:
    print('=>{} 74. Miscellaneous field 2 [NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 75. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 76. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Miscellaneous field 3 [NONE]:
    print('=>{} 77. Miscellaneous field 3 [NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 78. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 79. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Miscellaneous field 4 [NONE]:
    print('=>{} 80. Miscellaneous field 4 [NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 81. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 82. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Miscellaneous field 5 [NONE]:
    print('=>{} 83. Miscellaneous field 5 [NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 84. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 85. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Multiport Update Enabled [0-1/NONE]:
    print('=>{} 86. Multiport Update Enabled [0-1/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 87. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 88. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Virtual Network [0-500/NONE]:
    print('=>{} 89. Virtual Network [0-500/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 90. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 91. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- HWC Profile Enabled [0-1/NONE]:
    print('=>{} 92. HWC Profile Enabled [0-1/NONE]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 93. NONE'.format(host))
    telnet.write(b'NONE\r\n')
    print('=>{} 94. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Select unit types (separate by comma, if more than one)
    #                 [1=DC1, 2=DC2, 3=IRT]:
    print('=>{} 95. [1=DC1, 2=DC2, 3=IRT]:'.format(host))
    telnet.read_until(b':')
    print('=>{} 96. 2'.format(host))
    telnet.write(b'2\r\n')
    print('=>{} 97. time.sleep(20)'.format(host))
    time.sleep(20)

    # -- Wish to audit another operator group [YES/NO]?:
    print('=>{} 98. Wish to audit another operator group [YES/NO]?'.format(host))
    telnet.read_until(b'?')
    print('=>{} 99. NO'.format(host))
    telnet.write(b'NO\r\n')
    print('=>{} 100. time.sleep(1)'.format(host))
    time.sleep(1)

    telnet.close()

    return "ПРОВЕРЬТЕ ФАЙЛЫ В ДИРЕКТОРИИ UCS$SCRIPT: УДАЛЕННОГО ХОСТА " + host


# TELNET - - - - - - - - - - - - - - - - - - - -
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
    telnet.read_until(b'?')
    print('=>{} 11. y'.format(host))
    telnet.write(b'y\r\n')
    print('=>{} 12. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- Enter bulk file specification:
    print('=>{} 13. Enter bulk file specification:'.format(host))
    telnet.read_until(b'specification:')
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
    telnet.read_until(b'?')
    print('=>{} 20. n'.format(host))
    telnet.write(b'n\r\n')
    print('=>{} 21. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- ucs_offbulk
    print('=>{} 22. $'.format(host))
    telnet.read_until(b'$')
    print('=>{} 23. ucs_offbulk'.format(host))
    telnet.write(b'ucs_offbulk\r\n')
    print('=>{} 24. time.sleep(1)'.format(host))
    time.sleep(1)

    # -- bulk-файл для обрабокти
    print('=>{} 25. File name (64 char max) :'.format(host))
    telnet.read_until(b':')
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
            # -- параллельно для каждого приемника из внутрнней БД UCS получаем скрипт-описание приемника.
            # -- он будет храниться на удаленном хосте.
            # -- потом его нужно скачивать и править вручную, если нужны какие-либо изменения.
            print(telnet_ucs_audit(KATEL2, ird_name.rstrip()))

            ird_name_list.append(ird_name.rstrip())
    pprint(ird_name_list)
