import ds_client
from ds_protocol import *

PORT = 3021

class DirectMessage:
    def __init__(self, recipient, message, timestamp, sender):
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp
        self.sender = sender
    
    def get_recipient(self):
        return self.recipient
    
    def get_message(self):
        return self.message
    
    def get_timestamp(self):
        return self.timestamp
    
    def get_sender(self):
        return self.sender


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.username = username
        self.password = password
        self.dsuserver = dsuserver
		
    def send(self, dm: DirectMessage) -> bool:
        # must return true if message successfully sent, false if send failed.

        msg = '{"token":"' + self.token + '", "directmessage": {"entry": "' + dm.get_message() + '", "recipient": "' + dm.get_recipient() + '", "timestamp": "' + dm.get_timestamp() + '"}}'
        response = ds_client.send(self.dsuserver, PORT, self.username, self.password, msg)
        data_tuple = extract_json(response)
        if data_tuple.type == "error":
            return False
        elif data_tuple.type == "ok":
            return True

    def retrieve_new(self) -> list:
        # must return a list of DirectMessage objects containing all new messages

        dm_list = []
        msg = '{"token":"' + self.token + '", "directmessage": "new"}'
        response = ds_client.send(self.dsuserver, PORT, self.username, self.password, msg)
        data_tuple = extract_json(response)

        if data_tuple.type == "error":
            return False
        elif data_tuple.type == "ok":
            for i in data_tuple[1]:
                m = DirectMessage(recipient = self.username, message = i['message'], timestamp = i['timestamp'], sender = i['from'])
                
                dm_list.append(m)
        
        return dm_list
 
    def retrieve_all(self) -> list:
        # must return a list of DirectMessage objects containing all messages

        dm_list = []
        msg = '{"token":"' + self.token + '", "directmessage": "all"}'
        response = ds_client.send(self.dsuserver, PORT, self.username, self.password, msg)
        data_tuple = extract_json(response)


        if data_tuple.type == "error":
            return False
        elif data_tuple.type == "ok":
            for i in data_tuple[1]:
                m = DirectMessage(recipient = self.username, message = i['message'], timestamp = i['timestamp'], sender = i['from'])
                dm_list.append(m)

        return dm_list
