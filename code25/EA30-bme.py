import csv
import os
import time
from datetime import datetime
from bme280 import BME280

# Initialize BME280 sensor
bme280 = BME280()

# Define the CSV file name
csv_file = "EA30-bme280_data.csv"

# Check if the file exists, if not, create it with headers
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "temperature_C", "pressure_hPa", "humidity_%"])  # Write headers

def save_to_csv(timestamp, temperature, pressure, humidity):
    """Appends BME280 sensor data to the CSV file."""
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, temperature, pressure, humidity])

# Main loop to collect and save data
try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        temperature = bme280.get_temperature()
        pressure = bme280.get_pressure()
        humidity = bme280.get_humidity()
        
        save_to_csv(timestamp, temperature, pressure, humidity)
        print(f"Data saved: {timestamp}, Temp: {temperature}°C, Pressure: {pressure}hPa, Humidity: {humidity}%")
        
        time.sleep(60)  # Adjust the interval as needed

except KeyboardInterrupt:
    print("Data collection stopped.")
