#!/usr/bin/env python3

import nvcp_transport
import nvcp_datalink
import serial
import debug_log

class NVCP:

    __MAX_COMM_ATTEMPTS = 3

    def __init__(self, ser: serial.Serial()) -> None:
        self.transport_xmtr = nvcp_transport.NVCP_Transport()
        self.transport_rcvr = nvcp_transport.NVCP_Transport()
        self.datalink       = nvcp_datalink.NVCP_Datalink()
        self.serial         = ser

    def send(self, data_out):
        segment_out = self.transport_xmtr.send(
            self.transport_xmtr.SEG_TYPE_PDU,
            data_out
        )

        frame_out = self.datalink.frame(segment_out)

        for attempt in range(self.__MAX_COMM_ATTEMPTS):
            self.__write(frame_out)

            frame_in = self.__read()

            if len(frame_in) >= self.datalink.PDU_MIN_LEN:
                segment_in = self.datalink.deframe(frame_in)

                if segment_in != None:
                    seg_type, data_in = self.transport_rcvr.receive(segment_in)

                    if seg_type == self.transport_rcvr.SEG_TYPE_ACK:
                        return 0
                    else:
                        debug_log.log(
                            f'Unexpected segment received: {segment_in}'
                            f'Expected seg_type          : {self.transport_rcvr.SEG_TYPE_ACK}'
                            f'Received seg_type          : {seg_type}'
                        )
                else:
                    debug_log.log(
                        f'Bad frame received: {frame_in}'
                    )
            else:
                debug_log.log(
                    f'Read timeout occurred'
                )

            if (attempt + 1) == self.__MAX_COMM_ATTEMPTS:
                debug_log.log(
                    'Max comm attempts reached. Skipping...'
                )
                attempt = 0
                return -1

    def receive(self):
        data_in = b''
        while len(data_in) == 0:
            frame_in = self.__read()

            if len(frame_in) >= self.datalink.PDU_MIN_LEN:
                segment_in = self.datalink.deframe(frame_in)
                
                if segment_in != None:
                    seg_type, data_in = self.transport_rcvr.receive(segment_in)

                    if seg_type == self.transport_rcvr.SEG_TYPE_PDU:
                        segment_out = self.transport_xmtr.send(
                            self.transport_xmtr.SEG_TYPE_ACK,
                            None
                        )

                        frame_out = self.datalink.frame(segment_out)
                        self.__write(frame_out)

                    else:
                        debug_log.log(
                            f'Unexpected segment received: {segment_in}'
                            f'Expected seg_type          : {self.transport_rcvr.SEG_TYPE_ACK}'
                            f'Received seg_type          : {seg_type}'
                        )
                else:
                    debug_log.log(
                        f'Bad frame received: {frame_in}'
                    )
            else:
                # debug_log.log(
                #     f'Read timeout occurred'
                # )
                pass

        return data_in

    def __write(self, frame: bytes) -> None:
        """
        Write the frame to the serial port. This will block until the entire
        frame is written.

        Keyword arguments:
            frame -- The byte string to write to the serial port.
        """
        bytes_written = 0
        while bytes_written < len(frame):
            bytes_written += self.serial.write(frame)

    def __read(self) -> bytes:
        read_buf = self.serial.read_until(self.datalink.DELIMITER)
        return read_buf






















