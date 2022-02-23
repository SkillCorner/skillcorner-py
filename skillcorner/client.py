import json
import logging
import os
import requests
from datetime import datetime, timedelta
from functools import wraps
from inspect import currentframe, getargvalues
from requests.auth import HTTPBasicAuth
from makefun import create_function

BASE_URL = 'https://skillcorner.com'

METHOD_DOCSTRING = 'Returns full {url} request response data in the json format. ' \
                   'To learn more about endpoint go to: https://skillcorner.com/api/docs/#{docs_url_anchor}\n'

METHOD_ID_DOCSTRING = 'Returns full {url}' \
                      ' request response data in the json format. ' \
                      'To learn more about endpoint go to: https://skillcorner.com/api/docs/#{docs_url_anchor}\n'

METHOD_URL_BINDING = {
    '_get_matches': {
        'url': '/api/matches/',
        'paginated_request': True,
        'docs_url_anchor': '/matches/matches_list',
    },
    '_get_teams': {
        'url': '/api/teams/',
        'paginated_request': True,
        'docs_url_anchor': '/teams/teams_list',
    },
    '_get_players': {
        'url': '/api/players/',
        'paginated_request': True,
        'docs_url_anchor': '/players/players_list',
    },
    '_get_competitions': {
        'url': '/api/competitions/',
        'paginated_request': True,
        'docs_url_anchor': '/competitions/competitions_list',
    },
    '_get_physical': {
        'url': '/api/physical',
        'paginated_request': False,
        'docs_url_anchor': '/physical/physical',
    }
}

METHOD_URL_ID_BINDING = {
    '_get_match': {
        'url': '/api/match/{}',
        'paginated_request': False,
        'docs_url_anchor': '/match/match_read',
        'id_name': 'match_id',
    },
    '_get_match_video_tracking_data': {
        'url': '/api/match/{}/video/tracking',
        'paginated_request': True,
        'docs_url_anchor': '/match/match_video_tracking_list',
        'id_name': 'match_id',
    },
    '_get_match_tracking_data': {
        'url': '/api/match/{}/tracking',
        'paginated_request': False,
        'docs_url_anchor': '/match/match_tracking_list',
        'id_name': 'match_id',
    },
    '_get_match_data_collection': {
        'url': '/api/match/{}/data_collection',
        'paginated_request': False,
        'docs_url_anchor': '/match/match_data_collection_read',
        'id_name': 'match_id',
    },
    '_get_team': {
        'url': '/api/teams/{}',
        'paginated_request': False,
        'docs_url_anchor': '/teams/teams_read',
        'id_name': 'team_id',
    },
    '_get_player': {
        'url': '/api/players/{}',
        'paginated_request': False,
        'docs_url_anchor': '/players/players_read',
        'id_name': 'player_id',
    },
    '_get_competition_editions': {
        'url': '/api/competitions/{}/editions',
        'paginated_request': True,
        'docs_url_anchor': '/competitions/competitions_editions_list',
        'id_name': 'competition_id',
    }
}

logger = logging.getLogger(__name__)


def _args_logging(logger):
    """Decorator logging arguments passed to the function

    :param logging logger: logging object created for Skillcorner Client
    :return: decorator
    """

    def decorator(func):
        fname = func.__name__
        argnames = func.__code__.co_varnames[:func.__code__.co_argcount]

        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.debug(f'Calling {fname} with following arguments: ')
            for pair in zip(argnames, args):
                if pair[0] == "self":
                    continue
                logger.debug(f'Setting {pair[0]} to: {pair[1]}')
            return func(*args, **kwargs)

        return wrapper

    return decorator


