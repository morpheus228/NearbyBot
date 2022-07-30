from geopy.distance import geodesic as GD


def calc_distance(first_coords, second_coords):
    return GD(first_coords, second_coords).km
