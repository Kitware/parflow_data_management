from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models.conceptual_model import ConceptualModel
from ..models.mesh import Mesh
from ..models.metadata import Metadata
from ..models.project import Project
from ..models.project_asset import check_project_asset_perm
from ..models.simulation import Simulation


class PermissionTestCase(TestCase):
    def setUp(self):
        # First get the user model and create a test user
        User = get_user_model()
        test_user = User.objects.create(name="test_user")

        # Now create a project
        test_project = Project.objects.create(name="test_project", owner=test_user)

        # Assign some assets to it
        test_concep_model = ConceptualModel.objects.create(project=test_project)
        test_mesh = Mesh.objects.create(project=test_project)
        test_metadata = Metadata.objects.create(project=test_project)
        test_simulation = Simulation.objects.create(project=test_project)

    def test_project_permissions(self):
        # Get the user
        User = get_user_model()
        test_user = User.objects.get(name="test_user")

        # Get the project
        test_project = Project.objects.get(name="test_project")

        # Check the user has the correct permissions on the project
        self.assertTrue(test_user.has_perm("scheduler.change_project", test_project))
        self.assertTrue(test_user.has_perm("scheduler.delete_project", test_project))
        self.assertTrue(test_user.has_perm("scheduler.view_project", test_project))

    def test_project_asset_permissions(self):
        # Get the user
        User = get_user_model()
        test_user = User.objects.get(name="test_user")

        # Get the project
        test_project = Project.objects.get(name="test_project")

        # Get the project assets
        test_mesh = Mesh.objects.get(project=test_project)
        test_metadata = Metadata.objects.get(project=test_project)
        test_concep_model = ConceptualModel.objects.get(project=test_project)
        test_simulation = Simulation.objects.get(project=test_project)

        # Check the user has the correct permissions on the project asset
        for perm in ["change", "delete", "view"]:
            self.assertTrue(check_project_asset_perm(test_user, perm, test_concep_model))
            self.assertTrue(check_project_asset_perm(test_user, perm, test_mesh))
            self.assertTrue(check_project_asset_perm(test_user, perm, test_metadata))
            self.assertTrue(check_project_asset_perm(test_user, perm, test_simulation))
