from asgiref.sync import async_to_sync
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..transport.models.authorized_key import AuthorizedKey
from parflow_data_management.scheduler.tasks import remote_execute_cmd


def cluster_execute_page(request):
    return render(request, "execute.html")


@api_view(["POST"])
def start_execution(request, cluster_id):
    auth_key = AuthorizedKey.objects.filter(
        cluster__id=cluster_id, owner__id=request.user.id
    )[0]
    key = auth_key.key_pair
    if key.is_unlocked():
        remote_execute_cmd.delay(cluster_id, request.user.id, "ls")
        return Response()

    content = "Please unlock your private key for this cluster"
    return HttpResponseBadRequest(content)
