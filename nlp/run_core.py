import asyncio
import logging
import uuid
import os
import shutil
from functools import partial
from typing import Any, List, Optional, Text, Union

import rasa.core.utils
import rasa.utils
import rasa.utils.common
import rasa.utils.io
from rasa import model, server
from rasa.constants import ENV_SANIC_BACKLOG
from rasa.core import agent, channels, constants
from rasa.core.agent import Agent
from rasa.core.brokers.broker import EventBroker
from rasa.core.channels import console
from rasa.core.channels.channel import InputChannel
from rasa.core.interpreter import NaturalLanguageInterpreter
from rasa.core.lock_store import LockStore
from rasa.core.run import create_http_input_channels, configure_app, load_agent_on_start
from rasa.core.tracker_store import TrackerStore
from rasa.core.utils import AvailableEndpoints
from rasa.utils.common import raise_warning
from sanic import Sanic
from sanic.log import logger

from api import api


def serve_application(
    model_path: Optional[Text] = None,
    channel: Optional[Text] = None,
    port: int = constants.DEFAULT_SERVER_PORT,
    credentials: Optional[Text] = None,
    cors: Optional[Union[Text, List[Text]]] = None,
    auth_token: Optional[Text] = None,
    enable_api: bool = True,
    response_timeout: int = constants.DEFAULT_RESPONSE_TIMEOUT,
    jwt_secret: Optional[Text] = None,
    jwt_method: Optional[Text] = None,
    endpoints: Optional[AvailableEndpoints] = None,
    remote_storage: Optional[Text] = None,
    log_file: Optional[Text] = None,
    ssl_certificate: Optional[Text] = None,
    ssl_keyfile: Optional[Text] = None,
    ssl_ca_file: Optional[Text] = None,
    ssl_password: Optional[Text] = None,
    conversation_id: Optional[Text] = uuid.uuid4().hex,
):
    """Run the API entrypoint."""
    from rasa import server

    if not channel and not credentials:
        channel = "cmdline"

    input_channels = create_http_input_channels(channel, credentials)

    app = configure_app(
        input_channels,
        cors,
        auth_token,
        enable_api,
        response_timeout,
        jwt_secret,
        jwt_method,
        port=port,
        endpoints=endpoints,
        log_file=log_file,
        conversation_id=conversation_id,
    )

    ssl_context = server.create_ssl_context(
        ssl_certificate, ssl_keyfile, ssl_ca_file, ssl_password
    )
    protocol = "https" if ssl_context else "http"

    logger.info(
        "Starting Rasa server on "
        "{}".format(constants.DEFAULT_SERVER_FORMAT.format(protocol, port))
    )

    app.register_listener(
        partial(load_agent_on_start, model_path, endpoints, remote_storage),
        "before_server_start",
    )

    # noinspection PyUnresolvedReferences
    async def clear_model_files(_app: Sanic, _loop: Text) -> None:
        if app.agent.model_directory:
            shutil.rmtree(_app.agent.model_directory)

    app.register_listener(clear_model_files, "after_server_stop")

    rasa.utils.common.update_sanic_log_level(log_file)


    # 注册自己的蓝图
    app.register_blueprint(api)

    app.run(
        host="0.0.0.0",
        port=port,
        ssl=ssl_context,
        backlog=int(os.environ.get(ENV_SANIC_BACKLOG, "100")),
        workers=rasa.core.utils.number_of_sanic_workers(
            endpoints.lock_store if endpoints else None
        ),
    )



