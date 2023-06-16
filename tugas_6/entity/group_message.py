import datetime


class GroupMessage:
    def __init__(
            self,
            sender,
            sender_realm,
            receiver_group,
            receiver_realm,
            message,
    ):
        self.sender = sender
        self.sender_realm = sender_realm
        self.receiver_group = receiver_group
        self.receiver_realm = receiver_realm
        self.message = message
        self.created_at = str(datetime.datetime.now())

    def toDict(self):
        return vars(self)
