# Starter code for assignment 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Abraham Manu
# apmanu@uci.edu
# 26411611

import socket
from ds_protocol import *

def send(server:str, port:int, username:str, password:str, message:str=None, bio:str=None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    #TODO: return either True or False depending on results of required operation
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((server, port))

            send = client.makefile("wb")
            recv = client.makefile("rb")
            
            if message == "join":
                join_msg = '{"join": {"username": ' + '"' + username + '"' + ', "password": ' + '"' + password + '"' + ', "token":""}}'
                # print(join_msg)
                send.write(join_msg.encode() + b"\r\n")
                send.flush()

                srv_msg = recv.readline()[:-2]
                
            elif "token" in message:
                send.write(message.encode() + b"\r\n")
                send.flush()
                srv_msg = recv.readline()[:-2]

    except:
        raise
    else:
        return srv_msg

