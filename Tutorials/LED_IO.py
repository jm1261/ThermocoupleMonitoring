import time
from gpiozero import LED

led = LED(17)  # Set to the GPIO pin

led.on()  # On
# led.off()  # Off

time.sleep(30)

# Note, script does not need to turn off LED, script finishing changes that.
