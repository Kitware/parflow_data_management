import json

from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

class GeneralConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        group = compute_group_for_user(self.scope["user"].id)
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def disconnect(self, close_code):
        group = compute_group_for_user(self.scope["user"].id)
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)

    def public_key_with_passphrase(self, message):
        self.send_json({
            "type": "public.key.with.passphrase",
            "data": message["data"],
        })

    def command_output(self, message):
        self.send_json({
            "type": "command.output",
            "data": message["data"],
            })

# Compute a unique group name that will contain only the connection
# for the given user.
def compute_group_for_user(user_id):
    return "user_" + str(user_id) + "_group"