# -*- coding: utf-8 -*-
"""
@author: Karl C. Goedel (mail@karl-goedel.de)

This module provides functions for the communication between pyGC and the TinyG board

"""

import serial

ser = None

# Connect via (virtual) serial port
def connect(port='/dev/ttyUSB0',baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=0.1):
    #print "pyTG: Open TinyG connection"    
    global ser
    try:
        ser = serial.Serial(port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits, timeout=timeout)
    except:
        return False
    if not ser.isOpen():
        ser.open()
    return True

# Close the serial connection
def close():
    global ser
    if ser == None:
        #print "pyTG: No connection established"
        return False
    ser.close()
    #print "pyTG: TinyG connection closed"
    return True

# Send a command to the TinyG (CR is added) and return answer
def cmd(cmd):
    global ser
    if ser == None:
        #print "pyTG: No connection established, try 'connect()'"
        return
    ser.write(cmd+"\r")
    print ""
    lines = ser.readlines()
    output = ''
    for l in lines:
        #print l[:-1]
        output += l[:-1] + "\n"
    return output

# Send a sequence of commands (from a list) to the TinyG 
def cmdseq(cmdlist):
    global ser
    if ser == None:
        #print "pyTG: No connection established, try 'connect()'"
        return
    output = ""
    for l in cmdlist:
        if not l[0] == "#":
			output += cmd(l)
    #print "pyTG: Command sequence finished"
    return output

# Send a sequence of commands (from a text block) to the TinyG 
def cmdblock(block):
    global ser
    if ser == None:
        #print "pyTG: No connection established, try 'connect()'"
        return
    cleanblock = ""
    cmdlist = block.split('\n')
    for l in cmdlist:
        if not l[0] == "#":
            cleanblock+=l+"\n"	
    output = cmd(cleanblock)
    #print "pyTG: Command block finished"
    return output

# Run a sequence of commands froma file
def script(filename, sequence=True):
    f = open(filename,"r")
    cmdlines = f.readlines()
    if sequence:
        output = cmdseq(cmdlines)
    else:
        block = ""		
        for l in cmdlines:
            block += l + "\n"
        output = cmdblock(block)
    #print "pyTG: Script finished"
    return output
