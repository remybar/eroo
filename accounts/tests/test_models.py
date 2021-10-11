from unittest import TestCase
from unittest.mock import Mock

from ..models import ErooUser


class ModelTestCase(TestCase):

    def test_str_method(self):
        mock_user = Mock(spec=ErooUser)
        mock_user.username = "toto"

        self.assertEqual(ErooUser.__str__(mock_user), mock_user.username)
