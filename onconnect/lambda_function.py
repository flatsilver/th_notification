import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table("groupwork3_notification")

def lambda_handler(event, context):
    connection_id = event.get('requestContext',{}).get('connectionId')
    result = connections.put_item(Item={ 'id': connection_id })
    return { 'statusCode': 200,'body': 'ok' }