# group_2_util.py
import time
import random
from group_2_data_generator import DataGenerator

start_id = 111

#generator for each sensor
generator_temp = DataGenerator(data_range=(-10, 40), pattern="sine", mean=15, std_dev=5)
generator_humidity = DataGenerator(data_range=(20, 100), pattern="random", mean=60, std_dev=10)
generator_wind = DataGenerator(data_range=(0, 50), pattern="random", mean=20, std_dev=10)
generator_pressure = DataGenerator(data_range=(980, 1050), pattern="gaussian", mean=1015, std_dev=5)
generator_aqi = DataGenerator(data_range=(0, 200), pattern="random", mean=50, std_dev=20)

locations = ['Toronto', 'Vancouver', 'Ottawa', 'Calgary']
conditions = ['Sunny', 'Cloudy', 'Rainy', 'Partly Cloudy', 'Thunderstorm', 'Snowy']
wind_directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

#Create data
def create_data():
    global start_id
    data = {
        'id': start_id,
        'location': random.choice(locations),
        'time': time.asctime(),
        'temperature': round(generator_temp.value, 1),
        'humidity': round(generator_humidity.value, 1),
        'wind': {
            'speed': round(generator_wind.value, 1),
            'direction': random.choice(wind_directions)
        },
        'pressure': round(generator_pressure.value, 1),
        'air_quality_index': int(generator_aqi.value),
        'condition': random.choice(conditions)
    }
    start_id += 1
    return data

def print_data(data):
    print("\n Weather Data Received:")
    print(f" Location: {data['location']} (ID: {data['id']})")
    print(f" Time: {data['time']}")
    print(f"️ Temperature: {data['temperature']} °C")
    print(f" Humidity: {data['humidity']} %")
    print(f"️ Wind: {data['wind']['speed']} km/h {data['wind']['direction']}")
    print(f" Pressure: {data['pressure']} hPa")
    print(f" Air Quality Index: {data['air_quality_index']}")
    print(f"️ Condition: {data['condition']}")


if __name__ == "__main__":
    data = create_data()
    print_data(data)