import json

from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync

class ClusterExecuteConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()
        group = compute_group_for_user_execute(self.scope["user"].id)
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def disconnect(self, close_code):
        group = compute_group_for_user_execute(self.scope["user"].id)
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)

    def command_output(self, message):
        self.send_json({
            "type": "command.output",
            "data": message["data"],
        })


# TODO: Figure out a better way for handling
# the channel / websocket connection
def compute_group_for_user_execute(user_id):
    return "user_" + str(user_id) + "_cluster_execute_group"