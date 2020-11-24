from django.contrib.auth import get_user_model
from django.core.cache import cache
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
        err_msg = "Please unlock private key"

        # Check if private key is in cache
        data_for_cluster = cache.get(self._cluster.id)
        if data_for_cluster is None:
            raise KeyError(err_msg)

        try:
            private_key = data_for_cluster["private_keys"][self._user.id]
        except KeyError as e:
            raise KeyError(err_msg) from e
        else:
            # Find authorized keys file for this user / cluster combo to get
            # public key
            auth_keys = AuthorizedKeys.objects.get(
                cluster=self._cluster, owner=self._user
            )

            # For now we're assuming there's one key_pair per authorized keys file
            public_key = auth_keys.key_pair.public_key  # TODO: need this?
            username = auth_keys.username

            # Start Paramiko connection
            self._client = paramiko.SSHClient()
            self._client.connect(hostname=hostname, username=username, pkey=private_key)

    def __exit__(self):
        self._client.close()
