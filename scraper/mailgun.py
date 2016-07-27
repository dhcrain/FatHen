import boto
import sys
from boto.s3.key import Key

aws_bucket_name = os.environ['aws_bucket']
aws_access_key_id = os.environ['aws_access_key_id']
aws_secret_access_key = os.environ['aws_secret_access_key']

AWS_STORAGE_BUCKET_NAME = 'aws_bucket_name'
AWS_ACCESS_KEY_ID = 'aws_access_key_id'
AWS_SECRET_ACCESS_KEY = 'aws_secret_access_key'


conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
bucket = conn.get_bucket(BUCKET_NAME, validate=False)
k = Key(bucket)
k.key = 'barbaz'
k.set_contents_from_filename('/tmp/barbaz.txt')
