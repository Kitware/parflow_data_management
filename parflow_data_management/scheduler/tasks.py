from asgiref.sync import async_to_sync
from django.core.cache import cache
from celery import shared_task
from channels.layers import get_channel_layer
from paramiko.rsakey import RSAKey

from .models.cluster import Cluster
from ..transport.connections.ssh_connection import SSHConnection

# TODO: rework this logic to handle multiple private keys per
# cluster and user combination
@shared_task
def remote_execute_cmd(cluster_id, user_id, command):
    try:
        con = SSHConnection(cluster_id, user_id)
    except:
        pass


    # Which key to get?
    # If unencrypted key is in the cache:
    # Start paramiko connection and execute
    # Else
    # Get password from user - How? - post request
    # Exit and notify where to post passphrase? Do it here?
    # Create a new ssh connection for now. Accepts passphrase
    # Uses passphrase to unencrypt private key - How does cluster have this particular private key?
    #   - authorized keys file.
    # Send ls or echo over ssh connection
    # returns output

    # Should the unencrypted private key only ever be in the cache?
    #

    # Return error message.
    print("In remote_execute_cmd")
