from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CharField, IntegerField
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from guardian.shortcuts import assign_perm


class Cluster(TimeStampedModel, models.Model):
    # Attributes common to all cluster types
    name = CharField(_("Name of Cluster"), blank=False, max_length=255)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="clusters"
    )
    hostname = CharField(_("Hostname"), blank=False, max_length=253)

    # GC3Pie related options. Any blanks refer to GC3Pie's defaults
    # These are CharFields as the unit needs to be specified
    # (hours, GB, etc.)
    scheduler_type = CharField(max_length=8)
    max_cores_per_job = CharField(max_length=8)
    max_memory_per_core = CharField(max_length=64)
    max_walltime = CharField(max_length=64)
    max_cores = CharField(max_length=8)
    architecture = CharField(max_length=64)
    time_cmd = CharField(max_length=64, blank=True)
    large_file_threshold = CharField(max_length=64, blank=True)
    large_file_chunk_size = CharField(max_length=64, blank=True)

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
