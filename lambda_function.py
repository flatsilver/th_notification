import boto3
import logging
import os
import ast

logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

    #とりあえずメールを送信することを想定
    response = client.publish(TopicArn = arn, Message = msg, Subject = sub)
    print("sub:{},msg:{}".format(sub,msg))
    logger.info("th_notification end")
    return response

if __name__ == '__main__':
    # ローカル確認用
    os.environ["ARN"] = "snsで取得したarn"