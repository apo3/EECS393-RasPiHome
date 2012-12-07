import sys
import Logger
import os
import sqlite3
import imp
import handler
import sched, time
#The Runner is for starting the handler services while the Website Server is
#currently online. If the server is offline something must be wrong so we no longer
#want to change states remotely.


#h = handler()
#handler = imp.load_source('Handler','C:\Users\Cimara\Documents\GitHub\EECS393-RasPiHome\Client Stuff\handler.py')
s = sched.scheduler(time.time, time.sleep)
#def dostuff(sc):
#    handler.checkAlarms()
#    sc.enter(10,1, dostuff, (sc,))
#    Logger.inputInvalid("Testing the Logger!")
    #sc.enter(13,1, dostuff2, (sc,))
def dostuff2(sc):
    handler.checkAlarms()
    handler.checkOutlets()
    #handler.flipState(2)
    #handler.flipState(3)
    sc.enter(2,1, dostuff2, (sc,))
#s.enter(10,1,dostuff,(s,))
s.enter(2,1,dostuff2,(s,))
s.run()
