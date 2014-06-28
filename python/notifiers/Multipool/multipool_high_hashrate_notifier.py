#!/usr/bin/python

#
# Version 0.001 Pre-Alpha
#
# Known Bugs: Email Headers not sent correctly
#
# Multipool notifier
# notifies you via email (or text if you have text to email) when multipool.in is
# taking >50% of the network, or goes over a certain percentage of the total network hashrate on a coin
# adds their data to a database for future reference
# will give updates once an hour if they are online
#
# Requires freicoin.us to be online to parse the network hashrates.
#
# Copyright 2014 Joe White joe@freicoin.us
# 
# FRC & BTC donation: 1FRCJoeWXbYe47cmuW3do8VoqAr9HuWbpJ
#
# Released under the AGPL license
# Released on June 28th, 2014

# Requires smtplib, urllib2, json and twisted (for ease of on screen logging)

# START CONFIGURATION OPTIONS

#names and emails of persons to notify of multipool hash-n-dash
notifyNameOne = "Joe"
notifyEmailOne = "joe@FreiCoin.US"
#emailType signifies if you want a short or long form email (0 for short, 1 for long)
emailTypeOne = 1

#this is ususally a cell
notifyNameTwo = "Joe Cell"
notifyEmailTwo = "5705555555@vtext.com"
#emailType signifies if you want a short or long form email (0 for short, 1 for long)
emailTypeTwo = 0


# you can create as many of these as you want, just make sure to update the email().sendEmail... and logging info to be good to go
#notifyNameThree = "name"
#notifyEmailThree = "email"
#emailTypeThree = 1

#name and email the messages come from
senderName = "Multipool Alerts"
senderEmail = "hash-n-dash@freicoin.us"

# ticker letters for coin. eg frc for freicoin doge for dogecoin btc for bitcoin
# MUST BE LOWER CASED!
coinToWatch = "frc"

# END CONFIGURATION OPTIONS

# START CODE
# DO NOT CHANGE BELOW!

import smtplib
import urllib2
import json
from twisted.python import log


class email:
	def __init__(self):
			self.x = 'Hi'
	
	def sendEmail(self, sender, receiver, receiverName, senderName, emailType, level, multipoolHash, multipoolRate, totalNetwork, knownNetworkMinusMultipool):
		#emailType is 1 for long, 0 for sms friendly short

		#check if we want to use the long email alert tempate, if not we will use the small one
		if str(emailType) == str('1'):
			#tell the user that the email is long format
			print 'Long format email being sent'

			#The actual email message and header construction
			message = """From: """ + str(senderName) + """ <""" + str(senderEmail) + """>
			To: """ + str(receiverName) + """ <""" + str(receiver) + """> 
			Subject: Alert """ + str(multipoolHash) + """% of network controlled by Multipool

			Hello,
			Multipool is """ + str(multipoolHash) + """% of the network!
			Multipool Hashrate:  """ + str(multipoolRate  / 100) + """TH/s

			Network Hashrate:  """ + str(totalNetwork / 100) + """TH/s
			Non-Multipool pools total:  """ + str(knownNetworkMinusMultipool / 100) + """TH/s

			Threat Level: """ + str(level) +""" (1-7 the smaller the number higher risk)
			"""
		else:
                        #tell the user that the email is long format
                        print 'Short format email being sent'

                        #The actual email message and header construction
			message = """From: """ + str(senderName)+ """ <""" + str(senderEmail) + """>
			To: """ + str(receiverName) + """ <""" + str(receiver) + """> 
			Subject: Alert """ + str(multipoolHash) + """% of network controlled by Multipool

			LVL: """ + str(level) + """
			MP: """ + str(multipoolHash) + """%
			HR: """ + str(multipoolRate) + """TH/s
			NET HR: """ + str(totalNetwork) + """TH/s
			POOLS: """ + str(knownNetworkMinusMultipool) + """TH/s"""


		print message
		try:
			smtpObj = smtplib.SMTP('localhost')
			smtpObj.sendmail(sender, receiver, message)         
			print "Sending email"
			success = 1

		except SMTPException:
			print "Error: unable to send email"
			success = 0

		finally:
			if success == 1:
				print 'Successfully sent email to ' + str(receiver)
			

class apiCalls:
	def __init__(self):
			self.x = 'Hi'
			
	def joesApi(self, coin):

		#set variables
		info = 0 #set to 0 because it will be used later and needs to be defined

		#parse knownpools json string to get pool+network reported hashrate
		joesTicker = urllib2.urlopen('http://freicoin.us/knownpools.php')
		joesTicker_obj = json.load(joesTicker)

		#total known network hashrates (this doesn't need to be perfect because we just want to know when multipool is about to hash-n-dash 
		totalNetwork = float(joesTicker_obj['Network Total'])

                #hashrate of multipool
                multipoolRate = float(joesTicker_obj['Multipool'])

		#multipool's hashrate is subtracted from the total power of the known network pools
		knownNetworkMinusMultipool = float(float(totalNetwork) - float(multipoolRate))

		#now we are getting the percentage of the network that everyone else is vs total known network
		knownPoolsPercentage = float(knownNetworkMinusMultipool) / float(totalNetwork) * float(100)

		#figuring out multipool's percentage of the network. Round it to 4 decimal places, we don't really need more but we could do it...
		multipoolHash = round(float((float(100) - float(knownPoolsPercentage))), 4 )

		#Set the thread level, 7(least risk) - 1 (danger above 99% of the network)
		level = 7

		#using decimals vs percentages for ease of coding
		if multipoolHash >= 50: #50% of network notify on screen but wait as it could be a fluke or they could have a few dedicated miners not on the "multiport"
			print 'Here comes multipool, they are at ' + str(float(multipoolRate) / float(100)) + 'TH/s! They are ' + str(multipoolHash) + '% of the known network'

			#level is the level of the attack (how bad is it). Are they more than the rest of the network? and how much more?
			level = 6
			if multipoolHash >= 75:
				level = 5
				print '\nThey are really coming now!'

				#if hashrate is above 80% of the total network
				if multipoolHash >= 80:
					level = 4

                                #if hashrate is above 90% of the total network
				if multipoolHash >= 90:
					level = 3

                                #if hashrate is above 95% of the total network
				if multipoolHAsh >= 95:
					level = 2

                                #if hashrate is above 99% of the total network
				if multipoolHAsh >= 99:
					level = 1

			#print threat level
			print 'Threat level ' + str(level)

			#call sendEmail function to send email to the first alert address, it is a regular email address so we pass 0 to let our emailer know the format
			print '\nSending email to ' + notifyEmailOne
			email().sendEmail(senderEmail, notifyEmailOne, notifyNameOne, senderName, int(emailTypeOne), level, multipoolHash, multipoolRate, totalNetwork, knownNetworkMinusMultipool)


			#call sendEmail function to send email to the second alert address
			print 'Sending email to ' + notifyEmailTwo
                        email().sendEmail(senderEmail, notifyEmailTwo, notifyNameTwo, senderName, int(emailTypeTwo), level, multipoolHash, multipoolRate, totalNetwork, knownNetworkMinusMultipool)

			#you can send this email to as many addresses as you want, just change the email().sendEmail... Line to reflect emailTypeThree, notifyNameThree, etc

		return level, multipoolHash, multipoolRate, totalNetwork, knownNetworkMinusMultipool
		


if __name__ == "__main__":

	#running the application from the classes/functions is really this easy!
	apiCalls().joesApi(coinToWatch)