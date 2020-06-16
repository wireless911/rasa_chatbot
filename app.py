from rasa import run
from rasa.server import create_app

from train.context import PathContext


# def main():
#     """Sanic server """
#     # 创建路径上下文对象
#     path_context = PathContext()
#     # 代理商
#     agent = create_agent(path_context.model_directory)
#     # jwt secret　key
#     # jwt_secret = '9faupnfvqxeu0@_2wl61!jine0urasw^yidj&b_j_1s$!8e2tr'
#
#     api = create_app(agent=agent)
#
#     # 注册input_channel
#     from nlu.channels import MyRestInput
#     register(input_channels=[MyRestInput()],api=api,route=api.router)
#
#     api.run(host='0.0.0.0', port=5005, debug="DEBUG", access_log=True)
#     pass


def rasa_run():
    """rasa run """
    # 创建路径上下文对象
    path_context = PathContext()
    run(model=path_context.model_directory, endpoints=path_context.endpoints_file_path,
        credentials=path_context.credentials_file_path,log_file="./logs/wireless.log")




if __name__ == '__main__':
    rasa_run()
