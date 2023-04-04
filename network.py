import wifi

class Network:
    """
    Simple stuff to help with making finding printers easier.
    """

    MAX_LOGIN_TRIES = 3
    PRINTER_PASSWORDS = [
        "12345678"
    ]

    def __init__(self) -> None:
        pass

    def fetch_printers(self) -> list[wifi.Network]:
        """
        Fetch nearby printers that are advertising
        """
        printers_perhaps: list[wifi.Network] = []
        for i in wifi.radio.start_scanning_networks():
            if i.ssid[0:10] == "DIRECT-FA-" and not i in printers_perhaps:
                printers_perhaps.append(i)
        
        return printers_perhaps
    
    def bruteforce_logins(self,printer:wifi.Network) -> bool:
        for x in self.PRINTER_PASSWORDS:
            print(f"P:{x}")
            for i in range(self.MAX_LOGIN_TRIES):
                print(f"Attempt {i} - ",end="")
                try:
                    wifi.radio.connect(printer.ssid,x)
                except ConnectionError or ConnectionRefusedError:
                    print("X")
                    continue
                finally:
                    print("OK")
                    return True
                
        return False