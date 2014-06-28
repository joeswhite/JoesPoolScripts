 Version 0.002 Alpha


 Multipool notifier
 notifies you via email (or text if you have text to email) when multipool.in is
 taking >50% of the network, or goes over a certain percentage of the total network hashrate on a coin
 adds their data to a database for future reference
 will give updates once an hour if they are online

 Requires freicoin.us to be online to parse the network hashrates.

 Copyright 2014 Joe White joe@freicoin.us
 
 FRC & BTC donation: 1FRCJoeWXbYe47cmuW3do8VoqAr9HuWbpJ

 Released under the AGPL license
 Released on June 28th, 2014

To run notifier:
edit multipool_high_hashrate_notifier.py configuration section with notification email address, 
email addresses to send to, email type. 

run start.sh in screen, once a minute it will check to see if there are


Why did i make this script? Simple, so when I'm not right at a computer I know when multipool is hash-n-dashing on freicoin.