from math import *
import numpy as np
import yaml
import random
import scipy.io as scio

class AgentInit:
    def __init__(self,
                 mainConfig):
        """
        类初始化，获取配置文件中的参数
        :param mainConfig:
        """
        self.mainConfig = mainConfig
        self.density = mainConfig['simulation']['density']
        self.N = mainConfig['agentParams']['N']
        self.L = mainConfig['agentParams']['L']
        self.V = mainConfig['agentParams']['V']
        self.initStatus = mainConfig['simulation']['initStatus']
        self.agentsPos = np.zeros((self.N, 2))
        self.agentsDir = np.zeros((self.N, 2))
        self.agentsVel = np.zeros((self.N, 1))
        #保留参数
        self.messages = []

    def createAgentsInit(self):
        """
        创建一个集群初始化状态
        """
        if self.initStatus == 0:
            for i in range(self.N):
                #初始化位置
                self.agentsPos[i][0] = random.uniform(0, self.L)
                self.agentsPos[i][1] = random.uniform(0, self.L)
                #初始化速度，这里固定了
                self.agentsVel[i][0] = self.V
                #初始化方向
                angle = random.uniform(0, 2 * pi)
                self.agentsDir[i][0] = cos(angle)
                self.agentsDir[i][1] = sin(angle)

        return self.agentsPos, self.agentsDir, self.agentsVel

    def saveAgentsInit(self, fileName='xxx.mat'):
        """
        保存初始化好的数据到mat中
        :param fileName:
        :return:
        """
        #粒子初始化
        self.createAgentsInit()
        #保存到文件中
        filePath = str(self.mainConfig['filePath']['initAgents']) + fileName
        scio.savemat(filePath, {'agentsPos': self.agentsPos,
                                'agentsVel': self.agentsVel,
                                'agentsDir': self.agentsDir,
                                'messages': np.array([self.L, self.L, self.N])})

    def getInitFromFile(self,
                        filePath='xxx/xxx.mat',
                        num=0):
        """
        从文件中获取初始粒子群状态。
        :param filePath: 保存的文件名
        :return:
        """
        parameters={}
        try:
            parameters = scio.loadmat(filePath)
        except FileNotFoundError:
            print(filePath + '文件不存在！')
            self.saveOneAgentInit(num)
            parameters = scio.loadmat(filePath)
        self.agentsPos = parameters['agentsPos']
        self.agentsVel = parameters['agentsVel']
        self.agentsDir = parameters['agentsDir']
        self.messages = parameters['messages'][0]
        if self.messages[0] != self.L or \
            self.messages[1] != self.L or \
            self.messages[2] != self.N:
            print('初始化集群信息错误！')
            return None

        return self.agentsPos, self.agentsDir, self.agentsVel

    def getAgentInitWithName(self,
                            fileName='xxx.mat',
                             num=0):
        """
        获取集群的初始状态
        :param fileName: 当从文件获取这个就是文件名，如果是每次都是新的则不使用
        :return:
        """
        if self.mainConfig['simulation']['useFile']:
            #从文件中获取
            return self.getInitFromFile(str(self.mainConfig['filePath']['initAgents']) + \
                                            fileName,
                                            num=num)
        else:
            return self.createAgentsInit()

    def getAgentInitWithIndex(self,
                               index):
        """
        包装getAgentInitWithName，按照下标获取
        :param index:
        :return:
        """
        fileName = 'agentsInit_' + str(self.L) + \
                   '_' + str(self.N) + \
                   '_' + str(index) + '.mat'
        return self.getAgentInitWithName(fileName,num=index)

    def saveMultiAgentsInit(self,
                            num=1):
        """
        创建num个初始化状态保存到问价中
        :param num: 个数
        :return:
        """
        for i in range(num):
            fileName = 'agentsInit_' + str(self.L) + \
                       '_' + str(self.N) + \
                       '_' + str(i) + '.mat'
            self.saveAgentsInit(fileName)

    def saveOneAgentInit(self,
                        num=0):
        """
        创建num个初始化状态保存到问价中
        :param num: 个数
        :return:
        """
        fileName = 'agentsInit_' + str(self.L) + \
                   '_' + str(self.N) + \
                   '_' + str(num) + '.mat'
        self.saveAgentsInit(fileName)


    def __str__(self) -> str:
        return '{' + 'L:' + str(self.L) + \
               ',N:' + str(self.N) + '}'


if __name__ == '__main__':
    path1 = "config/config.yml"
    f1 = open(path1, 'r', encoding='utf-8')
    content1 = f1.read()
    config1 = yaml.load(content1, Loader=yaml.FullLoader)
    mainConfig1 = config1['mainConfig']
    ai = AgentInit(mainConfig1)
    print(ai)
    #ai.saveMultiAgentsInit(10)
    ap, ad, av = ai.getAgentInitWithIndex(0)
    print(ap)
    print(ad)
    print(av)
