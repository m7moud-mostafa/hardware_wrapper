#!/usr/bin/python3
"""
SerialBaseDriver class for USB and UART communication

Author: Mahmoud Mostafa
Email: mah2002moud@gmail.com
"""

import serial
from hardware.base_driver import BaseDriver
import time
class SerialBaseDriver(BaseDriver):
    """Base class for serial communication (USB/UART)"""

    def __init__(self, msgName, operation, port, msgID=None, msgIDLength=0, baudrate=115200, timeout=5):
        super().__init__(msgName, operation, msgID)
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.msgIDLength = msgIDLength
        self.serial_conn = None
        self.connect()

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        if not isinstance(value, str):
            raise TypeError("'port' must be of type (str)")
        self.__port = value

    @property
    def msgIDLength(self):
        return self.__msgIDLength

    @msgIDLength.setter
    def msgIDLength(self, value):
        if not isinstance(value, int):
            raise TypeError("'msgIDLength' must be of type (int)")
        self.__msgIDLength = value

    @property
    def baudrate(self):
        return self.__baudrate

    @baudrate.setter
    def baudrate(self, value):
        if not isinstance(value, int):
            raise TypeError("'baudrate' must be of type (int)")
        self.__baudrate = value

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, value):
        if not isinstance(value, int):
            raise TypeError("'timeout' must be of type (int)")
        self.__timeout = value

    def connect(self):
        """Establish a serial connection"""
        try:
            self.serial_conn = serial.Serial(port=self.__port, baudrate=self.__baudrate, timeout=self.__timeout)
            print(f"Connected to {self.__port} at {self.__baudrate} baud")
        except serial.SerialException as e:
            print(f"Failed to connect to {self.__port}: {e}")

    def disconnect(self):
        """Close the serial connection"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print(f"Disconnected from {self.port}")

    def send(self, data):
        """Send data over the serial connection with a 2-byte header for msgID"""
        if self.serial_conn and self.serial_conn.is_open:
            try:
                if self.__msgIDLength:
                    msg_id_bytes = self.msgID.to_bytes(self.__msgIDLength, byteorder='big')
                    payload = msg_id_bytes + bytes(data)
                else:
                    payload = bytes(data)
                self.serial_conn.write(payload)
                print(f"Sent data: ID={self.msgID}, Payload={data}")
            except serial.SerialException as e:
                print(f"Failed to send data: {e}")

    def receive(self):
        """Receive data over the serial connection and extract the msgID"""
        if self.serial_conn and self.serial_conn.is_open:
            try:
                pass
            except serial.SerialException as e:
                print(f"Failed to receive data: {e}")
        return None, None


    def __del__(self):
        """Ensure the serial connection is closed on deletion"""
        self.disconnect()


if __name__ == "__main__":
    test = SerialBaseDriver("test", "send", "/dev/ttyACM0", baudrate=9600)
    while True:
        test.send([0x07, 0xD2])
        time.sleep(1)