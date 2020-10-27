from django.urls import include, path
from rest_framework import routers
from .rest import cluster, conceptual_model, mesh, metadata, project, simulation

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"clusters", cluster.ClusterViewSet)
router.register(r"conceptual_models", conceptual_model.ConceptualModelViewSet)
router.register(r"meshs", mesh.MeshViewSet)
router.register(r"metadatas", metadata.MetadataViewSet)
router.register(r"projects", project.ProjectViewSet)
router.register(r"simulations", simulation.SimulationViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
