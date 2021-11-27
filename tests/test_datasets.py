from rich import print

from opencanada.api import get_package, DatasetPackage
from opencanada.datasets import inventory


def test_open_canada_dataset():
    assert inventory
    print(inventory)


def test_dataset_url():
    print()
    assert inventory.inventory_dataset
    assert inventory.inventory_dataset.url() == 'https://open.canada.ca/data/en/dataset/4ed351cf-95d8-4c10-97ac-6b3511f359b7'


def test_dataset_resources():
    assert not inventory.metadata().resources.empty


def test_get_dataset():
    id = '2c15d988-646d-e6e5-cf37-285d87b50c45'
    dataset: DatasetPackage = get_package(id)
    assert dataset.id == id
    print()
    print(dataset)
    # print(dataset._json)



