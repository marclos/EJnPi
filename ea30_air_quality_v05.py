#!/usr/bin/env python3
# Deployed 3/1/2025, Updated 1/3/2026
# Customize log file: PiZ[1:15]_ea30_sp25_v1.log (line 35)
# Customize CSV file: PiZ[1:15]_ea30_sp25_v1.csv (line 36)

import colorsys
import csv
import os
import sys
import time
from datetime import datetime

import st7735

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559

import logging

from bme280 import BME280
from fonts.ttf import RobotoMedium as UserFont
from PIL import Image, ImageDraw, ImageFont
from pms5003 import PMS5003
from pms5003 import ReadTimeoutError as pmsReadTimeoutError

from enviroplus import gas

# Configuration
LOG_FILE = "/home/pi/EJnPi/PiZ15_ea30_sp26_v05.log"
CSV_FILE = "/home/pi/EJnPi/PiZ15_ea30_sp26_v05.csv"

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M",
    filename=LOG_FILE,
    filemode="a")

logging.info("""
RPi ZeroW Powered On (systemd service start)!

""")

# CSV Setup - create file with headers if it doesn't exist
CSV_HEADERS = [
    "timestamp", "temperature_C", "pressure_hPa", "humidity_pct",
    "light_lux", "oxidised_kO", "reduced_kO", "nh3_kO",
    "pm1_ug_m3", "pm25_ug_m3", "pm10_ug_m3"
]

