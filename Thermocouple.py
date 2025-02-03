import os
import time
import pandas as pd

import HelperUtils.Thermocouple as th

from pathlib import Path
from datetime import datetime

# Output file names
output_data_name = 'Outdoor_Weekend'

# Time step
time_step = 1

# Current date
current_date = datetime.now().strftime('%Y%m%d')

# Output filename
root = Path(
    '/',
    'home',
    'phorest',
    'Documents',
    'Github',
    'ThermocoupleMonitoring')
output_file = f'{output_data_name}_{current_date}.csv'
output_data = Path(root, output_file)

# Dir paths
base_dir = Path('/', 'sys', 'bus', 'w1', 'devices')
output_graph_name = f'{output_file[0: -4]}.png'
output_graph = Path(root, output_graph_name)

# Mount devices
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Sensor IDs
sensor_IDs = {
    '28-00000ff87b7a': 'Sensor 1',
    '28-00000ff85af7': 'Sensor 2',
    '28-00000ff83a39': 'Sensor 3',
    '28-00000ff8d0d9': 'Sensor 4',
    '28-00000ff94455': 'Sensor 5'
}

# Create a empty dataframe to store the data
columns = ','.join(['Timestamp'] + list(sensor_IDs.values()))
if output_data.is_file():
    pass
else:
    with open(output_data, 'w') as f:
        f.writelines(f'{columns}\n')

i = 0
while True:
    current_time = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

    # Create a temporary dictionary to store sensor data for this time step
    temp_data = [f'{current_time}']

    for key in sensor_IDs.keys():
        sensor_dir = Path(base_dir, key)
        sensor_id = th.read_sensor_name(directory=sensor_dir)
        sensor_name = sensor_IDs[sensor_id.strip()]
        sensor_file = Path(sensor_dir, 'w1_slave')

        try:
            sensor_temperature = th.read_temperature(file_path=sensor_file)
            temp_data.append(f'{sensor_temperature}')

        except FileNotFoundError:
            print(f'Sensor file not found for {sensor_name}')
            exit(69)

        except Exception as e:
            temp_data.append('')
            print(f'Error reading temperature for {sensor_name}: {e}')

    # Write the string to the output file
    with open(output_data, 'a') as f:
        line = ','.join(temp_data)
        f.writelines(f'{line}\n')

    # Sleep for specified interval
    time.sleep(time_step)

    # Plot if needed
    if i % 60 == 0:
        dataframe = pd.read_csv(output_data)
        th.plot_thermocouples_data(
            dataframe=dataframe,
            columns_to_plot=(['Timestamp'] + list(sensor_IDs.values()))[1:],
            outpath=output_graph
        )
        del dataframe

    # Increase Index
    i += 1
