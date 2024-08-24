from time import sleep
import base64
import requests

idf = '004'
idf_2 = 'f222'
idf_3 = 'f333'
idf_4 = 'f444'
idf_user_1 = '005'
idf_user_2 = 'ry78235823658923523fwef'
idf_user_3 = '578326487235176236478235'


def auth_flesh(idf_key):
    try:
        response = requests.post('http://localhost:8000/auth_flesh', json={'code': '1234', 'idf': idf_key})
        if response.status_code == 200:
            print(f'Успешная авторизация! Статус: {response.status_code}')
            print(response.json()['idf_user'])
        elif response.status_code == 404:
            print(f'Не найден объект IDF! Код ошибки {response.status_code}')
        elif response.status_code == 401:
            print(f"{response.json()['message']} Код ошибки: {response.status_code}")
        elif response.status_code == 405:
            print(f"{response.json()['message']} Код ошибки: {response.status_code}")
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
                with open('keys_2.txt', 'w') as fw:
                    fw.write(f'{response.json()["idf_user"]["token_dialog"]}\n')
                    fw.write(f'{response.json()["idf_user"]["f_key"]}\n')
                    fw.write(f'{response.json()["idf_user"]["s_key"]}\n')
                    fw.write(f'{response.json()["idf_user"]["img_patch"]}\n')
                    fw.close()
                    with open('keys_2.txt', 'r') as fr:
                        lines = fr.readlines()

                # Декодирование строки base64 обратно в изображение и сохранение его
                img_data = base64.b64decode(response.json()['idf_user']['img_patch'])
                with open('img_key_2.jpg', 'wb') as f:
                    f.write(img_data)
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
            while True:
                sleep(int(response.json()['sleep_idf']))
                if response.status_code == 201 or response.status_code == 200:
                    with open('keys.txt', 'r') as fr:
                        read_file = fr.readlines()
                        if len(read_file) >= 2:
                            f_key = read_file[1]
                            s_key = read_file[2]
                            img_patch = read_file[3]
                        else:
                            return "Обнаружен невалидный файл! Повторите операцию записи ключей еще раз!"
                    response = requests.post('http://localhost:8000/online_connection_idf',
                                             json={'code': '1234', 'idf': idf_key,
                                                   'key_idf': {
                                                       'f_key': f_key,
                                                       's_key': s_key,
                                                       'img_patch': img_patch
                                                   }})
                    print(f'{response.json()["message"]} Статус: {response.status_code}')
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

list_active = ['003', '004']

for idf in list_active:
    online_connection_idf(idf_key=idf)


# auth_flesh(idf_key=idf_user_1)
# write_idf_key(idf_key=idf_user_1)
# del_idf_connect(idf_key=idf)
#online_connection_idf(idf_key=idf_2)

