"""
Скрипт запрашивает электронный номер приёмника,
считывает по нему информацию из базы данных ua.db из таблиц KATEL3 и ktr,
подготавливает скрипт-файл files/temp/UA_SCRIPT.SCR;1 для последующего
редактирования и загрузки на сервер.
"""

import sqlite3
from pprint import pprint

ua_script_template = '''
    SUI                    ! Set Unit Information
    {
    GID = 0;                    ! UCS Group ID
    UA = 0X0000000000;                    ! Unit Address
    PFE = 0;                    ! IRD HWC Profile Enabled
    MPIU = 0;                    ! Multiport IRD Update
    IPPR = 0;                    ! IPPV Password Reset
    RPR = 0;                    ! Ratings Password Reset
    INPR = 0;                    ! Installer Password Reset
    LCIE = 0;                    ! Last Channel IPG Entry
    IPG = 0;                    ! IPG Enable
    DS = 0;                    ! Adjust for daylight savings
    ENBO = 0;                    ! Enable blackouts
    RC = 0;                    ! Region Code
    SVCMID = 311;                    ! Single VCM ID
    AT [0] = 0x0;                    ! Authorization Tiers
    AT [1] = 0x0;                    ! Authorization Tiers
    AT [2] = 0x0;                    ! Authorization Tiers
    AT [3] = 0x0;                    ! Authorization Tiers
    AT [4] = 0x0;                    ! Authorization Tiers
    AT [5] = 0x0;                    ! Authorization Tiers
    AT [6] = 0x0;                    ! Authorization Tiers
    AT [7] = 0x0;                    ! Authorization Tiers
    AT [8] = 0x0;                    ! Authorization Tiers
    AT [9] = 0x0;                    ! Authorization Tiers
    AT [10] = 0x0;                    ! Authorization Tiers
    AT [11] = 0x0;                    ! Authorization Tiers
    AT [12] = 0x0;                    ! Authorization Tiers
    AT [13] = 0x0;                    ! Authorization Tiers
    AT [14] = 0x0;                    ! Authorization Tiers
    AT [15] = 0x0;                    ! Authorization Tiers
    AT [16] = 0x0;                    ! Authorization Tiers
    AT [17] = 0x0;                    ! Authorization Tiers
    AT [18] = 0x0;                    ! Authorization Tiers
    AT [19] = 0x0;                    ! Authorization Tiers
    AT [20] = 0x0;                    ! Authorization Tiers
    AT [21] = 0x0;                    ! Authorization Tiers
    AT [22] = 0x0;                    ! Authorization Tiers
    AT [23] = 0x0;                    ! Authorization Tiers
    AT [24] = 0x0;                    ! Authorization Tiers
    AT [25] = 0x0;                    ! Authorization Tiers
    AT [26] = 0x0;                    ! Authorization Tiers
    AT [27] = 0x0;                    ! Authorization Tiers
    AT [28] = 0x0;                    ! Authorization Tiers
    AT [29] = 0x0;                    ! Authorization Tiers
    AT [30] = 0x0;                    ! Authorization Tiers
    AT [31] = 0x0;                    ! Authorization Tiers
    AT [32] = 0x0;                    ! Authorization Tiers
    AT [33] = 0x0;                    ! Authorization Tiers
    AT [34] = 0x0;                    ! Authorization Tiers
    AT [35] = 0x0;                    ! Authorization Tiers
    AT [36] = 0x0;                    ! Authorization Tiers
    AT [37] = 0x0;                    ! Authorization Tiers
    AT [38] = 0x0;                    ! Authorization Tiers
    AT [39] = 0x0;                    ! Authorization Tiers
    AT [40] = 0x0;                    ! Authorization Tiers
    AT [41] = 0x0;                    ! Authorization Tiers
    AT [42] = 0x0;                    ! Authorization Tiers
    AT [43] = 0x0;                    ! Authorization Tiers
    AT [44] = 0x0;                    ! Authorization Tiers
    AT [45] = 0x0;                    ! Authorization Tiers
    AT [46] = 0x0;                    ! Authorization Tiers
    AT [47] = 0x0;                    ! Authorization Tiers
    AT [48] = 0x0;                    ! Authorization Tiers
    AT [49] = 0x0;                    ! Authorization Tiers
    AT [50] = 0x0;                    ! Authorization Tiers
    AT [51] = 0x0;                    ! Authorization Tiers
    AT [52] = 0x0;                    ! Authorization Tiers
    AT [53] = 0x0;                    ! Authorization Tiers
    AT [54] = 0x0;                    ! Authorization Tiers
    AT [55] = 0x0;                    ! Authorization Tiers
    AT [56] = 0x0;                    ! Authorization Tiers
    AT [57] = 0x0;                    ! Authorization Tiers
    AT [58] = 0x0;                    ! Authorization Tiers
    AT [59] = 0x0;                    ! Authorization Tiers
    AT [60] = 0x0;                    ! Authorization Tiers
    AT [61] = 0x0;                    ! Authorization Tiers
    AT [62] = 0x0;                    ! Authorization Tiers
    AT [63] = 0x0;                    ! Authorization Tiers
    AT [64] = 0x0;                    ! Authorization Tiers
    AT [65] = 0x0;                    ! Authorization Tiers
    AT [66] = 0x0;                    ! Authorization Tiers
    AT [67] = 0x0;                    ! Authorization Tiers
    AT [68] = 0x0;                    ! Authorization Tiers
    AT [69] = 0x0;                    ! Authorization Tiers
    AT [70] = 0x0;                    ! Authorization Tiers
    AT [71] = 0x0;                    ! Authorization Tiers
    AT [72] = 0x0;                    ! Authorization Tiers
    AT [73] = 0x0;                    ! Authorization Tiers
    AT [74] = 0x0;                    ! Authorization Tiers
    AT [75] = 0x0;                    ! Authorization Tiers
    AT [76] = 0x0;                    ! Authorization Tiers
    AT [77] = 0x0;                    ! Authorization Tiers
    AT [78] = 0x0;                    ! Authorization Tiers
    AT [79] = 0x0;                    ! Authorization Tiers
    AT [80] = 0x0;                    ! Authorization Tiers
    AT [81] = 0x0;                    ! Authorization Tiers
    AT [82] = 0x0;                    ! Authorization Tiers
    AT [83] = 0x0;                    ! Authorization Tiers
    AT [84] = 0x0;                    ! Authorization Tiers
    AT [85] = 0x0;                    ! Authorization Tiers
    AT [86] = 0x0;                    ! Authorization Tiers
    AT [87] = 0x0;                    ! Authorization Tiers
    AT [88] = 0x0;                    ! Authorization Tiers
    AT [89] = 0x0;                    ! Authorization Tiers
    AT [90] = 0x0;                    ! Authorization Tiers
    AT [91] = 0x0;                    ! Authorization Tiers
    AT [92] = 0x0;                    ! Authorization Tiers
    AT [93] = 0x0;                    ! Authorization Tiers
    AT [94] = 0x0;                    ! Authorization Tiers
    AT [95] = 0x0;                    ! Authorization Tiers
    AT [96] = 0x0;                    ! Authorization Tiers
    AT [97] = 0x0;                    ! Authorization Tiers
    AT [98] = 0x0;                    ! Authorization Tiers
    AT [99] = 0x0;                    ! Authorization Tiers
    AT [100] = 0x0;                    ! Authorization Tiers
    AT [101] = 0x0;                    ! Authorization Tiers
    AT [102] = 0x0;                    ! Authorization Tiers
    AT [103] = 0x0;                    ! Authorization Tiers
    AT [104] = 0x0;                    ! Authorization Tiers
    AT [105] = 0x0;                    ! Authorization Tiers
    AT [106] = 0x0;                    ! Authorization Tiers
    AT [107] = 0x0;                    ! Authorization Tiers
    AT [108] = 0x0;                    ! Authorization Tiers
    AT [109] = 0x0;                    ! Authorization Tiers
    AT [110] = 0x0;                    ! Authorization Tiers
    AT [111] = 0x0;                    ! Authorization Tiers
    AT [112] = 0x0;                    ! Authorization Tiers
    AT [113] = 0x0;                    ! Authorization Tiers
    AT [114] = 0x0;                    ! Authorization Tiers
    AT [115] = 0x0;                    ! Authorization Tiers
    AT [116] = 0x0;                    ! Authorization Tiers
    AT [117] = 0x0;                    ! Authorization Tiers
    AT [118] = 0x0;                    ! Authorization Tiers
    AT [119] = 0x0;                    ! Authorization Tiers
    AT [120] = 0x0;                    ! Authorization Tiers
    AT [121] = 0x0;                    ! Authorization Tiers
    AT [122] = 0x0;                    ! Authorization Tiers
    AT [123] = 0x0;                    ! Authorization Tiers
    AT [124] = 0x0;                    ! Authorization Tiers
    AT [125] = 0x0;                    ! Authorization Tiers
    AT [126] = 0x0;                    ! Authorization Tiers
    AT [127] = 0x0;                    ! Authorization Tiers
    AT [128] = 0x0;                    ! Authorization Tiers
    AT [129] = 0x0;                    ! Authorization Tiers
    AT [130] = 0x0;                    ! Authorization Tiers
    AT [131] = 0x0;                    ! Authorization Tiers
    AT [132] = 0x0;                    ! Authorization Tiers
    AT [133] = 0x0;                    ! Authorization Tiers
    AT [134] = 0x0;                    ! Authorization Tiers
    AT [135] = 0x0;                    ! Authorization Tiers
    AT [136] = 0x0;                    ! Authorization Tiers
    AT [137] = 0x0;                    ! Authorization Tiers
    AT [138] = 0x0;                    ! Authorization Tiers
    AT [139] = 0x0;                    ! Authorization Tiers
    AT [140] = 0x0;                    ! Authorization Tiers
    AT [141] = 0x0;                    ! Authorization Tiers
    AT [142] = 0x0;                    ! Authorization Tiers
    AT [143] = 0x0;                    ! Authorization Tiers
    AT [144] = 0x0;                    ! Authorization Tiers
    AT [145] = 0x0;                    ! Authorization Tiers
    AT [146] = 0x0;                    ! Authorization Tiers
    AT [147] = 0x0;                    ! Authorization Tiers
    AT [148] = 0x0;                    ! Authorization Tiers
    AT [149] = 0x0;                    ! Authorization Tiers
    AT [150] = 0x0;                    ! Authorization Tiers
    AT [151] = 0x0;                    ! Authorization Tiers
    AT [152] = 0x0;                    ! Authorization Tiers
    AT [153] = 0x0;                    ! Authorization Tiers
    AT [154] = 0x0;                    ! Authorization Tiers
    AT [155] = 0x0;                    ! Authorization Tiers
    AT [156] = 0x0;                    ! Authorization Tiers
    AT [157] = 0x0;                    ! Authorization Tiers
    AT [158] = 0x0;                    ! Authorization Tiers
    AT [159] = 0x0;                    ! Authorization Tiers
    AT [160] = 0x0;                    ! Authorization Tiers
    AT [161] = 0x0;                    ! Authorization Tiers
    AT [162] = 0x0;                    ! Authorization Tiers
    AT [163] = 0x0;                    ! Authorization Tiers
    AT [164] = 0x0;                    ! Authorization Tiers
    AT [165] = 0x0;                    ! Authorization Tiers
    AT [166] = 0x0;                    ! Authorization Tiers
    AT [167] = 0x0;                    ! Authorization Tiers
    AT [168] = 0x0;                    ! Authorization Tiers
    AT [169] = 0x0;                    ! Authorization Tiers
    AT [170] = 0x0;                    ! Authorization Tiers
    AT [171] = 0x0;                    ! Authorization Tiers
    AT [172] = 0x0;                    ! Authorization Tiers
    AT [173] = 0x0;                    ! Authorization Tiers
    AT [174] = 0x0;                    ! Authorization Tiers
    AT [175] = 0x0;                    ! Authorization Tiers
    AT [176] = 0x0;                    ! Authorization Tiers
    AT [177] = 0x0;                    ! Authorization Tiers
    AT [178] = 0x0;                    ! Authorization Tiers
    AT [179] = 0x0;                    ! Authorization Tiers
    AT [180] = 0x0;                    ! Authorization Tiers
    AT [181] = 0x0;                    ! Authorization Tiers
    AT [182] = 0x0;                    ! Authorization Tiers
    AT [183] = 0x0;                    ! Authorization Tiers
    AT [184] = 0x0;                    ! Authorization Tiers
    AT [185] = 0x0;                    ! Authorization Tiers
    AT [186] = 0x0;                    ! Authorization Tiers
    AT [187] = 0x0;                    ! Authorization Tiers
    AT [188] = 0x0;                    ! Authorization Tiers
    AT [189] = 0x0;                    ! Authorization Tiers
    AT [190] = 0x0;                    ! Authorization Tiers
    AT [191] = 0x0;                    ! Authorization Tiers
    AT [192] = 0x0;                    ! Authorization Tiers
    AT [193] = 0x0;                    ! Authorization Tiers
    AT [194] = 0x0;                    ! Authorization Tiers
    AT [195] = 0x0;                    ! Authorization Tiers
    AT [196] = 0x0;                    ! Authorization Tiers
    AT [197] = 0x0;                    ! Authorization Tiers
    AT [198] = 0x0;                    ! Authorization Tiers
    AT [199] = 0x0;                    ! Authorization Tiers
    AT [200] = 0x0;                    ! Authorization Tiers
    AT [201] = 0x0;                    ! Authorization Tiers
    AT [202] = 0x0;                    ! Authorization Tiers
    AT [203] = 0x0;                    ! Authorization Tiers
    AT [204] = 0x0;                    ! Authorization Tiers
    AT [205] = 0x0;                    ! Authorization Tiers
    AT [206] = 0x0;                    ! Authorization Tiers
    AT [207] = 0x0;                    ! Authorization Tiers
    AT [208] = 0x0;                    ! Authorization Tiers
    AT [209] = 0x0;                    ! Authorization Tiers
    AT [210] = 0x0;                    ! Authorization Tiers
    AT [211] = 0x0;                    ! Authorization Tiers
    AT [212] = 0x0;                    ! Authorization Tiers
    AT [213] = 0x0;                    ! Authorization Tiers
    AT [214] = 0x0;                    ! Authorization Tiers
    AT [215] = 0x0;                    ! Authorization Tiers
    AT [216] = 0x0;                    ! Authorization Tiers
    AT [217] = 0x0;                    ! Authorization Tiers
    AT [218] = 0x0;                    ! Authorization Tiers
    AT [219] = 0x0;                    ! Authorization Tiers
    AT [220] = 0x0;                    ! Authorization Tiers
    AT [221] = 0x0;                    ! Authorization Tiers
    AT [222] = 0x0;                    ! Authorization Tiers
    AT [223] = 0x0;                    ! Authorization Tiers
    AT [224] = 0x0;                    ! Authorization Tiers
    AT [225] = 0x0;                    ! Authorization Tiers
    AT [226] = 0x0;                    ! Authorization Tiers
    AT [227] = 0x0;                    ! Authorization Tiers
    AT [228] = 0x0;                    ! Authorization Tiers
    AT [229] = 0x0;                    ! Authorization Tiers
    AT [230] = 0x0;                    ! Authorization Tiers
    AT [231] = 0x0;                    ! Authorization Tiers
    AT [232] = 0x0;                    ! Authorization Tiers
    AT [233] = 0x0;                    ! Authorization Tiers
    AT [234] = 0x0;                    ! Authorization Tiers
    AT [235] = 0x0;                    ! Authorization Tiers
    AT [236] = 0x0;                    ! Authorization Tiers
    AT [237] = 0x0;                    ! Authorization Tiers
    AT [238] = 0x0;                    ! Authorization Tiers
    AT [239] = 0x0;                    ! Authorization Tiers
    AT [240] = 0x0;                    ! Authorization Tiers
    AT [241] = 0x0;                    ! Authorization Tiers
    AT [242] = 0x0;                    ! Authorization Tiers
    AT [243] = 0x0;                    ! Authorization Tiers
    AT [244] = 0x0;                    ! Authorization Tiers
    AT [245] = 0x0;                    ! Authorization Tiers
    AT [246] = 0x0;                    ! Authorization Tiers
    AT [247] = 0x0;                    ! Authorization Tiers
    AT [248] = 0x0;                    ! Authorization Tiers
    AT [249] = 0x0;                    ! Authorization Tiers
    AT [250] = 0x0;                    ! Authorization Tiers
    AT [251] = 0x0;                    ! Authorization Tiers
    AT [252] = 0x0;                    ! Authorization Tiers
    AT [253] = 0x0;                    ! Authorization Tiers
    AT [254] = 0x0;                    ! Authorization Tiers
    AT [255] = 0x0;                    ! Authorization Tiers
    APC = "";                    ! Area Postal Code
    RR = 0;                    ! Ratings region
    TZ = 360;                    ! Time Zone
    UG = 0;                    ! Unit DEM Group
    IPGSN = 0;                    ! Commercial IPG svc number index
    NAME = "000-00000-00000-000           ";                    ! Name
    MISC1 = "                                                                                ";                    ! Misc field 1
    MISC2 = "                                                                                ";                    ! Misc field 2
    MISC3 = "                                                                                ";                    ! Misc field 3
    MISC4 = "                                                                                ";                    ! Misc field 4
    MISC5 = "                                                                                ";                    ! Misc field 5
    MISC6 = "                                                                                ";                    ! Misc field 6
    P1LLC = "";                    ! Port1 Left Language
    P1RLC = "";                    ! Port1 Right Language
    P2LLC = "";                    ! Port2 Left Language
    P2RLC = "";                    ! Port2 Right Language
    SUBLC = "";                    ! Subtitle Language
    ARM = 0;                    ! Acquisition Recovery Mode
    DOE = 0;                    ! Data Output
    TSOE = 0;                    ! Transport Stream Output
    CPE = 0;                    ! Control Port
    FPE = 0;                    ! Front Panel
    VNW = 0;                    ! Virtual Network
    ARED = 0;                    ! Acquisition Recovery Entry Delay
    }
    '''


