import gc3libs
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from ..consumers import compute_group_for_user
from ..transport.connections.ssh_connection import SSHConnection

# TODO: Make this modular
class GdemoSimpleApp(gc3libs.Application):
    """
    This simple application will run `/bin/hostname`:file: on the remote host,
    and retrieve the output in a file named `stdout.txt`:file: into a
    directory `GdemoSimpleApp_output`:file: inside the current directory.
    """

    def __init__(self):
        gc3libs.Application.__init__(
            self,
            # the following arguments are mandatory:
            arguments=["/bin/hostname"],
            inputs=[],
            outputs=[],
            output_dir="./GdemoSimpleApp_output",
            # the rest is optional and has reasonable defaults:
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
    auth_key = AuthorizedKey.objects.filter(
        cluster__id=cluster_id, owner__id=user_id
    )[0]
    cluster = Cluster.objects.filter(cluster__id=cluster_id)[0]
    simulation = Simulation.objects.filter(simulation__id=simulation_id)[0]
    app = GdemoSimpleApp()

    # TODO: parameterize auth name?
    gc3_cfg = {"auth/ssh": {
        "type": "ssh",
        "username": auth_key.username,
    }}

    resource_settings = cluster._gc3_settings_dict()
    resource_settings["auth"] = "ssh"
    resource_settings["enabled"] = "yes"
    gc3_cfg["resource/{}".format(cluster.name)] = resource_settings

    engine = gc3libs.create_engine(cfg_dict=gc3_cfg)
    engine.add(app)

    # TODO: how to handle this?
    while app.execution.state != gc3libs.Run.State.TERMINATED:
        print("Job in status %s " % app.execution.state)
        engine.progress()
        time.sleep(1)

