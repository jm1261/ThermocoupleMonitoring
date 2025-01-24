import os
import time

from pathlib import Path

# These two lines mount the device
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = Path('/sys/bus/w1/devices')
print(os.listdir(base_dir))

# Get all the filenames beginning with 28 in the path base_dir
device_folder_1 = Path(base_dir, '28-00000ff94455')
print(os.listdir(device_folder_1))
device_file_1 = Path(device_folder_1, 'w1_slave')

device_folder_2 = Path(base_dir, '28-00000ff87b7a')
print(os.listdir(device_folder_2))
device_file_2 = Path(device_folder_2, 'w1_slave')


def read_rom(folder):
    name_file = Path(folder, 'name')
    f = open(name_file, 'r')
    return f.readline()


def read_temp_raw(file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp(file):
    lines = read_temp_raw(file)

    # Analyse if the last 3 characters are 'yes'
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()

    # Find the index of 't=' in a string
    equal_pos = lines[1].find('t=')

    if equal_pos != -1:

        # Read temp
        temp_string = lines[1][equal_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


print('rom1: ' + read_rom(folder=device_folder_1))
print('rom2: ' + read_rom(folder=device_folder_2))
while True:
    print(
        'Sensor 1 C = %3.2f F = %3.3f' % read_temp(file=device_file_1),
        'Sensor 2 C = %3.2f F = %3.3f' % read_temp(file=device_file_2))
time.sleep(1)
