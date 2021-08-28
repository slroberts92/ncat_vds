#!/usr/bin/env python3

import sys
import serial
from nvcp import NVCP
import datetime

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

            num_packets = 100

            print(f'\n******Sending {num_packets} packets******\n')

            failures = 0

            start_time = datetime.datetime.now()

            for i in range(num_packets):
                print(f'Sending packet : {i}......', end='')
                message = i.to_bytes(10, "big")
                if nvcp.send(message) == 0:
                    print('Success')
                else:
                    print('Failure')
                    failures += 1

            end_time = datetime.datetime.now()

            print(
                f'\n'
                f'------Test Report------\n'
                f'* Elapsed time: {end_time - start_time}\n'
                f'* Packets sent: {num_packets}\n'
                f'* Packets rcvd: {num_packets - failures}\n'
                f'* Success rate: {((num_packets - failures) / num_packets) * 100}%\n'
            )

        except serial.SerialException as e:
            print(f"\nSerial port error: {e}")
            retval = 1
    else:
        print("\nNo port argument given.")
        retval = 1

    return retval


if __name__ == "__main__":
    sys.exit(main())
