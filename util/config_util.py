#%%

import yaml

# This code provides various utility functions to load YAML files, 
# extract values from dictionaries using dot notation keys, and retrieve configuration 
# values from a YAML file. Additionally, it includes functions to determine if the 
# application is running in production mode, and to retrieve directory paths for processing, 
# media, fonts, and prompts. 

# load YAML file
def load_yaml(file_path):
    with open(file_path) as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exception:
            print(exception)

def get_value(settings, dot_notation_key: str):
    try:
        value = settings
        for key in dot_notation_key.strip('.').split('.'):
            value = value[key]
    except (KeyError, TypeError):
        value = None
    return value

settings = load_yaml('config/app.config.yaml')

def isProd():
    return get_value(settings, 'prod')

def getProcessingDir():
    return get_value(settings, 'workspace.processing')

def getMediaDir():
    return get_value(settings, 'workspace.media')

def getFontDir():
    return get_value(settings, 'workspace.font')

def getPromptDir():
    return get_value(settings, 'workspace.prompt')
  
def getTemplateBox():
    try:
        return getMediaDir()+'/'+get_value(settings, 'templates.box')
    except Exception as e:
        print('TemplateBox not found')

def getContainer():
    try:
        return getMediaDir()+'/'+get_value(settings, 'templates.container')
    except Exception as e:
        print('Container not found')

# %%
