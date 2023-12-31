#!/usr/bin/env python3
import sys
from datetime import datetime
import time

from escpos import feature
from escpos.impl.epson import GenericESCPOS
#from escpos import showcase

from kivy.utils import platform
if platform == 'android':
    from BlueT import BluetoothConnection
else:
    from escpos import BluetoothConnection

class Ticket:
    
    def __init__(self, settings):
        self.btConn = None
        self.printer = None
        self.connOK = False
        self.settings = settings


    def printTicket(self, queue, tNumber, owner, item, problem):
        self.connectPrinter()
        self.queue(queue)
        self.number(tNumber)
        self.owner(owner)
        self.item(item, problem)
        self.disclamer()
        self.logo()
        self.location(self.settings.locationName(), self.settings.locationDate())
        self.endDoc()
        self.disconnectPrinter()
        

    def connectPrinter(self):
        print("Conn OK "+str(self.connOK))
        if self.connOK:
            return
        # uses SPD (service port discovery) services to find which port to connect to
        self.btConn = BluetoothConnection(self.settings.printerMAC())
        self.printer = GenericESCPOS(self.btConn)
        self.connOK = True
        self.printer.init()
        self.printer.hardware_features.update({
           feature.COLUMNS: feature.Columns(
               normal=32,
               expanded=16,
               condensed=48
              ),
           })
           
           
    def disconnectPrinter(self):
        if platform == 'android':
            self.btConn.rfsocket.close()
            self.connOK = False          
                  
           
    def logo(self):
        #printer.image("Logo_Repair_Circle_Grey.png")
        #printer.device.write(<bytes>)
        self.printer.init()
        self.printer.justify_center()
        self.printer.set_expanded(True)
        self.printer.text('Repair Cafe') #é
        self.printer.text('Pasadena')
        self.printer.set_expanded(False)
        self.printer.lf()
        time.sleep(0.1)


    def number(self, tNum: int):
        self.printer.init()
        self.printer.justify_center()
        self.printer.set_expanded(True)
        self.printer.text('Ticket #{:d}'.format(tNum))
        self.printer.set_expanded(False)
        self.printer.lf()
        self.printer.text('{:%x %X}'.format(datetime.now()))
        self.printer.lf()
        time.sleep(0.1)


    def queue(self, rqueue: str):
        self.printer.init()
        self.printer.justify_center()
        self.printer.set_text_size(3, 7)
        self.printer.lf()
        self.printer.text(rqueue)
        self.printer.lf()
        time.sleep(0.1)
        

    def owner(self, name: str):
        self.printer.init()
        self.printer.set_emphasized(True)
        self.printer.textout('Owner: ')
        self.printer.set_emphasized(False)
        self.printer.text(name)
        self.printer.lf()
        time.sleep(0.1)
        
        
    def item(self, thing: str, problem: str):
        self.printer.init()
        self.printer.set_emphasized(True)
        self.printer.textout('Item: ')
        self.printer.set_emphasized(False)
        self.printer.text(thing)
        self.printer.set_emphasized(True)
        self.printer.text('Problem:')
        self.printer.set_emphasized(False)
        self.printer.text(problem)
        self.printer.lf()
        time.sleep(0.1)
        

    def disclamer(self):
        self.printer.init()
        self.printer.text('By Signing I acknowledge...')
        self.printer.set_condensed(True)    
        self.printer.text('1) I have had an oppporunity to communicate the nature of the problem')
        self.printer.text('2) An effort has been made to evaluate and/or\nrepair my item')
        self.printer.set_condensed(False)
        time.sleep(0.1)
        self.printer.lf()
        self.printer.lf()
        self.printer.lf()
        self.printer.text('-' * self.printer.feature.columns.normal)
        self.printer.lf()

        
    def location(self, loc: str, day: str):
        self.printer.init()
        self.printer.justify_center()
        self.printer.set_emphasized(True)
        self.printer.text(loc)
        self.printer.text(day)
        time.sleep(0.1)
        
    def endDoc(self):
        self.printer.lf()
        self.printer.lf()


if __name__ == '__main__':
    ticket = Ticket()
    sys.exit(ticket.printTicket())
 
