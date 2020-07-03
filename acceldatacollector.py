'''
Fix serial Exception of multiple or disconnected 
device or empty buffer:
To manually change the settings, edit the kernel command line 
with ---sudo nano /boot/cmdline.txt---. Find the console entry that 
refers to the serial0 device, and remove it, including the baud 
rate setting. It will look something like console=serial0,115200. 
Make sure the rest of the line remains the same, as errors in 
this configuration can stop the Raspberry Pi from booting.

'''
import pickle
import time
import serial
import mpu6050
import os

m = mpu6050.mpu6050(0x68)

port = '/dev/ttyS0'
connection = serial.Serial(port,baudrate = 9600)
findwallavg = True
wall_distance_avg =[]
sample_time = 0.1
start_time = time.time()
prev_time = start_time
episode = []
previous_acc = m.get_accel_data()
previous_distance_tavelled = 0

def walldist(dist,no = 200):
	wall_distance_avg.append(dist)
	#print(wall_distance_avg)
	if len(wall_distance_avg) == no:
		#collect no samples but find average using last 100 vals
		avg = sum(wall_distance_avg)/no
		return avg



if not os.path.exists('data.pickle'):
	with open('data.pickle','wb') as file:
		pickle.dump([],file)
		print('new file init')
		file.close()

global all_data
with open('data.pickle','rb')as file:
	all_data = pickle.load(file)
	file.close()
print('loaded file',all_data)

while True:
	if connection.in_waiting>0:
		
			raw_data = connection.readline()
			distance = eval(raw_data)
			current_acc = m.get_accel_data()
			data = current_acc
			#data['distance'] = distance
			#print(distance)
			global wall_dist
			if findwallavg:
				
				wall_dist = walldist(distance)
				print(distance,wall_dist,'----> estimating avg swd')
				if wall_dist != None: #after wall_dist is returned
					findwallavg = False
					print('average wall distance found:',wall_dist)
					
			current_time = time.time()
			if not findwallavg:
		
				if current_time - prev_time >= sample_time:
					
					travel_dist = wall_dist - distance
					current_distance_travelled = travel_dist
					dt = current_time-prev_time
					travel_time = time.time()-start_time
					prev_time = current_time 
					
					dx = current_acc['x']-previous_acc['x']
					dy = current_acc['y']-previous_acc['y']
					dz = current_acc['z']-previous_acc['z'] 
					#print(current_acc,previous_acc,dx,dy,dz)
					previous_acc = current_acc
					
					
					data['travel_time'] = travel_time
					data['dt'] = dt
					data['travel_dist'] =travel_dist
					data['dx'] = dx
					data['dy'] = dy
					data['dz'] = dz
					data['d(travel_dist)'] = current_distance_travelled-previous_distance_tavelled
					data['v(t)'] = (current_distance_travelled-previous_distance_tavelled)/dt
					print('velocity:',data['v(t)'])
					previous_distance_tavelled = current_distance_travelled
					
					#print(dt,travel_time)
					#print('swd:',wall_dist,'tavel_distance','time:',travel_time)
					
					
					episode.append(data)
			
				    
					#print(len(episode))
					
					if len(episode) == 40:
						for a in episode: print(round(a['travel_dist'],2),round(a['travel_time'],2),round(a['dt'],2),round(a['x'],2),round(a['y'],2),round(a['z'],2))
						save = input('Save and append this data ? (y/n)  :')
						if save.lower() == 'y':
							all_data.append(episode)
							with open('data.pickle','wb') as file:
								pickle.dump(all_data,file)
							print('episode recorded successfully')
							print('data now contains',len(all_data),'episodes')
						else: print('episode data ignored')
						break
						
