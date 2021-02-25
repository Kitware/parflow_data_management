from django.contrib import admin
from .models import (
    cluster,
    conceptual_model,
    folder,
    mesh,
    metadata,
    project,
    simulation,
    workflow,
)
from .models.file import File  # To avoid name collision

admin.site.register(cluster.Cluster)
admin.site.register(conceptual_model.ConceptualModel)
admin.site.register(File)
admin.site.register(folder.Folder)
admin.site.register(mesh.Mesh)
admin.site.register(metadata.Metadata)
admin.site.register(project.Project)
admin.site.register(simulation.Simulation)
admin.site.register(workflow.Workflow)