def _freeze_args(func, id_name=None, request_data=None, **kwargs):
    """Wrapper freezing url and paginated_request arguments defined for methods.

    This method binds and freezes function with arguments defined in METHOD_URL_BINDING and METHOD_URL_ID_BINDING.
    Ensures url or paginated request will not be overwrite by user.

    :param func: method to be bind with url
    :param id_name: specific id argument
    :param kwargs: keyword arguments passed to method
    :return: wrapper
    """

    frozen_kwargs = kwargs

    def wrapper(*args, **kwargs):
        frame = currentframe()
        passed_args = getargvalues(frame).locals["args"]
        passed_kwargs = getargvalues(frame).locals["kwargs"]

        logger.debug(f'Arguments passed in {func.__name__} call: {passed_args}')
        logger.debug(f'Keyword arguments passed in {func.__name__} call: {passed_kwargs}')

        if ('paginated_request' in passed_kwargs.keys()) or ('url' in passed_kwargs.keys()):
            raise ValueError('Forbidden to pass \'url\' or \'paginated_request\' as an argument and overwrite '
                            'default values.')

        if 'id' in passed_kwargs.keys():
            raise ValueError(f"Unexpected argument: 'id'")

        if id_name:
            if id_name in passed_kwargs:
                id_value = passed_kwargs[id_name]
                kwargs['id'] = id_value
                del kwargs[id_name]

        if request_data:
            if request_data in passed_kwargs:
                request_data_value = passed_kwargs[request_data]
                kwargs['request_data'] = request_data_value
                del kwargs[request_data]

        kwargs.update(frozen_kwargs)

        return func(*args, **kwargs)

    return wrapper


class _MethodsGenerator(type):
    """Class generating all client methods used to request data from API.

    As all methods used to send get request method have the same structure their names, stored as keys in
    METHOD_URL_BINDING and METHOD_URL_ID_BINDING dictionaries, are being connected with generic functions
    _get_data, _get_and_write_data, _get_data_with_id, _get_and_write_data_with_id.
    METHOD_URL_BINDING contains methods which use simple URL without any additional ID needed to generate proper
    and valid URL.
    METHOD_URL_ID_BINDING contains methods which use URL with additional ID needed to be provided to generate
    proper and valid URL (e. g. 'match_id' for 'get_matches' method).
    """

    def _generate_signature(cls, func_name, filepath=None, id_name=None):
        func = getattr(cls, func_name)
        public_func_name = func_name.strip("_")
        if filepath and not id_name:
            public_func_sig = f"{public_func_name}(self, filepath, params=None)"
        elif id_name and not filepath:
            public_func_sig = f"{public_func_name}(self, {id_name}, params=None)"
        elif id_name and filepath:
            public_func_sig = f"{public_func_name}(self, {id_name}, filepath, params=None)"
        else:
            public_func_sig = f"{public_func_name}(self, params=None)"
        public_func_gen = create_function(public_func_sig, func)
        setattr(cls, public_func_name, public_func_gen)
        public_func = getattr(cls, public_func_name)
        return public_func

    def __new__(cls, classname, supers, cls_dict):
        skcr_client = super().__new__(cls, classname, supers, cls_dict)

        for key, value in METHOD_URL_BINDING.items():
            setattr(skcr_client,
                    key,
                    _freeze_args(skcr_client._get_data,
                                 url=value['url'],
                                 paginated_request=value['paginated_request']))
            cls_dict[key.strip("_")] = skcr_client._generate_signature(key)

            docs_url_anchor = value.get('docs_url_anchor', False)
            if docs_url_anchor:
                docstring = METHOD_DOCSTRING.format(url=value['url'],
                                                    docs_url_anchor=docs_url_anchor)
            else:
                docstring = 'Returns full {url} request response data in the json format.'.format(url=value['url'])
            cls_dict[key.strip("_")].__doc__ = docstring

            get_and_save_func_name = key.replace('_get_', '_get_and_save_')
            setattr(skcr_client,
                    get_and_save_func_name,
                    _freeze_args(skcr_client._get_and_write_data,
                                 url=value['url'],
                                 paginated_request=value['paginated_request']))
            cls_dict[get_and_save_func_name.strip("_")] = skcr_client._generate_signature(get_and_save_func_name,
                                                                                          filepath=True)

            get_and_save_docstring = docstring.split(" in the ")[0] + " and saves in the file using " + \
                                     docstring.split(" in the ")[1]
            cls_dict[get_and_save_func_name.strip("_")].__doc__ = get_and_save_docstring

        for key, value in METHOD_URL_ID_BINDING.items():

            setattr(skcr_client, key, _freeze_args(skcr_client._get_data_with_id,
                                                   id_name=value["id_name"],
                                                   url=value['url'],
                                                   paginated_request=value['paginated_request']))
            cls_dict[key.strip("_")] = skcr_client._generate_signature(key, id_name=value['id_name'])

            docks_url = value['url'].split('{}')[0] + '{' + value['id_name'] + '}' + value['url'].split('{}')[1]
            docs_url_anchor = value.get('docs_url_anchor', False)
            if docs_url_anchor:
                docstring = METHOD_ID_DOCSTRING.format(url=value['url'],
                                                    docs_url_anchor=docs_url_anchor)
            else:
                docstring = 'Returns full {url} request response data in the json format.'.format(url=value['url'])
            cls_dict[key.strip("_")].__doc__ = docstring

            get_and_save_method_name = key.replace('_get_', '_get_and_save_')
            setattr(skcr_client,
                    get_and_save_method_name,
                    _freeze_args(skcr_client._get_and_write_data_with_id,
                                 id_name=value["id_name"],
                                 url=value['url'],
                                 paginated_request=value['paginated_request']))

            cls_dict[get_and_save_method_name.strip("_")] = skcr_client._generate_signature(get_and_save_method_name,
                                                                                            filepath=True,
                                                                                            id_name=value['id_name'])

            get_and_save_docstring = docstring.split(" in the ")[0] + " and saves in the file using " + \
                                     docstring.split(" in the ")[1]

            cls_dict[get_and_save_method_name.strip("_")].__doc__ = get_and_save_docstring

        return type.__new__(cls, classname, supers, cls_dict)


