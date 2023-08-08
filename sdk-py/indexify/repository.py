import aiohttp
import requests

from .data_containers import TextChunk
from .settings import DEFAULT_INDEXIFY_URL
from .utils import _get_payload, wait_until


def create_repository(name: str, extractors: list = [], metadata: dict = {},
                      base_url: str = DEFAULT_INDEXIFY_URL) -> None:
    req = {"name": name, "extractors": extractors, "metadata": metadata}
    response = requests.post(f"{base_url}/repository/create", json=req)
    response.raise_for_status()
    return response.json()


def list_repositories(base_url: str = DEFAULT_INDEXIFY_URL) -> list[dict]:
    response = requests.get(f"{base_url}/repository/list")
    response.raise_for_status()
    return response.json()['repositories']


class ARepository:

    def __init__(self, base_url: str, name: str):
        self._base_url = base_url
        self._name = name
        self._url = f"{self._base_url}/repository"
        # TODO: self._url = f"{self._base_url}/repository/{self._name}"

    async def run_extractors(self) -> dict:
        req = {"repository": self._name}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self._url}/run_extractors", json=req) as resp:
                return await _get_payload(resp)

    async def add(self, *chunks: TextChunk) -> None:
        parsed_chunks = []
        for chunk in chunks:
            parsed_chunks.append(chunk.to_dict())
        req = {"documents": parsed_chunks, "repository": self._name}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self._url}/add_texts", json=req) as resp:
                return await _get_payload(resp)

    async def add_documents(self, *documents: dict) -> None:
        req = {"documents": documents, "repository": self._name}
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self._url}/add_texts", json=req) as resp:
                return await _get_payload(resp)

    async def _create_repository(self):
       req = {"name": self._name, "extractors": [], "metadata": {}}
       async with aiohttp.ClientSession() as session:
            async with session.post(f"{self._url}/create", json=req) as resp:
                return await _get_payload(resp)

    async def _list_repositories(self):
       async with aiohttp.ClientSession() as session:
            async with session.get(f"{self._url}/list") as resp:
                return await _get_payload(resp)




class Repository(ARepository):

    def __init__(self, base_url: str = DEFAULT_INDEXIFY_URL, name: str = "default"):
        super().__init__(base_url, name)
        if not self._name_exists():
            print(f"creating repo {self._name}")
            create_repository(name=self._name, base_url=self._base_url)

    def add(self, *chunks: TextChunk) -> None:
        return wait_until(ARepository.add(self, *chunks))

    def add_documents(self, *documents: dict) -> None:
        return wait_until(ARepository.add_documents(self, *documents))

    def run_extractors(self) -> dict:
        return wait_until(ARepository.run_extractors(self, self._name))

    def _name_exists(self) -> bool:
        return self._name in [r['name'] for r in list_repositories(self._base_url)]
