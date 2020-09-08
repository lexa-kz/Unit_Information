import re
from SetUnitInformation import tiers_list_to_script
from SetUnitInformation import get_info_from_db
from parser_script import tier_translation


def script_file_changing(file, q):
    """
    функция вносит изменения в скрипт-файл
    :param file: - файл, который будет изменен
            q - какие изменения внести в файл'
                  + добавить тиер-бит
                  - удалить тиер-бит
                  n изменить имя name
                  m1 - m6 изменить дескриптор MISC1-MISC6
    :return: отчёт, что изменения внесены
    """

    # считаем файл, в переменную data, которую будем изменять
    data = open(file).read()

    if q:
        if q.startswith('+'):
            t_add = q[1:]
            print(' - добавляем тиер-бит', t_add)
            #   input('какой тиер-бит добавить? : ')

            # вычисляем какой в блок и какое число записывать (SetUnitInformation)
            t_hex = tiers_list_to_script([(t_add)])
            print('это: ', t_hex[0])
            AT_num, hex_num = re.search('AT \[(\d+)\] = 0x(\d+)', t_hex[0]).groups()

            # есть ли в исходном блоке АТ такой (или другой) тиер-бит?
            trbt = re.search('AT \[{}\] = 0x(\d+)'.format(AT_num), data).group(1)
            if int(trbt):
                old_tiers = tier_translation(['AT [{}] = 0x'.format(AT_num) + trbt])
                print('но в блоке АТ [{}] уже есть тиер-биты: '.format(AT_num),
                      '0x' + trbt, '(dec: {})'.format(old_tiers))
                #   проверяем это тиер-бит тот же самый?
                if int(t_add) in old_tiers:
                    print('и он тот же самый, поэтому ничего делать не нужно')
                else:
                    print('и он другой, поэтому его надо добавить')
                    new_tier_list = old_tiers
                    new_tier_list.append(int(t_add))
                    print('new_tier_list', new_tier_list)

                    # обновленный список тиер-битов преобразуем в строку для скрипта
                    trs_lst = tiers_list_to_script(new_tier_list)[0]
                    print(trs_lst)

                    print('пишем в файл...')
                    o = open(file, 'w')
                    o.write(re.sub('AT \[{}\] = 0x\d+'.format(AT_num), trs_lst, data))
                    o.close()

            else:
                print('в блоке АТ [{}] исходного скрипта нет тиер-битов ( AT [{}] = 0х0), \n'
                      'продолжаем работу...'.format(AT_num, AT_num))

                # запишем изменения обратно в файл
                o = open(file, 'w')
                o.write(re.sub('AT \[{}\] = 0x\d+'.format(AT_num), 'AT [' + AT_num + '] = 0x' + hex_num, data))
                o.close()

        elif q.startswith('-'):
            t_del = input('какой тиер-бит удалить? : ')

            o = open(file, 'w')
            o.write(re.sub('AT \[0\] = 0x\d+', 'AT [0] = 0x0', data))
            o.close()

        elif q.startswith('m'):
            print('описательное поле MISC{} меняем на "{}"'.format(q[1], q[3:]))
            o = open(file, 'w')
            o.write(re.sub('MISC{} = ".*";                    ! Misc field {}'.format(q[1], q[1]),
                           'MISC{} = "{}'.format(q[1], q[3:]) + ' '*(80-len(q[3:])) + '";                    ! Misc field {}'.format(q[1]), data))
            o.close()

        else:
            print('так как ничего не введено, то не будет внесено, никаких изменений')

    return 'в файл {} внесены изменения и он готов к загрузке на сервер'.format(file)


if __name__=="__main__":

    file = 'files/temp/result_file.SCR;1'

    print(script_file_changing(file, '+9'))
