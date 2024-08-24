from time import sleep

import requests

idf = 'NIVHEBNBOJERNHVIBEURBVIERUBVIERNBIUERNB'
idf_2 = 'IUGVRB9GVUH408GH349H2049HG09HEVWON'
idf_3 = '3CWE24CWE3FWWE12NVIJERBV98HF9032H409H304FH4320H'


def auth_flesh():
    try:
        response = requests.post('http://localhost:8000/auth_flesh', json={'code': '1234', 'idf': idf})
        if response.status_code == 200:
            print(f'Успешная авторизация! Статус: {response.status_code}')
            print(response.json()['idf_user'])
        elif response.status_code == 404:
            print(f'Не найден объект IDF! Код ошибки {response.status_code}')
        else:
            print(f'Ошибка авторизации! Код ошибки {response.status_code}')
    except requests.exceptions.HTTPError as errh:
        print("Http ошибка:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Ошибка подключения:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout ошибка:", errt)
    except requests.exceptions.RequestException as err:
        print("Ошибка подключения:", err)


def write_idf_key(idf_key):
    try:
        response = requests.post('http://localhost:8000/write_key_idf', json={'code': '1234', 'idf': idf_key})
        if response.status_code == 201:
            print(f'Успешное принятие ключей! Статус: {response.status_code}')
            if response.json()['idf_user']['save_local']:
                with open('keys.txt', 'w') as fw:
                    fw.write(f'{response.json()["idf_user"]["token_dialog"]}\n')
                    fw.write(f'{response.json()["idf_user"]["f_key"]}\n')
                    fw.write(f'{response.json()["idf_user"]["s_key"]}\n')
                    fw.write(f'{response.json()["idf_user"]["img_patch"]}\n')
                    fw.close()
                    with open('keys.txt', 'r') as fr:
                        lines = fr.readlines()
            else:
                print(f'Ошибка записи ключей! Повторите попытку еще раз!')
        elif response.status_code == 404:
            print(f'Не найден объект IDF! Код ошибки {response.status_code}')
        elif response.status_code == 402:
            print(f'Ошибка авторизации! Код ошибки {response.status_code}')
        elif response.status_code == 405:
            print(f'Чат сервер не авторизован пользователем! Код ошибки {response.status_code}')
        else:
            print(f'Ошибка подключения! Код ошибки {response.status_code}')
    except requests.exceptions.HTTPError as errh:
        print("Http ошибка:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Ошибка подключения:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout ошибка:", errt)
    except requests.exceptions.RequestException as err:
        print("Ошибка подключения:", err)


def del_idf_connect(idf_key):
    try:
        response = requests.post('http://localhost:8000/del_idf_connect', json={'code': '1234', 'idf': idf_key})
        if response.status_code == 203:
            print(f'{response.json()["message"]}! Статус: {response.status_code}')
        elif response.status_code == 409:
            print(f"{response.json()['message']} Статус: {response.status_code}")
        elif response.status_code == 404:
            print(f'Не найден объект IDF! Код ошибки {response.status_code}')
        elif response.status_code == 402:
            print(f'Ошибка авторизации! Код ошибки {response.status_code}')
        elif response.status_code == 405:
            print(f'Чат сервер не авторизован пользователем! Код ошибки {response.status_code}')
        else:
            print(f'Ошибка подключения! Код ошибки {response.status_code}')
    except requests.exceptions.HTTPError as errh:
        print("Http ошибка:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Ошибка подключения:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout ошибка:", errt)
    except requests.exceptions.RequestException as err:
        print("Ошибка подключения:", err)


def online_connection_idf(idf_key):
    try:
        response = requests.post('http://localhost:8000/online_connection_idf', json={'code': '1234', 'idf': idf_key,
                                                                                      'key_idf': None})
        if response.status_code == 201 or response.status_code == 200:
            print(f'{response.json()["message"]}! Статус: {response.status_code}')
            sleep(3)
            while True:
                if response.status_code == 201 or response.status_code == 200:
                    with open('keys.txt', 'r') as fr:
                        f_key = fr.readlines()
                        if len(f_key) >= 2:  # проверяем, что в файле есть хотя бы две строки
                            pass  # печатаем вторую строку
                        else:
                            return "Обнаружен неваллидный файл! Повторите операцию записи ключей еще раз!"
                    response = requests.post('http://localhost:8000/online_connection_idf',
                                             json={'code': '1234', 'idf': idf_key,
                                                   'key_idf': {
                                                       'f_key': f_key[1],
                                                       's_key': f_key[2],
                                                       'img_patch': f_key[3]
                                                   }})
                    print(f'{response.json()["message"]}! Статус: {response.status_code}')
                else:
                    print(f'Непредвиденная ошибка подключения! Повторите подключение')
                    return
        elif response.status_code == 409:
            print(f"{response.json()['message']} Статус: {response.status_code}")
        elif response.status_code == 404:
            print(f'Не найден объект IDF! Код ошибки {response.status_code}')
        elif response.status_code == 402:
            print(f'Ошибка авторизации! Код ошибки {response.status_code}')
        elif response.status_code == 407:
            print(f'{response.json()["message"]} Код ошибки {response.status_code}')
        elif response.status_code == 405:
            print(f'{response.json()["message"]} Код ошибки {response.status_code}')
        else:
            print(f'Ошибка подключения! Код ошибки {response.status_code}')
    except requests.exceptions.HTTPError as errh:
        print("Http ошибка:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Ошибка подключения:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout ошибка:", errt)
    except requests.exceptions.RequestException as err:
        print("Ошибка подключения:", err)


# auth_flesh(idf_key)
#write_idf_key(idf_key=idf_3)
#del_idf_connect(idf_key=idf_2)
online_connection_idf(idf_key=idf_3)
