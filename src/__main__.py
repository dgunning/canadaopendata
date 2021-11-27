import typer
from rich import print

from opencanada.datasets import inventory

import pandas as pd
pd.options.display.max_columns = 30


def main():
    print(inventory.metadata)
    print(inventory.metadata.resources
          .filter(['name', 'resource_type', 'state', 'url'])
          .rename(columns={'resource_type': 'type'})
          )


if __name__ == '__main__':
    typer.run(main)