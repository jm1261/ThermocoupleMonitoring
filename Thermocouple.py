import os
import time
import pandas as pd

import HelperUtils.Thermocouple as th

from pathlib import Path

# Output file names
output_data = 'Test.csv'
output_graph = 'Test.png'

# Time step
time_step = 1

# Directories
root = Path().absolute()
base_dir = Path('/sys', 'bus', 'w1', 'devices')

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

# Create an empty dataframe to store the data
columns = ['Timestamp'] + list(sensor_IDs.values()) 
df = pd.DataFrame(columns=columns)

i = 0
while True:
    current_time = pd.Timestamp.now()

    # Create a temporary dictionary to store sensor data for this time step
    temp_data = {'Timestamp': current_time}

    for directory in os.listdir(base_dir):
        if '28' in directory:
            sensor_dir = Path(base_dir, directory)
            sensor_id = th.read_sensor_name(directory=sensor_dir)
            sensor_name = sensor_IDs[sensor_id.strip()]
            sensor_file = Path(sensor_dir, 'w1_slave')

            try:
                sensor_temperature = th.read_temperature(file_path=sensor_file)
                temp_data[sensor_name] = sensor_temperature

            except FileNotFoundError:
                print(f'Sensor file not found for {sensor_name}')

            except Exception as e:
                print(f'Error reading temperature for {sensor_name}: {e}')

    # Append the temporary data to the main dataframe using 'loc' for safety
    df.loc[len(df)] = temp_data

    # Write the dataframe to the output file
    df.to_csv(output_data, index=False)

    # Sleep for specified interval
    time.sleep(time_step)

    # Plot if needed
    if i % 20 == 0:
        dataframe = pd.read_csv(output_data)
        th.plot_thermocouples_data(
            dataframe=dataframe,
            columns_to_plot=columns[1:],
            outpath=output_graph
        )

    # Increase Index
    i += 1
