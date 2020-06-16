from sanic import Blueprint

from .conversations import conversations
from .model import model

# 蓝图注册
api = Blueprint.group(conversations, model, url_prefix='/api')