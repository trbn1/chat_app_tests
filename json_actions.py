# -*- coding: utf-8 -*-

"""
This script is used when working with JSON format,
in particular when encoding/decoding.
"""
import base64
import json


def initial_message(username):
    """Set proper format of initial message and encode it into JSON format."""
    msg = { 
        'request': username,
    }
    return json.dumps(msg)


def recv_initial_message(msg_recv):
    """Decode received initial message from JSON format."""
    msg = json.loads(msg_recv)

    if 'request' in msg:
        return msg['request']


def encode_text(text, username):
    """Encode given text to Base64 and, with username, encode it to
    JSON format."""
    # Create text string.
    text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    msg = { 
        'msg': text,
        'from': username,
    }
    return json.dumps(msg)


def decode_text(msg_recv):
    """Decode received message from JSON format and decide if it's
    an encryption request or a message with text."""
    msg = json.loads(msg_recv)

    # Is true if the received message is a message with username.
    if 'request' in msg:
        return base64.b64decode(msg['request']).decode()

    # Is true if the received message is a message with text.
    if 'msg' in msg:
        return base64.b64decode(msg['msg']).decode(), msg['from']

