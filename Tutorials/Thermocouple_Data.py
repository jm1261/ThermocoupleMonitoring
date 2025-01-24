import os
import time
import warnings
import pandas as pd

from pathlib import Path

warnings.filterwarnings("ignore", category=FutureWarning)

# Output file name
output_file = 'Cups_of_Tea.csv'

# These lines mount the device
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Base directory for devices
base_dir = Path('/sys', 'bus', 'w1', 'devices')
device_file = 'w1_slave'

# Sensor IDs
sensor_IDs = {
    '28-00000ff87b7a': 'Sensor 1',
    '28-00000ff85af7': 'Sensor 2',
    '28-00000ff83a39': 'Sensor 3',
    '28-00000ff8d0d9': 'Sensor 4',
    '28-00000ff94455': 'Sensor 5'
}

# Functions


def read_sensor_name(directory: os.PathLike) -> str:
    """
    Function Details
    ================
    Get sensor ID key from folder.

    Parameters
    ----------
    directory: os.PathLike
        Path to device directory.

    Returns
    -------
    name: str
        Sensor ID name.

    """
    name_file = Path(directory, 'name')
    f = open(name_file, 'r')
    return f.readline()


def read_raw_temperature(file_path: os.PathLike) -> list:
    """
    Function Details
    ================
    Pull raw temperature information from sensor file.

    Parameters
    ----------
    file_path: os.PathLike
        Path to sensor data file.

    Returns
    -------
    lines: list
        List of temperature data from sensor file.

    """
    file = open(file_path, 'r')
    lines = file.readlines()
    file.close()
    return lines


def read_temperature(file_path: os.PathLike) -> float:
    """
    Function Details
    ================
    Read temperature data from sensor file and convert to Celsius.

    Parameters
    ----------
    file_path: os.PathLike
        Path to sensor file.

    Return
    ------
    temp_c: float
        Temperature value in degrees Celsius.

    """
    lines = read_raw_temperature(file_path=file_path)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_raw_temperature()
    equal_position = lines[1].find('t=')
    if equal_position != -1:
        temperature_string = lines[1][equal_position + 2:]
        temp_c = float(temperature_string) / 1000.0
        return temp_c


df = pd.DataFrame(columns=['Timestamp'])

while True:
    current_time = pd.to_datetime('now')
    temp_data = {'Timestamp': current_time}
    for directory in os.listdir(base_dir):
        if '28' in directory:
            sensor_dir = Path(base_dir, directory)
            sensor_id = read_sensor_name(directory=sensor_dir)
            sensor_name = sensor_IDs[sensor_id.strip()]
            sensor_file = Path(sensor_dir, 'w1_slave')
            try:
                sensor_temperature = read_temperature(file_path=sensor_file)
                temp_data[sensor_name] = sensor_temperature
            except FileNotFoundError:
                print(f"Sensor file not found for {sensor_name}")
            except Exception as e:
                print(f"Error reading temperature for {sensor_name}: {e}")
    df = df.append(temp_data, ignore_index=True)
    df.to_csv(output_file, index=False)
    time.sleep(1)
