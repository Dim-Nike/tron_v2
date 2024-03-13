from Tron.server.scripts.encrypte_v1 import *
from Tron.server.scripts.decoding import *
test_de_msg = []
test_de_f_key = []
test_de_s_key = []
test_msg =  [
    "Широкая электрификация южных губерний даст мощный толчок развитию сельского хозяйства.",
    "Ждем чуда, когда же он придет?",
    "Жук целует щеку дивной красавицы.",
    "Эй, жлоб! Где туз?",
    "Шеф взъерошенным волосом часто гордился.",
    "Жюри оценило выступление артиста на 8 баллов.",
    "Шум дождя за окном создает уютную атмосферу.",
    "Жду факса с экстренной информацией.",
    "Жил да был добрый человек.",
    "Шалунья Женя часто шутила на уроках.",
    "Жаркое лето было особенно жарким в этом году.",
    "Шахматы - это умственный спорт.",
    "Жук съел шоколадку и улетел вдаль.",
    "Шеф попросил принести отчет к обеду.",
    "Желтая шапка на зеленой траве выглядит очень ярко.",
    "Ждем звонка с хорошими новостями.",
    "Железный занавес разделял страны.",
    "Шумный город не дает спокойно выспаться.",
    "Жук-сенсационист удивил всех своими трюками.",
    "Шеф поздравил коллег с успешным завершением проекта."
]

test_f_key = ['!', ' ',  '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '/', ':', ';', '<', '=', '>',
              '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
              'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f',
              'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
              '{', '|', '}', '~', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О',
              'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в',
              'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
              'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

test_s_key = [str(i) for i in range(101)]

print('--- Проверка шифровки сообщения ---')
for i, el_msg in enumerate(test_msg):
    msg_test = en_msg(msg_user=el_msg, ESRS=ESRS, f_key=test_f_key[0], img_path='/home/trigger/Рабочий стол/КБССК.png',
           s_key=test_s_key[0],
           esrs_number=ERSR_number, noise_list=noise_list)
    test_de_msg.append(msg_test)
    print(f'Тест {i+1}/{len(test_msg)} пройден!')

print(test_de_msg)

print('Проверка на корректность первого ключа')
for i, el_f_key in enumerate(test_f_key):
    f_key_test = en_msg(msg_user=test_msg[0], ESRS=ESRS, f_key=el_f_key, img_path='/home/trigger/Рабочий стол/КБССК.png',
           s_key=test_s_key[0],
           esrs_number=ERSR_number, noise_list=noise_list)
    test_de_f_key.append(f_key_test)
    print(f'Тест {i+1}/{len(test_f_key)} пройден!')

print('Проверка на корректность второго ключа')
for i, el_s_key in enumerate(test_s_key):
    s_key_test = en_msg(msg_user=test_msg[0], ESRS=ESRS, f_key=test_f_key[0], img_path='/home/trigger/Рабочий стол/КБССК.png',
           s_key=el_s_key,
           esrs_number=ERSR_number, noise_list=noise_list)
    test_de_s_key.append(s_key_test)
    print(f'Тест {i+1}/{len(test_s_key)} пройден!')



print('--- Проверка дешифрования сообщения ---')
print('Проверка на корректность сообщение')
for i, el_msg in enumerate(test_de_msg):
    new_msg = de_msg(msg_en=el_msg, f_key=test_f_key[0], s_key=test_s_key[0], noise_l=noise_list,
           image_patch='/home/trigger/Рабочий стол/КБССК.png', esrs_number=ERSR_number, esrs=ESRS)
    if test_msg[i] == new_msg:
        print(f'Тест {i + 1}/{len(test_s_key)} пройден!')
    else:
        print('Тест не пройден')

print('Проверка на корректность первого ключа')
for i, el_f_key in enumerate(test_f_key):
    new_msg = de_msg(msg_en=test_de_f_key[i], f_key=el_f_key, s_key=test_s_key[0], noise_l=noise_list,
           image_patch='/home/trigger/Рабочий стол/КБССК.png', esrs_number=ERSR_number, esrs=ESRS)
    if test_msg[0] == new_msg:
        print(f'Тест {i + 1}/{len(test_s_key)} пройден!')

print('Проверка на корректность второго ключа')
for i, el_s_key in enumerate(test_s_key):
    new_msg = de_msg(msg_en=test_de_s_key[i], f_key=test_f_key[0], s_key=el_s_key, noise_l=noise_list,
           image_patch='/home/trigger/Рабочий стол/КБССК.png', esrs_number=ERSR_number, esrs=ESRS)
    if test_msg[0] == new_msg:
        print(f'Тест {i + 1}/{len(test_s_key)} пройден!')


