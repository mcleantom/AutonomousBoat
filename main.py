# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 09:19:51 2021

@author: Rastko
"""


class parent:

    def __init__(self):
        self.c = child(self)

    def newMessage(self):
        print("new message")


class child():
    
    def __init__(self, parent):
        self.p = parent
    
    def message(self):
        self.p.newMessage()
