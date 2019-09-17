import datetime
import os
import asyncio
import concurrent.futures
import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth

print('Program started')
start_time = datetime.datetime.now()
cams_file = 'cams.csv'
cams_url = 'http://{}/jpg/1/image.jpg'
cams_login = 'root'
cams_password = 'root'
output_path = '\\\\192.168.0.1\\archive\\cameras'
months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
date = dict()
delta = datetime.timedelta(hours=2)
today = datetime.datetime.now() - delta
date['year'] = today.strftime('%Y')
date['month_number'] = today.strftime('%m')
date['month'] = months[int(date['month_number'])-1]
date['day'] = today.strftime('%d')
date['hour'] = today.strftime('%H')
date['minute'] = today.strftime('%M')
futures = []


def make_path(path, date):
    path_year = '{}/{}'.format(path, date['year'])
    path_month = '{}/{}/{}'.format(path, date['year'], date['month'])
    path_day = '{}/{}/{}/{}'.format(path, date['year'], date['month'], date['day'])
    if not os.path.isdir(path_year):
        os.makedirs(path_year)
    if not os.path.isdir(path_month):
        os.makedirs(path_month)
    if not os.path.isdir(path_day):
        os.makedirs(path_day)
    return path_day


def request_cam(name, ip):
    print('Current cam: {} - started at {}'.format(name, str(datetime.datetime.now() - start_time)))
    try:
        response = requests.get(cams_url.format(ip), auth=HTTPDigestAuth(cams_login, cams_password))
        if response.status_code == 200:
            output_file = '{}/{}-{}-{}-{}-{}-{}.jpg'.format(path, name, date['year'], date['month_number'], date['day'], date['hour'], date['minute'])
            with open(output_file, 'wb') as of:
                for chunk in response:
                    of.write(chunk)
            print('DONE on cam: {} - finished at {}'.format(name, str(datetime.datetime.now() - start_time)))
        else:
            print(response)
    except:
        print('ERROR on cam: {}'.format(name))


async def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        loop = asyncio.get_event_loop()
        with open(cams_file) as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                line = line.split(',')
                futures.append(
                    loop.run_in_executor(
                        executor, 
                        request_cam, 
                        *[line[1], line[0]])                )    
        for response in await asyncio.gather(*futures):
            pass

path = make_path(output_path, date)
print('Path created in {}'.format(str(datetime.datetime.now() - start_time)))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print('Done in {}'.format(str(datetime.datetime.now() - start_time)))
