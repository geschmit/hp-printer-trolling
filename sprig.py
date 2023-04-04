
import terminalio # required for the terminal stuff
import displayio
import adafruit_st7735r # we just need the init codes. will remove later.
import board
import busio
import digitalio
import microcontroller
import keypad

class Button:
    """
    Sprig input mapping.
    """
    BUTTON_W = 0
    BUTTON_A = 1
    BUTTON_S = 2
    BUTTON_D = 3

    MC_BUTTON_W:microcontroller.Pin = board.GP5
    MC_BUTTON_A:microcontroller.Pin = board.GP6
    MC_BUTTON_S:microcontroller.Pin = board.GP7
    MC_BUTTON_D:microcontroller.Pin = board.GP8
    MC_BUTTON_I:microcontroller.Pin = board.GP12
    MC_BUTTON_J:microcontroller.Pin = board.GP13
    MC_BUTTON_K:microcontroller.Pin = board.GP14
    MC_BUTTON_L:microcontroller.Pin = board.GP15
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
    buttons: keypad.Keys

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
        self.buttons = keypad.Keys(pins=(
            # never actually had a use planned for the righthand buttons lol
            Button.MC_BUTTON_W,
            Button.MC_BUTTON_A,
            Button.MC_BUTTON_S,
            Button.MC_BUTTON_D
        ),value_when_pressed=False,pull=True)
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
    
    def poll_input(self,button:int|None=None) -> int|None:
        """
        Waits until an input is detected from one of the sprig's buttons. 
        If an argument is given, will pause until that button is pushed, otherwise will 
        return the button's name.
        """
        while True:
            ev = self.buttons.events.get()
            if ev and ev.pressed:
                if button:
                    if button == ev.key_number:
                        return
                else:
                    return ev.key_number

    def selection_screen(self,items:list[str],title:str|None=None) -> str:
        """
        Basic UI interface. Returns string selected.
        """
        if len(items) > 8:
            raise Exception("Items exceeds display size")

        self.reset_display()
        if title:
            self.set_title(title)

        for i in items:
            print(f"  {i}")

        cursor = 1
        print(f"\x1b[0;0H>",end="")
        while True:
            movement = self.poll_input()

            if movement == Button.BUTTON_W:
                if cursor == 1:
                    continue
                else:
                    print(f"\x1b[{cursor};0H \r\x1b[{cursor-1};0H>",end="")
                    cursor=cursor-1
            elif movement == Button.BUTTON_S:
                if cursor >= len(items):
                    continue
                else:
                    print(f"\x1b[{cursor};0H \r\x1b[{cursor+1};0H>",end="")
                    cursor=cursor+1
            elif movement == Button.BUTTON_D:
                return items[cursor-1]

            # print(f"\x1b[5;0H{cursor}",end="")



