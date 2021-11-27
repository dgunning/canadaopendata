from pathlib import Path
import json
from opencanada.api import Package, DatasetPackage
from rich import print


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
