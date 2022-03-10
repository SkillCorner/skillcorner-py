import os
import json
import logging

from skillcorner.client import SkillcornerClient

logger = logging.getLogger(__name__)


class FakeResponse:
    """
    Fake Response class mocking json method into returning dict.
    """
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def json(self):
        return self.dictionary


class MockSkillcornerClient(SkillcornerClient):
    """
    Mocked Skillcorner client class.
    """
    def __init__(self, *args, **kwargs):
        """
        Constructor of mocked Skillcorner API client object.
        """
        super(MockSkillcornerClient, self).__init__(*args, **kwargs)
        logger.debug(f'Creating Skillcorner mock client instance')

    def _skillcorner_request(self, url, method, params, paginated_request, timeout, pagination_limit=300):
        """
        Mocked skillcorner_request method returning fake json response read from file.

        :return: json dict with fake response data
        """
        if url.startswith('/'):
            url = url[1:]
        file_path = os.path.join('skillcorner', 'tests', 'fixtures', f'{url}.json')
        logger.debug(f'Loading file data as json response: {file_path}')
        with open(file_path) as file:
            data = FakeResponse(json.load(file))
        logger.info(f'Returning mock json response')
        return data.json()
