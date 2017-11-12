#!/usr/bin/env python
import roslib; roslib.load_manifest('assign4')
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math
import matplotlib.pyplot as plt

global ip
global ip1
ip=[]
ip1=[]
pub=rospy.Publisher('/robot/cmd_vel',Twist,queue_size=5)


# definition of normal curve
def gauss (x, mu, sigma):
    exp= 0 - (((float(x)-float(mu))** 2) / (2 * float(sigma) * float(sigma)))
    return (1/(float(sigma) * math.sqrt(2*math.pi))) * (math.e ** exp)

# this experimentally approximates door sensor performance
def door(mu, x):
    sigma= .75
    peak= gauss(0, 0, sigma)   
    return 0.8 * gauss(x, mu, sigma)/peak

# doors are centered at 11m, 18.5m, and 41m
def p_door(x):
    return 0.1 + door(11, x) + door(18.5, x) + door(41, x)

def p_wall(x):
    return 1.0 - p_door(x)

def talker(data):
	print data.data	
	sum=0
	msg = Twist()
	msg.linear.x=4
	pub.publish(msg)
	for a in range(0,599):
		temp=ip[a]
		ip[a]=0
		for b in range(a,a+4):
			ip[b] += temp *gauss(b-a,msg.linear.x,4/3)
	for i in range(0,599):
		if data.data =='door':
			ip[i]=ip[i]*p_door(i/10)
		else:
			ip[i]=ip[i]*p_wall(i/10)		
		sum=sum+ip[i]
	for j in range(0,599):
		ip[j]=ip[j]/sum
	for k in range(0,599):
		if ip[k] > 0:
			ip1[k]='%.6f *'%ip[k]
		else:
			ip1[k]='_'
	#print ip	
	print ip1
	
			
			
def listener():
	rospy.init_node('ListenerTalker',anonymous=True)
	rospy.Subscriber('/robot/wall_door_sensor', String,talker)
	rospy.spin()

if __name__=='__main__':
	for i in range(0,599):
		ip.append(1.0/600.0)
		ip1.append(0)
	for j in range(600,610):
		ip.append(0)
	listener()
