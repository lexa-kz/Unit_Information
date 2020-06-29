import re
from pprint import pprint


def tier_translation(tiers_list_hex):
    """
    переводит список строк в список tier-битов в дес.виде
    :param tiers_list_hex:
    :return: tiers_list_dec
    """

    tiers_list_dec = list()
    for tiers_string in tiers_list_hex:
        # print(tiers_string)
        tier_block = int(tiers_string.split()[1].replace('[', '').replace(']', ''))
        tier_bit = int(tiers_string.split()[-1], 16)

        tb = '{:08b}'.format(tier_bit)
        # print(tb)
        bt = tb[::-1]
        # тиер-бит в двоичном виде и превернут, чтобы посчитать
        # 10000000 -> 00000001

        # посчитаем количество "1"
        nums = bt.count('1')
        # print('nums_of_1:', nums)

        # теперь находим '1', вычисляем её позицию
        for i in range(0, nums):
            # print('- {}: '.format(i), bt, )
            index_1 = bt.find('1')
            tier_real = tier_block * 8 + index_1

            tiers_list_dec.append(tier_real)

            # меняем 1 на 0, что больше не считало, и далее
            # по циклу остальные 1 считать

            bt = bt[0:index_1] + '0' + bt[index_1 + 1:]

        # print(tiers_list_dec)

    return tiers_list_dec


def parse_script(filename):
    """
    функция парсит .scr файл из UCS и возвращает список приемников;

    :param: filename
    :return: ird_dict
    """

    file = open(filename)

    ird_info_list = file.read().rstrip().split('}')
    # получился список строк, где одна строка - инфо про весь приемник
    ird_dict = dict()
    for string in ird_info_list:
        # пробегаемся по параметрам приемника

        if 'UA =' in string:

            ird_info = dict()

            # выделяем номер приемника
            ua = str(int(re.search(r'UA = 0x(\w*);.*', string).group(1), 16))
            ua = '000-0' + ua[0:4] + '-' + ua[4:]
            # print(ua)
            ird_dict.setdefault(ua)

            # выписываем все тиер-биты в список
            tiers_list = re.findall(r'(AT \[.*);', string)

            # из полного списка tiers_list удаляем все нулевые тиер-биты ('0х0')
            for i in range(len(tiers_list)):
                while '0x0' in tiers_list:
                    tiers_list.remove(tiers_list[i])

            # добавляем в итоговый словарь словарь тиер-битов
            ird_info.update({'TIERS': tier_translation(tiers_list)})

            #  выделяем описательные поля
            name = re.search(r'NAME = "(\S*)\s*";.*', string)
            if name:
                ird_info.update({'NAME': name.group(1)})
            else:
                ird_info.update({'NAME': ''})

            misc1 = re.search(r'MISC1 = "(\w*\s?\w*)\s+";.*', string)
            if misc1:
                ird_info.update({'MISC1': misc1.group(1).rstrip()})
            else:
                ird_info.update({'MISC1': ''})

            misc2 = re.search(r'MISC2 = "(\w*\s?\w*)\s+";.*', string)
            if misc2:
                ird_info.update({'MISC2': misc2.group(1).rstrip()})
            else:
                ird_info.update({'MISC2': ''})

            misc3 = re.search(r'MISC3 = "(\w*\s?\w*)\s+";.*', string)
            if misc3:
                ird_info.update({'MISC3': misc3.group(1).rstrip()})
            else:
                ird_info.update({'MISC3': ''})

            misc4 = re.search(r'MISC4 = "(\w*\s?\w*)\s+";.*', string)
            if misc4:
                ird_info.update({'MISC4': misc4.group(1).rstrip()})
            else:
                ird_info.update({'MISC4': ''})

            misc5 = re.search(r'MISC5 = "(\w*\s*,\s\w*)\s+";.*', string)
            if misc5:
                ird_info.update({'MISC5': misc5.group(1).rstrip()})
            else:
                ird_info.update({'MISC5': ''})

            misc6 = re.search(r'MISC6 = "(\w*\s?\w*)\s+";.*', string)
            if misc6:
                ird_info.update({'MISC6': misc6.group(1).rstrip()})
            else:
                ird_info.update({'MISC6': ''})

            ird_dict[ua] = ird_info

        else:
            continue

        file.close()

    return ird_dict


if __name__ == "__main__":
    pprint(parse_script('../UCS_DB.SCR;1'), sort_dicts=False)
