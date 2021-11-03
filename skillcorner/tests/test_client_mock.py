import logging
import requests
from unittest import TestCase
from mock import patch, MagicMock
from requests.exceptions import HTTPError
from skillcorner.client import SkillcornerClient

logger = logging.getLogger(__name__)


class TestClientMock(TestCase):
    """
    Test class for testing mocked Skillcorner API client behaviour
    """
    @patch('requests.Session')
    def test_client_raise_exception(self, mock_request):
        """
        Test verifying if 400 response raises an exception
        :param mock_request:
        :return:
        """
        logger.info("Start test for client raising an exeption.")
        response = requests.models.Response()
        response.status_code = 400
        request_mock = MagicMock()
        request_mock.request = MagicMock(return_value=response)
        requests.Session.return_value.__enter__.return_value = request_mock
        client = SkillcornerClient(username="wrong_username", password="wrong_password")
        with self.assertRaises(HTTPError):
            logger.info("Raising HTTPError exception")
            client.get_match(42586)
