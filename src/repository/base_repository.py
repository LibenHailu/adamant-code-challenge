from contextlib import AbstractContextManager
from typing import Callable, Type, TypeVar

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.exceptions import DuplicatedError
from src.model.base_model import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[Session]],
        model: Type[T],
    ) -> None:
        self.session_factory = session_factory
        self.model = model

    def create(self, schema: T):
        with self.session_factory() as session:
            query = self.model(**schema.model_dump())
            try:
                session.add(query)
                session.commit()
                session.refresh(query)
            except IntegrityError as e:
                raise DuplicatedError(detail=str(e.orig))
            return query

    def close_scoped_session(self):
        with self.session_factory() as session:
            return session.close()
