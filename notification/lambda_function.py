import boto3
import logging
import os
import ast

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

    # POSTリクエストでmsgとsubを渡す予定
    try:
        body_dict = ast.literal_eval(event['body'])

        if 'msg' in body_dict:
            msg = body_dict['msg']

        if 'sub' in body_dict:
            sub = body_dict['sub']
        
    except KeyError:
        print("Please include body")
        
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