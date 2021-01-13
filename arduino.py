# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 09:22:08 2021

@author: Rastko
"""
import serial
import threading


class arduino:
    """Class used for reading and sending serial data coming from an arduino
    
    Parameters
    ----------
    COM_PORT : str:`COM3`
        The COM that the arduino is connected to. 
    BAUDRATE : int:115200
        The baudrate that the serial port is set to use on the arduino.
    TIMEOUT : int:3
        The maximum amount of time to wait when reading serial data.
    parents : list:[]
        The arduino will call the function update(), referencing it's self to
        any parents in this list.
    ID : str:`Arduino1`
        A given ID of the class.

    Attributes
    ----------
    COM_PORT : str
        The COM that the arduino is connected to. 
    BAUDRATE : int
        The baudrate that the serial port is set to use on the arduino.
    TIMEOUT : int
        The maximum amount of time to wait when reading serial data.
    parents : list
        The arduino will call the function update(), referencing it's self to
        any parents in this list.
    readingSerial : bool
        A flag which states weather the arduino is currently updating it's
        self with the incoming serial messages.
    lastMessage : str
        The last message that the class read from the serial port.
    allMessages : list
        A list of strings of all the messages that have been recieved.

    Methods
    ----------
    openSerialPort : bool
        Opens the serial port. Returns True if the serial port was open.
        Returns False if the serial port failed to open. If this occurs, this
        can be fixed by disconnecting and reconnecting the arduino.
    start : None
        Starts logging the data coming from the serial port
    stop : None
        Stop logging data from the serial port
    closeSerialPort : None
        Close the serial port.

    """

    def __init__(self, COM_PORT="COM3", BAUDRATE=115200, TIMEOUT=3, parents=[], ID="Arduino1"):
        """Initialises the arduino class"""
        self.ID = ID
        self.parents = parents
        self.COM_PORT = COM_PORT
        self.BAUDRATE = BAUDRATE
        self.TIMEOUT = TIMEOUT
        self.readingSerial = False
        self.lastMessage = ""
        self.allMessages = []
        if self.openSerialPort():
            self.start()

    def openSerialPort(self):
        """Open the serial port"""
        try:
            self.ser = serial.Serial(  # set parameters, in fact use your own :-)
                port=self.COM_PORT,
                baudrate=self.BAUDRATE,
                bytesize=serial.SEVENBITS,
                parity=serial.PARITY_EVEN,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.TIMEOUT
            )
            self.ser.isOpen()  # try to open port, if possible print message and proceed with 'while True:'
            return True

        except Exception:  # There was an error in opening the serial port
            print("CANNOT OPEN SERIAL PORT")
            return False

    def start(self):
        """Starts logging data"""
        self.readingSerial = True
        self.thread = threading.Thread(target=self.readSerial)
        self.thread.start()

    def stop(self):
        """Stops logging data, but does not close the serial port"""
        self.readingSerial = False
        self.thread.join()

    def closeSerialPort(self):
        """Closes the serial port"""
        self.stop()
        self.ser.close()

    def readSerial(self):
        """A while loop which is run in a thread which continuously reads the
        incoming serial data as it is sent, so long as self.readingSerial is
        set to True"""
        while self.readingSerial:
            while self.ser.in_waiting:
                try:
                    self.lastMessage = self.ser.readline().decode()
                    self.allMessages.append(self.lastMessage)
                    self.updateParents()
                except Exception:  # There was an error in reading
                    pass

    def updateParents(self):
        """
        A function which is called whenever there is a new message recieved.
        The function calls .update(self) on each of the classes within the
        self.parents list.
        """
        # If there are any parents to call an update function
        if self.parents:
            [p.update(self, self.lastMessage) for p in self.parents]
