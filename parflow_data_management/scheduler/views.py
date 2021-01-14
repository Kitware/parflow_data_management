from asgiref.sync import async_to_sync
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..transport.models.authorized_key import AuthorizedKey
from parflow_data_management.scheduler.tasks import remote_execute_cmd, submit_job


def cluster_execute_page(request):
    return render(request, "execute.html")


@api_view(["POST"])
def start_execution(request, cluster_id):
    auth_keys = AuthorizedKey.objects.filter(
        cluster__id=cluster_id, owner__id=request.user.id
    )
    if not auth_keys:
        content = "Authorized key needs to be added for cluster"
        return HttpResponseBadRequest(content)

    key = auth_keys[0].key_pair
    if key.is_unlocked():
        remote_execute_cmd.delay(cluster_id, request.user.id, "ls")
        return Response()

    content = "Private key needs to be unlocked"
    return HttpResponseBadRequest(content)

@api_view(["POST"])
def start_submit(request, cluster_id, simulation_id):
    submit_job(request.user.id, cluster_id, simulation_id)