from django.contrib.auth import get_user_model
import paramiko

from parflow_data_management.scheduler.models.cluster import Cluster
from .connection import Connection


# Representation of an ssh connection to a cluster
class SSHConnection(Connection):
    def __init__(self, cluster_id, user_id):
        self._cluster = Cluster.objects.get(pk=cluster_id)
        self._user = get_user_model().objects.get(pk=user_id)

    def execute(self, command):
        raise NotImplementedError("Implemented by subclass")

    def __enter__(self):
        # Check if private key is in cache
        try:
            private_key = cache[cluster_id]["private_keys"][self._user.id]
        except KeyError:
            pass  # TODO error, please unlock key
        else:
            # Find authorized keys file for this user / cluster combo to get
            # public key
            auth_keys = AuthorizedKeys.objects.get(
                cluster=self._cluster, owner=self._user
            )

            # For now we're assuming there's one key_pair per authorized keys file
            public_key = auth_keys.key_pair.public_key # TODO: need this?
            username = auth_keys.username

            # Start Paramiko connection
            self._client = paramiko.SSHClient()
            self._client.connect(hostname=hostname, username=username, pkey=private_key)

    def __exit__(self):
        self._client.close()