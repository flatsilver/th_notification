import boto3
import logging
import os
import json
import urllib.parse

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
connections = dynamodb.Table("groupwork3_notification")

url=f"https://uiso9zequl.execute-api.ap-northeast-1.amazonaws.com/production"

def lambda_handler(event, context):
    logger.info("th_notification start")
    client = boto3.client("sns")
    arn = os.environ["ARN"]
    msg = "zoomから取得出来たメッセージとか"
    sub = "生徒からのメッセージ"

    # SlackからのPOSTリクエストをparseして、messageを取り出す
    # SlackからのJSONは以下を参照
    # https://api.slack.com/reference/interaction-payloads/shortcuts
    data = urllib.parse.unquote(event['body']).replace("payload=", "")
    body = json.loads(data)
    msg = body['message']['text']

    items = connections.scan(ProjectionExpression='id').get('Items')

    if not items is None:
        apigw_management = boto3.client('apigatewaymanagementapi',
                                        endpoint_url=url)
        for item in items:
            apigw_management.post_to_connection(ConnectionId=item["id"],Data=msg)


    #とりあえずメールを送信することを想定
    #response = client.publish(TopicArn = arn, Message = msg, Subject = sub)
    print("sub:{},msg:{}".format(sub,msg))
    logger.info("th_notification end")
    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {},
        'body': '{"message": "ok"}'
    }


if __name__ == '__main__':
    # ローカル確認用
    os.environ["ARN"] = "snsで取得したarn"