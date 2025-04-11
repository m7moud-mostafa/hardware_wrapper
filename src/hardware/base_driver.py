#!/usr/bin/python3
"""
BaseDriver class to handle hardware communication with logging.

Author: Mahmoud Mostafa
Email: mah2002moud@gmail.com
"""

from abc import ABC, abstractmethod
from hardware.logging_mixin import LoggingMixin

class BaseDriver(LoggingMixin, ABC):
    """
    BaseDriver class with logging capabilities inherited from LoggingMixin.
    Includes necessary functions for any driver.
    """
    instancesInfo = {}

    def __init__(self, msgName, operation, msgID):
        """Initialize the driver and log its creation."""
        # Set attributes
        self.msgName = msgName
        self.operation = operation
        self.msgID = msgID
        self.__isRunning = True

        # Call the parent class's __init__ (LoggingMixin) to initialize the logger
        super().__init__()

        # Store instance info
        BaseDriver.instancesInfo[self.__msgName] = {
            "id": self.__msgID,
            "protocol": self.__class__.__name__,
            "operation": self.__operation,
            "running": self.__isRunning
        }

        # Now that logger is initialized, log instance creation
        self.log_instance_created()

    def stop(self):
        """Stops the driver safely and logs the event."""
        self.__isRunning = False
        BaseDriver.instancesInfo[self.__msgName]["running"] = self.__isRunning
        self.log_stop()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

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
            raise TypeError("'msgName' must be of type (str)")
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
        if not (isinstance(value, int) or value is None):
            raise TypeError("msgID must be of type (int)")
        self.__msgID = value