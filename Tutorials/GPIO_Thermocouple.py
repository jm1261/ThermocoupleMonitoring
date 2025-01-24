import os
import time
import glob

from pathlib import Path

# These two lines mount the device
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = Path('/sys/bus/w1/devices')
print(os.listdir(base_dir))

# Get all the filenames beginning with 28 in the path base_dir
device_folder = Path(base_dir, '28-00000ff94455')
print(os.listdir(device_folder))
device_file = Path(device_folder, 'w1_slave')


def read_rom():
    name_file = Path(device_folder, 'name')
    f = open(name_file, 'r')
    return f.readline()


def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()

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


print('rom: ' + read_rom())
while True:
    print('C = %3.2f F = %3.3f' % read_temp())
time.sleep(1)
