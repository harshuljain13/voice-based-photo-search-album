import json
import os
import math
import dateutil.parser
import datetime
import time
import logging
import boto3
from botocore.vendored import requests


"""
https://medium.com/@dhruvarora2/access-aws-services-like-rekognition-from-a-vpc-enabled-lambda-b1d6907bae93

follow the above link to tackle VPC issues.
"""

def lambda_handler(event, context):
    # TODO implement
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    
    client = boto3.client('lex-runtime')
    
    #input_text = event["queryStringParameters"]['q']
    input_text = "Show me the photos with Water and Canal in them"
    
    #logger.debug("In lambda")
    response_lex = client.post_text(
            botName='voicealbumbot',
            botAlias="test",
            userId='test',
            inputText=input_text )
            
    
    if 'slots' in response_lex:
        keys = [response_lex['slots']['keyone'],response_lex['slots']['keytwo']]
        print(keys)
        pictures = search_intent(keys) #get images keys from elastic search labels
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": json.dumps(pictures),
            "isBase64Encoded": False
        }
    else:
        response = {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin":"*","Content-Type":"application/json"},
            "body": [],
            "isBase64Encoded": False}
    #logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return response
    
def search_intent(labels):

    # key1 = get_slots(intent_request)['keyone']
    # key2 = get_slots(intent_request)['keytwo']
    # key3 = get_slots(intent_request)['keythree']
    url = 'https://vpc-photos-efyz5iahzrgd7lpuqw54twafku.us-east-1.es.amazonaws.com/photos/_search?q='
    #labels = [key1,key2,key3]
    resp = []
    for label in labels:
        if (label is not None) and label != '':
            url2 = url+label
            resp.append(requests.get(url2).json())
    print (resp)
  
    output = []
    for r in resp:
        if 'hits' in r:
             for val in r['hits']['hits']:
                key = val['_source']['objectKey']
                if key not in output:
                    output.append(key)
    #url = "https://vpc-photos-b4al4b3cnk5jcfbvlrgxxu3vhu.us-east-1.es.amazonaws.com/photos/_search?pretty=true&q=*:*"
    #print(url)
    #resp = requests.get(url,headers={"Content-Type": "application/json"}).json()
    #resp = requests.get(url)
    print(output)

    return output