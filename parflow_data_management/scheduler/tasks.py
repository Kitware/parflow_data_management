from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from paramiko.rsakey import RSAKey
from celery import shared_task


@shared_task
def remote_execute_cmd(cluster_id, command):
    # Get password from user - How? - post request
    # Create a new ssh connection for now. Accepts passphrase
    # Uses passphrase to unencrypt private key - How does cluster have this particular private key?
    #   - authorized keys file.
    # Send ls or echo over ssh connection
    # returns output

    # TODO: Re-adjust authorized keys model to have 1 user and a list of key pairs
    print("In remote_execute_cmd")