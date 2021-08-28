#!/usr/bin/env python3

import threading
import serial
import sys

def read_from_port(ser):
    while True:
        data = ser.readline().decode('ascii')
        print(f'{data[:-1]}')

def write_to_port(ser):
    while True:
        data = input().encode('ascii')
        data += b'\n'
        ser.write(data)

def main():

    retval = 0

    if 1 < len(sys.argv):
        try:
            ser = serial.Serial(port = sys.argv[1],
                                baudrate = 9600,
                                timeout = None,
                                parity = serial.PARITY_NONE,
                                stopbits = serial.STOPBITS_ONE)

            print(f"\nUsing serial port {ser.name}\n")

            t1 = threading.Thread(target=read_from_port, args=(ser,))
            t2 = threading.Thread(target=write_to_port, args=(ser,))

            t1.start()
            t2.start()

        except serial.SerialException as e:
            print(f"\nSerial port error: {e}")
            retval = 1
        except KeyboardInterrupt:
            print('\nExiting...')
            ser.close()
            retval = 0
    else:
        print("\nNo port argument given.")
        retval = 1

    return retval

if __name__ == "__main__":
    sys.exit(main())
