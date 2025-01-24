from signal import pause
from gpiozero import LED, Button

led = LED(17)
button = Button(5)

button.when_pressed = led.on
button.when_released = led.off

pause()
