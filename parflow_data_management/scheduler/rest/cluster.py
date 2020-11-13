from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from parflow_data_management.scheduler.models.cluster import Cluster

class ClusterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cluster
        fields = ("id", "user")

class ClusterViewSet(ModelViewSet):
    queryset = Cluster.objects.all()

    serializer_class = ClusterSerializer
