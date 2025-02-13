#!/usr/bin/env python3
# Commented out lines 42-44 and added CSV
# 30 second sleep time


import logging
import time
import csv
from pms5003 import PMS5003, ReadTimeoutError

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S")

logging.info("""Print readings from the PMS5003 particulate sensor.

Press Ctrl+C to exit!

""")

pms5003 = PMS5003()
time.sleep(1.0)

# Open the CSV file in append mode
with open('pms5003_data.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Write the header row if the file is empty
    if csvfile.tell() == 0:
        csvwriter.writerow(['timestamp', 'pm1_0', 'pm2_5', 'pm10', 'pm1_0_atm', 'pm2_5_atm', 'pm10_atm', 'gt0_3um', 'gt0_5um', 'gt1_0um', 'gt2_5um', 'gt5_0um', 'gt10um'])

    try:
        while True:
            try:
                readings = pms5003.read()
                logging.info(readings)
                
                # Write the readings to the CSV file
                csvwriter.writerow([
                    time.strftime('%Y-%m-%d %H:%M:%S'),
                    readings.pm_ug_per_m3(1.0),
                    readings.pm_ug_per_m3(2.5),
                    readings.pm_ug_per_m3(10),
                    #readings.pm_ug_per_m3(1.0, atmospheric_environment=True),
                    #readings.pm_ug_per_m3(2.5, atmospheric_environment=True),
                    #readings.pm_ug_per_m3(10, atmospheric_environment=True),
                    readings.pm_per_1l_air(0.3),
                    readings.pm_per_1l_air(0.5),
                    readings.pm_per_1l_air(1.0),
                    readings.pm_per_1l_air(2.5),
                    readings.pm_per_1l_air(5.0),
                    readings.pm_per_1l_air(10)
                ])
                time.sleep(30)  # wait for 0.5 minutes (30 seconds)
            except ReadTimeoutError:
                pms5003 = PMS5003()
    except KeyboardInterrupt:
        pass
