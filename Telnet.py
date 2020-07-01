"""
в этом файле попробуем реализовать различные способы подключени по телнет (telnetlib, paramiko, netmiko, pexpect),
чтобы корректно передать параметр NAME в ucs_audit.
"""

import pexpect

with pexpect.spawn('telnet 172.31.176.4') as telnet:

    telnet.expect('Username:')
    telnet.sendline('ucsmanager')

    telnet.expect('Password:')
    telnet.sendline('ucsmanager')

    telnet.expect('Username:')
    telnet.sendline('gotalife')

    telnet.expect('(UCSMANAGER)$')
    print(telnet.before.decode())