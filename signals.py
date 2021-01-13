# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 09:19:51 2021

@author: Rastko
"""
import arduino
import numpy as np
import time


class signals:
    """The signal class is used to handle all of the incoming signals from
    different sources
    """

    def __init__(self):
        """Initialises the signals class"""
        self.accelerometer = arduino.arduino(parents=[self], ID="ACC1")
        self.signals = {}
        self.decoder = decoder()

    def update(self, obj, msg):
        """
        The function which is called every time that there is an update from a
        signal.
        """
        obj_ID = obj.ID
        decoded = self.decoder.decode(obj, msg)
        self.signals[obj_ID] = decoded


class decoder:
    """The decoder class takes data and then reformats it into some
    standardised format
    """

    def __init__(self):
        """Initialises the decoder class"""
        pass

    def decode(self, obj, msg):
        """Decodes the message from a signal"""
        if isinstance(obj, arduino.arduino):
            return self.arduinoMSG(msg)

    def arduinoMSG(self, msg):
        """Decodes the message from an arduino"""
        acceleration = np.array([float(x.strip()) for x in msg.split(',')])
        return self.accelerations(acceleration[1],
                                  acceleration[2],
                                  acceleration[3])

    def accelerations(self, x, y, z):
        """Converts three numbers into a standardised acceleration format"""
        return {"time": time.time(), "X": x, "Y": y, "Z": z}

