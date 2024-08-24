import random
from PIL import Image


noise_list = [' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '/', ':', ';', '<', '=', '>',
              '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
              'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f',
              'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
              '{', '|', '}', '~', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О',
              'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в',
              'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х',
              'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

ESRS = {' ': 729145, '!': 492464, '"': 951240, '#': 769264, '$': 375016, '%': 831990, '&': 281732,
        "'": 469678, '(': 309681, ')': 817659, '*': 155000, '+': 887631, ',': 121102, '-': 741111, '.': 666680,
        '/': 930891, '0': 341614, '1': 165711, '2': 480379, '3': 249053, '4': 401701, '5': 409126, '6': 707314,
        '7': 850200, '8': 161221, '9': 430417, ':': 810728, ';': 227110, '<': 377540, '=': 544206, '>': 591071,
        '?': 617941, '@': 705629, 'A': 577319, 'B': 981940, 'C': 475455, 'D': 475443, 'E': 972526, 'F': 961893,
        'G': 177951, 'H': 822829, 'I': 664200, 'J': 766557, 'K': 739121, 'L': 554060, 'M': 542642, 'N': 828076,
        'O': 249875, 'P': 732751, 'Q': 616966, 'R': 587566, 'S': 233904, 'T': 435612, 'U': 949529, 'V': 195930,
        'W': 964140, 'X': 981643, 'Y': 473643, 'Z': 419075, 'a': 524826, 'b': 822045, 'c': 209820, 'd': 771398,
        'e': 124553, 'f': 213169, 'g': 484267, 'h': 597938, 'i': 579076, 'j': 945663, 'k': 209953, 'l': 741171,
        'm': 399989, 'n': 395150, 'o': 316146, 'p': 196056, 'q': 764334, 'r': 185816, 's': 168754, 't': 615299,
        'u': 372816, 'v': 783680, 'w': 987137, 'x': 576352, 'y': 957051, 'z': 670710, '{': 684090, '|': 773771,
        '}': 391310, '~': 923228, 'А': 509194, 'Б': 535418, 'В': 785359, 'Г': 502683, 'Д': 803404, 'Е': 356401,
        'Ж': 389182, 'З': 527579, 'И': 492061, 'Й': 270699, 'К': 245802, 'Л': 216972, 'М': 403942, 'Н': 244133,
        'О': 815087, 'П': 915499, 'Р': 142838, 'С': 330529, 'Т': 155231, 'У': 709442, 'Ф': 330180, 'Х': 776471,
        'Ц': 162397, 'Ч': 487656, 'Ш': 763687, 'Щ': 771561, 'Ъ': 847038, 'Ы': 673364, 'Ь': 787586, 'Э': 219275,
        'Ю': 755313, 'Я': 125314, 'а': 591912, 'б': 510694, 'в': 498119, 'г': 218796, 'д': 851705, 'е': 828474,
        'ж': 968599, 'з': 213840, 'и': 355141, 'й': 691332, 'к': 393060, 'л': 636838, 'м': 432096, 'н': 294887,
        'о': 972132, 'п': 850931, 'р': 266583, 'с': 521888, 'т': 545544, 'у': 791214, 'ф': 218927, 'х': 675963,
        'ц': 233330, 'ч': 136142, 'ш': 633886, 'щ': 155411, 'ъ': 992709, 'ы': 795362, 'ь': 645359, 'э': 133053,
        'ю': 662095, 'я': 334814, '^': 776645, '_': 832668, '[': 356023, ']': 225508, '\\': 897782}

ERSR_number = {'0': 572740, '1': 450670, '2': 753051, '3': 353144, '4': 195655, '5': 880697, '6': 440939, '7': 549976, '8': 650593, '9': 418544}


def get_image_pixels(image_path):
    img_sum_pxl_img_l = []
    image = Image.open(image_path)  # Открываем изображение
    pixels = list(image.getdata())  # Получаем пиксели изображения в виде списка
    for el_pxl in pixels:
        img_sum_pxl_img_l.append(sum(el_pxl))
    return img_sum_pxl_img_l


def re_noise_msg(msg_en: str, f_key: str, noise_l: list):
    new_noise_l = []
    re_noise_msg_user = ''

    for new_el in list(noise_l):
        if new_el == f_key:
            continue
        else:
            new_noise_l.append(new_el)

    for el_msg in msg_en:
        if el_msg in new_noise_l:
            continue
        else:
            re_noise_msg_user += el_msg

    return re_noise_msg_user


# def re_msg_img(func_img: list, user_msg:list, s_key:str):
#     new_msg = ''
#     key_img = 0
#
#     if int(s_key) % 2 == 0:
#         key_img += sum(func_img) + int(s_key)
#     else:
#         key_img += sum(func_img) - int(s_key)
#
#     for el_msg in user_msg:
#         if ''.join(el_msg).isdigit():
#             new_msg += str(int(''.join(el_msg)) - key_img)
#         else:
#             new_msg += ''.join(el_msg)
#
#     return new_msg


def re_esrs_v2_msg(re_noise_msg_user:str, esrs_number:dict, f_key:str, img_pxl, s_key:str, esrs: dict):
    edit_re_noise_msg_user = re_noise_msg_user+f_key
    main_check_msg_ersr_l = []
    check_msg_ersr_l = []
    check_msg_ersr = ''
    check_msg_l = []
    check_msg = ''

    for el_msg in list(edit_re_noise_msg_user):
        if el_msg.isdigit():
            check_msg += el_msg
        else:
            check_msg_l.append(check_msg)
            check_msg = ''

    for i, el_esrs_number in enumerate(check_msg_l):
        if i != 0:
            main_check_msg_ersr_l.append(check_msg_ersr_l)
            check_msg_ersr_l.append(check_msg_ersr)
            check_msg_ersr = ''
            check_msg_ersr_l = []
        for i, el in enumerate(list(el_esrs_number)):
            if i % 6 == 0 and i != 0:
                check_msg_ersr_l.append(check_msg_ersr)
                check_msg_ersr = el
            else:
                check_msg_ersr += el
    check_msg_ersr_l.append(check_msg_ersr)
    main_check_msg_ersr_l.append(check_msg_ersr_l)
    main_esrs_not_img = []
    main_intermediate = []
    esrs_l = []
    msg_user = ''
    key_img = 0

    for check_ersr in main_check_msg_ersr_l:
        esrs_not_img = []  # Создаем пустой список для текущего подмассива
        for el in check_ersr:
            if el.isdigit():
                if int(el) in esrs_number.values():
                    key = next(key for key, value in esrs_number.items() if value == int(el))
                    esrs_not_img.append(key)
        main_esrs_not_img.append(esrs_not_img)  # Добавляем текущий подмассив в общий список

    for el in main_esrs_not_img:
        main_intermediate.append([el[i:i+int(len(str(sum(img_pxl))))] for i in range(0, len(el), 10)])

    if int(s_key) % 2 == 0:
        key_img += sum(img_pxl) + int(s_key)
    else:
        key_img += sum(img_pxl) - int(s_key)

    for intermediate in main_intermediate:
        el_esrs_l = []
        for el_inter_1 in intermediate:
            el_esrs_l.append(int(''.join(el_inter_1))-key_img)
        esrs_l.append(''.join(map(str, el_esrs_l)))

    for msg in esrs_l:
        for el in msg:
            if el.isdigit():
                print('Шифрование символов')
                if int(msg) in esrs.values():
                    msg_world = next(key for key, value in esrs.items() if value == int(msg))
                    print(f'Расшифрованный символ - {msg_world}')
                    msg_user += msg_world

    return esrs_l


msg_en = input('Введите сообщение ')
f_key = input('Введите первый ключ(буква) ')
s_key = input('Введите второй ключ(цифра) ')
img_path=r'C:\Users\User\Desktop\ИП Хорошко М.png'
#
#
#
#
def de_msg(msg_en, f_key, s_key, noise_l, image_patch, esrs_number, esrs):
    de_noise = re_noise_msg(msg_en=msg_en, f_key=f_key, noise_l=noise_l)
    img_pxl = get_image_pixels(image_path=image_patch)
    de_esrs_v2_msg = re_esrs_v2_msg(re_noise_msg_user=de_noise, esrs_number=esrs_number, f_key=f_key, img_pxl=img_pxl,
                                    s_key=s_key, esrs=esrs)

    return de_esrs_v2_msg


print(de_msg(msg_en=msg_en, f_key=f_key, s_key=s_key, noise_l=noise_list, image_patch=img_path, esrs_number=ERSR_number,
             esrs=ESRS))











