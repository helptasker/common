from fastapi import FastAPI

from .logger import logger_init
from .middlewares import Middleware


class HelpTaskerCommonFastApiInstrumentator:
    def __init__(self, logger_load: bool = True):
        self.logger_load = logger_load

    def instrument(self, app: FastAPI):
        if self.logger_load:
            logger_init()

        app.add_middleware(Middleware)
        return self
