# HP Troller
Hacking tool to help me juju on HP-based printers.

### About
This is a little project I made while bored one weekend. It takes advantage of several exploits in HP-based printers to print previously-stored files.

Payloads in this repository are taken from [textfiles.com.](https://textfiles.com/)

My implimentation of the Sprig hardware is located in `sprig.py`, and can be used in your own projects; please remember to follow licensing as such.

### Requirements
This requires a Sprig console and a Pico W. You CANNOT use the Pico H originally provided in the kit.

- Ensure you have CircuitPython 8.X flashed to your Pico. You can find it [here.](https://downloads.circuitpython.org/bin/raspberry_pi_pico_w/en_US/adafruit-circuitpython-raspberry_pi_pico_w-en_US-8.0.5.uf2)
- Download the latest release and clone it to your Pico's directory.
- Add files, as needed to `/payloads/`.

### Future plans
- [X] Add direct-print attack
- [ ] Add support for PostScript and images
- [ ] Attack other common ports(FTP, Telnet, SMTP)
- [ ] Improve UI library for Sprig
- [ ] Add audio support

### Licensing
Licensed under GNU GPL v3.0.
