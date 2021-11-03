import logging
from mock import patch
from unittest import TestCase

from skillcorner.tests.mocks.client_mock import MockSkillcornerClient

logger = logging.getLogger(__name__)


class TestMatchMocked(TestCase):
    """
    Test class for mocked match endpoint testing.
    """
    @patch('skillcorner.client.requests.request')
    def test_get_match(self, mock_request):
        """
        Test verifying response from one particular match endpoint
        """
        logger.info("Start test for match endpoint.")
        client = MockSkillcornerClient()
        client.get_match(match_id=42586)
