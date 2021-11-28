from rich import print
import pandas as pd
from opencanada import inventory
from opencanada.api import Resource
from opencanada.settings import get_config


def test_inventory():
    assert inventory
    assert inventory.inventory_id == get_config().inventory_dataset


def test_inventory_get_dataset():
    dataset = inventory.get_dataset_package()
    assert dataset
    assert dataset.id == inventory.inventory_id
    print(dataset)


def test_inventory_get_resources():
    dataset = inventory.get_dataset_package()
    resources = inventory.get_resources()
    print(resources)
    assert resources == dataset.get_resources()


def test_get_guide_resource():
    # Can we get the resource that is the guide
    resource: Resource = inventory.get_guide_resource()
    print()
    assert resource
    assert resource.resource_type == 'guide'
    print(resource)


def test_inventory_guide():
    # Test that we can get an actual guide
    guide = inventory.guide
    print(guide)
    content = guide.contents('en')
    print(content)


def test_get_dataset_resource():
    # Can we get the resource that is the guide
    resource: Resource = inventory.get_dataset_resource()
    print()
    assert resource
    assert resource.resource_type == 'dataset'
    print(resource)


def test_get_inventory_data():
    data: pd.DataFrame = inventory.get_data()
    print(data)
