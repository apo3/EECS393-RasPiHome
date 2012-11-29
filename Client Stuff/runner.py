import sys
import Logger
import os
import sqlite3
import imp
import handler
import sched, time

#h = handler()
#handler = imp.load_source('Handler','C:\Users\Cimara\Documents\GitHub\EECS393-RasPiHome\Client Stuff\handler.py')
s = sched.scheduler(time.time, time.sleep)
def dostuff(sc):
    handler.checkAlarms()
    sc.enter(10,1, dostuff, (sc,))
    Logger.inputInvalid("Testing the Logger!")
s.enter(10,1,dostuff,(s,))
s.run()
