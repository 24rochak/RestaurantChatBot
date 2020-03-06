import boto3

inp = {"messageVersion": "1.0", "invocationSource": "DialogCodeHook", "userId": "nxneu19o7s8r491hq7dft145wwm7314j",
       "sessionAttributes": {}, "requestAttributes": "None",
       "bot": {"name": "DiningBot", "alias": "$LATEST", "version": "$LATEST"}, "outputDialogMode": "Text",
       "currentIntent": {"name": "DiningSuggestionsIntent",
                         "slots": {"Cuisine": "None", "People": "None", "PhoneNumber": "None", "DiningTime": "None",
                                   "Location": "None"},
                         "slotDetails": {"Cuisine": {"resolutions": "[]", "originalValue": "None"},
                                         "People": {"resolutions": "[]", "originalValue": "None"},
                                         "PhoneNumber": {"resolutions": "[]", "originalValue": "None"},
                                         "DiningTime": {"resolutions": "[]", "originalValue": "None"},
                                         "Location": {"resolutions": "[]", "originalValue": "None"}},
                         "confirmationStatus": "None"}, "inputTranscript": "i want suggestions for restaurants",
       "recentIntentSummaryView": "None", "sentimentResponse": "None"}


def elicitSlotResponse(slotName, slotData, message=None, ok=True):
    dialogAction = {}
    dialogAction["type"] = "ElicitSlot"
    dialogAction["intentName"] = "DiningSuggestionsIntent"
    dialogAction["slotToElicit"] = slotName
    dialogAction["slots"] = slotData
    if ok:
        return {"dialogAction": dialogAction}
    else:
        dialogAction["message"] = {}
        dialogAction["message"]["contentType"] = "PlainText"
        dialogAction["message"]["content"] = message
        return {"dialogAction": dialogAction}


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


def validateSlot(slotName, slotData):
    if slotName == "Location":
        return elicitSlotResponse("Cuisine", slotData)
    elif slotName == "Cuisine":
        lex = boto3.client("lex-models")
        response = lex.get_slot_type(name='Cuisine', version='$LATEST')
        values = response["enumerationValues"]
        cuisines = [item['value'] for item in values]
        message = "Available cuisines are: " + " ".join(item for item in cuisines) + "."
        if slotData["Cuisine"] in cuisines:
            return elicitSlotResponse("people", slotData)
        else:
            return elicitSlotResponse("cuisine", slotData, message, False)
    elif slotName == "People":
        return elicitSlotResponse("DiningTime", slotData)
    elif slotName == "DiningTime":
        return elicitSlotResponse("PhoneNumber", slotData)
    elif slotName == "PhoneNumber":
        phone = slotData["PhoneNumber"]
        if len(phone) == 10:
            return handleFullfilment(slotData)
        else:
            message = "Please enter a valid 10 digit number."
            return elicitSlotResponse("PhoneNumber", slotData, message, False)


intent = inp["currentIntent"]
name = intent["name"]
slotData = intent["slots"]

# response = elicitSlotresponse("Location", slotData=slotData)
response = validateSlot("Cuisine", slotData)
print(response)
