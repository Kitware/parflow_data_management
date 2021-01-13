from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import CharField, IntegerField
from django.dispatch import receiver
from django_extensions.db.models import TimeStampedModel
from django.utils.translation import gettext_lazy as _
from guardian.shortcuts import assign_perm


class Cluster(TimeStampedModel, models.Model):
    # Attributes common to all cluster types
    name = CharField(_("Name of Cluster"), blank=True, max_length=255)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="clusters")
    hostname = CharField(_("Hostname"), blank=False, max_length=253)

    # GC3Pie related options. Any blanks refer to GC3Pie's defaults
    # Most of these are CharFields as the unit needs to be specified
    # (hours, GB, etc.)
    scheduler_type = CharField(max_length=8)
    max_cores_per_job = IntegerField()
    max_memory_per_core = CharField(max_length=64)
    max_walltime = CharField(max_length=64)
    max_cores = IntegerField()
    architecture = CharField(max_length=64)
    time_cmd = CharField(max_length=64, blank=True)
    large_file_threshold = CharField(max_length=64)
    large_file_chunk_size = CharField(max_length=64)


@receiver(models.signals.post_save, sender=Cluster)
def _cluster_post_save(sender, instance, created, *args, **kwargs):
    if created:
        assign_perm("scheduler.change_cluster", instance.owner, instance)
        assign_perm("scheduler.delete_cluster", instance.owner, instance)
        assign_perm("scheduler.view_cluster", instance.owner, instance)
        # TODO: group permissions
