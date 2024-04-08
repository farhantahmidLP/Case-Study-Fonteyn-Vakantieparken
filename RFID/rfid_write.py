from Phidget22.Phidget import *
from Phidget22.Devices.RFID import *
from Phidget22.Devices.DigitalOutput import *
import time

digitalOutput2 = DigitalOutput()
rfid0 = RFID()

def onAttach(self):
	print("Attach!")

def onDetach(self):
	print("Detach!")

def main():
	
	
	rfid0.setDeviceSerialNumber(385105)
	digitalOutput2.setDeviceSerialNumber(385105)
	digitalOutput2.setChannel(2)
	
	rfid0.setOnAttachHandler(onAttach)
	rfid0.setOnDetachHandler(onDetach)

	rfid0.openWaitForAttachment(5000)
	digitalOutput2.openWaitForAttachment(5000)
	digitalOutput2.setState(0)
	rfid0.write("12345678ab",RFIDProtocol.PROTOCOL_EM4100,False)
	digitalOutput2.setState(1)
	time.sleep(5)
	rfid0.close()
	digitalOutput2.close()

main()