import logging
from dataclasses import dataclass
from functools import lru_cache
from io import BytesIO

import pandas as pd
import requests
from openpyxl import load_workbook

from opencanada.api import Resource, get_dataset
from opencanada.settings import get_config
from opencanada.utils import first, lang

logger = logging.getLogger(__name__)

__all__ = ['inventory', 'Inventory', 'InventoryGuide']


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

    def __init__(self, inventory_dataset_id: str):
        self.inventory_id = inventory_dataset_id

    @lru_cache()
    def get_dataset_package(self):
        return get_dataset(self.inventory_id)

    @lru_cache()
    def get_resources(self):
        return self.get_dataset_package().get_resources()

    @lru_cache()
    def get_guide_resource(self):
        guide_resource = first([resource for
                                resource in self.get_resources()
                                if resource.resource_type == 'guide'])
        return guide_resource

    @property
    def guide(self):
        guide_resource = self.get_guide_resource()
        guide = InventoryGuide(guide_resource)
        return guide

    @lru_cache()
    def get_dataset_resource(self):
        dataset_resource = first([resource for
                                  resource in self.get_resources()
                                  if resource.resource_type == 'dataset'])
        return dataset_resource

    def get_data(self):
        dataset_resource = self.get_dataset_resource()
        return pd.read_csv(
            dataset_resource.url,
            dtype={'size': 'Int64'}
        )

    def metadata(self):
        return self.inventory_dataset.metadata


inventory = Inventory(
    inventory_dataset_id=get_config().inventory_dataset
)
