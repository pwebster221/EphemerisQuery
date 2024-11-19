# post_processing.py
import csv
import os

def save_to_csv(data, filename='natal_chart.csv'):
    headers = [
        'NatalChartID', 'User', 'Birth Year', 'Birth Month', 'Birth Day',
        'Location', 'Birth location', 'Sun Placement', 'Moon Placement',
        'Mercury Placement', 'Venus Placement', 'Mars Placement', 'Jupiter Placement',
        'Saturn Placement', 'Uranus Placement', 'Neptune Placement', 'Pluto Placement',
        'Chiron Placement', 'Lilith Placement', 'Pallas Placement', 'Ceres Placement',
        'Juno Placement', 'Vesta Placement', 'Ascendant Placement', 'Midheaven Placement',
        'North Node Placement', 'South Node Placement', 'Vertex Placement', 'Part of Fortune Placement'
    ]

    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)