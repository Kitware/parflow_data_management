import io

from django.contrib.auth import get_user_model
import paramiko

from ..models.authorized_key import AuthorizedKey
from .connection import Connection
from parflow_data_management.scheduler.models.cluster import Cluster


# Representation of an ssh connection to a cluster
class SSHConnection(Connection):
    def __init__(self, cluster_id, user_id):
        self._cluster = Cluster.objects.get(pk=cluster_id)
        self._user = get_user_model().objects.get(pk=user_id)

    def execute(self, command):
        chan = self._client.get_transport().open_session()
        chan.exec_command(command)
        stdout = chan.makefile('r', -1)
        stderr = chan.makefile_stderr('r', -1)

        output = stdout.readlines() + stderr.readlines()
        return output

    def __enter__(self):
        # Find authorized keys file for this user / cluster combo
        auth_key = AuthorizedKey.objects.get(cluster=self._cluster, owner=self._user)

        # For now we're assuming there's one key_pair per authorized keys file
        key_pair = auth_key.key_pair

        # Start Paramiko connection
        self._client = paramiko.SSHClient()
        self._client.load_system_host_keys()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._client.connect(
            hostname=self._cluster.hostname,
            username=auth_key.username,
            pkey=key_pair._private_key_decrypted(),
            look_for_keys=False,
            allow_agent=False
        )
        return self

    def __exit__(self, type, value, traceback):
        self._client.close()
