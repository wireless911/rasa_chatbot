from sanic import Blueprint

import asyncio
import functools
import logging

import os
import tempfile
import traceback
import typing

from typing import Any, Callable, List, Optional, Text, Union
from rasa.train import train as train_model
import rasa
import rasa.core.utils
from rasa.utils.common import raise_warning, arguments_of
import rasa.utils.endpoints
import rasa.utils.io

from rasa.constants import (
    DEFAULT_DOMAIN_PATH,
    DEFAULT_MODELS_PATH,
    DEFAULT_RESPONSE_TIMEOUT,
    DOCS_BASE_URL,
    MINIMUM_COMPATIBLE_VERSION,
)

from rasa.core.domain import InvalidDomain
from sanic import Sanic, response
from sanic.request import Request
from sanic.response import HTTPResponse

from train.context import PathContext

logger = logging.getLogger(__name__)
model = Blueprint('model', url_prefix='/model')


@model.route('/')
async def home(request):
    return response.text(request.path)


@model.post("/train")
async def train(request: Request) -> HTTPResponse:
    """Train a Rasa Model."""
    path_context =  PathContext()

    params = {

    }


    train_model()









