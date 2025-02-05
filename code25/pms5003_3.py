#!/usr/bin/env python3

import logging
import time
import csv
from pms5003 import PMS5003, ReadTimeoutError

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S")

logging.info("""particulates.py - Print readings from the PMS5003 particulate sensor.

Press Ctrl+C to exit!

""")

pms5003 = PMS5003()
time.sleep(1.0)

# Open the CSV file in append mode
with open('pms5003_data.csv', 'a', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    # Write the header row if the file is empty
    if csvfile.tell() == 0:
        csvwriter.writerow(['timestamp', 'pm1_0', 'pm2_5', 'pm10'])

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
                    readings.pm_ug_per_m3(10)
                ])
                
            except ReadTimeoutError:
                pms5003 = PMS5003()
    except KeyboardInterrupt:
        pass
