import time

from gpiozero import LED, Button

led = LED(17)
button = Button(5)

while True:
    button.wait_for_press()
    led.toggle()
    time.sleep(0.5)
