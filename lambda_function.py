import boto3
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info("th_notification start")
    client = boto3.client("sns")
    arn = os.environ["ARN"]
    msg = "zoomから取得出来たメッセージとか"
    sub = "生徒からのメッセージ"

    #とりあえずメールを送信することを想定
    response = client.publish(TopicArn = arn, Message = msg, Subject = sub)
    logger.info("th_notification end")
    return response

if __name__ == '__main__':
    # ローカル確認用
    os.environ["ARN"] = "snsで取得したarn"