#The Handler will be responsible for taking care of changes in the database
#when an outlets state is modified from an alarm.
from datetime import datetime
import Logger
import sys
import imp
import sqlite3
import os
from time import gmtime, strftime

#Import and create a connection to the databae.
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

#This function is for checking the state of an outlet
#It is used so useless calls to the DB will not called.
def checkOutlet():
        count = 0
	outlets = query.execute('SELECT * FROM piServer_outlet WHERE buildingID_id = %s' % bID)        
        outletOneState = 0
        outletTwoState = 0
        outletThreeState = 0
        string = ""
        for outlet in outlets:
                if outlet[0] == 1:
                        outletOneState = outlet[3]
                if outlet[1] == 2:
                        outletTwoState = outlet[3]
                if outlet[2] == 3:
                        outletThreeState = outlet[3]
                print outlet[3]
        #if outletNewState == True: ALL CODE COMMENTED OUT IS LEFT IN TO REFERENCE FOR FUTURE CHANGES
        #        outletNewStateInt = 1
        #else:
        #        outletNewStateInt = 0
        #if oID == 1:
        string = '"C:\Program Files\PowerUSB\PwrUsbCmd.exe" ' + str(outletOneState) + " " + str(outletTwoState) + " " + str(outletThreeState) 
        #if oID == 2:
        #        string = '"C:\Program Files\PowerUSB\PwrUsbCmd.exe" ' + str(outletOneState) + " " + str(outletTwoState) + " " + str(outletThreeState)
        #if oID == 3:
        #       string = '"C:\Program Files\PowerUSB\PwrUsbCmd.exe" ' + str(outletOneState) + " " + str(outletTwoState) + " " + str(outletThreeState)
        #cmd = str(string)
        #print cmd
        print string
        #Make the CMD call to change the hardware state.
        os.system(string)
#Flip State is used by checkAlarm and checkTimer
#to make sure a state is changed when the alarm/timer is completed.
def flipState(oID):
        count = 0
	outlet1 = query.execute('SELECT * FROM piServer_outlet WHERE buildingID_id = %s' % bID)
        for outlet in outlet1:
                count = count + 1
                print "Hey"
                if count == oID:
                        state = outlet[3]
                        print state
        #print "DATA %s" % data
        
	outletNewState = not state
	print state
	outlets = query.execute('SELECT * FROM piServer_outlet WHERE buildingID_id = %s' % bID)
	query.execute('UPDATE piServer_outlet SET state = ? WHERE id = ?',(outletNewState,oID))
        createDB.commit()
        outletOneState = 0
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
        print outletNewState
        if outletNewState == True:
                outletNewStateInt = 1
        else:
                outletNewStateInt = 0
        if oID == 1:
                string = '"C:\Program Files\PowerUSB\PwrUsbCmd.exe" ' + str(outletNewStateInt) + " " + str(outletTwoState) + " " + str(outletThreeState) 
        if oID == 2:
                string = '"C:\Program Files\PowerUSB\PwrUsbCmd.exe" ' + outletOneState + " 1 " + outletThreeState
        if oID == 3:
                string = '"C:\Program Files\PowerUSB\PwrUsbCmd.exe" ' + outletsOneState + " " + outletTwoState + " 1"
        #cmd = str(string)
        #print cmd
        print string
        #Make the CMD call to change the hardware.
        os.system(string)
	#log(user.lastAddress, user.username, "".join(["Outlet ", outlet.outletName, " was switched from ", "off" if outlet.state else "on", " to ", "on" if outlet.state else "off"]), 0)
	#else
	#log(user.lastAddress, user.username, "".join(["Outlet ", outlet.outletName, " was not switched due to a hardware error"]), 1)
def checkAlarms():
        #This function checks the ALARMS table in the DB
        #This will then call the correct function to handle the timer or alarm.
        alarms = query.execute('SELECT * FROM piServer_alarm WHERE buildingID_id = %s' % bID)
	for alarm in alarms:
                startTime = alarm[5]
                print "Checked an Alarm %s",startTime
		if startTime == None:
			checkAlarm(alarm)
		else:
			checkTimer(alarm)
def checkOutlets():
        #This is for updating an outlets state if it has changed by user input
        outlets = query.execute('SELECT * FROM piServer_outlet')
        string = '"C:\Program Files\PowerUSB\PwrUsbCmd.exe" '
        count = 0
        for outlet in outlets:
                outletState = outlet[3]
                count = count + 1
                if outletState == True:
                        stringAdd = "1"
                if outletState == False:
                        stringAdd = "0"
                string = string + stringAdd
                if count < 3:
                        string = string + " "
        print "This is the input String: "+ string
        #Make the call to change the hardware to match the DB
        os.system(string)
def checkTimer(timer):
        #Checks if its time for an outlet to change based on a Timer.
	if datetime.strptime(time, '%Y-%m-%d %H:%M:%S'):
		flipState(timer.outletID)
		#logTimer(timer.pk)
def checkAlarm(alarm):
        #Check an alarm and compares the time to now then changes state if needed
        aID = alarm[0]
        #print alarm[6]
        now = datetime.utcnow()
        time = alarm[6]
        print "in checkAlarm"
        print time
        
        #now = strptime(gmtime(),'%Y-%m-%d %H:%M:%S')
        print now
	if now >= datetime.strptime(time, '%Y-%m-%d %H:%M:%S'):
                print "in the IF"
                oID = alarm[3]
                int(oID)
                print oID
		outlets = query.execute('SELECT * FROM piServer_outlet WHERE id = %s' % oID)
                for outlet in outlets:
                        state = outlet[3]
                        if state is not alarm[7]:
                                flipState(oID)
                query.execute('DELETE FROM piServer_alarm WHERE id = %s' % aID)
                createDB.commit()
                                #logAlarm(alarm[0], true)
                        #else:
                                #logAlarm(alarm[0], false)
#Kill server is now handled elsewhere.
#def killServer():
        #buildings = query.execute('SELECT * FROM piServer_building WHERE id = ?',bID)
        #for building in buildings:
                #if building["onlineState"] is False:
                        #users2 = ('SELECT * FROM piServer_building WHERE user_id = ?',owner)
                        #for user2 in users2:
                        #        lastAddress = user2[4]
                        #log(lastAddress, username, "The building associated with these alarms is no longer online... Shutting down", 0)
         sys.exit("The building associated with these alarms is no longer online... Shutting down")
