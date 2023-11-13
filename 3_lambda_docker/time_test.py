import json
from datetime import datetime
from pytz import timezone
import pandas as pd
import os
import boto3
import csv 
    
# from dotenv import load_dotenv

AWS_ACCESS_KEY_ID = "IAM Access Key"
AWS_ACCESS_KEY_SECRET = "IAM Secret Key"
        
# set aws credentials 
s3r = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_ACCESS_KEY_SECRET)
bucket = s3r.Bucket('python-apart')

data = pd.DataFrame({
    "a":[1,123],
    "b":['aa','ff']
})



now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print(current_time)
print(current_time)

today = datetime.now(timezone('Asia/Seoul'))
print(today)

file_name = "apart_trans" + current_time + ".csv"
 
def lambda_handler(event, context):
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    file_name = "apart_trans" + current_time + ".csv"


    today = datetime.now(timezone('Asia/Seoul'))
    
    print(current_time)
    print(today)
    
    data.to_csv("/tmp/asdf1.csv")
    bucket.upload_file("/tmp/asdf1.csv",file_name)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'time': current_time
    }
