# Example Instrument Setup For Landscape_DataStream v1.0
# Example for instrument with scan + read functions
# Speed Test
from time import sleep
import re
import pyvisa
import numpy as np
import random
import datetime

address = ""
mode = "Speed Test"
rampstep = "0.001"
rampdelay = "0ms"
readstrs = ["Test 1", "Test 2",]
debug = False

previous_value = 0

def array1D(start, end, step):
    if start <= end:
        step = +abs(step)
    else:
        step = -abs(step)
    array = np.arange(start,end,step)
    array = np.append(array, end)
    return array.tolist()

def findnum(instring):
    numpattern = '[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d+ ) ?'
    rx = re.compile(numpattern, re.VERBOSE)
    numarray = rx.findall(instring)
    numarray = list(map(float, numarray))
    if len(numarray)==0:
        numarray = [0]
    return numarray

def Call(parameters):
    # parameters is a list of tuples.
    # parameters = list(parameters)
    global mode
    upparameters = [
        ("Instrument Status", "Called, None"),
        ("Range", "Called, None"),
        ]
    for pair in parameters:
        (parameter_name, parameter_value) = pair
        if parameter_name == "Mode":
            mode = parameter_value
            upparameters.append((parameter_name, parameter_value))
        elif parameter_name == "Ramp Step":
            rampstep = findnum(parameter_value)[0]
            upparameters.append((parameter_name, parameter_value))
        else:
            upparameters.append((parameter_name, parameter_value))
            pass
    returnstr = "Speed Test is Called"
    print(returnstr)
    return (upparameters, returnstr)

def Initialize(*arg):

    returnstr = "Speed Test is Initialized"
    
    return returnstr

def Retrieve(*arg):
    global previous_value

    previous_value = random.random()

    returnstr = "%g" %(previous_value)

    return returnstr

def Scan1(Scan_Value):
    global previous_value
    global rampstep
    global rampdelay
    global debug

    rampstepnum = max(findnum(rampstep)+[0.0005])
    rampdelaynum = max(findnum(rampdelay)+[0])/1000

    try:
        print("Speed Test is ramping from %g to %g..." % (previous_value, Scan_Value))
        if Scan_Value != previous_value:
            for sv in array1D(previous_value, Scan_Value, rampstepnum):
                comstr = "set %.5f" % (sv)
                #sleep(rampdelaynum)
                if debug:
                    print("write to Speed Test: " + comstr)
        returnstr = "Speed Test scanned to %gV from %gV with step %gV and delay %gs" % (Scan_Value, previous_value, rampstepnum, rampdelaynum)
        previous_value = Scan_Value
    except Exception as e:
        returnstr = "Speed Test Scan with error: " + e.__doc__
        print(returnstr)
        returnstr = False

    stb = False
    stbtime = 0

    print(returnstr, stb, stbtime)
    return (returnstr, stb, stbtime)

def Scan(Scan_Value):
    global previous_value
    global rampstep
    global rampdelay
    global debug

    rampstepnum = max(findnum(rampstep)+[0.0005])
    rampdelaynum = max(findnum(rampdelay)+[0])/1000

    try:
        sv = previous_value
        print("Speed Test is ramping from %g to %g..." % (previous_value, Scan_Value))
        if Scan_Value != previous_value:
            if Scan_Value > previous_value:
                sv = min(Scan_Value, previous_value+rampstepnum)
                #sleep(rampdelaynum)
                comstr = "set %.5f" % (sv)
                if debug:
                    print("write to Speed Test: " + comstr)
            else:
                sv = max(Scan_Value, previous_value-rampstepnum)
                comstr = "set %.5f" % (sv)
                #sleep(rampdelaynum)
                if debug:
                    print("write to Speed Test: " + comstr)
            returnstr = "Speed Test scanned to %gV targeting %gV from %gV by step %gV and delay %gs" % (sv, Scan_Value, previous_value, rampstepnum, rampdelaynum)
            previous_value = sv
            if sv == Scan_Value:
                stb = False
                stbtime = 0
            else:
                stb = True
                stbtime = 600
        else:
            returnstr = "Speed Test is at target value %gV" % (Scan_Value)
            previous_value = Scan_Value
            stb = False
            stbtime = 0
    except Exception as e:
        returnstr = "Speed Test Scan with error: " + e.__doc__
        print(returnstr)
        returnstr = False

    print(returnstr, stb, stbtime)
    return (returnstr, stb, stbtime)

def Approach(Scan_Value):
    global previous_value
    global rampstep
    global rampdelay
    global debug

    rampstepnum = max(findnum(rampstep)+[0.0005])
    rampdelaynum = max(findnum(rampdelay)+[0])/1000

    try:
        sv = previous_value
        print("Speed Test is ramping from %g to %g..." % (previous_value, Scan_Value))
        if Scan_Value != previous_value:
            if Scan_Value > previous_value:
                sv = min(Scan_Value, previous_value+rampstepnum)
                comstr = "set %.5f" % (sv)
                #sleep(rampdelaynum)
                if debug:
                    print("write to Speed Test: " + comstr)
            else:
                sv = max(Scan_Value, previous_value-rampstepnum)
                comstr = "set %.5f" % (sv)
                #sleep(rampdelaynum)
                if debug:
                    print("write to Speed Test: " + comstr)
            returnstr = "Speed Test scanned to %gV targeting %gV from %gV by step %gV and delay %gs" % (sv, Scan_Value, previous_value, rampstepnum, rampdelaynum)
            previous_value = sv
            if sv == Scan_Value:
                stb = True
            else:
                stb = False
        else:
            returnstr = "Speed Test is at target value %gV" % (Scan_Value)
            previous_value = Scan_Value
            stb = True
    except Exception as e:
        returnstr = "Speed Test Scan with error: " + e.__doc__
        print(returnstr)
        stb = True
        returnstr = False

    stbtime = 0

    print(returnstr, stb, stbtime)
    return (returnstr, stb, stbtime)

def Write():

    global readstrs
    global debug
    try:
        for comstr in readstrs:
            if debug:
                print("write to Speed Test: " + comstr)
        returnstr = "Write to Speed Test Completed"
    except Exception as e:
        returnstr = "Speed Test Write with error: " + e.__doc__
        print(returnstr)
        returnstr = False
    
    if debug:
        print(returnstr)
    return returnstr

def Read():
    returnstr = "%g" % (previous_value)
    try:
        for comstr in readstrs:
            readstr = "%g" %(random.random())
            if debug:
                print("read from Speed Test: " + readstr)
            returnstr = returnstr + ", " + readstr
    except Exception as e:
        returnstr = "Speed Test Read with error: " + e.__doc__
        print(returnstr)
        returnstr = False
    print(returnstr)
    return returnstr

def Close():

    returnstr = "Speed Test is closed"
    print(returnstr)
    return returnstr

def main():
    Initialize()
    Retrieve()
    starttime = datetime.datetime.now()
    itnum = 0
    for sv in array1D(0, 20, 0.1):
        (returnstr, stb, stbtime) = Scan(sv)
        Write()
        Read()
        itnum = itnum + 1
        if stb:
            while True:
                (returnstr, stb, stbtime) = Approach(sv)
                Write()
                Read()
                itnum = itnum + 1
                if stb:
                    break
        #sleep(0.05)
    endtime = datetime.datetime.now()
    pasttime = (endtime - starttime).microseconds
    print("Excecuted %g commands using time %gus, speed %gus/command" % (itnum, pasttime, pasttime/itnum))
    Close()

if __name__ == '__main__':
    main()
