

import re   # for using regulars parsing
from pprint import pprint

text_file = 'files/PRM.txt'


def parse_txt(txt_file):
    """
    функция парсит текстовый вариант Excel-файла по номерам приемников и
    возвращает список приемников и список номеров с ошибками;

    :param txt_file:
    :return: ird_dict, wrong_ua
    """

    file = open(txt_file)
    # print(file.read())
    text = file.read().split('\n')  # разбиваем на строчки
    # print(text)
    ird_dict = {}
    wrong_ua = list()
    for items in text:  # каждую строчку...
        if '000-' in items:  # проверяем на наличие номера приемника
            # print(' - - ' * 20)
            # print(items.rstrip())

            # Например: ['С-Казахстанская', 'Айыртауский', 'Арыкбалык', '22', 'Казахстан', 'DigiCipher-II',
            # 'DSR205K', '000-03454-52574-025']

            if re.search(r'(000-0.*)\w*.*', items):
                ua = re.search(r'(000-0.*)\w*.*', items).group(0)
            else:
                continue
            
            unit_address = ua.split('\t')[0].rstrip().replace('.', '')

            # проверка номера на правильность формата
            if unit_address.startswith('000-'):
                ua_check = re.search(r'000-\d{5}-\d{5}-\d{3}', unit_address)
                if not ua_check:
                    unit_address += ' требуется проверка номера!'
                    wrong_ua.append({unit_address: items.split('\t')})

            # заполняем данные по каждому приемнику
            ird_name = unit_address
            odrt = items.split('\t')[1].replace(':', '').rstrip()
            # region = items.split('\t')[1]
            city = items.split('\t')[2]
            program = items.split('\t')[3]
            print(ird_name)
            uch_tv = items.split('\t')[8] if len(items.split('\t')) >= 8 else ''
            # print(items.split('\t'))
            obl_br = items.split('\t')[9]
                                                
            # чтобы в поле OBL_BR было какое-то значение (потом для БД)
            # print(obl_br.split(), '\n', 'len(obl_br.split())', len(obl_br.split()))
            obl_br_str = "ОБЛ_ТВ" if len(obl_br.split()) >  3 else "-"
            

            # чтобы в поле PROGRAM было какое-то значение (потом для БД)
            if program:
                program_str = program
            else:
                if obl_br:
                    program_str = 'Казахстан'
                else:
                    program_str = '-'

            ird_dict[unit_address] = dict(NAME=ird_name,
                                          ODRT=odrt,
                                          CITY=city,
                                          PROGRAM=program_str,
                                          UCH_TV=uch_tv,
                                          OBL_BR=obl_br_str)

        else:
            '''
            print(' - - ' * 20)
            print('* !!! ошибка в распаковке данных! нет номера приемника DCII',
                 '\n в строке:'
                 '\n', items, 'не найден номер приемника')
            '''
    file.close()
    return ird_dict, wrong_ua


irds_dict, wrong_ua_list = parse_txt(text_file)

if __name__ == "__main__":

    pprint(irds_dict, sort_dicts=False)

    if wrong_ua_list:
        print('Есть номера с ОШИБКАМИ\n(см. файл wrong_nums.txt):\n')
        pprint(wrong_ua_list)

        with open('files/wrong_nums.txt', 'w') as file_for_correct:
            for dicts in wrong_ua_list:
                file_for_correct.write(str(dicts).join("\n\n"))

    '''
    #   перевод электронного номера в шестнадцатиричный вид
    UA = '0x{:010x}'.format(int(ua.split('-')[1] + ua.split('-')[2]))
    '''
