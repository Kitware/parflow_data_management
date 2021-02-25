from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import TextField, IntegerField
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from guardian.shortcuts import assign_perm


class Cluster(TimeStampedModel, models.Model):
    # Attributes common to all cluster types
    name = TextField(_("Name of Cluster"), blank=False)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="clusters"
    )
    hostname = TextField(_("Hostname"), blank=False)

    # GC3Pie related options. Any blanks refer to GC3Pie's defaults
    # These are TextFields as the unit needs to be specified
    # (hours, GB, etc.)
    scheduler_type = TextField()
    max_cores_per_job = TextField()
    max_memory_per_core = TextField()
    max_walltime = TextField()
    max_cores = TextField()
    architecture = TextField()
    time_cmd = TextField(blank=True)
    large_file_threshold = TextField(blank=True)
    large_file_chunk_size = TextField(blank=True)

    def _gc3_settings_dict(self):
        ret = {
            "name": self.name,
            "max_cores_per_job": self.max_cores_per_job,
            "max_memory_per_core": self.max_memory_per_core,
            "max_walltime": self.max_walltime,
            "max_cores": self.max_cores,
            "architecture": self.architecture,
            "frontend": self.hostname,
            "type": self.scheduler_type,
        }
        if self.time_cmd:
            ret["time_cmd"] = self.time_cmd

        if self.large_file_threshold:
            ret["large_file_threshold"] = self.large_file_threshold

        if self.large_file_chunk_size:
            ret["large_file_chunk_size"] = self.large_file_chunk_size

        return ret


@receiver(models.signals.post_save, sender=Cluster)
def _cluster_post_save(sender, instance, created, *args, **kwargs):
    if created:
        assign_perm("scheduler.change_cluster", instance.owner, instance)
        assign_perm("scheduler.delete_cluster", instance.owner, instance)
        assign_perm("scheduler.view_cluster", instance.owner, instance)
        # TODO: group permissions
