from train.context import PathContext
from rasa.train import train as train_model


def train():
    "train rasa model"

    path_context = PathContext()

    params = {
        "domain": path_context.domain_path,
        "config": path_context.config_file_path,
        "training_files": [path_context.nlu_md_path, path_context.stories_path],
        "output": path_context.model_directory,
    }

    train_model(**params)


if __name__ == '__main__':
    train()
