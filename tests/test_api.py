from pathlib import Path
import json
from opencanada.api import Package, DatasetPackage, list_packages
from opencanada.indexes import PackagesGuidIndex
from rich import print
import asyncio


def get_resources_package():
    with Path("tests/data/package.json").open('r') as f:
        return Package(json.load(f)['result'])


def get_no_resources_package():
    with Path("tests/data/package_noresources.json").open('r') as f:
        return Package(json.load(f))


def test_package_date_published():
    package = get_no_resources_package()
    print(package.date_published)


def test_package_translated_properties():
    package = get_no_resources_package()
    print("id", package.id)
    assert package.title() == "Coral and Sponge Concentrations in the Eastern Arctic Region of Canada"
    assert package.title('fr') == ("Concentrations de corail et d'Ã©ponge dans la zone biogÃ©ographique "
                                   "de l'Arctique de l'Est du Canada")

    print(package.notes("fr"))


def test_get_dataset_resources():
    dataset: DatasetPackage = get_resources_package()
    print()
    resources = dataset.get_resources()

    print(resources)


def test_list_packages():
    packages = asyncio.run(list_packages())
    assert len(packages) == len(set(packages))
    package_headers = list(map(lambda s: s[:8], packages))
    assert len(package_headers) == len(set(package_headers))
    print(packages[:6])
    packages_index = PackagesGuidIndex(packages)
    assert packages_index.get('0002555a') == '0002555a-9d30-43b0-baab-a61603431a9d'
    assert packages_index.get('a61603431a9d') == '0002555a-9d30-43b0-baab-a61603431a9d'
    assert packages_index.get('000fe5aa') == '000fe5aa-1d77-42d1-bfe7-458c51dacfef'
    assert packages_index.get('458c51dacfef') == '000fe5aa-1d77-42d1-bfe7-458c51dacfef'
