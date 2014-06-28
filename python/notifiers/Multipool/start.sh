#!/bin/bash
# simple script to run the notifier, run in screen to have it as a daemon
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
#set to time in minutes to sleep, don't go less than 1 minute, it's futile as the knownpools api only updates once per minute
sleepTime = 1

#DON'T CHANGE BELOW
#loop until we break the loop but killing the script
for (( ; ; ))
do
        python multipool_high_hashrate_notifier.py
        #after the process is done, i sleep for 1 minute, any more and there's no point as the knownpools api won't update
		sleep $((($sleepTime) * 60))
done

