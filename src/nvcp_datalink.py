#!/usr/bin/env python3

import crcmod.predefined
from cobs import cobs

class NVCP_Datalink:

    SDU_MAX_LEN     = 252
    SDU_MIN_LEN     = 0

    PDU_MAX_LEN     = 256
    PDU_MIN_LEN     = 4

    DELIMITER = b'\x00'

    def __init__(self) -> None:
        pass

    def frame(self, sdu):
        crc16 = crcmod.predefined.Crc('crc-16-usb')
        crc16.update(sdu)
        payload = sdu + crc16.crcValue.to_bytes(2, 'big')
        encoded = cobs.encode(payload)
        pdu = encoded + self.DELIMITER
        return pdu

    def deframe(self, pdu):
        encoded = pdu[:-1]

        try:
            payload = cobs.decode(encoded)
        except cobs.DecodeError as e:
            #TODO Add to error log
            print(f'Cobs decode error')
            return None

        sdu, crc16_in = payload[:-2], payload[-2:]

        crc16 = crcmod.predefined.Crc('crc-16-usb')
        crc16.update(sdu)
        if crc16_in != crc16.crcValue.to_bytes(2, 'big'):
            #TODO Add to error log
            return None

        return sdu

