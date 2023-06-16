import sys
import os
import json
import uuid
import logging
from queue import Queue
sys.path.append('../')
from database.database import Database
from entity.group_message import GroupMessage
from entity.private_message import PrivateMessage

class Chat:
    def __init__(self):
        # databases
        self.user_db = Database('user.json')
        self.group_db = Database('group.json')
        self.private_message_db = Database('private_message.json')
        self.group_message_db = Database('group_message.json')

        self.sessions = {}
        self.server_id = ''

    def proses(self, data, server_id):
        self.server_id = server_id
        j = data.split(" ")
        try:
            command = j[0].strip()
            if (command == 'auth'):
                username = j[1].strip()
                password = j[2].strip()
                logging.warning(
                    "AUTH: auth {} {}" . format(username, password))
                return self.autentikasi_user(username, password)
            elif (command == 'sendprivate'):
                sessionid = j[1].strip()
                usernameto = j[2].strip()
                message = ""
                for w in j[3:]:
                    message = "{} {}" . format(message, w)
                usernamefrom = self.sessions[sessionid]['username']
                logging.warning("SEND: session {} send message from {} to {}" . format(
                    sessionid, usernamefrom, usernameto))
                return self.send_message(sessionid, usernamefrom, usernameto, message)
            elif (command == 'sendgroup'):
                sessionid = j[1].strip()
                groupto = j[2].strip()
                message = ""
                for w in j[3:]:
                    message = "{} {}" . format(message, w)
                usernamefrom = self.sessions[sessionid]['username']
                logging.warning("SEND GROUP: session {} send message from {} to {}" . format(
                    sessionid, usernamefrom, groupto))
                return self.send_message_group(sessionid, usernamefrom, groupto, message)
            elif (command == 'inbox'):
                sessionid = j[1].strip()
                username = self.sessions[sessionid]['username']
                logging.warning("INBOX: {}" . format(sessionid))
                return self.get_inbox(username)
            elif (command == 'inboxgroup'):
                sessionid = j[1].strip()
                groupname = j[2].strip()
                logging.warning("INBOX GROUP: {} {}" . format(sessionid, groupname))
                return self.get_inbox_group(groupname)
            else:
                return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
        except KeyError:
            return {'status': 'ERROR', 'message': 'Informasi tidak ditemukan'}
        except IndexError:
            return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}

    def autentikasi_user(self, username, password):
        user = self.user_db.get_by_key_value('username', username)
        print(user)
        if not user:
            return {'status': 'ERROR', 'message': 'user tidak ditemukan'}
        if user['password'] != password:
            return {'status': 'ERROR', 'message': 'password salah'}
        tokenid = str(uuid.uuid4())
        self.sessions[tokenid] = {'username': user['username']}
        return {'status': 'OK', 'token_id': tokenid, 'realm_id': user['realm_id']}

    def get_user(self, username):
        user = self.user_db.get_by_key_value('username', username)
        if (not user):
            return False
        return user

    def get_group(self, groupname):
        group = self.group_db.get_by_key_value('name', groupname)
        if (not group):
            return False
        return group

    def send_message(self, sessionid, username_from, username_dest, message):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        s_fr = self.get_user(username_from)
        s_to = self.get_user(username_dest)

        if (s_fr == False or s_to == False):
            return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

        message = PrivateMessage(
            s_fr['username'],
            s_fr['realm_id'],
            s_to['username'],
            s_to['realm_id'],
            message
        )

        self.private_message_db.insert_data(message.toDict())

        return {'status': 'OK', 'message': 'Message Sent'}

    def send_message_group(self, sessionid, username_from, groupname_dest, message):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        s_fr = self.get_user(username_from)
        s_to = self.get_group(groupname_dest)

        if (s_fr == False or s_to == False):
            return {'status': 'ERROR', 'message': 'Grup Tidak Ditemukan'}

        message = GroupMessage(
            s_fr['username'],
            s_fr['realm_id'],
            s_to['name'],
            s_to['realm_id'],
            message
        )

        self.group_message_db.insert_data(message.toDict())

        return {'status': 'OK', 'message': 'Message Sent'}

    def get_inbox(self, username):
        msgs = self.private_message_db.get_by_key_value('receiver', username)
        return {'status': 'OK', 'messages': msgs}

    def get_inbox_group(self, groupname):
        msgs = self.group_message_db.get_by_key_value(
            'receiver_group', groupname)
        return {'status': 'OK', 'messages': msgs}


if __name__ == "__main__":
    j = Chat()
    sesi = j.proses("auth messi surabaya")
    print(sesi)
    # sesi = j.autentikasi_user('messi','surabaya')
    # print sesi
    tokenid = sesi['tokenid']
    print(j.proses("send {} henderson hello gimana kabarnya son " . format(tokenid)))
    print(j.proses("send {} messi hello gimana kabarnya mess " . format(tokenid)))

    # print j.send_message(tokenid,'messi','henderson','hello son')
    # print j.send_message(tokenid,'henderson','messi','hello si')
    # print j.send_message(tokenid,'lineker','messi','hello si dari lineker')

    print("isi mailbox dari messi")
    print(j.get_inbox('messi'))
    print("isi mailbox dari henderson")
    print(j.get_inbox('henderson'))
