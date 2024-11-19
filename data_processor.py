# data_processor.py
from ephemeris_query import calculate_planetary_positions
from post_processing import save_to_csv
import datetime
import pytz

def process_webhook_data(data):
    try:
        # Extract and validate data
        birth_year = int(data.get('field3'))
        birth_month = int(data.get('field6'))
        birth_day = int(data.get('field7'))
        birth_time_str = data.get('field8')  # e.g., "15:10 EST"
        longitude_str = data.get('field4', {}).get('value', '').strip(' .')
        latitude_str = data.get('field5', {}).get('value', '').strip()

        # Validate presence of necessary fields
        required_fields = [birth_year, birth_month, birth_day, birth_time_str, longitude_str, latitude_str]
        if not all(required_fields):
            return {'error': 'Incomplete data received'}

        # Parse birth time and timezone
        time_parts = birth_time_str.strip().split()
        time_str = time_parts[0]  # e.g., "15:10"
        timezone_str = time_parts[1] if len(time_parts) > 1 else 'UTC'

        try:
            tz = pytz.timezone(timezone_str)
        except pytz.UnknownTimeZoneError:
            return {'error': f'Unknown timezone: {timezone_str}'}

        hour, minute = map(int, time_str.split(':'))

        # Convert local time to UTC
        naive_datetime = datetime.datetime(birth_year, birth_month, birth_day, hour, minute)
        local_datetime = tz.localize(naive_datetime)
        utc_datetime = local_datetime.astimezone(pytz.utc)

        # Calculate Julian Day
        jd = calculate_julian_day(utc_datetime)

        # Process longitude and latitude
        longitude = float(longitude_str)
        latitude = float(latitude_str)

        # Pass data to the ephemeris query module
        planetary_positions = calculate_planetary_positions(jd)

        # Pass results to the post-processing module
        csv_data = prepare_csv_data(data, planetary_positions, birth_year, birth_month, birth_day, longitude, latitude)
        save_to_csv(csv_data)

        return {'message': 'Data processed successfully', 'planetary_positions': planetary_positions}

    except Exception as e:
        return {'error': 'Exception occurred', 'details': str(e)}

def calculate_julian_day(utc_datetime):
    jd = swe.julday(
        utc_datetime.year,
        utc_datetime.month,
        utc_datetime.day,
        utc_datetime.hour + utc_datetime.minute / 60.0 + utc_datetime.second / 3600.0
    )
    return jd

def prepare_csv_data(data, planetary_positions, birth_year, birth_month, birth_day, longitude, latitude):
    csv_data = {
        'NatalChartID': data.get('field1'),
        'User': data.get('User'),  # Update according to your data
        'Birth Year': birth_year,
        'Birth Month': birth_month,
        'Birth Day': birth_day,
        'Location': f"{latitude}, {longitude}",
        'Birth location': data.get('field4', {}).get('location', 'Unknown'),
        'Sun Placement': planetary_positions.get('Sun', {}).get('longitude'),
        'Moon Placement': planetary_positions.get('Moon', {}).get('longitude'),
        'Mercury Placement': planetary_positions.get('Mercury', {}).get('longitude'),
        'Venus Placement': planetary_positions.get('Venus', {}).get('longitude'),
        'Mars Placement': planetary_positions.get('Mars', {}).get('longitude'),
        'Jupiter Placement': planetary_positions.get('Jupiter', {}).get('longitude'),
        'Saturn Placement': planetary_positions.get('Saturn', {}).get('longitude'),
        'Uranus Placement': planetary_positions.get('Uranus', {}).get('longitude'),
        'Neptune Placement': planetary_positions.get('Neptune', {}).get('longitude'),
        'Chiron Placement': planetary_positions.get('Chiron', {}).get('longitude'),
        'Lilith Placement': planetary_positions.get('Lilith', {}).get('longitude'),
        'North Node Placement': planetary_positions.get('North Node', {}).get('longitude'),
        'South Node Placement': planetary_positions.get('South Node', {}).get('longitude'),
        'Ceres Placement': planetary_positions.get('Ceres', {}).get('longitude'),
        'Juno Placement': planetary_positions.get('Juno', {}).get('longitude'),
        'Pallas Placement': planetary_positions.get('Pallas', {}).get('longitude'),
        'Vesta Placement': planetary_positions.get('Vesta', {}).get('longitude'),
        'Vertex Placement': planetary_positions.get('Vertex', {}).get('longitude'),
        'Ascendant Placement': planetary_positions.get('Ascendant', {}).get('longitude'),
        'Midheaven Placement': planetary_positions.get('Midheaven', {}).get('longitude'),
        'Part of Fortune Placement': planetary_positions.get('Part of Fortune', {}).get('longitude'),
        # Add other planetary placements...
    }
    return csv_data