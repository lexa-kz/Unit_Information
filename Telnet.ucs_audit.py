import ftplib
import telnetlib
import time
from pprint import pprint
# from concurrent.futures import ThreadPoolExecutor


KATEL2 = '172.31.176.4'
KATEL3 = '172.31.177.4'


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

    print('логинимся по telnet на', host, ' - ', hostname)

    telnet = telnetlib.Telnet(host)
    telnet.read_until(b'Username:')
    telnet.write(b'ucsmanager\r\n')
    telnet.read_until(b'Password:')
    telnet.write(b'gotalife\r\n')
    time.sleep(3)
    t7 = telnet.read_until(b'(UCSMANAGER)$').decode()
    print(t7)

    for name_of_ird in ird_names_list:

        print('\nдля приемника ', name_of_ird, 'выполняется утилита ucs_audit:\n')

        # -- ucs_audit
        telnet.write(b'ucs_audit\r\n')
        time.sleep(1)

        # -- Please enter operator group to audit [0-15/ALL]:
        telnet.write(b'0\r\n')
        time.sleep(1)

        # -- Do you want to create a report file [YES/NO]?:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Do you want to create a script file [YES/NO]?:
        telnet.write(b'YES\r\n')
        time.sleep(1)

        # --  Enter the script file specification (UCS$SCRIPT:UCSAUDITALL.SCR):
        time.sleep(1)
        string_script_filename = 'ucs$script:' + name_of_ird + '.scr\r\n'
        telnet.write(string_script_filename.encode())
        time.sleep(1)

        # -- Do you want to create a bulk file [YES/NO]?:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Do you wish filter on transaction data [YES/NO]?:
        telnet.write(b'YES\r\n')
        time.sleep(1)

        # -- Last channel IPG entry [0-1/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- IPG enable [0-1/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Adjust for daylight savings [0-1/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

        # -- Release to EMM Provider ID [0x0-0xFFFF/NONE]:
        telnet.write(b'\r\n')
        time.sleep(1)

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

        # -- Select unit types (separate by comma, if more than one)
        #                 [1=DC1, 2=DC2, 3=IRT]:
        telnet.write(b'2\r\n')
        time.sleep(40)

        # -- Wish to audit the authorization file for operator group 0 again [YES/NO]?
        telnet.write(b'\r\n')
        time.sleep(1)

        '''
        # -- Wish to audit another operator group [YES/NO]?:
        telnet.write(b'\r\n')
        time.sleep(1)
        '''

    telnet.close()

    return "\nПРОВЕРЬТЕ И ОТРЕДАКТИРУЙТЕ ФАЙЛЫ В ДИРЕКТОРИИ UCS$SCRIPT: УДАЛЕННОГО ХОСТА " + host


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
