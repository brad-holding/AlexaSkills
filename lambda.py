import boto3
import requests
import time


##### Program Entry #####


def lammbda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return launch_request_handler(event, context)
    elif event['request']['type'] == "IntentRequest":
        return intent_handler(event, context)


##### Helper Functions #####


def get_ip_address():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ip-address')
    response = table.get_item(
        Key={'id': '1'}
    )
    return response['Item']['ip-address']


##### Launch Handler #####


def launch_request_handler(event, context):
    return statement("This is the title", "This is the body")


##### Responses #####


def conversation(title, body, session_attributes):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_Response(speechlet, session_attributes=session_attributes)


def statement(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = True
    return build_Response(speechlet)


def continue_dialog():
    message = {}
    message['shouldEndSession'] = False
    message['directives'] = [{'type': 'Dialog.Delegate'}]
    return build_Response(message)


##### Builders #####


def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech


def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card


def build_Response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response

##### Intent Routing #####


def intent_handler(event, context):
    intent = event['request']['intent']['name']

    if intent == "AMAZON.CancelIntent":
        return cancel_intent()

    if intent == "AMAZON.HelpIntent":
        return help_intent()

    if intent == "AMAZON.StopIntent":
        return stop_intent()

    if intent == "TurnOffTV":
        return intent_turn_off_tv(event, context)

    if intent == "Blippi":
        return intent_blippi(event, context)

##### Required Intents #####

def cancel_intent():
    return statement("CancelIntent", "You want to cancel")

def help_intent():
    return statement("CancelIntent", "You want help")

def stop_intent():
    return statement("StopIntent", "You want to stop")

##### Custom Intents #####

def intent_blippi(event, context):
    requests.post('http://{}:8060/keypress/home'.format(get_ip_address()))
    time.sleep(1)
    requests.post('http://{}:8060/launch/837?contentID=JG5gTF0S2LI'.format(get_ip_address()))
    title = "Blippi Intent"
    body = "Ok, firing up Blippi"
    return statement(title, body)
