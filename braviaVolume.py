"""
My first attempt at getting the Sony Bravia python RC working
Checks the time if it's during the day and the kids have the TV to 
loud it forces the volume down. 
 """
from bravia_tv import BraviaRC as BRC
import time

#Tv Details
ipadr = '192.168.0.157'
pin ='6679'
name ="Living Room TV"

#The Rules
start_mins = 6 * 60 # 6 am
stop_mins  = 19 * 60  # 7 pm
max_vol = 18
set_vol = max_vol/100.0
poll_time = 20
power_wait_time = 600
trip_limit = 10 # if the volume is back up for n times I'll set it to zero
def getMins():
	""" Gets the minutes of day """
	t = time.gmtime()
	mins = t.tm_hour * 60 + t.tm_min
	return mins

def checkTimeWindow(t,tl,th):
	if t > tl  and  t < th:
		return True
	else:
		return False

def main():
	# connect to the tv, pin flashes on the screen the first time
	# you connect to the TV and is fixed from them on
	tv = BRC(ipadr)
	#make the inital connection
	tv.connect(pin, ipadr, name)
	power_status = tv.get_power_status()
	print (power_status)
	print(tv.is_connected())
	trip_flag = False
	trip_cnt = 0
	while True:
		t = getMins()
		now = time.asctime()
		if checkTimeWindow(t,start_mins, stop_mins) == False:
			if t > stop_mins:
				min_to_sleep = (24*60) - t + start_mins
			else:	
				min_to_sleep = (start_mins - t ) 
			print(now + " :: Outside if time window sleeping for %d minutes"% min_to_sleep)
			time.sleep(min_to_sleep * 60)
		else:
			
			#step one the tv could have been turned off so check if 
			#it's still connected.
			if tv.is_connected():
				power_status = tv.get_power_status()
				#step two is the tv on
				if power_status == 'active':
					#step 3 get and chech the volume
					volume_info = tv.get_volume_info()
					vol = volume_info['volume']
					print(now + " :: TV Volume : %d"%vol)
					if vol > max_vol:
						trip_flag = True
						print(now + " :: To Loud Lowering Volume")
						tv.set_volume_level(set_vol)
						trip_cnt += 1
						if trip_cnt >= trip_limit :
							tv.set_volume_level(0)
							
					else:
						print(now + ":: Volume	 OK no action needed")
						if trip_flag == False:
							trip_cnt -= 1
							if trip_cnt < 0: trip_cnt = 0
						trip_flag = False
						
					time.sleep(poll_time)
				else: 							 # the tv is in stand by so
					print(now + " :: TV off waiting 10 minutes")
					time.sleep(power_wait_time)  # wait ten minutes
			else:
				
				if tv.connect(pin, ipadr, name):
					# got a new connection will break or of if
					# and naturally loop back around
					pass
				else:          #connection filed
					print(now + " :: No Connection To TV foing to seep for 10 minutes")
					time.sleep(power_wait_time) # sleep for ten minutes


if __name__ == '__main__':
	main()
