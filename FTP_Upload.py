import ftplib
from Telnet.ucs_audit import

KATEL2 = '172.31.176.4'

def ftp_upload(host, file_list):
    print('соединение по FTP с сервером ', host)
    ftp = ftplib.FTP(host, 'ucsmanager', 'gotalife')
    time.sleep(5)
    path = 'sys$sysdevice:[dc2.ucs.script]'
    ftp.cwd(path)

    for files_for_upload in file_list:
        print('по FTP грузим файл {} на хост {}'.format(files_for_upload, host))
        with open(files_for_upload, 'r') as file:
            ftp.storlines('STOR ' + files_for_upload, file)
    time.sleep(15)
    ftp.close()
    print('...done')


print(telnet_ucs_bulktxt_ucs_offbulk(KATEL2, 'result_file.SCR;1'))