#!/usr/bin/env python

import json
import os

from watson_developer_cloud import AssistantV1

service = AssistantV1(
    version='2018-02-16',
    # url=os.environ.get('APP_URL'),
    username=os.environ.get('APP_USERNAME'), password=os.environ.get('APP_PASSWORD'))

# replace with your own workspace_id
workspace_id = os.environ.get('APP_WORKSPACE_ID')

# Initialize with empty value to start the conversation.
user_input = ''
context = {}

# Main input/output loop
while True:

    # Send message to Assistant service.
    response = service.message(
        workspace_id = workspace_id,
        input = { 'text': user_input },
        context = context)

    # print(json.dumps(response, indent=2))
    # If an intent was detected, print it to the console.
    if response['intents']:
        print('Detected intent: #' + response['intents'][0]['intent'])

    # Print the output from dialog, if any.
    if response['output']['text']:
        print(response['output']['text'][0])

    # Update the stored context with the latest received from the dialog.
    context = response['context']

    # Prompt for next round of input.
    user_input = input('>> ')

