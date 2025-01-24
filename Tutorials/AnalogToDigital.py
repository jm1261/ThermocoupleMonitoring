import spidev
import time

# Set up SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000


def read_adc(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


def convert_to_voltage(adc_value):
    return (adc_value * 3.3) / 1023  # 3.3V reference


def convert_to_temp(voltage):
    return (voltage/0.041)  # 41 �V/�C (type K thermocouple)


try:
    while True:
        adc_value = read_adc(0)  # Channel 0 for thermocouple
        voltage = convert_to_voltage(adc_value)
        temp = convert_to_temp(voltage)
        print(f"ADC Value: {adc_value}, Voltage: {voltage:.6f} V")
        time.sleep(1)

except KeyboardInterrupt:
    spi.close()
