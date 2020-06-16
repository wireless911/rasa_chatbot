from sanic import Blueprint
from sanic import response

conversations = Blueprint('conversations', url_prefix='/conversations')

@conversations.route('/')
async def home(request):
    return response.text(request.path)