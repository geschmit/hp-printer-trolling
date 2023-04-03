import wifi

class Network:
    """
    Simple stuff to help with making finding printers easier.
    """

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
            if i.ssid[0:10] == "DIRECT-FA-":
                printers_perhaps.append(i)
        
        return printers_perhaps