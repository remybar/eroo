from unittest import TestCase
from unittest.mock import Mock

from ..models import CustomUser


class ModelTestCase(TestCase):

    def test_str_method(self):
        mock_user = Mock(spec=CustomUser)
        mock_user.username = "toto"

        self.assertEqual(CustomUser.__str__(mock_user), mock_user.username)
