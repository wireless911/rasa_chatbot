from rasa.core.agent import Agent

from rasa.core.interpreter import RasaNLUInterpreter
from train.context import PathContext


class LSTMAgent(Agent):
    def __init__(self, *args, **kwargs):
        # 创建路径上下文对象
        path_context = PathContext()
        # nlu 模块
        interpreter = RasaNLUInterpreter(model_directory=path_context.model_directory,config_file=path_context.config_file_path)

        super(LSTMAgent).__init__(domain=path_context.domain_path, interpreter=interpreter,model_directory=path_context.model_directory)




