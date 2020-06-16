import os
import sys

from rasa.model import get_model

from setting.settings import (CHATBOT_NLU_PATH, TRAIN_DATA_PATH, MODEL_PATH)


class PathContext(object):
    def __init__(self):
        self.nlu_data_path = CHATBOT_NLU_PATH
        # config
        self.config_file_path = os.path.join(CHATBOT_NLU_PATH,"config.yml")
        self.credentials_file_path = os.path.join(CHATBOT_NLU_PATH,"credentials.yml")
        self.endpoints_file_path = os.path.join(CHATBOT_NLU_PATH,"endpoints.yml")
        self.connect_path = os.path.join(CHATBOT_NLU_PATH,"channels.")
        self.domain_path = os.path.join(CHATBOT_NLU_PATH, "domain.yml")

        # data

        self.nlu_md_path = os.path.join(TRAIN_DATA_PATH, "nlu.md")
        self.stories_path = os.path.join(TRAIN_DATA_PATH, "stories.md")
        # model
        # self.model_directory =get_model(MODEL_PATH)  # model 解压缩
        self.model_directory = MODEL_PATH # model 解压缩

        # actions floder
        # self.action_package_path = "actions"
        self.action_package_path = os.path.join(TRAIN_DATA_PATH, "actions")
        # sys.path.insert(0,self.action_package_path)







