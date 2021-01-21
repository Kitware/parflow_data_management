from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from ..consumers import compute_group_for_user


def send_data_to_user(data, user_id, message_type):
    group = compute_group_for_user(user_id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {"type": message_type, "data": data}
    )