import logging
from dataclasses import dataclass
from functools import cached_property
from typing import Dict, List, Any

import requests
from dateutil.parser import parse
from rich import print

from opencanada.settings import get_config
from opencanada.utils import lang

'https://open.canada.ca/data/api/action/package_show?id=4ed351cf-95d8-4c10-97ac-6b3511f359b7'

package_list = '/action/package_list'
package_show = '/action/package_show?id='

group_list = '/action/action/group_list'

logger = logging.getLogger((__name__))


def api_url(path: str):
    return f"{get_config().api_url}/{path.lstrip('/')}"


async def list_packages():
    logger.info('Getting the full list of packages from Open Canada')
    resp = requests.get(api_url(package_list))
    package_json = resp.json()
    return package_json['result']


def get_group_list():
    resp = requests.get(api_url(group_list))
    return resp


@dataclass
class Resource:

    def __init__(self, resource_json: Dict[str, object]):
        self._json = resource_json

    @property
    def id(self):
        return self._json['id']

    @property
    def name(self):
        return self._json['name']

    @property
    def url(self):
        return self._json['url']

    @property
    def state(self):
        return self._json.get('state')

    @property
    def language(self):
        return '/'.join(self._json.get('language', []))

    @property
    def resource_type(self):
        return self._json.get('resource_type')

    @property
    def resource_format(self):
        return self._json.get('format')

    def __repr__(self):
        return (f"{self.name}\n"
                f"{self.language} {self.resource_type} {self.resource_format}\n"
                )


class Package:

    def __init__(self, package_json: Dict[str, object]):
        self._json: Dict[str, Any] = package_json

    @property
    def id(self):
        return self._json['id']

    @property
    def name(self):
        return self._json.get('name')

    @cached_property
    def date_published(self):
        return parse(self._json.get('date_published'))

    def title(self, language: str = None):
        return self._json['title_translated'][lang(language)]

    def notes(self, language: str = None):
        return self._json['notes_translated'][lang(language)]

    def get_resources(self) -> List:
        return [Resource(rec) for rec in self._json['resources']]

    @property
    def package_type(self):
        return self._json.get('type')

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and
                self.id == other.id
        )

    def __repr__(self):
        return (f"{self.title()}\n"
                f"{self.package_type.title()} {self.id}\n"
                f"{self.notes()}"
                )


class DatasetPackage(Package):

    def __init__(self, package_json):
        super().__init__(package_json)


def get_package(package_id: str):
    resp = requests.get(f"{api_url(package_show)}{package_id}")
    response_json = resp.json()
    package_json = response_json['result']
    if package_json.get('type') == 'dataset':
        return DatasetPackage(package_json)
    return Package(package_json)


def get_dataset(dataset_id: str):
    return get_package(dataset_id)


if __name__ == '__main__':
    # print(get_package_list())
    # package = get_package('fff7604f-8963-4210-aead-8fc9cade59b7')
    # print(package)

    dataset = get_dataset("4ed351cf-95d8-4c10-97ac-6b3511f359b7")
    print(dataset)
