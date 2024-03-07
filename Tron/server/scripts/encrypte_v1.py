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

ERSR_number = {'0': 572740, '1': 450670, '2': 753051, '3': 353144, '4': 195655, '5': 880697, '6': 440939, '7': 549976,
               '8': 650593, '9': 418544}



def get_image_pixels(image_path):
    img_sum_pxl_img_l = []
    image = Image.open(image_path)  # Открываем изображение
    pixels = list(image.getdata())  # Получаем пиксели изображения в виде списка
    for el_pxl in pixels:
        img_sum_pxl_img_l.append(sum(el_pxl))
    return img_sum_pxl_img_l


def create_ESRS_dict():
    esrs = {}
    key_list = set()

    all_symbols = [chr(i) for i in range(32, 127) if i not in [91, 92, 93, 94, 95, 96]]
    all_symbols += [chr(i) for i in range(1040, 1104) if i not in [1104, 1025, 1105]]
    all_symbols += [str(i) for i in range(10)]
    all_symbols += ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}', '[', ']', ';', ':',
                    '<', '>', '.', ',', '/', '?', '|', '\\', '~']

    for el_symbol in all_symbols:
        new_key = random.randint(100000, 999999)
        while new_key in key_list:
            new_key = random.randint(100000, 999999)
        key_list.add(new_key)
        esrs[el_symbol] = new_key
    return esrs


def create_ERSR_number():
    key_list = set()
    ersr_number_dict = {}
    ersr_number = [str(i) for i in range(10)]
    for el_symbol in ersr_number:
        new_key = random.randint(100000, 999999)
        while new_key in key_list:
            new_key = random.randint(100000, 999999)
        key_list.add(new_key)
        ersr_number_dict[el_symbol] = new_key
    return ersr_number


def msg_user_on_ESRS(msg: str, ESRS: dict, f_key):
    msg_ERSR = ''

    for el_msg in list(msg):
        msg_ERSR += f'{str(ESRS[el_msg])}{f_key}'

    return msg_ERSR


def msg_ERSR_on_img(func_img: list, msg_ersr: str, s_key: str):
    msg_user_l = list(msg_ersr)
    msg_img = ''
    key_img = 0

    if int(s_key) % 2 == 0:
        key_img += sum(func_img) + int(s_key)
    else:
        key_img += sum(func_img) - int(s_key)

    for el_msg in msg_user_l:
        if el_msg.isdigit():
            msg_img += str(int(el_msg) + key_img)
        else:
            msg_img += el_msg

    return msg_img


def msg_img_on_ESRS_number(msg_img: str, esrs_number):
    msg_esrs_v2 = ''

    for el_msg in list(msg_img):
        if el_msg in esrs_number:
            msg_esrs_v2 += str(esrs_number[el_msg])
        if el_msg not in esrs_number:
            msg_esrs_v2 += el_msg

    return msg_esrs_v2


def msg_esrs_v2_on_noise(msg_esrs_v2, noise_l: list, f_key):
    msg_noise = ''
    new_noise_l = []

    for new_el in noise_l:
        if new_el == f_key:
            continue
        else:
            new_noise_l.append(new_el)

    for el_msg in list(msg_esrs_v2):
        msg_noise += el_msg
        for el_rand in range(1, 2):
            rand_num = random.randint(0, len(new_noise_l)-1)
            msg_noise += str(new_noise_l[rand_num])

    return msg_noise


# msg_user = input('Введите сообщение ')  # Сообщение которое нужно зашифровать
# f_key = input(f'Введите первый ключ')  # Ключ: любой символ, но не цифра
# s_key = input(f'Введите второй ключ')  # Ключ: любая цифра
# #
# #
def en_msg(msg_user, ESRS, f_key, img_path, s_key, esrs_number, noise_list):
    msg_esrs = msg_user_on_ESRS(msg=msg_user, ESRS=ESRS, f_key=f_key)
    img_pxl = get_image_pixels(image_path=img_path)
    msg_img = msg_ERSR_on_img(func_img=img_pxl, msg_ersr=msg_esrs, s_key=s_key)
    msg_ersr_v2 = msg_img_on_ESRS_number(msg_img=msg_img, esrs_number=esrs_number)
    msg_noise = msg_esrs_v2_on_noise(msg_esrs_v2=msg_ersr_v2, noise_l=noise_list, f_key=f_key)

    return msg_noise
# #
# #
# new_msg = en_msg(msg_user=msg_user, ESRS=ESRS, f_key=f_key, img_path='/home/trigger/Рабочий стол/КБССК.png', s_key=s_key,
#                  esrs_number=ERSR_number, noise_list=noise_list)

# print(new_msg)



