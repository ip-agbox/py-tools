import requests
from requests.auth import HTTPBasicAuth
import datetime
import time
import cv2
import numpy as np
import argparse
import os

base_path = '\\\\192.168.0.1\\фотоотчёты'
months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
date = dict()
delta = datetime.timedelta(hours=2)
today = datetime.datetime.now() - delta
date['year'] = today.strftime('%Y')
date['month_number'] = today.strftime('%m')
date['month'] = months[int(date['month_number'])-1]
date['day'] = today.strftime('%d')
date['hour'] = today.strftime('%I')
date['minute'] = today.strftime('%M')

def make_path(path, date):
    path_year = '{}/{}'.format(path, date['year'])
    path_month = '{}/{}'.format(path_year, date['month'])
    path_moscow = '{}\\Москва'.format(path_month)
    path_caramel = '{}\\Арбат'.format(path_moscow)
    path_camera = '{}\\Видео с камеры'.format(path_caramel)

    if not os.path.isdir(path_year):
        os.makedirs(path_year)
    if not os.path.isdir(path_month):
        os.makedirs(path_month)
    if not os.path.isdir(path_moscow):
        os.makedirs(path_moscow)
    if not os.path.isdir(path_caramel):
        os.makedirs(path_caramel)
    if not os.path.isdir(path_camera):
        os.makedirs(path_camera)
    return path_camera

path = make_path(base_path, date)


ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", required=False, default='output.mp4', help="output video file")
args = vars(ap.parse_args())
output = args['output']

time_start = datetime.datetime.now()
frame_counter = 0

url = 'http://8.8.8.8/jpg/1/image.jpg?resolution=640x480'
while (datetime.datetime.now() - time_start).seconds < 60:
	time.sleep(1)
	response = requests.get(url, auth=HTTPBasicAuth('guest', 'guest'))
	if response.status_code == 200:
		timestamp = datetime.datetime.now()
		frame = cv2.imdecode(np.fromstring(response.content, dtype=np.uint8), cv2.IMREAD_COLOR)
		if frame_counter == 0:
			height, width, channels = frame.shape
			print(height, width, channels, sep=":")
			fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
			out = cv2.VideoWriter(path + '\\' + timestamp.strftime("%A-%d-%B-%Y-%I-%M-") + output, fourcc, 5.0, (width, height))
		
		cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)
		out.write(frame) 
		frame_counter += 1
		print("Added frame:" + str(frame_counter))
out.release()
print('DONE!')