import os

from starlette.requests import Request

from src.database.engine import Postgres


def provide_database(request: Request) -> Postgres:
    return request.app.state.postgres
