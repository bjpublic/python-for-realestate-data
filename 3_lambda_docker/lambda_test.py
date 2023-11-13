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
s3r = boto3.resource('s3', 
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_ACCESS_KEY_SECRET)
bucket = s3r.Bucket('apart-bucket')

data = pd.DataFrame({
    "a":[1,2,3],
    "b":['a','b', 'c']
})
 
def lambda_handler(event, context):
    current_time  = datetime.now(timezone('Asia/Seoul'))
    current_time = current_time.strftime("%H:%M:%S")
    print(current_time)

    file_name = "apart_trans" + "_" + current_time + "_" + ".csv"

    data.to_csv("/tmp/python_test.csv")
    bucket.upload_file("/tmp/python_test.csv",file_name)
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Success !')
    }
