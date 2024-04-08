from Phidget22.Phidget import *
from Phidget22.Devices.RFID import *
from Phidget22.Devices.DigitalOutput import *
import sqlite3

con=sqlite3.connect('rfid.db', check_same_thread=False)
cur=con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Tickets (names, tags);")
print("Table Created : Tickets")

cur.execute("Select Tickets.names, Tickets.tags FROM Tickets;")
tags=cur.fetchall()


digitalOutput2 = DigitalOutput()


def onTag(self, tag, protocol):
	verified=0
	userName=''
	for users in tags:
		if str(tag)==users[1]:
			verified=1
			userName=users[0]
	if verified:
		print("Ticket verified for "+userName)
		digitalOutput2.setState(1)
		print("----------")
	else:
		print("Ticket not valid!")
		print("----------")
	#print("Tag: " + str(tag))
	#print("Protocol: " + RFIDProtocol.getName(protocol))
	
	

	

def onTagLost(self, tag, protocol):
	print("Tag lost!")
	digitalOutput2.setState(0)

def onAttach(self):
	print("Attach!")

def onDetach(self):
	print("Detach!")

def main():
	rfid0 = RFID()
	
	rfid0.setDeviceSerialNumber(385105)
	digitalOutput2.setDeviceSerialNumber(385105)
	digitalOutput2.setChannel(2)

	rfid0.setOnTagHandler(onTag)
	rfid0.setOnTagLostHandler(onTagLost)
	rfid0.setOnAttachHandler(onAttach)
	rfid0.setOnDetachHandler(onDetach)

	rfid0.openWaitForAttachment(5000)
	digitalOutput2.openWaitForAttachment(5000)
	digitalOutput2.setState(0)
	

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	rfid0.close()
	digitalOutput2.close()

main()