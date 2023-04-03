from time import sleep as wait # hi lua kiddie here
from sprig import Sprig
from network import Network

nw = Network()
printers = []
sprig = Sprig() # terminal uses a 26x8 viewport, giving us 208 characters
sprig.reset_display()

# Intro
sprig.set_title("PRINTSPAM 0.0.1")
print("Created by geschmit")
print("haha printer funny")
wait(1.5)
print("Scanning nearby networks..",end="")
sprig.ledLeft.value = True
printers = nw.fetch_printers()
sprig.ledLeft.value = False
print(f"Found {len(printers)} printers.")
wait(1.5)

sprig.reset_display()

while True:
    ans = sprig.selection_screen([
        "Option 1",
        "Option 2"
    ])

    