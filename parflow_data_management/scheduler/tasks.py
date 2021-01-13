from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from ..consumers import compute_group_for_user
from ..transport.connections.ssh_connection import SSHConnection


# TODO: rework this logic to handle multiple private keys per
# cluster and user combination
@shared_task
def remote_execute_cmd(cluster_id, user_id, command):
    with SSHConnection(cluster_id, user_id) as con:
        output = con.execute(command)

    data = {"output": output}
    group = compute_group_for_user(user_id)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group, {"type": "command.output", "data": data}
    )

@shared_task
def submit_job(cluster_id, simulation_id):
    pass