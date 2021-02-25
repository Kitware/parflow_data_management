import os
import stat

import parflow_data_management.scheduler.models as psm


from django.contrib.auth import get_user_model
from django.db import models

from parflow_data_management.scheduler.models.cluster import Cluster

from ..connections.ssh_connection import SSHConnection

# Abstract mapping of a file to its location on a remote machine


class AssetStore(models.Model):
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="asset_stores"
    )
    cluster = models.OneToOneField(
        Cluster, on_delete=models.CASCADE, related_name="asset_store"
    )

    def _ingest(self, import_path, parent, ssh=None):
        ret = list()
        with ssh.open_sftp() as sftp:
            for p in sftp.listdir_iter(path=import_path):
                name = p.filename

                full_path = os.path.join(import_path, name)
                if name in [".", ".."]:
                    continue

                if stat.S_ISDIR(p.st_mode):
                    # Create folder and recurse
                    new_parent = psm.folder.Folder.objects.create(
                        name=name,
                        parent=parent,
                        asset_store=self,
                        abs_path=full_path,
                    )
                    self._ingest(full_path, new_parent, ssh=ssh)
                else:
                    # Create a file
                    psm.file.File.objects.create(
                        name=name, folder=parent, asset_store=self
                    )

    def ingest(self, import_path):
        import_path = import_path.strip()

        if import_path and import_path[0] != "/":
            import_path = "/%s" % import_path

        dir_to_ingest = psm.folder.Folder.objects.create(
            name=import_path.rsplit("/", 1)[1], asset_store=self,
            abs_path=import_path,
        )

        with SSHConnection(self.cluster.id, self.owner.id) as ssh:
            self._ingest(import_path, dir_to_ingest, ssh=ssh)
