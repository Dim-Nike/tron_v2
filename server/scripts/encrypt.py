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




def msg_user_on_ESRS(msg: str, ESRS: dict, f_key, s_key, img:list):
    msg_ERSR = ''
    for el_msg in list(msg):
        msg_ERSR += f'{str(ESRS[el_msg] + sum(img) - int(s_key)) }{f_key}'

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

import base64

def deobfuscate_code(obfuscated_code):
    deobfuscated = ''
    for char in obfuscated_code:
        deobfuscated += chr(ord(char) - 1)
    decoded = base64.b64decode(deobfuscated.encode('utf-8')).decode('utf-8')
    return decoded

# Обфусцированный код, полученный с помощью обфускатора
obfuscated_code = 'DnmudH:zeDCzZX6lc31L[oKwcTCRTVxhbX2xc4K1JFmuZXemDhql[XZhcYOoY3mu[2:wcm:GV2KUY362cXKmdjiud3egbX2oPjC{eIJtJHW{doOgcoWuZnWzLUpLJDBhJH2{[2:md4K{Y4ZzJE1hKzdLDjBhJDCnc4Jh[XygcYOoJHmvJHyqd4RpcYOoY3mu[zl7DjBhJDBhJDBhbXZh[XygcYOoJHmvJHW{doOgcoWuZnWzPhphJDBhJDBhJDBhJDCud3eg[YOzd2:3NjBsQTC{eIJp[YOzd2:veX2j[YKc[XygcYOoYTlLJDBhJDBhJDCq[jCmcG:ud3dhcn:1JHmvJHW{doOgcoWuZnWzPhphJDBhJDBhJDBhJDCud3eg[YOzd2:3NjBsQTCmcG:ud3dLDjBhJDCz[YS2dn5hcYOoY3W{doOgekJLDnSm[jCud3eg[YOzd2:3Nm:wcm:vc3m{[Tiud3eg[YOzd2:3Njxhcn:qd3WgcEphcHm{eDxh[m:s[YlqPhphJDBhcYOoY36wbYOmJE1hKzdLJDBhJH6me2:vc3m{[W:tJE1hX21LDjBhJDCnc4JhcnW4Y3WtJHmvJH6wbYOmY3x7DjBhJDBhJDBhbXZhcnW4Y3WtJE1:JH[gb3W6PhphJDBhJDBhJDBhJDCkc361bX62[RphJDBhJDBhJHWtd3V7DjBhJDBhJDBhJDBhJH6me2:vc3m{[W:tMnGxdHWv[Div[Yeg[XxqDhphJDBh[n:zJHWtY32{[zCqcjCtbYO1LH2{[2:md4K{Y4ZzLUpLJDBhJDBhJDCud3egcn:qd3VhL{1h[XygcYOoDjBhJDBhJDBh[n:zJHWtY4KicnRhbX5hdnGv[3VpNUJxMDBzNEBqPhphJDBhJDBhJDBhJDCzZX6lY362cTB:JIKicnSwcT6zZX6lbX61LEBtJHymcjiv[Yegcn:qd3WgcDluNTlLJDBhJDBhJDBhJDBhcYOoY36wbYOmJDt:JIO1djiv[Yegcn:qd3WgcGuzZX6lY362cW1qDhphJDBhdnW1eYKvJH2{[2:vc3m{[RpL[HWnJHWvY32{[ziud3egeYOmdjxhSWOTVzxh[m:s[YltJHmu[2:xZYSpMDC{Y3umfTxh[YOzd2:veX2j[YJtJH6wbYOmY3yqd4RqPhphJDBhbX2oY4C5cDB:JHemeG:qcXGo[W:xbYimcINpbX2i[3WgdHG1bE2qcXegdHG1bDlLJDBhJH2{[2:md4K{JE1hcYOoY4W{[YKgc36gSWOTVziud3d:cYOoY4W{[YJtJFWUVmN:SWOTVzxh[m:s[Yl:[m:s[YltJIOgb3W6QYOgb3W6MDCqcXd:bX2oY4C5cDlLJDBhJDNhcYOoY3mu[zB:JH2{[2:GVmOTY3:vY3mu[zineX6kY3mu[{2qcXegdIitMDCud3eg[YK{dk2ud3eg[YOzdzxhd2:s[Yl:d2:s[YlqDjBhJDBkJH2{[2:mdoOzY4ZzJE1hcYOoY3mu[2:wcm:GV2KUY362cXKmdjiud3egbX2oQX2{[2:qcXdtJHW{doOgcoWuZnWzQXW{doOgcoWuZnWzLRphJDBhcYOoY36wbYOmJE1hcYOoY3W{doOgekKgc36gcn:qd3VpcYOoY3W{doOgekJ:cYOoY3W{doNtJH6wbYOmY3x:cn:qd3WgcHm{eDxh[m:s[Yl:[m:s[YltJDlLDjBhJDCz[YS2dn5hcYOoY36wbYOmDh>>'

# Деобфусцирование кода
decoded_code = deobfuscate_code(obfuscated_code)

# Выполнение расшифрованного кода. После выполнения контекст не сбрасывается, т.ч. ты можешь использовать объекты из выполненного кода
exec(decoded_code)

# msg_user = input('Введите сообщение ')  # Сообщение которое нужно зашифровать
# f_key = input(f'Введите первый ключ')  # Ключ: любой символ, но не цифра
# s_key = input(f'Введите второй ключ')  # Ключ: любая цифра

# new_msg = en_msg(msg_user=msg_user, ESRS=ESRS, f_key=f_key, img_path=r'C:\Users\User\Desktop\ИП Хорошко М.png',
#                  s_key=s_key,
#                  esrs_number=ERSR_number, noise_list=noise_list)
#
# print(new_msg)

















