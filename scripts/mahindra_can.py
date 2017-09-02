#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import canlib.canlib as canlib
import time
import thread
global char
char = 'b'
status= "start"
R_flag=0
L_flag=0
H_flag=0

def setUpChannel(channel=0,
                 openFlags=canlib.canOPEN_ACCEPT_VIRTUAL,
                 bitrate=canlib.canBITRATE_500K,
                 bitrateFlags=canlib.canDRIVER_NORMAL):
    cl = canlib.canlib()
    ch = cl.openChannel(channel, openFlags)
    print("Using channel: %s, EAN: %s" % (ch.getChannelData_Name(),
                                          ch.getChannelData_EAN()))
    ch.setBusOutputControl(bitrateFlags)
    ch.setBusParams(bitrate)
    ch.busOn()
    return ch

def tearDownChannel(ch):
    ch.busOff()
    ch.close()

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    global char
    global status
    global H_flag
    global L_flag
    global R_flag
    if data.data == "W_ON":
        char = "W_ON"
    elif data.data == "LI_ON":
        char = "LI_ON"
	L_flag=1
    elif data.data == "RI_ON":
        char = "RI_ON"
	R_flag=1
    elif data.data == "H_ON":
        char = "H_ON"
	H_flag=1
    elif data.data == "W_OFF":
         char = "W_OFF"
    elif data.data == "LI_OFF":
         char = "LI_OFF"
	 R_flag=0
    elif data.data == "RI_OFF":
        char = "RI_OFF"
	R_flag=0
    elif data.data == "H_OFF":
        char = "H_OFF"
	H_flag=0
    if data.data=="start":
        status="start"
    elif data.data=="stop":
        status="stop"

def listener(delay):
    rospy.init_node('subscribe', anonymous=True)
    rospy.Subscriber("chatter", String, callback)
    print delay
    #time.sleep(delay/1000)
    rospy.spin()

def c_send():
   global char
   global H_flag
   global R_flag
   global L_flag
   while (1):
       if status=="start":
           '''
           if char  == "W_ON":
               msgId = 0x76E
               msg = [0, 0, 0,0,0,0,0,127]
               flg = canlib.canMSG_STD     #use canlib.canMSG_EXT for using extended arbitration ID 18 bits
               ch0.write(msgId, msg, flg)
           elif char  == "W_OFF":
               msgId = 0x76E
               msg = [0, 0, 0,0,0,0,0,0]
               flg = canlib.canMSG_STD     #use canlib.canMSG_EXT for using extended arbitration ID 18 bits
               ch0.write(msgId, msg, flg)
           if char == "LI_ON":
               msgId = 0x776
               msg = [0,0,0,0,0,0,0,8]
               flg = canlib.canMSG_STD
               ch0.write(msgId, msg, flg)
           elif char == "LI_OFF":
               msgId = 0x776
               msg = [0,0,0,0,0,0,0,0]
               flg = canlib.canMSG_STD
               ch0.write(msgId, msg, flg)
           elif char =="RI_ON":
               msgId = 0x776
               msg = [0,0,0,0,0,0,0,127]
               flg = canlib.canMSG_STD
               ch0.write(msgId, msg, flg)
           elif char =="RI_OFF":
               msgId = 0x776
               msg = [0,0,0,0,0,0,0,0]
               flg = canlib.canMSG_STD
               ch0.write(msgId, msg, flg)
           if char == "H_ON":
               msgId = 0x776
               msg = [0,0,0,0,0,0,32,11]
               flg = canlib.canMSG_STD
               ch0.write(msgId, msg, flg)
           elif char == "H_OFF":
               msgId = 0x776
               msg = [0,0,0,0,0,0,32,9]
               flg = canlib.canMSG_STD
               ch0.write(msgId, msg, flg)'''
	   if H_flag:
		   msgId = 0x776
		   msg = [0,0,0,0,0,0,32,13]
		   flg = canlib.canMSG_STD
		   ch0.write(msgId, msg, flg)
	   else:
		   msgId = 0x776
		   msg = [0,0,0,0,0,0,32,9]
		   flg = canlib.canMSG_STD
		   ch0.write(msgId, msg, flg)
	   if R_flag:
		msgId2 = 0X774
  	        msg2 = [0,0,0,0,0,0,216,130]
	        flg2 = canlib.canMSG_STD
	        ch0.write(msgId2, msg2, flg)
	   elif L_flag:
		msgId2 = 0X774
  	        msg2 = [0,0,0,0,0,0,216,129]
	        flg2 = canlib.canMSG_STD
	        ch0.write(msgId2, msg2, flg)
	   else:
	        msgId2 = 0X774
  	        msg2 = [0,0,0,0,0,0,216,1]
	        flg2 = canlib.canMSG_STD
	        ch0.write(msgId2, msg2, flg)
           msgId1 = 0X778
	   msg1 = [0,0,0,0,0,0,36,0]
	   flg1 = canlib.canMSG_STD
	   ch0.write(msgId1, msg1, flg)

           msgId3 = 0X772
	   msg3 = [0,0,0,0,0,0,0,1]
	   flg3 = canlib.canMSG_STD
	   ch0.write(msgId3, msg3, flg)
           msgId4 = 0X770
	   msg4 = [0,0,0,0,0,0,0,1]
	   flg4 = canlib.canMSG_STD
	   ch0.write(msgId4, msg4, flg)
           msgId4 = 0X76D
	   msg4 = [0,0,0,0,0,0,0,40]
	   flg4 = canlib.canMSG_STD
	   ch0.write(msgId4, msg4, flg)

       time.sleep(10/1000)
def c_recieve():
    while True:
        try:
            (msgId, msg, dlc, flg, time) = ch0.read()
            data = ''.join(format(x, '02x') for x in msg)
            '''print("time:%9d id:%9d  flag:0x%02x  dlc:%d  data:%s" %
            (time, msgId, flg, dlc, data))'''
            if msgId == 0x76C:
                if data[13]=='1':
                    print "Velocity : " , int(data[14])*16 + int(data[15])
                else:
                    print "Invalid velocity"
        except:
            pass
if __name__ == '__main__':
    cl = canlib.canlib()
    print("canlib version: %s" % cl.getVersion())


    channel_0 = 0
    ch0 = setUpChannel(channel=0)
    thread.start_new_thread( c_send , ())
    thread.start_new_thread( c_recieve , ())
    listener(10)


    #while 1:
        #pass
    tearDownChannel(ch0)
