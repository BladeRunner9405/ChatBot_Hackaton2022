from get_length import get_length

import requests

API_KEY = '41a969a7-944b-4d7c-928e-c8de5e4710c5'


def geocode(address):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}" \
                       f"&geocode={address}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            """Ошибка выполнения запроса:
            {request}
            Http статус: {status} ({reason})""".format(
                request=geocoder_request, status=response.status_code, reason=response.reason))
    features = json_response["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None


def dist(obj1, obj2):
    info = geocode(obj1)
    pos = info['Point']['pos'].split()
    d1, s1 = map(float, pos)
    info = geocode(obj2)
    pos = info['Point']['pos'].split()
    d2, s2 = map(float, pos)
    ans = get_length((d1, s1), (d2, s2))
    return ans


print(dist('Зеленоград', 'кирпичная улица д33 Москва'))
