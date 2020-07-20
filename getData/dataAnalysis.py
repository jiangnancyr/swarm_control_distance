import numpy as np
from math import *
from Env.env import *

class DataAnalysis:
    def __init__(self,
                 mainConfig):
        self.mainConfig = mainConfig
        self.L = mainConfig['agentParams']['L']
        self.N = mainConfig['agentParams']['N']

        self.cellNumber = mainConfig['simulation']['cellNumber']
        self.cellCut = sqrt(self.cellNumber)
        self.cellLength = self.L / self.cellCut
        self.cellCount = np.zeros((int(self.cellCut),int(self.cellCut)))
        self.entropy = 0

        self.resMap = resMap
        self.syncRate = 0
        self.localSyncRate = 0
        self.sumDir = np.array([0.0, 0.0])
        #共输入多少粒子
        self.agentNum = 0


    def getSyncRate(self,
                    realAgent,
                    key='syncRate'):
        """
        获取同步率
        :param realAgent: 输入一个粒子
        :return:
        """
        #方向累加
        self.sumDir += realAgent.nextDir

        if self.agentNum == self.N:
            self.syncRate = sqrt(self.sumDir[0]**2 + self.sumDir[1]**2) / self.N
            self.sumDir = np.array([0.0, 0.0])
            self.resMap[key] = self.syncRate

    def getLocalSyncRate(self,
                         realAgent,
                         key='localSyncRate'):

        self.localSyncRate += realAgent.syncRate
        if self.agentNum == self.N:
            resMap[key] =  self.localSyncRate/self.N
            self.localSyncRate = 0

    def getEntropy(self,
                   realAgent,
                   key='entropy'):

        xIndex = int(realAgent.nextPos[0] / self.cellLength)
        yIndex = int(realAgent.nextPos[1] / self.cellLength)
        self.cellCount[xIndex][yIndex] += 1

        if self.agentNum == self.N:
            self.entropy = 0.0
            self.cellCount /= self.N
            for cow in self.cellCount:
                for col in cow:
                    if col != 0:
                        self.entropy -= col*log(col)
            self.cellCount = np.zeros((int(self.cellCut), int(self.cellCut)))
            self.resMap[key] = self.entropy


    def dealAllData(self,
                    realAgent):
        """
        :param realAgent:
        :return:
        """
        self.agentNum += 1
        # 添加需要获取的数据算法
        # 获取同步速度
        self.getSyncRate(realAgent)
        # 获取熵值
        self.getEntropy(realAgent)
        # 获取局部同步
        # self.getLocalSyncRate(realAgent)

        if self.agentNum >= self.N:
            self.agentNum = 0

    def getAllAnalysis(self,
                       key):
        """
        从结果集合中获取数据
        :param key:
        :return:
        """
        return self.resMap[key]
