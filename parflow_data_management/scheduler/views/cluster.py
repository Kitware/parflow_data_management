from rest_framework.decorators import api_view

from ..models.cluster import Cluster


@api_view(['POST'])
def run_command(request):
    pass