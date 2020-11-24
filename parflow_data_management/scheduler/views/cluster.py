from asgiref.sync import async_to_sync
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models.cluster import Cluster
from parflow_data_management.scheduler.tasks import remote_execute_cmd


def cluster_execute_page(request):
    return render(request, "execute.html")


@api_view(["POST"])
def start_execution(request, cluster_id):
    try:
        remote_execute_cmd(cluster_id, "ls")
    except KeyError as e:
        raise  # TODO: This should return an error code instead of propagate the exception
    return Response()
