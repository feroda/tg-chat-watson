#!/usr/bin/env python

import json
import os
import sys

from watson_developer_cloud import SpeechToTextV1

DEBUG = os.environ.get('APP_DEBUG', 'False') not in ['False', 'None', '0', ''] 

speech_to_text = SpeechToTextV1(
    username=os.environ.get('APP_SPEECH2TEXT_USERNAME'),
    password=os.environ.get('APP_SPEECH2TEXT_PASSWORD'),
    url=os.environ.get('APP_SPEECH2TEXT_URL'))


# replace with your own workspace_id
workspace_id = os.environ.get('APP_WORKSPACE_ID')

# Initialize with empty value to start the conversation.
user_input = ''
context = {}

def process_msg(msg, content_type="audio/wav", context={}):

    response = speech_to_text.recognize(
        audio=msg,
        content_type=content_type,
        timestamps=True,
        word_alternatives_threshold=0.9)
        # keywords=[],
        # keywords_threshold=0.5)

    if DEBUG:
        print(json.dumps(response, indent=2))

    # Print the output from dialog, if any.
    if response['results'][0]['alternatives'][0]['transcript']:
        print(response['results'][0]['alternatives'][0]['transcript'])

    return response


# Main input/output loop
if __name__ == "__main__":

    try:
        filename = sys.argv[1]
    except IndexError:
        print("Usage %s <wav audio file>" % sys.argv[0])
        sys.exit(100)

    with open(filename, 'rb') as file:

        response = process_msg(file)
