#!/usr/bin/python3
"""
BaseDriver class to handle hardware communication

Author: Mahmoud Mostafa
Email: mah2002moud@gmail.com
"""

from abc import ABC, abstractmethod

class BaseDriver(ABC):
    """
    BaseDriver class will include the necessary functions
    of any driver
    """
    instancesInfo = {}

    def __init__(self, msgName, operation, msgID):
        """Initializing the function"""
        self.msgName = msgName
        self.operation = operation
        self.msgID = msgID
        self.__isRunning = True

        # Store instance info
        BaseDriver.instancesInfo[self.msgName] = {
            "id": self.msgID,
            "protocol": self.__class__.__name__,
            "operation": self.operation,
            "running": self.__isRunning
        }

    def stop(self):
        """Stops the driver safely"""
        self.__isRunning = False
        BaseDriver.instancesInfo[self.msgName]["running"] = self.__isRunning

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
            raise TypeError("msgName must be of type (str)")
        self.__msgName = value

    @property
    def operation(self):
        """Returns the operation type"""
        return self.__operation

    @operation.setter
    def operation(self, value):
        """Sets the operation type value"""
        if not isinstance(value, str):
            raise TypeError("operation must be of type (str)")

        if value not in ["send", "receive"]:
            raise ValueError("operation must be either 'send' or 'receive'")

        self.__operation = value

    @property
    def msgID(self):
        """Returns the msgID"""
        return self.__msgID

    @msgID.setter
    def msgID(self, value):
        """Sets the msgID value"""
        if not isinstance(value, int):
            raise TypeError("msgID must be of type (int)")
        self.__msgID = value
