
from datetime import datetime
import Logger
import sys
import imp
import sqlite3
from time import gmtime, strftime

createDB = sqlite3.connect("myDatabase")

query = createDB.cursor()
query.execute('SELECT SQLITE_VERSION() ')
data = query.fetchone()
         
bID = 1
buildings = query.execute('SELECT * FROM piServer_building WHERE id = %s' % bID)
for building in buildings:
        owner = building[2]
        print ("YO I AM PRINT THE OWNER I THINK %s" ,owner)
users = query.execute('SELECT * FROM piServer_userprofile WHERE user_id = %s' % owner)
def flipState(oID):
	outlet = query.execute('SELECT * FROM piServer_outlet WHERE id = %s' % oID)
	outletNewState = outlet[0].state
	query.execute('UPDATE piServer_outlet SET state = ? WHERE id = ?',(outletNewState,outlet[0].id))
        createDB.commit()
	#call hardware code to actually flip
	#if actual flip was successful
	print "YO STATE CHANGE"
	#log(user.lastAddress, user.username, "".join(["Outlet ", outlet.outletName, " was switched from ", "off" if outlet.state else "on", " to ", "on" if outlet.state else "off"]), 0)
	#else
	#log(user.lastAddress, user.username, "".join(["Outlet ", outlet.outletName, " was not switched due to a hardware error"]), 1)
def checkAlarms():
        alarms = query.execute('SELECT * FROM piServer_alarm WHERE id = %s' % bID)
	for alarm in alarms:
                startTime = alarm[5]
                print "Checked an Alarm"
		if startTime == None:
			checkTimer(alarm)
		else:
			checkAlarm(alarm)
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
		outlets = query.exectue('SELECT * FROM piServer_outlet WHERE id = ?',oID)
                for outlet in outlets:
                        state = outlet[3]
                        if state is not alarm[7]:
                                flipState(oID)
                                logAlarm(alarm[0], true)
                        else:
                                logAlarm(alarm[0], false)
		#alarm.delete()
def killServer():
        buildings = query.execute('SELECT * FROM piServer_building WHERE id = ?',bID)
        for building in buildings:
                if building["onlineState"] is False:
                        users2 = ('SELECT * FROM piServer_building WHERE user_id = ?',owner)
                        for user2 in users2:
                                lastAddress = user2[4]
                        log(lastAddress, username, "The building associated with these alarms is no longer online... Shutting down", 0)
                        sys.exit("The building associated with these alarms is no longer online... Shutting down")
