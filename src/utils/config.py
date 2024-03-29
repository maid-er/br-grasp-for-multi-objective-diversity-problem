import os
import yaml


def read_config(instance_name):
    yaml_relative_path = os.path.join('..', '..', 'config', f'{instance_name}.yaml')
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), yaml_relative_path)
    with open(file_path, 'r', encoding='utf-8') as yamlfile:
        config = yaml.safe_load(yamlfile)

    return config
