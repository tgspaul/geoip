# GeoIP
# Показывает принадлежность IP-адреса к стране, региону, городу
# использование: python geoip.py api-key [ip] - покажет геоинфо по этому IP-адресу,
#                если IP-адрес не указан, то определит собственный IP и покажет геоинфо по нему

import requests
import sys

CHECK_IP = 'check'  # строка 'check' или IP-адрес, например, '134.201.250.155'

if __name__ == '__main__':

    # API-ключ для доступа к ipstack.com, можно указать ниже, можно в файле api.key
    YOUR_ACCESS_KEY = ''
    if not YOUR_ACCESS_KEY:
        try:
            with open('api.key', 'r') as f:
                YOUR_ACCESS_KEY = f.readline()
        except (FileExistsError, FileNotFoundError):
            print('API-key not found...')

    if len(sys.argv) > 1:
        CHECK_IP = sys.argv[1]

    # получаем ответ от сайта в виде JSON-словаря {'ключ':'значение'}
    response = requests.get(f'http://api.ipstack.com/{CHECK_IP}?access_key={YOUR_ACCESS_KEY}').json()

    # список выходных данных
    res = []

    try:
        # перебираем все ключи
        for i in response:

            # значение, соответствующее этому ключу
            r = response['country_name']
            # если это нужный нам ключ и значение по этому ключу не пустое (бывает None)
            if i == 'country_name' and r:
                # то добавляем значение в список выходных данных
                res.append(r)

            r = response['region_name']
            if i == 'region_name' and r:
                res.append(r)

            r = response['city']
            if i == 'city' and r:
                res.append(r)

            # если IP не задан, добавляем его в список выходных данных
            if CHECK_IP == 'check':
                r = response['ip']
                if i == 'ip' and r:
                    res.append(r)

    except KeyError:
        print('Response error...')

    # выводим список выходных данных в виде строки с запятыми
    print(', '.join(res))
