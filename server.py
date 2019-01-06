# -*- coding: utf-8 -*-

"""
This is a server for client-server chat system.
"""
import argparse
import json_actions as ja

from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread


# Define server username globally.
SERVERNAME = 'Server'


def main(mode='normal'):
    SERVER.listen(5)
    verboseprint('Listening on %s:%s' % ADDR)
    verboseprint('Waiting for connections...')
    if mode == 'normal':
        # Create new thread for each incoming connection.
        ACCEPT_THREAD = Thread(target=accept_incoming_connection)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
    SERVER.close()
    return True


def accept_incoming_connection():
    """Accept incoming connection and create client thread."""
    while True:
        (client, client_address) = SERVER.accept()
        addresses[client] = client_address
        verboseprint('\n%s:%s has connected.' % addresses[client])
        Thread(target=handle_client, args=(client, )).start()


def handle_client(client):
    """Handle single client from accepted incoming connection."""
    # Receive and decode initial message.
    username = ja.recv_initial_message(client.recv(BUFSIZ).decode())
    verboseprint('Connected user:', username)
    send_message_to_all('%s has joined the chat.' % username)
    clients[client] = username

    # Receive messages from client, as long as the connection exists.
    while True:
        verboseprint('Waiting for message...')
        # Receive message.
        text, username = ja.decode_text(client.recv(BUFSIZ).decode())
        verboseprint('\nReceived message:', text,
                    'Username:', username)

        # Ignore empty messages.
        if text == '':
            continue

        # Broadcast message to all clients.
        if text != '/exit':
            send_message_to_all(text, username)
        # End connection, if client requests so.
        else:
            close_connection(client, username)
            break


def send_message(client, text, username=SERVERNAME):
    """Send message to a single client, username defaults to SERVERNAME, if not given."""
    try:
        verboseprint('\nSending message...')
        verboseprint('Message sent to %s:' % clients[client], text)
        # Send plain-text message.
        client.send(ja.encode_text(text, username).encode('utf-8'))
    except:
        print('ERROR: Couldnt send the message, dropping client connection.')
        close_connection(client)


def send_message_to_all(text, username=SERVERNAME):
    """Broadcast message to all clients."""
    if clients != {}:
        for client in clients:
            send_message(client, text, username)


def close_connection(client, username='unknown'):
    """Default behavior on client closing connection with server."""
    verboseprint('Ending connection with %s:%s.' % addresses[client])
    # Close client connection.
    client.close()
    # Delete information about client, if it exists.
    if client in clients:
        del clients[client]
    if client in addresses:
        del addresses[client]
    # Broadcast message, that somebody has left the chat.
    send_message_to_all('%s has left the chat.' % username)


"""Main application"""
# Parse command-line arguments.
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', help='show additional info during runtime')
parser.add_argument('--ip', metavar='x.x.x.x', dest='HOST', nargs='?', const=1, help='choose ip to listen on', default='0.0.0.0')
parser.add_argument('--port', metavar='N', dest='PORT', nargs='?', const=1, help='choose port to listen on', type=int, default=54321)
args = parser.parse_args()

# Check, if verbose mode was requested.
if args.verbose:
    def verboseprint(*args):
        """Print given arguments."""
        for arg in args:
           print(arg)
        print
else:
    # Do nothing
    verboseprint = lambda *a: None

# Initialize required lists.
clients = {}
addresses = {}

# Define server parameters.
BUFSIZ = 8192
ADDR = (args.HOST, args.PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
try:
    SERVER.bind(ADDR)
except:
    print('Couldnt initialize server, exiting...')
    exit()
# Run server.
if __name__ == '__main__':
    main()