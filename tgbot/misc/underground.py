import requests
from tgbot.misc.geo import calc_distance

cities_coords = {
    'moscow': (55.7522, 37.6156),
    'saint_petersburg': (59.9386, 30.3141),
    'ekaterinburg': (56.8519, 60.6122),
    'novosibirsk': (55.0415, 82.9346)
}

cities = {
    'moscow': 1,
    'saint_petersburg': 2,
    'ekaterinburg': 3,
    'novosibirsk': 4
}


def find_nearest_city(coords):
    distances = {city: calc_distance(coords, cities_coords[city]) for city in cities_coords.keys()}
    for city in distances.keys():
        if distances[city] <= 50:
            return city


def find_nearest_underground(coords):
    city = find_nearest_city(coords)
    if city is not None:
        city_code = cities[city]

        response = requests.get(f'https://api.hh.ru/metro/{city_code}')
        info = response.json()

        station_distances = []
        for line in info['lines']:
            for station in line['stations']:
                dist = calc_distance(coords, (station['lat'], station['lng']))
                station_distances.append((station['name'], dist))

        station_name, distance = min(station_distances, key=lambda x: x[1])
        return station_name, distance

    return None, None