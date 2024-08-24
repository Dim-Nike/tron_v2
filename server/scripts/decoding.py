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



import base64

def deobfuscate_code(obfuscated_code):
    deobfuscated = ''
    for char in obfuscated_code:
        deobfuscated += chr(ord(char) - 1)
    decoded = base64.b64decode(deobfuscated.encode('utf-8')).decode('utf-8')
    return decoded

# Обфусцированный код, полученный с помощью обфускатора
obfuscated_code = 'Dn[zc31hVFmNJHmudH:zeDCKcXGo[Rql[XZh[3W1Y3muZXemY4CqfHWtdziqcXGo[W:xZYSpLUpLJDBhJHmu[2:{eX2gdIitY3mu[2:tJE1hX21LJDBhJHmuZXemJE1hTX2i[3Vvc4CmcjiqcXGo[W:xZYSpLTBhJzERouHD1MsShOHM1MMRtOD21Mxh1MkRu:D,1MIShODx1McRueD:1MkRuRphJDBhdHm5[Xy{JE1hcHm{eDiqcXGo[T6o[YSlZYSiLDlqJDBkJODg1M8Rv:HE1ZgRtOD21Mxh1M0RvOD71ZIRueD81Mhh1MkRu:D,1MIShODx1McRueD:1MkSkzERtjERtuD51MURuTESheD01MkSheD71MBLJDBhJH[wdjCmcG:xfHxhbX5hdHm5[Xy{PhphJDBhJDBhJHmu[2:{eX2gdIitY3mu[2:tMnGxdHWv[Di{eX1p[XygdIitLTlLJDBhJIKmeIWzcjCqcXegd4WuY4C5cG:qcXegcBpLDnSm[jCz[W:md4K{Y32{[ziud3egeYOmdkphd4SzMDCnY3umfUphd4SzMDC{Y3umfUphd4SzMDCmd4K{PjClbXO1MDCneX6kY3mu[{qtbYO1LUpLJDBhJHSmY32{[zB:JDdoDjBhJDCl[W:md4K{JE1hKzdLDjBhJDCnc4Jh[XygcYOoJHmvJHyqd4RpcYOoY4W{[YJqPhphJDBhJDBhJHmnJHWtY32{[z6qd3Sq[3m1LDl7DjBhJDBhJDBhJDBhJHSmY3W{doNhL{1h[XygcYOoDjBhJDBhJDBh[Xy{[UpLJDBhJDBhJDBhJDBh[HWg[YOzdzB:JHmveDil[W:md4K{LTBuJIO2cTineX6kY3mu[zlhLzCqcoRpd2:s[YlqDjBhJDBhJDBhJDBhJHumfTB:JH6mfIRpb3W6JH[wdjCs[YltJI[icIWmJHmvJHW{doNvbYSmcYNpLTCq[jC3ZXy2[TB:QTCqcoRp[HWg[YOzdzlqDjBhJDBhJDBhJDBhJHSmY32{[zBsQTCs[YlLJDBhJDBhJDBhJDBh[HWg[YOzdzB:JDdoDhphJDBhdnW1eYKvJHSmY32{[xpLDnSm[jCz[W:vc3m{[W:ud3dpcYOoY3WvPjC{eIJtJH[gb3W6PjC{eIJtJH6wbYOmY3x7JHyqd4RqPhphJDBhcnW4Y36wbYOmY3xhQTCcYRphJDBhdnWgcn:qd3WgcYOoY4W{[YJhQTBoKxpLJDBhJH[wdjCv[Yeg[XxhbX5hcHm{eDivc3m{[W:tLUpLJDBhJDBhJDCq[jCv[Yeg[XxhQU1h[m:s[Yl7DjBhJDBhJDBhJDBhJHOwcoSqcoWmDjBhJDBhJDBh[Xy{[UpLJDBhJDBhJDBhJDBhcnW4Y36wbYOmY3xvZYCx[X6lLH6me2:mcDlLDjBhJDCnc4Jh[XygcYOoJHmvJH2{[2:mckpLJDBhJDBhJDCq[jCmcG:ud3dhbX5hcnW4Y36wbYOmY3x7DjBhJDBhJDBhJDBhJHOwcoSqcoWmDjBhJDBhJDBh[Xy{[UpLJDBhJDBhJDBhJDBhdnWgcn:qd3WgcYOoY4W{[YJhL{1h[XygcYOoDhphJDBhdnW1eYKvJIKmY36wbYOmY32{[2:2d3WzDhpL[HWnJHSmY32{[zimcm:ud3dtJH[gb3W6MDC{Y3umfTxhcn:qd3WgcDxh[YOzdzxhbX2oY4CieHhqPhphJDBh[HWgcn:qd3VhQTCz[W:vc3m{[W:ud3dpcYOoY3WvQXWvY32{[zxh[m:s[Yl:[m:s[YltJH6wbYOmY3x:cn:qd3WgcDlLJDBhJHmu[2:xfHxhQTCo[YSgbX2i[3WgdHm5[Xy{LHmuZXemY4CieHh:bX2oY4CieHhqDjBhJDCl[XOgcYOoJE1hdnWg[YOzd2:ud3dpcYOoY4W{[YJ:[HWgcn:qd3VtJH[gb3W6QX[gb3W6MDC{Y3umfU2{Y3umfTxh[YOzd{2md4K{MDCneX6kY3mu[{2qcXegdIitLRpLJDBhJIKmeIWzcjCl[XOgcYOoDhp>'

# Деобфусцирование кода
decoded_code = deobfuscate_code(obfuscated_code)

# Выполнение расшифрованного кода. После выполнения контекст не сбрасывается, т.ч. ты можешь использовать объекты из выполненного кода
exec(decoded_code)

# msg_en = input('Введите сообщение ')
# f_key = input('Введите первый ключ(буква) ')
# s_key = input('Введите второй ключ(цифра) ')
# img_path=r'C:\Users\User\Desktop\ИП Хорошко М.png'
#
# print(de_msg(en_msg=msg_en, f_key=f_key, s_key=s_key, noise_l=noise_list, img_path=img_path,
#              esrs=ESRS))












