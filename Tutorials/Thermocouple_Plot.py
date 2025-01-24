import time
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

# Root
root = Path().absolute()

# Filename
output_file = 'Cups_of_Tea.csv'
output_graph = 'Cups_of_Tea.png'

# FIlepath
file_path = Path(root, output_file)

while True:
    dataframe = pd.read_csv(file_path, parse_dates=['Timestamp'])
    columns_to_plot = ['Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5']

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=[15, 9], dpi=600)
    for column in columns_to_plot:
        ax.plot(dataframe['Timestamp'], dataframe[column], lw=2, label=column)
    ax.set_xlabel('Timestamp', fontsize=10, fontweight='bold')
    ax.set_ylabel('Temperature [Deg C]', fontsize=10, fontweight='bold')
    ax.set_title('Sensor Temperature Readings', fontsize=18, fontweight='bold')
    ax.legend(loc=0, ncol=1, prop={'size': 10})
    ax.grid(True)
    fig.tight_layout()
    plt.savefig(output_graph, bbox_inches='tight')
    time.sleep(30)
