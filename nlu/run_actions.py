

import types
from typing import List, Text, Union

from rasa_sdk.endpoint import configure_cors, run
from sanic import Sanic, response
from sanic.response import HTTPResponse
from sanic.request import Request
from rasa_sdk import utils
from rasa_sdk.executor import ActionExecutor
from rasa_sdk.interfaces import ActionExecutionRejection, ActionNotFoundException
from sanic.log import logger as _logger
from setting.logger_setting import  get_logging_config



def configure_app(
    action_package_name:Union[Text,types.ModuleType],
    app:Sanic = None
) -> Sanic:
    executor = ActionExecutor()
    executor.register_package(action_package_name)

    @app.get("/health")
    async def health(_) -> HTTPResponse:
        """Ping endpoint to check if the server is running and well."""
        body = {"status": "ok"}
        return response.json(body, status=200)

    @app.post("/webhook")
    async def webhook(request: Request) -> HTTPResponse:
        """Webhook to retrieve action calls."""
        action_call = request.json
        if action_call is None:
            body = {"error": "Invalid body request"}
            return response.json(body, status=400)

        utils.check_version_compatibility(action_call.get("version"))
        try:
            result = await executor.run(action_call)
        except ActionExecutionRejection as e:
            _logger.error(e)
            body = {"error": e.message, "action_name": e.action_name}
            return response.json(body, status=400)
        except ActionNotFoundException as e:
            _logger.error(e)
            body = {"error": e.message, "action_name": e.action_name}
            return response.json(body, status=404)

        return response.json(result, status=200)

    @app.get("/actions")
    async def actions(_) -> HTTPResponse:
        """List all registered actions."""
        body = [{"name": k} for k in executor.actions.keys()]
        return response.json(body, status=200)

    return app


def run_rasa_actions(port=5055, workers_num=4,cors_origins="*"):
    """
    run rasa actions
    :return:
    """

    action_package_name = "actions"
    app = Sanic(__name__, configure_logging=True,log_config=get_logging_config(name=run_rasa_actions.__name__))

    configure_cors(app, cors_origins)

    app = configure_app(action_package_name,app=app)
    app.run("0.0.0.0", port, workers=workers_num, debug=True, access_log=True, auto_reload=True)


if __name__ == '__main__':
    run_rasa_actions()
