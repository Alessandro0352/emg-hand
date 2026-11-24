"""Reads the binary packets sent by the acquisition firmware.
port can be a real port ("COM5") or a fake board that replays a file ("fake:../data/sim/S1_test.npz")."""
import struct
import numpy as np
import serial

N_FIELDS = 9                  # sync, counter, 4 EMG, 3 accelerometer
PKT = 2 * N_FIELDS            # 18 bytes
FMT = "<" + "H" * N_FIELDS


def open_port(port, baud):
    """Real serial port, or a FakeBoard when the name starts with 'fake:'."""
    if port.startswith("fake:"):
        from fake_board import FakeBoard
        board = FakeBoard(port[len("fake:"):])
        return board.port, board
    return serial.Serial(port, baud, timeout=0.01), None


class PacketReader:
    def __init__(self, port, baud=921600):
        self.ser, self.board = open_port(port, baud)
        self.buf = bytearray()
        self.last_counter = None
        self.lost = 0             # lost packets (counter jumps)
        self.received = 0

    def read(self):
        """Returns everything that has arrived as an array (m, 8):
        columns 0 = counter, 1-4 = EMG (ADC counts), 5-7 = accelerometer (raw/4 + 8192)."""
        self.buf += self.ser.read(self.ser.in_waiting or 1)
        rows = []
        while len(self.buf) >= PKT + 2:   # one packet + the next sync word
            fields = struct.unpack_from(FMT, self.buf)
            next_sync = self.buf[PKT] == 0x5A and self.buf[PKT + 1] == 0xA5
            if fields[0] == 0xA55A and next_sync and max(fields[1:]) < 0x4000:
                del self.buf[:PKT]
                cnt = fields[1]
                if self.last_counter is not None:
                    self.lost += (cnt - self.last_counter - 1) & 0x3FFF
                self.last_counter = cnt
                self.received += 1
                rows.append(fields[1:])
            else:
                del self.buf[0]           # damaged or out of sync: skip one byte
        return np.array(rows, dtype=float).reshape(-1, N_FIELDS - 1)

    def close(self):
        if self.board is not None:
            self.board.stop()
        self.ser.close()