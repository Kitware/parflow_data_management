from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers
from .rest import cluster, conceptual_model, mesh, metadata, project, simulation

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"clusters", cluster.ClusterViewSet)
router.register(r"conceptual_models", conceptual_model.ConceptualModelViewSet)
router.register(r"meshs", mesh.MeshViewSet)
router.register(r"metadatas", metadata.MetadataViewSet)
router.register(r"projects", project.ProjectViewSet)
router.register(r"simulations", simulation.SimulationViewSet)

schema_view = get_schema_view(
    openapi.Info(title="", default_version="v1", description=""),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/docs/redoc/", schema_view.with_ui("redoc"), name="docs-redoc"),
    path("api/docs/swagger/", schema_view.with_ui("swagger"), name="docs-swagger"),
]
