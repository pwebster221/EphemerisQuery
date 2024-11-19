# ephemeris_query.py

import os
import swisseph as swe

# Set the ephemeris path (update this path to where your ephemeris files are located)
ephemeris_path = os.environ.get('EPHEMERIS_PATH', './ephe/')
swe.set_ephe_path(ephemeris_path)

def calculate_planetary_positions(jd, latitude, longitude):
    """
    Calculates the positions of various celestial bodies and points using the Swiss Ephemeris.

    Parameters:
    - jd (float): Julian Day in Universal Time.
    - latitude (float): Geographic latitude in degrees (positive for North, negative for South).
    - longitude (float): Geographic longitude in degrees (positive for East, negative for West).

    Returns:
    - positions (dict): Dictionary containing positions of celestial bodies and points.
    """

    # Dictionary of celestial bodies with their Swiss Ephemeris IDs
    planets = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mercury': swe.MERCURY,
        'Venus': swe.VENUS,
        'Mars': swe.MARS,
        'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN,
        'Uranus': swe.URANUS,
        'Neptune': swe.NEPTUNE,
        'Pluto': swe.PLUTO,
        'Chiron': 15,              # Chiron's Swiss Ephemeris number
        'Lilith': swe.MEAN_APOG,   # Mean Black Moon Lilith
        'North Node': swe.MEAN_NODE,
        'Ceres': 1,                # Asteroid number for Ceres
        'Pallas': 2,               # Asteroid number for Pallas
        'Juno': 3,                 # Asteroid number for Juno
        'Vesta': 4,                # Asteroid number for Vesta
        # Ascendant, Midheaven, Vertex, Part of Fortune, and South Node will be calculated separately
    }

    # Flags for calculations
    flag = swe.FLG_SWIEPH | swe.FLG_SPEED

    positions = {}

    # Calculate planetary positions
    for name, body in planets.items():
        result = swe.calc_ut(jd, body, flag)
        if result[1] != swe.ERR:
            lon, lat, dist, speed_lon, speed_lat, speed_dist = result[0]
            positions[name] = {
                'longitude': lon % 360,
                'latitude': lat,
                'distance': dist,
                'speed_longitude': speed_lon,
                'speed_latitude': speed_lat,
                'speed_distance': speed_dist
            }
        else:
            positions[name] = {'error': result[0]}

    # Calculate house cusps and key points
    # Ensure longitude is in the correct format for swe.houses (East positive)
    geo_longitude = -longitude  # Convert to East-positive longitude if necessary

    # Calculate houses to get Ascendant, Midheaven, Vertex
    # 'P' indicates the Placidus house system
    cusps, ascmc = swe.houses(jd, latitude, geo_longitude, b'P')

    # Ascendant
    positions['Ascendant'] = {
        'longitude': ascmc[swe.SE_ASC] % 360,  # ascmc[0]
        'latitude': 0.0,
    }

    # Midheaven (MC)
    positions['Midheaven'] = {
        'longitude': ascmc[swe.SE_MC] % 360,  # ascmc[1]
        'latitude': 0.0,
    }

    # Vertex
    positions['Vertex'] = {
        'longitude': ascmc[swe.SE_VERTEX] % 360,  # ascmc[3]
        'latitude': 0.0,
    }

    # Calculate the South Node (directly opposite the North Node)
    if 'North Node' in positions and 'longitude' in positions['North Node']:
        north_node_lon = positions['North Node']['longitude']
        south_node_lon = (north_node_lon + 180) % 360
        positions['South Node'] = {
            'longitude': south_node_lon,
            'latitude': -positions['North Node']['latitude'],  # Opposite latitude
        }

    # Calculate Part of Fortune
    # Get obliquity of the ecliptic
    ecl_nut = swe.calc(jd, swe.ECL_NUT)
    eps = ecl_nut[0][0]  # Obliquity of the ecliptic

    # Check if the chart is diurnal (Sun above the horizon)
    sun_altitude = swe.houses(jd, latitude, geo_longitude, b'P', [positions['Sun']['longitude'], positions['Sun']['latitude']])[2]
    is_diurnal = sun_altitude > 0

    # Calculate Part of Fortune based on diurnal or nocturnal chart
    if is_diurnal:
        # Diurnal formula
        pof = (positions['Ascendant']['longitude'] + positions['Moon']['longitude'] - positions['Sun']['longitude']) % 360
    else:
        # Nocturnal formula
        pof = (positions['Ascendant']['longitude'] + positions['Sun']['longitude'] - positions['Moon']['longitude']) % 360

    positions['Part of Fortune'] = {
        'longitude': pof,
        'latitude': 0.0,
    }

    return positions