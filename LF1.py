import json
import boto3


def getSlotData(event):
    return event['currentIntent']['slots']


def send_sqs_message(QueueName, msg_body):
    sqs_client = boto3.client('sqs')
    sqs_queue_url = sqs_client.get_queue_url(QueueName=QueueName)['QueueUrl']
    try:
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url, MessageBody=json.dumps(msg_body))
    except ClientError as e:
        logging.error(e)
        return None
    return msg


def handleFullfilment(slotData):
    QueueName = 'Q1'
    msg = send_sqs_message(QueueName, slotData)
    if msg is not None:
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "We have received the request and will notify you over SMS once we have the list of restaurants"
                }
            }
        }
    else:
        return {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "There was an issue please try again later. Sorry for the inconvenience."
                }
            }
        }


def lambda_handler(event, context):
    slotData = getSlotData(event)
    return handleFullfilment(slotData)