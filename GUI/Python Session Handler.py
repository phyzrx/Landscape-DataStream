# Put this file under the same path of the Landscape DataStream GUI
# This file decribe the operation to terminate Python sessions using its PID code called by Landscape DataStream Data Acquisition GUI
# Due to the limitation of os.kill() under win32, this function will terminate the whole session instead of sending a KeyBoardInteruption

import os
import signal
import psutil #pip install psutil

def Call():
    returnstr = "Python Session Handler Called"
    print(returnstr)
    return 0

def ValidSig():
    print("Valid Signals:")
    print(signal.valid_signals())
    return 0

def GetPID():
    pid = os.getpid()
    returnstr = "Session PID %g" % (pid)
    print(returnstr)
    return pid

def Stop(pid):
    os.kill(pid, signal.CTRL_C_EVENT)
    #os.kill(pid, signal.CTRL_BREAK_EVENT)
    #os.kill(pid, signal.SIGINT)
    #os.kill(pid, signal.SIGFPE)
    #os.kill(pid, signal.SIGTERM)
    #os.kill(pid, signal.SIGBREAK)
    #os.kill(pid, signal.SIGABRT)
    #os.kill(pid, 2)
    #process = psutil.Process(pid)
    #process.terminate()
    sleep(600)
    returnstr = "Killed Session PID %g" % (pid)
    print(returnstr)
    return 0

def PrintPID(pid):
    pidname = psutil.Process(pid).name()
    print("%s Session PID %g" % (pidname, pid))
    return 0

def main():
    Call()
    ValidSig()
    return 0

if __name__ == '__main__':
    main()
