from typing import Any, Protocol


class RepositoryProtocol(Protocol):
    def create(self, schema: Any) -> Any: ...


class BaseService:
    def __init__(self, repository: RepositoryProtocol) -> None:
        self._repository = repository

    def create(self, schema: Any) -> Any:
        return self._repository.create(schema)

    def close_scoped_session(self):
        self._repository.close_scoped_session()
