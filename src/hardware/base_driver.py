#!/usr/bin/python3
"""
BaseDriver class to handle hardware communication

Author: Mahmoud Mostafa
Email: mah2002moud@gmail.com
"""

from abc import ABC, abstractmethod
import threading
import time


class BaseDriver(ABC):
    """
    BaseDriver class will include the necessary functions
    of any driver
    """
    instancesInfo = {}

    def __init__(self, msgName, opration, msgID ):
        """Initializing the function"""
        self.msgName = msgName
        self.opration = opration
        self.msgID = msgID
        self.__isRunning = True
        self.__thread = None

        # Store instance info
        BaseDriver.instancesInfo[self.__msgName] = {
            "id": self.__msgID,
            "protocol": self.__class__.__name__,
            "opration": self.__opration,
            "running": self.__isRunning
        }

        def __run(self):
            """Continuously send or receive messages"""
        try:
            while self.__isRunning:
                if self.opration == "send":
                    self.__thread = threading.Thread(target=self.send, daemon=True)
                    self.__thread.start()

                elif self.opration == "receive":
                    self.__thread = threading.Thread(target=self.receive, daemon=True)
                    self.__thread.start()
                # time.sleep(0.01)  # Prevent high CPU usage
        except Exception:
            self.stop()

    def stop(self):
        """Stops the driver safely"""
        self.__isRunning = False
        if self.__thread.is_alive():
            self.__thread.join(timeout=1)


    @abstractmethod
    def send(self):
        """To be implemented in child class"""
        pass

    @abstractmethod
    def receive(self):
        """To be implemented in child class"""
        pass

    @property
    def msgName(self):
        """Returns the msg name"""
        return self.__msgName

    @msgName.setter
    def msgName(self, value):
        """Sets the msg name value"""
        if not isinstance(value, str):
            raise TypeError("msgName Value must be of type (str)")
        self.__msgName = value

    @property
    def opration(self):
        """Returns the opration type"""
        return self.__opration

    @opration.setter
    def opration(self, value):
        """Sets the opration type value"""
        if not isinstance(value, str):
            raise TypeError("opration value must be of type (str)")

        supportedValues = ["send", "receive"]
        if value not in supportedValues:
            raise ValueError("opration value must be equal to either send/receive")

        self.__opration = value

    @property
    def msgID(self):
        """Returns the msgID"""
        return self.__msgID

    @msgID.setter
    def msgID(self, value):
        """Sets the msgID value"""
        if not isinstance(value, int):
            raise TypeError("msgID Value must be of type (int)")
        self.__msgID = value

if __name__ == "__main__":
    # Creating an instance
    x = BaseDriver("imu", "send", 3)
    print(x.msgID)