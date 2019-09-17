import os
import zipfile
import time
import datetime


dt = datetime.datetime.now()
dt = dt.strftime('%Y_%m_%d')
DAYS_LIMIT = 2
FOLDER = 'D:\\FTP'
OUTPUT = 'D:\\mac\\mac_archive_{}.zip'.format(dt)

def zipdir(path, arch_file, days):
    for root, dirs, files in os.walk(path):
        if len(files) > 0:
            print('\nProcessing folder: {}'.format(root))
            ziphandler = zipfile.ZipFile(arch_file, 'a', zipfile.ZIP_DEFLATED)
            counter = 0
            for file in files:
                counter += 1
                draw_progress(counter, len(files))

                if time.time() - os.path.getmtime(os.path.join(root, file)) > days * 24 * 60 * 60:
                    if file.endswith('.csv'):
                        ziphandler.write(os.path.join(root, file))
                        os.remove(os.path.join(root, file))
            ziphandler.close()

def draw_progress(current, total):
    line_length = 33
    percent = current/total
    line_filled = round(line_length * percent)
    line_empty = line_length - line_filled
    print('\rCompleted: {}% [{}{}] {}/{}'.format(
                                                int(percent * 100),
                                                '█' * line_filled,
                                                '-' * line_empty,
                                                current,
                                                total), end='')

if __name__ == '__main__':    
    zipdir(FOLDER, OUTPUT, DAYS_LIMIT)
    


