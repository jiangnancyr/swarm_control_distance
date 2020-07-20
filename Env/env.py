import yaml
import os
resMap = {}
agentParams = {}

path = os.path.realpath(__file__)

path = path.split('Env\\env.py')[0] + 'config\\config.yml'
def getConfig(path="../config/config.yml",
              configName='mainConfig'):

    """
    读取配置文件内容
    """
    f = open(path, 'r', encoding='utf-8')
    content = f.read()
    config = yaml.load(content, Loader=yaml.FullLoader)
    return config[configName]

def real_N():
    density = Env_mainConfig['simulation']['density']
    L = Env_mainConfig['agentParams']['L']
    N = 0
    if density != 0:
        N = L ** 2 * density
    Env_mainConfig['agentParams']['N'] = N

Env_mainConfig = getConfig(path=path)
real_N()