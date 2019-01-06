# -*- coding: utf-8 -*-

"""
This is a client for client-server chat system.
"""
import argparse
import ipaddress
import json_actions as ja
import random
import tkinter

from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread


def get_server_ip():
    # Ask user for host ip.
    host = input('Input host (default is 127.0.0.1): ')
    while True:
        try:
            ipaddress.ip_address(host)
            break
        except:
            if not host:
                break
            print('ERROR: Invalid IP address!')
            host = input()
    # Defaults to 127.0.0.1, if user didn't input ip.
    if not host:
        host = '127.0.0.1'
    return host


def get_server_port():
    # Ask user for host port
    port = input('Input port (default is 54321): ')
    while True:
        if not port:
            break
        if int(port) > 65535 or int(port) < 1024:
            print('ERROR: Invalid port number!')
            port = input()
            continue
        else:
            break
    # Defaults to 54321, if user didn't input port.
    if not port:
        port = 54321
    else:
        port = int(port)
    return port

def get_username():
    # Ask user for username.
    username = input('Choose username (under 16 characters) or press ENTER to get random one:\n')
    while True:
        if not username.isascii():
            print('ERROR: Username contains non-ASCII characters!')
            username = input()
            continue
        elif len(username) > 16:
            print('ERROR: Username is too long!')
            username = input()
            continue
        else:
            break
    # Generate random username in format UserXXXX, where XXXX is random number,
    # if user didn't choose one.
    if not username:
        username = get_random_username()
    return username

def get_random_username():
    """Generate a random username."""
    # Generate a random number and append it to 'User' string.
    rng = random.SystemRandom()
    random_number = rng.randint(1000, 9999)
    return 'User' + str(random_number)


def init_app():
    """Initialize app with required parameters."""

    host = get_server_ip()
    port = get_server_port()

    # Set buffer size.
    buf_size = 8192
    addr = (host, port)

    username = get_username()

    return buf_size, addr, username


def receive_message():
    """Receive, decode and display the message."""
    # Try to receive the message as long as the client exist.
    while True:
        try:
            verboseprint('Waiting for message...')
            # Receive message.
            text, recv_username = ja.decode_text(client_socket.recv(buf_size).decode())
            verboseprint('\nReceived message:', text,
                        'Username:', recv_username)
            # Don't show the message again, if it's from this client.
            if bytes(username, 'utf-8') == bytes(recv_username, 'utf-8'):
                continue
            verboseprint('Received message:', text)
            # Display message in GUI.
            msg_list.insert(tkinter.END, recv_username + ': ' + text)
            # Autoscroll with text.
            msg_list.see('end')
        except OSError:
            # Break loop if unable to continue.
            break


def send_message(event=None):
    """Get message set in input box and send it to server."""
    # Get message from input box.
    text = my_msg.get()
    # Check, if message is longer than max_length.
    text_length = len(text.encode('utf-8'))
    max_length = 100
    if text_length > max_length:
        # Show info, that the encryption mode was successfully changed.
        msg_list.insert(tkinter.END, 'ERROR: Message is too long (over ' + str(max_length) + ' characters).')
        # Autoscroll with text.
        msg_list.see('end')
        return
    # Clear input box.
    my_msg.set('')

    verboseprint('\nSending message...')
    if text != '' and text != '/exit':
        # Display message in GUI instantly.
        msg_list.insert(tkinter.END, username + ': ' + text)
        # Autoscroll with text.
        msg_list.see('end')
    try:
        verboseprint('Message sent:', text)
        client_socket.send(ja.encode_text(text, username).encode('utf-8'))
    except:
        # Don't break the program, if for some reason user wants to quits before
        # completing client initialization.
        print('Complete setup first!')
        return
    # End program, if message is '/exit'.
    if text == '/exit':
        client_socket.close()
        top.quit()


def on_window_close(event=None):
    """Default behaviour when user closes app window."""
    # Set message to /exit and call send_message().
    print('Closing application.')
    my_msg.set('/exit')
    send_message()


"""Main application"""
# Parse command-line arguments.
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true')
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

mode = 'test'
#mode = 'normal'

if mode == 'normal':
    # Set global variables for required items.
    buf_size, addr, username = init_app()

    # Create socket.
    client_socket = socket(AF_INET, SOCK_STREAM)
    # Connect to given address.
    try:
        client_socket.connect(addr)
    except:
        print('Coundnt reach server, exiting...')
        exit()
    verboseprint('\nConnected to %s:%s' % addr)
    # Send initial message.
    try:
        client_socket.send(ja.initial_message(username).encode('utf-8'))
        verboseprint('Sent initial message:', ja.initial_message(username))
    except:
        print('Counldnt send initial message, exiting...')
        exit()
    # Define and start receiving thread.
    receive_thread = Thread(target=receive_message)
    receive_thread.start()
    print('Initialization complete.')

    """GUI"""
    # Initialize top-level widget.
    top = tkinter.Tk()
    # Make the window non-resizable.
    top.resizable(False, False)
    # Set window title.
    top.title('Chat')
    # Set frame for other widgets.
    messages_frame = tkinter.Frame(top)
    # Set variable that holds input messages and default it to empty.
    my_msg = tkinter.StringVar()
    my_msg.set('')
    # Create scrollbar widget.
    scrollbar = tkinter.Scrollbar(messages_frame)
    # Create box that displays all messages.
    msg_list = tkinter.Listbox(messages_frame, height=25, width=100, yscrollcommand=scrollbar.set, borderwidth=2)
    # Pack scrollbar and messages list widgets together.
    scrollbar.pack(side='right', fill='y')
    msg_list.pack(side='left', expand=True, fill='both')
    messages_frame.pack(expand=True, fill='both')
    # Create input field.
    entry_field = tkinter.Entry(top, textvariable=my_msg, borderwidth=2)
    # Bind input field to 'ENTER'.
    entry_field.bind('<Return>', send_message)
    entry_field.pack(side='left', expand=True, fill='x')
    # Create Send button that calls to send_message().
    send_button = tkinter.Button(top, text='Send', command=send_message)
    send_button.pack(side='left')
    # Default behaviour when user closes app window.
    top.wm_protocol('WM_DELETE_WINDOW', on_window_close)
    # Start GUI.
    tkinter.mainloop()