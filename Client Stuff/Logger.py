from datetime import datetime
import sys
import imp
import sqlite3
#to user the logger class effectively import imp
#and do the following line of code:
#   log =  imp.load_source('Logger', 'logger.py location')
#This should allow logger to be used easily. by making calls like:
#   log.log("0.0.0.0",bob,"I just turned something on.",0)
#in the code. These logging functions should not be seen by the user unless the Log.txt
#file is opened.

createDB = sqlite3.connect("myDatabase")

query = createDB.cursor()
#location will just be directly on the Pi when we can do that.
bID = 1
location = 'C:\\Users\\Cimara\\Documents\\GitHub\\EECS393-RasPiHome\\Client Stuff\\test.txt' #this is the location I currently am using
def logAlarm(aID, wasFlipped):
    a = query.execute('SELECT alarm FROM piServer_alarm WHERE id = ?', aID)
    f = open(location, "a")
    timeStamp = datetime.datetime.now()
    f.write(timeStamp)
    f.write(a)
    f.write(" ")
    f.write(wasFlipped)
    f.close()
def logTimer(aID):
    a = query.execute('SELECT alarm FROM piServer_alarm WHERE id = ?', aID)
    f = open(location, "a")
    timeStamp = datetime.datetime.now()
    f.write(timeStamp)
    f.write(a)
    f.close()
def log(address,user,msg,flag):
    f = open(location, "a")
    if flag == 0:
        f.write("info")
    if flag == 1:
        f.write("error")
    if flag == 2:
        f.write("warning")
    if flag == 3:
        f.write("debug")
    f.write(address)
    f.write(user)
    f.write(msg)
    timeStamp = datetime.datetime.now()
    f.write(timeStamp)
    f.write("\n")
    f.close()
def inputInvalid(msg):
    f = open (location, "a")
    print location
    f.write("The following input was invalid")
    f.write(msg)
    f.close()
def killServer(address, user,msg,flag):
    self.log(address,user,msg,flag)
    sys.exit("The Website Server was killed remotely")
        #change server status to Down or OFF
        #serverstatus flag in a file??? or the DB?
def checkServerStatus():
        #check if the status is Down or OFF
    if server == 0:
        sys.exit("The Website Client Server is off... Shutting down")            
        
    
