#!/usr/bin/env python3

class NVCP_Transport():

    SDU_MAX_LEN = 251
    SDU_MIN_LEN = 0

    PDU_MAX_LEN = 252
    PDU_MIN_LEN = 1

    SEG_TYPE_PDU = 0
    SEG_TYPE_ACK = 1

    __SEG_TYPE_PDU  = b'P'
    __SEG_TYPE_ACK  = b'A'

    def __init__(self) -> None:
        pass

    def send(self, seg_type: int, sdu: bytes) -> bytes:
        assert type(seg_type) == int

        if seg_type == self.SEG_TYPE_PDU:
            assert type(sdu) == bytes
            assert self.SDU_MIN_LEN <= len(sdu) <= self.SDU_MAX_LEN
            segment = self.__SEG_TYPE_PDU + sdu
        elif seg_type == self.SEG_TYPE_ACK:
            segment = self.__SEG_TYPE_ACK
        else:
            assert False

        return segment

    def receive(self, segment: bytes) -> bytes:
        assert type(segment) == bytes
        assert self.PDU_MIN_LEN <= len(segment) <= self.PDU_MAX_LEN

        if segment[0].to_bytes(1, 'big') == self.__SEG_TYPE_PDU:
            seg_type = self.SEG_TYPE_PDU
            sdu = segment[1:]
        elif segment[0].to_bytes(1, 'big') == self.__SEG_TYPE_ACK:
            seg_type = self.SEG_TYPE_ACK
            sdu = None
        else:
            assert False

        return seg_type, sdu
