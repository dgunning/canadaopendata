from rich import print
import pandas as pd
from opencanada.datasets import inventory

pd.options.display.max_columns = 50


def test_dataset_metadata():
    print()
    print(inventory.metadata())


def test_metadata_title():
    metadata = inventory.metadata()
    assert metadata.title == 'Open Data Inventory'


def test_metadata_notes():
    metadata = inventory.metadata()
    print(metadata.metadata['result'].keys())
    print(metadata.notes)


def test_metadata_properties():
    metadata = inventory.metadata()
    print()
    print(metadata.metadata['result'].keys())
    for key in ['name', "title", "organization", "date_published", "portal_release_date", "author",
                "resources"]:
        print(key, "=", metadata.metadata['result'].get(key))


def test_metadata_resources():
    metadata = inventory.metadata()
    print()
    print(metadata.resources)