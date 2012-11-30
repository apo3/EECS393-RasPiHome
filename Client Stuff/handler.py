
from datetime import datetime
import Logger
import sys
import imp
import sqlite3
import os
from time import gmtime, strftime

createDB = sqlite3.connect("myDatabase")

query = createDB.cursor()
query.execute('SELECT SQLITE_VERSION() ')
data = query.fetchone()
         
bID = 1
buildings = query.execute('SELECT * FROM piServer_building WHERE id = %s' % bID)
for building in buildings:
        owner = building[2]
        print ("Server is running for building ID: %s" ,owner)
users = query.execute('SELECT * FROM piServer_userprofile WHERE user_id = %s' % owner)
def flipState(oID):
        count = 0
	outlet1 = query.execute('SELECT * FROM piServer_outlet WHERE buildingID_id = %s' % oID)
        for outlet in outlet1:
                count = count + 1
                print "Hey"
                if count == oID:
                        state = outlet[3]
                        print state
        #print "DATA %s" % data
        
	outletNewState = state
	outlets = query.execute('SELECT * FROM piServer_outlet WHERE buildingID_id = %s' % bID)
	query.execute('UPDATE piServer_outlet SET state = ? WHERE id = ?',(outletNewState,oID))
        createDB.commit()
        outletOneState = 2
        outletTwoState = 0
        outletThreeState = 0
        string = ""
        for outlet in outlets:
                if outlet[0]:
                        outletOneState = outlet[3]
                if outlet[1]:
                        outletTwoState = outlet[3]
                if outlet[2]:
                        outletThreeState = outlet[3]
        if oID == 1:
                string = '"C:\Program Files\PowerUSB\PwrUsbCmd.exe" 1 ' + str(outletTwoState) + " " + str(outletThreeState) 
        if oID == 2:
                string = '"C:\Program Files\PowerUSB\PwrUsbCmd.exe" ' + outletOneState + " 1 " + outletThreeState
        if oID == 3:
                string = '"C:\Program Files\PowerUSB\PwrUsbCmd.exe" ' + outletsOneState + " " + outletTwoState + " 1"
        #cmd = str(string)
        #print cmd
        print string
        os.system(string)
	#log(user.lastAddress, user.username, "".join(["Outlet ", outlet.outletName, " was switched from ", "off" if outlet.state else "on", " to ", "on" if outlet.state else "off"]), 0)
	#else
	#log(user.lastAddress, user.username, "".join(["Outlet ", outlet.outletName, " was not switched due to a hardware error"]), 1)
def checkAlarms():
        alarms = query.execute('SELECT * FROM piServer_alarm WHERE buildingID_id = %s' % bID)
	for alarm in alarms:
                startTime = alarm[5]
                print "Checked an Alarm %s",startTime
		if startTime == None:
			checkTimer(alarm)
		else:
			checkAlarm(alarm)
def checkOutlets():
        outlets = query.execute('SELECT * FROM piServer_outlet')
        string = "C:\Program Files\PowerUSB\PwrUsbCmd.exe "
        count = 0
        for outlet in outlets:
                outletState = outlet
                count = count + 1
                if outletState == True:
                        stringAdd = "1"
                if outletState == False:
                        stringAdd = "0"
                string = string + stringAdd
                if count < 3:
                        string = string + " "
        os.system(string)
def checkTimer(timer):
	if datetime.datetime.now() >= timer.endTime:
		flipState(timer.outletID)
		#logTimer(timer.pk)
		#timer.delete()
def checkAlarm(alarm):
        #print alarm[6]
        now = datetime.now()
        time = alarm[6]
        #print now
	if now >= datetime.strptime(time, '%Y-%m-%d %H:%M:%S'):
                oID = alarm[3]
                int(oID)
                print oID
		outlets = query.execute('SELECT * FROM piServer_outlet WHERE id = %s' % oID)
                for outlet in outlets:
                        state = outlet[3]
                        if state is not alarm[7]:
                                flipState(oID)
                                #logAlarm(alarm[0], true)
                        #else:
                                #logAlarm(alarm[0], false)
		#alarm.delete()
def killServer():
        #buildings = query.execute('SELECT * FROM piServer_building WHERE id = ?',bID)
        #for building in buildings:
                #if building["onlineState"] is False:
                        #users2 = ('SELECT * FROM piServer_building WHERE user_id = ?',owner)
                        #for user2 in users2:
                        #        lastAddress = user2[4]
                        #log(lastAddress, username, "The building associated with these alarms is no longer online... Shutting down", 0)
         sys.exit("The building associated with these alarms is no longer online... Shutting down")
