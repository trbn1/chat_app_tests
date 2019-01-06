# Client-server Chat

## Introduction

This is a client-server chat system. It allows for simple communication between multiple users at once.

#### Main Features:

* Uses predefined JSON strings format to communicate between client and server
* Supports plain text messaging

#### Server-only features:

* Supports multiple clients at once

#### Client-only features:

* Connect to any server that supports predefined JSON strings format
* Generate random username, if it wasn't chosen by the user

## Requirements

* Python 3.7+

## Instructions

1) Make sure you have python executable in your PATH environment variable.
2) Clone the repository and cd into it.
3) To start the server, execute:
```
python server.py
```
4) To display available server command-line arguments, append -h or --help to the above command.
```
python server.py -h
usage: server.py [-h] [-v] [--ip [x.x.x.x]] [--port [N]]

optional arguments:
  -h, --help      show this help message and exit
  -v, --verbose   show additional info during runtime
  --ip [x.x.x.x]  choose ip to listen on
  --port [N]      choose port to listen on
```
5) To start the client, execute:
```
python client.py
```
6) To display additional information in the console, append -v or --verbose to the above command.

During start-up, client supports:
* custom host IP and port
* choosing username

Commands available in client GUI:
* /exit