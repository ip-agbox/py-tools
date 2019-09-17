import logging
import boto3
from botocore.exceptions import ClientError
import os
import progressbar

log_bucket = 'mac_addresses.log'
path = 'D:\\mac'


def upload_file(file_name, bucket, object_name=None):

    def upload_progress(chunk):
        up_progress.update(up_progress.currval + chunk)

    statinfo = os.stat(file_name)
    up_progress = progressbar.progressbar.ProgressBar(maxval=statinfo.st_size)
    up_progress.start()

    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3', 
                        aws_access_key_id='a-a-a-a-a-a-a-a-a-a-a-a-a-a-a',
                        aws_secret_access_key='s-s-s-s-s-s-s-s-s-s-s-s-s-s-s-s-s-s-s',
                      )
    try:
        response = s3_client.upload_file(file_name, bucket, object_name, Callback=upload_progress)
    except ClientError as e:
        logging.error(e)
        return False
    up_progress.finish()
    return True


if __name__ == '__main__': 
    for root, dirs, files in os.walk(path):
            if len(files) > 0:
                print('\nProcessing folder: {}'.format(root))                
                for file in files:              
                    if file.endswith('.zip'):
                        print('Uploading {}'.format(file))
                        res = upload_file(os.path.join(root, file), log_bucket, file)
                        if res:
                            os.remove(os.path.join(root, file))        
