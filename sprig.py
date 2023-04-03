
import terminalio # required for the terminal stuff
import displayio
import adafruit_st7735r # we just need the init codes. will remove later.
import board
import busio
import digitalio

class Sprig:
    """
    ### Helper library for using the sprig with Circuitpython.

    Adapted from my MicroGeiger project.
    """
    _fourwire: displayio.FourWire
    display: adafruit_st7735r.ST7735R
    ledLeft: digitalio.DigitalInOut
    ledRight: digitalio.DigitalInOut


    def __init__(self) -> None:
        displayio.release_displays()
        self._fourwire = displayio.FourWire(
            spi_bus=busio.SPI(clock=board.GP18,MOSI=board.GP19,MISO=board.GP16),
            chip_select=board.GP20,
            command=board.GP22,
            reset=board.GP26
        )
        self.display = adafruit_st7735r.ST7735R(
            bus=self._fourwire,
            rotation=270,
            width=160,
            height=128,
            backlight_pin=board.GP17
        )

        self.ledLeft = digitalio.DigitalInOut(board.GP)
