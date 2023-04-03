
import terminalio # required for the terminal stuff
import displayio
import adafruit_st7735r # we just need the init codes. will remove later.
import board
import busio
import digitalio
import microcontroller

class Button:
    """
    Sprig input mapping.
    """
    BUTTON_W:microcontroller.Pin = board.GP5
    BUTTON_A:microcontroller.Pin = board.GP6
    BUTTON_S:microcontroller.Pin = board.GP7
    BUTTON_D:microcontroller.Pin = board.GP8
    BUTTON_I:microcontroller.Pin = board.GP12
    BUTTON_J:microcontroller.Pin = board.GP13
    BUTTON_K:microcontroller.Pin = board.GP14
    BUTTON_L:microcontroller.Pin = board.GP15
    pass

class Sprig:
    """
    ### Helper library for using the sprig with Circuitpython.

    Adapted from my MicroGeiger project.
    """
    _fourwire: displayio.FourWire
    screen: str = "main_menu"
    cursor: int = 0
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
        self.ledLeft = digitalio.DigitalInOut(board.GP4)
        self.ledLeft.direction = digitalio.Direction.OUTPUT
        self.ledRight = digitalio.DigitalInOut(board.GP28)
        self.ledRight.direction = digitalio.Direction.OUTPUT
        return None

    def set_title(self,title:str) -> None:
        """
        Sets the display's title at the top.
        """
        print(f"\x1b]0; {title}\x1b\\",end="")

    def reset_display(self,reset_title:bool|None=True) -> None:
        """
        Helper function which clears the screen by writing an ANSI escape code.
        """
        if reset_title:
            self.set_title("")

        print("\x1b[2J\x1b[H",end="")
        return None
    
    def selection_screen(self,items:list[str]) -> str:

        return ""
    
    def poll_input(self) -> microcontroller.Pin:
        return board.A0

