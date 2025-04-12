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
    """Base class for serial communication"""

    def __init__(self, msgName, operation, port, msgID=None, msgIDLength=0, baudrate=115200, timeout=5):
        self.port = port
        self.baudrate = baudrate
        self.msgIDLength = msgIDLength
        self.serial_conn = None
        super().__init__(msgName, operation, msgID, timeout)

    def connect(self):
        """Establish a serial connection"""
        try:
            self.serial_conn = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
            self.log_connected(self.port)
            return 0 # for seccuss
        except serial.SerialException as e:
            self.log_warning(f"Failed to connect to {self.port}: {e}, Retry in 2 seconds")
            if self.serial_conn and self.serial_conn.is_open:
                self.serial_conn.close()
            return 1 # for failuer

    def disconnect(self):
        """Close the serial connection"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            self.stop()

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

class SerialSender(SerialBaseDriver):

    def __init__(self, msgName, port, msgID=None, msgIDLength=0, baudrate=115200, timeout=5):
        super().__init__(msgName, "send", port, msgID, msgIDLength, baudrate, timeout)

    def threaded_send(self, data):
        if not isinstance(data, bytes):
            raise TypeError("sent data must be of type (bytes)")
        
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            if self.serial_conn and self.serial_conn.is_open:
                try:
                    payload = (self.msgID.to_bytes(self.msgIDLength, 'big') + data) if self.msgIDLength else data
                    self.serial_conn.write(payload)
                    self.log_sent(data)
                    return 0
                except serial.SerialException as e:
                    self.log_error(f"Error: {e}, Retrying")
                    self.serial_conn.close()
                    self._try_to_connect()
            else:
                self.log_error("Device disconnected, Retrying")
                self._try_to_connect()
        self.log_error(f"Failed to send data: {data} within timeout")
        return 1

    def threaded_receive(self):
        raise NotImplementedError("'SerialSender' object can't be used to receive messages")

# class SerialSender(SerialBaseDriver)

#     def receive(self):
#         """Receive data over the serial connection and extract the msgID"""
#         if self.serial_conn and self.serial_conn.is_open:
#             try:
#                 pass
#             except serial.SerialException as e:
#                 print(f"Failed to receive data: {e}")
#         return None, None

if __name__ == "__main__":
    import struct

    # Create a single SerialSender instance
    sender = SerialSender("test", "/dev/ttyACM0", msgID=0x10, msgIDLength=1, baudrate=9600)
    
    # Wait for Arduino to initialize
    time.sleep(2)
    
    value = 0.0
    while True:
        value += 1.0
        
        # Send with msgID=0x10 (e.g., motor)
        sender.msgID = 0x10
        data = struct.pack('<f', value)
        status = sender.send(data)
        if status == 0:
            print(f"Sent msgID=0x10, value={value}")
        else:
            print(f"Failed to send msgID=0x10, value={value}")
        
        # Send with msgID=0x11 (e.g., LED)
        sender.msgID = 0x11
        data = struct.pack('<f', value * 2)
        status = sender.send(data)
        if status == 0:
            print(f"Sent msgID=0x11, value={value * 2}")
        else:
            print(f"Failed to send msgID=0x11, value={value * 2}")
        
        time.sleep(1)