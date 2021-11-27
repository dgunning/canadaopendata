from opencanada.settings import get_config


def test_get_config():
    config = get_config()
    assert config.inventory_dataset
