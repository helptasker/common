import typing

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .logger import logger_init
from .middlewares import Middleware


class HelpTaskerCommonFastApiInstrumentator:
    def __init__(
        self,
        logger_load: bool = True,
        cors_enable: bool = False,
        cors_allow_origins: typing.Sequence[str] = (),
        cors_allow_credentials: bool = False,
        cors_allow_methods: typing.Sequence[str] = ('GET',),
        cors_allow_headers: typing.Sequence[str] = (),
        trusted_host_enable: bool = True,
        trusted_host_allowed_hosts: typing.Sequence[str] | None = (),
    ):
        self.logger_load = logger_load
        self.cors_enable = cors_enable
        self.cors_allow_origins = cors_allow_origins
        self.cors_allow_credentials = cors_allow_credentials
        self.cors_allow_methods = cors_allow_methods
        self.cors_allow_headers = cors_allow_headers
        self.trusted_host_enable = trusted_host_enable
        self.trusted_host_allowed_hosts = trusted_host_allowed_hosts

    def instrument(self, app: FastAPI):
        if self.logger_load:
            logger_init()

        app.add_middleware(Middleware)

        if self.cors_enable:
            app.add_middleware(
                CORSMiddleware,
                allow_origins=self.cors_allow_origins,
                allow_credentials=self.cors_allow_credentials,
                allow_methods=self.cors_allow_methods,
                allow_headers=self.cors_allow_headers,
            )

        if self.trusted_host_enable:
            app.add_middleware(
                TrustedHostMiddleware,
                allowed_hosts=self.trusted_host_allowed_hosts,
            )

        return self
