import json
import boto3
from botocore.vendored import requests
import time


def lambda_handler(event, context):
    # TODO implement
    
    s3_info = event['Records'][0]['s3']
    bucket_name = s3_info['bucket']['name']
    key_name = s3_info['object']['key']
    
    print(bucket_name, key_name)
    print('hello')
    client = boto3.client('rekognition')
    pass_object = {'S3Object':{'Bucket':bucket_name,'Name':key_name}}
    print(pass_object)
    resp = client.detect_labels(Image={'S3Object':{'Bucket':bucket_name,'Name':key_name}}, MaxLabels=10)
    print(resp)
    
    timestamp = time.time()
    
    labels = []
    
    for i in range(len(resp['Labels'])):
        labels.append(resp['Labels'][i]['Name'])
    
    print('labels: ', labels)
    
    format = {'objectKey':key_name,'bucket':bucket_name,'createdTimestamp':timestamp,'labels':labels}
    
    url = "https://vpc-photos-efyz5iahzrgd7lpuqw54twafku.us-east-1.es.amazonaws.com/photos/0"
    headers = {"Content-Type": "application/json"}
    
    #url2 = "https://vpc-photos-efyz5iahzrgd7lpuqw54twafku.us-east-1.es.amazonaws.com/photos/_search?pretty=true&q=*:*"
    
    r = requests.post(url, data=json.dumps(format).encode("utf-8"), headers=headers)
    
    #resp_elastic = requests.get(url2,headers={"Content-Type": "application/json"}).json()
    #print('<------------------GET-------------------->')
    
    print(r.text)
    
    #print(json.dumps(resp_elastic, indent=4, sort_keys=True))
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
