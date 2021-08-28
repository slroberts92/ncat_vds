#!/usr/bin/env python3

import sys
import serial
from nvcp import NVCP

def main():

    retval = 0

    if 1 < len(sys.argv):
        try:
            ser = serial.Serial(port = sys.argv[1],
                                baudrate = 9600,
                                timeout = 1,
                                parity = serial.PARITY_NONE,
                                stopbits = serial.STOPBITS_ONE)

            print(f"\nUsing serial port {ser.name}\n")

            nvcp = NVCP(ser)

            while True:
                received = nvcp.receive()
                print(f'Received packet: {int.from_bytes(received, "big")}')

        except serial.SerialException as e:
            print(f"\nSerial port error: {e}")
            retval = 1
    else:
        print("\nNo port argument given.")
        retval = 1

    return retval


if __name__ == "__main__":
    sys.exit(main())