def tiers_list_to_script(tiers_list):
    """
    преобразует список тиер-битов из номеров в строковом виде
    в номер блока АТ[..] и шестнадцатиричное значение,
    которое в бинарном виде укажет на положение '1'.
    """

    tiers_dict_nums = dict()
    at_string_list = list()
    
    for tier in tiers_list:        
        at_num = (int(tier) // 8)  # проверяем какие тиер-биты в какие блоки АТ [..] попадают:

        one_position = int(tier) - at_num * 8  # позиция '1' в блоке АТ [..], начиная с 0!!!
        bits = list('00000000')
        bits[one_position] = '1'

        a = ''
        d = ''
        for digs in bits:
            a = a + digs
            b = a[::-1]  # переворачиваем число в привычное положение, где старший разряд будет слева
            d = hex((int(b, 2)))    # переводит в hex формат,

        # так как тиер-биты могут попадать в один блок AT, надо их скомбинировать в одном блоке.
        if at_num not in tiers_dict_nums.keys():
            tiers_dict_nums.setdefault(at_num)
            tiers_dict_nums[at_num] = d

        # а для неповторяющихся блоков сразу присваивается hex-значение
        else:
            tiers_dict_nums[at_num] = '0x{:x}'.format(int(tiers_dict_nums[at_num], 16) + int(d, 16))

    #   теперь формируем список строк для последующей вставки из в скрипт:
    for item in tiers_dict_nums.items():
        at_string_list.append('AT [{}] = '.format(item[0]) + item[1])

    return at_string_list

def create_script(ua_name, tiers_list, descriptors_dict):
    """
    по имени приемника, списку тиер-битов и словарю описательных элементов
    из шаблона формируется новый скрипт.
    """

    #   перевод электронного номера в шестнадцатиричный вид
    ua = '0x{:010x}'.format(int(ua_name.split('-')[1] + ua_name.split('-')[2])).upper()

    print('Данные для записи в скрипт:')
    print('ua_name: ', ua_name)
    print('ua:', ua)
    print('tiers: ', tiers_list)
    print('descriptors: ', descriptors)

    #   номер приемника (в шестнадцатиричном виде) и его строковое имя (для удобства поиска полный номер UA).
    #   исходные шаблонные значения заменяются в скрипте новыми реальными значениями:
    new_script = ua_script_template.replace('0x0000000000', ua).replace('000-00000-00000-000', ua_name)

    #   из списка тиер-битов отдельные тиер-биты переводим в бинарный вид
    #   и расставляем в соответствующие блоки "AT [..] = 0x.. " результирующего скрипта:
    if tiers_list:
        at_string = tiers_list_to_script(tiers_list)

        for at_s in at_string:
            if len(at_s.split(' = ')[1]) == 4:
                new_script = new_script.replace(at_s[0:-4] + '0x0; ', at_s + ';')
            else:
                new_script = new_script.replace(at_s[0:-4] + ' 0x0;', at_s + ';')

    if descriptors_dict:
        for misc_fields, describers in descriptors_dict.items():

            # описание длиной в 80 символов, изначально это пробелы.
            # их надо заменить соответствующими строками MISC1 = ".... и т.д.

            # попробовать позже:
            '''
            •   ljust(width):
             когда длина строки в Python меньше, чем параметр width,
              справа от неё добавляются пробелы для дополнения значения width,
               при этом происходит выравнивание строки по левому краю;
            '''

            new_script = new_script.replace(misc_fields + ' = "' + ' ' * (len(describers)),
                                            misc_fields + ' = "' + describers)

    return new_script


def get_info_from_db(ua, db_name):
    """
    из базы данных (ua.db) из одной из таблиц (ktr, ucs)
    достаётся информация по конкретному приёмнику.
    """
    # connect to ua.db - database with unit addresses
    connection = sqlite3.connect('ua.db')
    cursor = connection.cursor()

    query_str = "SELECT * FROM {} where ua = '{}';".format(db_name, ua)
    # print('query_str: ', query_str)

    cursor.execute(query_str)
    ird_data = cursor.fetchone()

    connection.close()

    return ird_data

if __name__ == "__main__":

    UA = input("ВВЕДИТЕ НОМЕР ПРИЁМНИКА (UA):\n")
    if not UA:
        UA = '000-03086-26596-214'  # пока для теста

    print('данные по приёмнику {} из базы данных UCS:'.format(UA))
    ucs_ua_info = get_info_from_db(UA[0:15], 'KATEL3')

    pprint(ucs_ua_info)
    print('- - '*20)

    tiers = list(ucs_ua_info[2].split(' '))
    MISC1 = ucs_ua_info[3]
    MISC2 = ucs_ua_info[4]
    MISC3 = ucs_ua_info[5]
    MISC4 = ucs_ua_info[6]
    MISC5 = ucs_ua_info[7]
    MISC6 = ucs_ua_info[8]
    descriptors = {'MISC1': MISC1, 'MISC2': MISC2, 'MISC3': MISC3, 'MISC4': MISC4,
                   'MISC5': MISC5, 'MISC6': MISC6}

    print('данные по приёмнику {} из базы данных Казтелерадио:'.format(UA))
    ktr_ua_info = get_info_from_db(UA[0:15], 'ktr')

    pprint(ktr_ua_info)
    print('- - '*20)

    UA_SCRIPT = create_script(UA, tiers, descriptors)
    print(UA_SCRIPT)
    with open('files/temp/UA_SCRIPT.SCR;1', 'w') as file:
        for lines in UA_SCRIPT:
            file.write(lines)
    print('в директоии files/temp/ подготовлен файл UA_SCRIPT.SCR;1\n')

    x = input('всё!\n\nнажмите любую клавишу')
