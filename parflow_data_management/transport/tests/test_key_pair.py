import io

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from paramiko import SSHException
from paramiko.rsakey import RSAKey

from ..models.key_pair import KeyPair


class KeyPairTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        test_user = User.objects.create(name="test_user")

        # Normally we'd submit a post request to create a new key_pair.
        # For testing purposes, we'll just set up the database accordingly
        new_key = RSAKey.generate(bits=4096)
        out_desc = io.StringIO()
        new_key.write_private_key(out_desc, password="test_password")

        self.expected_private_key = out_desc.getvalue()

        self.key_pair = KeyPair.objects.create()
        self.key_pair.owner = test_user
        self.key_pair.public_key = new_key.get_base64()
        self.key_pair.private_key_encrypted = out_desc.getvalue()
        self.key_pair.save()

    def test_unlock_successful(self):
        self.assertFalse(self.key_pair.is_unlocked())
        with self.assertRaises(RuntimeError, msg="Private key needs to be unlocked"):
            self.key_pair._private_key_decrypted()

        # Unlock key through endpoint
        args = {"passphrase": "test_password"}
        endpt = "/keypairs/{}/unlock/".format(str(self.key_pair.id))
        response = self.client.post(endpt, args)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.key_pair.is_unlocked())
        self.assertEqual(
            self.key_pair._private_key_decrypted(), self.expected_private_key
        )

    def test_unlock_unsuccessful(self):
        self.assertFalse(self.key_pair.is_unlocked())

        args = {"passphrase": "incorrect_password"}
        endpt = "/keypairs/{}/unlock/".format(self.key_pair.id)
        response = self.client.post(endpt, args)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Invalid passphrase")
        self.assertFalse(self.key_pair.is_unlocked())
