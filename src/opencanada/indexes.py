import logging
from typing import List
from rank_bm25 import BM25Okapi
from opencanada.api import list_packages
import asyncio

logger = logging.getLogger(__name__)


class PackagesGuidIndex:

    def __init__(self, packages: List[str]):
        tokens = [
            [p[:8], p[-12:]]
            for p in packages
        ]
        self.packages = packages
        self.bm25 = BM25Okapi(tokens)
        logger.info(f'Built index of guids from {len(self.packages):,} packages')

    def get(self, package_query: str):
        guid = self.bm25.get_top_n([package_query], self.packages, n=1)[0]
        return guid


async def load_packages_guid():
    packages = await list_packages()
    return PackagesGuidIndex(packages)

guid_index = asyncio.run(load_packages_guid())

if __name__ == '__main__':
    print(guid_index)
