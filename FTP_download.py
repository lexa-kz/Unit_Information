import os
import ftplib

host = "172.31.176.4"

print('соединение по FTP с сервером ', host)
ftp = ftplib.FTP(host, 'ucsmanager', 'gotalife')
ftp.cwd('ucs$script')

listing = []

ftp.retrlines('LIST', listing.append)   # список из листинга файлов

list_of_files = []

for lines in listing:
    if lines.startswith('18'):    # критерий отбора файлов.
        list_of_files.append(lines.split()[0])

for filename in list_of_files:
    local_filename = os.path.join(r'c:/IRDs', filename)
    local_file = open(local_filename, 'wb')
    ftp.retrbinary('RETR ' + filename, local_file.write)
    local_file.close()

ftp.close()

print('скачаны файлы:')
print(os.listdir('c:/IRDs'))
