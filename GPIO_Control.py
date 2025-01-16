import time

from gpiozero import LED, Button

led = LED(17)
button = Button(5)

button.wait_for_press()
led.on()
time.sleep(3)
led.off()
