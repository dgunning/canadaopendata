import logging
from dataclasses import dataclass
from functools import cached_property, lru_cache
from io import BytesIO
from typing import Dict

import pandas as pd
import requests
from openpyxl import load_workbook

from opencanada import exceptions
from opencanada.settings import get_config
from opencanada.utils import lang
from opencanada.api import Resource

logger = logging.getLogger(__name__)


class Metadata:

    def __init__(self, metadata_json: Dict[str, object]):
        self.metadata = metadata_json

    @cached_property
    def title(self):
        return self.metadata['result']['title']

    @cached_property
    def notes(self):
        return self.metadata['result']['notes']

    @cached_property
    def resources(self):
        df = (pd.DataFrame(self.metadata['result']['resources']))
        df = (df
              .dropna(how='all', axis=1)
              .filter(['package_id', 'id', 'resource_id', 'url_type', 'mimetype', 'cache_url', 'name', 'language',
                       'created', 'last_modified', 'url', 'state', 'hash', 'ignore_hash', 'description', 'format',
                       'ckan_url', 'data_quality', 'position', 'revision_id', 'resource_type'])
              )
        return df

    def __repr__(self):
        return f"""{self.title!r}
               """



@dataclass
class Dataset:
    id: str
    language: str

    def url(self):
        return f"{get_config().url}/data/{self.language}/dataset/{self.id}"

    def metadata_url(self):
        return f"{get_config().url}/data/api/action/package_show?id={self.id}"

    @cached_property
    def metadata(self):
        # Read the dataset metadata
        logger.info(f"Reading metadata for dataset {self.id}")
        metadata_json = requests.get(self.metadata_url()).json()
        return Metadata(metadata_json)

    @cached_property
    def resources(self):
        return self.metadata.resources

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (
                self.__class__ == other.__class__ and
                self.id == other.id
        )


inventory = Dataset(
    id=get_config().inventory_dataset,
    language=get_config().language
)


@dataclass
class InventoryGuide:

    def __init__(self, resource: Resource):
        self.resource: Resource = resource

    def read_workbook(self):
        content = requests.get(self.resource.url).content
        return load_workbook(BytesIO(content))

    def contents(self, language: str = 'en'):
        workbook = self.read_workbook()
        rows = []
        language_sheet_name = lang(language).upper()
        sheet = workbook[language_sheet_name]

        for row in sheet.rows:
            record = ' '.join([str(cell.value) for cell in row if cell.value])
            rows.append(record)
        return '\n'.join(rows)


class Inventory:
    dataset_id: str = "d0df95a8-31a9-46c9-853b-6952819ec7b4"
    webside_en_id: str = "bda0e815-db75-446e-9727-c959fe1eba41"
    webside_fr_id: str = "67a381f8-16a3-4934-bca1-4a07824444e6"
    guide_id: str = "21691d86-fe30-44a9-941f-3c6b84029f55"

    def __init__(self, inventory_dataset: Dataset):
        self.inventory_dataset = inventory_dataset

    def metadata(self):
        return self.inventory_dataset.metadata

    def guide(self):
        guide = (self.inventory_dataset.resources
                 .query(f"id=='{self.guide_id}'"))
        if guide.empty:
            raise exceptions.ResourceException(
                "Inventory Guide resource not found in resources dataframe" +
                f" .. there should be a record with id='{self.guide_id}' and resource_type=='guide'"
            )
        rec = guide.iloc[0]
        inventory_guide = InventoryGuide(
            Resource(
                id=rec.id,
                name=rec.name,
                resource_id=None if pd.isnull(rec.resource_id) else rec.resource_id,
                url=rec.url,
                resource_format=rec.format,
                resource_type=rec.resource_type
            )
        )

        return inventory_guide


_inventory_dataset = Dataset(
    id=get_config().inventory_dataset,
    language=get_config().language
)
inventory = Inventory(
    inventory_dataset=_inventory_dataset
)
