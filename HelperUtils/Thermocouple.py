import os
import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from pathlib import Path


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


def plot_thermocouples_data(dataframe,
                            columns_to_plot: list,
                            outpath: str):
    """
    Function Details
    ================
    Plot thermocouple dataframe.

    Parameters
    ----------
    dataframe: any
        Pandas dataframe
    columns_to_plot: list
        List of column headers.
    outpath: str
        Path to save graph.

    Returns
    -------
    None.

    """
    fig, ax = plt.subplots(
        nrows=1,
        ncols=1,
        figsize=[15, 9],
        dpi=600
    )
    dataframe['Timestamp'] = pd.to_datetime(dataframe['Timestamp'])
    for column in columns_to_plot:
        ax.plot(
            dataframe['Timestamp'],
            dataframe[column],
            lw=2,
            label=column
        )
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.set_xlabel(
        'Time',
        fontsize=10,
        fontweight='bold'
    )
    ax.set_ylabel(
        'Temperature [Deg C]',
        fontsize=10,
        fontweight='bold'
    )
    ax.set_title(
        'Sensor Temperature Readings',
        fontsize=18,
        fontweight='bold'
    )
    ax.legend(
        loc=0,
        ncol=1,
        prop={'size': 10}
    )
    ax.grid(True)
    plt.xticks(rotation=45)
    fig.tight_layout()
    plt.savefig(
        outpath,
        bbox_inches='tight'
    )
