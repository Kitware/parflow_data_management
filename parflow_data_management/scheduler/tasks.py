import io

import gc3libs
import time
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from paramiko import RSAKey

from .models.cluster import Cluster
from .models.simulation import Simulation
from ..consumers import compute_group_for_user
from ..transport.connections.ssh_connection import SSHConnection
from ..transport.models.authorized_key import AuthorizedKey


def create_app(simulation):
    return gc3libs.Application(
        arguments=simulation.arguments,
        inputs=[],
        outputs=[],
        output_dir="./GdemoSimpleApp_output",
        stdout="stdout.txt",
    )


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
def submit_job(user_id, cluster_id, simulation_id):
    auth_key = AuthorizedKey.objects.filter(cluster__id=cluster_id, owner__id=user_id)[
        0
    ]
    cluster = Cluster.objects.filter(pk=cluster_id)[0]
    simulation = Simulation.objects.filter(pk=simulation_id)[0]
    app = create_app(simulation)

    # TODO: parameterize auth name?
    gc3_cfg = {
        "auth/ssh": {
            "type": "ssh",
            "username": auth_key.username,
            "pkey": RSAKey.from_private_key(
                io.StringIO(auth_key.key_pair._private_key_decrypted())
            ),
        }
    }

    # Construct resource sections and add to cfg_dict
    resource_settings = cluster._gc3_settings_dict()
    resource_settings["auth"] = "ssh"
    resource_settings["transport"] = "ssh"
    resource_settings["enabled"] = "yes"
    gc3_cfg["resource/{}".format(cluster.name)] = resource_settings

    engine = gc3libs.create_engine(cfg_dict=gc3_cfg)
    engine.add(app)
    engine.select_resource(cluster.name)

    last_status = None
    while app.execution.state != gc3libs.Run.State.TERMINATED:
        # Job status change? Send update to user over websocket
        if app.execution.state != last_status:
            data = {"status": app.execution.state}
            group = compute_group_for_user(user_id)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                group, {"type": "job.status", "data": data}
            )
            last_status = app.execution.state

        engine.progress()
        time.sleep(1)
