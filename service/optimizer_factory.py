from typing import Hashable, Callable

from comradewolf.universe.olap_language_select_builders import OlapPostgresSelectBuilder
from sqlalchemy import Engine

from core.utils.exceptions import ClassNotFoundError
from service.optimizer_postgres import OptimizerPostgres


class OptimizerFactory:
    """
    Factory for different engine optimizers
    """
    @staticmethod
    def get(engine_name: str, max_connections: int, engine: Engine, **kwargs):
        """

        :param engine:
        :param max_connections:
        :param engine_name:
        :param kwargs:
        :return:
        """

        classes: dict[Hashable, Callable[..., object]] = {
            "postgresql+psycopg2": OptimizerPostgres,
        }

        class_ = classes.get(engine_name, None)
        if class_ is not None:
            return class_(max_connections=max_connections, engine=engine, **kwargs)

        raise ClassNotFoundError(engine_name)


class SelectBuilderFactory:
    @staticmethod
    def get(engine_name: str, **kwargs):


        classes: dict[Hashable, Callable[..., object]] = {
            "postgresql+psycopg2": OlapPostgresSelectBuilder,
        }

        class_ = classes.get(engine_name, None)
        if class_ is not None:
            return class_(**kwargs)

        raise ClassNotFoundError(engine_name)