def init_csv():
    """Initialize CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADERS)
        logging.info(f"Created new CSV file: {CSV_FILE}")

def write_csv_row(data_dict):
    """Append a row of data to the CSV file."""
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        row = [
            data_dict.get("timestamp", ""),
            f"{data_dict.get('temperature', 0):.2f}",
            f"{data_dict.get('pressure', 0):.2f}",
            f"{data_dict.get('humidity', 0):.2f}",
            f"{data_dict.get('light', 0):.2f}",
            f"{data_dict.get('oxidised', 0):.2f}",
            f"{data_dict.get('reduced', 0):.2f}",
            f"{data_dict.get('nh3', 0):.2f}",
            f"{data_dict.get('pm1', 0):.2f}",
            f"{data_dict.get('pm25', 0):.2f}",
            f"{data_dict.get('pm10', 0):.2f}",
        ]
        writer.writerow(row)

# Initialize CSV
init_csv()

# BME280 temperature/pressure/humidity sensor
bme280 = BME280()

# PMS5003 particulate sensor
pms5003 = PMS5003()

# Create ST7735 LCD display class
st7735 = st7735.ST7735(
    port=0,
    cs=1,
    dc="GPIO9",
    backlight="GPIO12",
    rotation=270,
    spi_speed_hz=10000000)

# Initialize display
st7735.begin()

WIDTH = st7735.width
HEIGHT = st7735.height

# Set up canvas and fonts
img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font_large = ImageFont.truetype(UserFont, 20)
font_medium = ImageFont.truetype(UserFont, 16)
font_small = ImageFont.truetype(UserFont, 14)

# Define output format
def logging_text(variable, data, unit):
    output = f"{variable[:4]}: {data:.1f} {unit}"
    logging.info(output)

# Display time and PM values on the 0.96" LCD
def display_pm_readings(pm1, pm25, pm10):
    """Display system time and PM1, PM2.5, PM10 readings."""
    # Clear display with dark background
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(0, 0, 0))
    
    # Get current time
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Display date and time at top
    draw.text((2, 2), current_date, font=font_small, fill=(150, 150, 150))
    draw.text((2, 18), current_time, font=font_large, fill=(255, 255, 255))
    
    # Draw separator line
    draw.line((0, 42, WIDTH, 42), fill=(100, 100, 100), width=1)
    
    # PM readings with color coding based on air quality
    y_offset = 46
    line_height = 18
    
    # PM1
    pm1_color = get_pm_color(pm1, thresholds=[12, 35, 55])
    draw.text((2, y_offset), f"PM1.0:", font=font_small, fill=(200, 200, 200))
    draw.text((60, y_offset), f"{pm1:.0f}", font=font_small, fill=pm1_color)
    draw.text((95, y_offset), "µg/m³", font=font_small, fill=(150, 150, 150))
    
    # PM2.5
    y_offset += line_height
    pm25_color = get_pm_color(pm25, thresholds=[12, 35, 55])
    draw.text((2, y_offset), f"PM2.5:", font=font_small, fill=(200, 200, 200))
    draw.text((60, y_offset), f"{pm25:.0f}", font=font_small, fill=pm25_color)
    draw.text((95, y_offset), "µg/m³", font=font_small, fill=(150, 150, 150))
    
    # PM10
    y_offset += line_height
    pm10_color = get_pm_color(pm10, thresholds=[54, 154, 254])
    draw.text((2, y_offset), f"PM10:", font=font_small, fill=(200, 200, 200))
    draw.text((60, y_offset), f"{pm10:.0f}", font=font_small, fill=pm10_color)
    draw.text((95, y_offset), "µg/m³", font=font_small, fill=(150, 150, 150))
    
    st7735.display(img)

def get_pm_color(value, thresholds):
    """Return color based on PM value - green/yellow/orange/red."""
    if value <= thresholds[0]:
        return (0, 255, 0)      # Green - Good
    elif value <= thresholds[1]:
        return (255, 255, 0)    # Yellow - Moderate
    elif value <= thresholds[2]:
        return (255, 165, 0)    # Orange - Unhealthy for sensitive
    else:
        return (255, 0, 0)      # Red - Unhealthy

# Get the temperature of the CPU for compensation
def get_cpu_temperature():
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp

# Tuning factor for compensation
factor = 2.25

cpu_temps = [get_cpu_temperature()] * 5

delay = 0.5
mode = 0
last_page = 0

# Create a values dict to store the data
variables = ["temperature", "pressure", "humidity", "light",
             "oxidised", "reduced", "nh3", "pm1", "pm25", "pm10"]

values = {v: [1] * WIDTH for v in variables}

# The main loop
try:
    while True:
        proximity = ltr559.get_proximity()
        
        # Dictionary to hold current readings for CSV
        current_data = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        # Temperature (compensated)
        cpu_temp = get_cpu_temperature()
        cpu_temps = cpu_temps[1:] + [cpu_temp]
        avg_cpu_temp = sum(cpu_temps) / float(len(cpu_temps))
        raw_temp = bme280.get_temperature()
        temperature = raw_temp - ((avg_cpu_temp - raw_temp) / factor)
        current_data["temperature"] = temperature
        logging_text("temperature", temperature, "°C")
        
        # Pressure
        pressure = bme280.get_pressure()
        current_data["pressure"] = pressure
        logging_text("pressure", pressure, "hPa")
        
        # Humidity
        humidity = bme280.get_humidity()
        current_data["humidity"] = humidity
        logging_text("humidity", humidity, "%")
        
        # Light
        if proximity < 10:
            light = ltr559.get_lux()
        else:
            light = 1
        current_data["light"] = light
        logging_text("light", light, "Lux")
        
        # Gas readings
        gas_data = gas.read_all()
        
        oxidised = gas_data.oxidising / 1000
        current_data["oxidised"] = oxidised
        logging_text("oxidised", oxidised, "kO")
        
        reduced = gas_data.reducing / 1000
        current_data["reduced"] = reduced
        logging_text("reduced", reduced, "kO")
        
        nh3 = gas_data.nh3 / 1000
        current_data["nh3"] = nh3
        logging_text("nh3", nh3, "kO")
        
        # PM readings
        pm1, pm25, pm10 = 0, 0, 0
        try:
            pm_data = pms5003.read()
            pm1 = float(pm_data.pm_ug_per_m3(1.0))
            pm25 = float(pm_data.pm_ug_per_m3(2.5))
            pm10 = float(pm_data.pm_ug_per_m3(10))
            
            current_data["pm1"] = pm1
            current_data["pm25"] = pm25
            current_data["pm10"] = pm10
            
            logging_text("pm1", pm1, "ug/m3")
            logging_text("pm25", pm25, "ug/m3")
            logging_text("pm10", pm10, "ug/m3")
            
        except pmsReadTimeoutError:
            logging.warning("Failed to read PMS5003")
            current_data["pm1"] = 0
            current_data["pm25"] = 0
            current_data["pm10"] = 0
        
        # Write all data to CSV
        write_csv_row(current_data)
        
        # Update display with time and PM values
        display_pm_readings(pm1, pm25, pm10)
        
        # Wait 10 minutes before next reading
        time.sleep(590)

# Exit cleanly
except KeyboardInterrupt:
    sys.exit(0)