class SkillcornerClient(metaclass=_MethodsGenerator):
    """Skillcorner API client class.

        Attributes:

            username str:
                the username of the skillcorner service user
            password str:
                password corresponding to the username
    """

    def __init__(self, username=None, password=None):
        """
        :param username: string containing authorised username
        :param password: string containing valid password
        """

        logger.debug(f'Init client object')
        if not (username or password):
            try:
                username = os.environ['SKC_USERNAME']
                password = os.environ['SKC_PASSWORD']
            except KeyError:
                pass
        self.auth = HTTPBasicAuth(username=username, password=password)
        logger.debug(f'Authentication class: HTTPBasicAuth')
        self.base_url = BASE_URL
        logger.debug(f'Base url: {self.base_url}')

    @_args_logging(logger)
    def _skillcorner_request(self, url, method, params, paginated_request, json_data=None, pagination_limit=300,
                             timeout=30):
        """Custom Skillcorner API request

        Custom request function using session object to persist parameters for Skillcorner host connection.
        Raises HTTP errors. edit docstring.

        :param string url: indicates to which endpoint send request
        :param string method: indicates HTTP method to use in request
        :param dict params: contains extra parameters for request
        :param int timeout: indicating request timeout in seconds
        :param boolean paginated_request: flag indicates if response should be paginated
        :param int pagination_limit: indicates pagination limit
        :return dict: contains response from server
        """

        url = '{}{}'.format(self.base_url, url)
        logger.info(f'Connecting to: {url}')

        with requests.Session() as skillcorner_session:

            if not params:
                params = {}
            data = {}

            if paginated_request:
                first_request_flag = True
                start_timestamp = datetime.now()

                while url:
                    if first_request_flag:
                        if 'limit' not in params.keys():
                            params['limit'] = pagination_limit
                    else:
                        if 'limit' in params.keys():
                            del (params['limit'])

                    skillcorner_response = skillcorner_session.request(url=url,
                                                                       method=method,
                                                                       json=json_data,
                                                                       params=params,
                                                                       auth=self.auth,
                                                                       timeout=timeout)
                    skillcorner_response.raise_for_status()
                    resp = skillcorner_response.json()
                    request_duration = datetime.now() - start_timestamp

                    if not data:
                        data = skillcorner_response.json()
                        estimated_request_amount = data['count'] / pagination_limit
                        estimated_request_duration = timedelta(
                            seconds=(estimated_request_amount * request_duration.total_seconds()))

                        if estimated_request_duration >= timedelta(seconds=6):
                            logger.warning(f"WARNING: Estimated request duration: {estimated_request_duration}.\n"
                                           "This request may take a while as it retrieves big amount of data. "
                                           "If needed, please use Ctrl+C to stop the request and call method with "
                                           "'params' argument to reduce its response time and obtain more precise "
                                           "results (e.g. get_matches(params={'season': 6})). For more details about "
                                           "'params' usage, go to: https://skillcorner.com/api/docs/.")

                    else:
                        data["results"].extend(skillcorner_response.json()["results"])

                    url = resp['next']
                    first_request_flag = False

                data = data['results']
                end_timestamp = datetime.now()

            else:

                start_timestamp = datetime.now()
                skillcorner_response = skillcorner_session.request(url=url,
                                                                   method=method,
                                                                   json=json_data,
                                                                   params=params,
                                                                   auth=self.auth,
                                                                   timeout=timeout)
                skillcorner_response.raise_for_status()

                try:
                    data = skillcorner_response.json()
                except json.decoder.JSONDecodeError:
                    data = skillcorner_response.content
                end_timestamp = datetime.now()

            full_request_duration = end_timestamp - start_timestamp

            logger.info(f'Api request duration: {full_request_duration}')
            logger.info(f'Response status code: {skillcorner_response.status_code}')
            logger.info(f'Response headers: {skillcorner_response.headers}')

            return data

    def _get_data(self, *, url, paginated_request, params=None):
        """General get... function

        Uses skillcorner request to get response from passed url without any additional parameters.
        It is used by partial for binding method name with url.

        :return: dict containing server response
        """

        return self._skillcorner_request(url=url,
                                         method='GET',
                                         params=params,
                                         paginated_request=paginated_request)

    def _get_and_write_data(self, filepath, *, url, paginated_request, params=None):
        """General get_and_write... function

        Uses skillcorner request to get response from passed url without any additional parameters and save
        the response in JSON file.
        It is used by partial for binding method name with url.

        :return: dict containing server response
        """

        data = self._skillcorner_request(url=url,
                                         method='GET',
                                         params=params,
                                         paginated_request=paginated_request)

        logger.info(f'Writing response to the file: {filepath}')
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)

    def _get_data_with_id(self, id, *, url, paginated_request, params=None):
        """General get...(id) function

        Uses skillcorner request to get response from passed url with one parameter.
        It is used by partial for binding method name with parametrized url.

        :return: dict containing server response
        """

        url = url.format(id)
        return self._skillcorner_request(url=url,
                                         method='GET',
                                         params=params,
                                         paginated_request=paginated_request)

    def _get_and_write_data_with_id(self, id, filepath, *, url, paginated_request, params=None):
        """General get_and_write...(id) function

        Uses skillcorner request to get response from passed url with one parameter and save the response in JSON file.
        It is used by partial for binding method name with parametrized url.

        :return: dict containing server response
        """

        url = url.format(id)
        data = self._skillcorner_request(url=url,
                                         method='GET',
                                         params=params,
                                         paginated_request=paginated_request)

        logger.info(f'Writing response to the file: {filepath}')
        try:
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)
        except TypeError:
            with open(filepath, 'wb') as file:
                file.write(data)
