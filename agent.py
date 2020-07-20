import numpy as np
import copy
from Env.env import agentParams, resMap
from math import *



class Agent:

    def __init__(self ,
                 params,
                 num,
                 nextDir,
                 nextPos):
        self.L = params['L']
        self.N = params['N']
        self.R = params['R']
        self.V = params['V']
        # 单步运行时间
        self.stepTime = params['stepTime']
        #粒子编号num
        self.num = num
        #粒子的位置
        self.pos = np.array([0,0])
        #粒子的方向
        self.dir = np.array([0,0])
        #下一步方向
        self.nextDir = nextDir
        #下一步的位置
        self.nextPos = nextPos
        # 是否更新过
        self.isUpdate = False
        # 局部同步率
        self.syncRate = 0


    def getNeighbors(self,
                    agentsList):
        """
        从粒子分区列表中获取当前邻居
        :param agentsList: 是一个存放个体的表，元素是Agent
        :return: 返回邻居列表
        """
        neighboursList = []
        n = len(agentsList)
        #获取自己的区域位置
        selfX = int(self.nextPos[0]/1)
        selfY = int(self.nextPos[1]/1)
        #读取四周区域内的粒子一共九块
        for i in range(selfX - 1, selfX + 2):
            for j in range(selfY - 1, selfY + 2):
                #周期性边界需要换算位置偏差。
                dx = 0 if (0 <= i < n) else \
                    (self.L if (i >= n) else -self.L)
                dy = 0 if (0 <= j < n) else \
                    (self.L if (j >= n) else -self.L)
                #获取该块的粒子
                blockAgents = agentsList[(i + n)%n][(j + n)%n]
                for blockAgent in blockAgents:
                    #判断是否更新过
                    p = blockAgent.pos if(blockAgent.isUpdate == True) else blockAgent.nextPos
                    #print(blockAgent.num ,' ', p)#[0.09840375 2.85768214]
                    if (p[0] - self.nextPos[0] + dx)**2 + \
                            (p[1] - self.nextPos[1] + dy)**2 <= self.R**2:
                        #在通讯范围内就就添加到邻居列表。保存的是变换后的位置，直接运算。
                        neighboursList.append(blockAgent)
        return neighboursList

    def LocalSyncRate(self,
                         neighboursList):
        dirSum = np.array([0.0, 0.0])
        for neighbour in neighboursList:
            neighborDir = neighbour.dir if (neighbour.isUpdate == True) else neighbour.nextDir
            dirSum += neighborDir
        dirSum /= len(neighboursList)
        self.syncRate = sqrt(dirSum[0]**2 + dirSum[1]**2)
        # print(self.syncRate)

    def updateAgent(self,
                  neighboursList,
                  algorithm):
        """
        更新邻居的位置，方向。
        :param neighboursList: 邻居列表,存放的还是粒子的对象。
        :param algorithm: 算法回调函数
        :return: 无
        """
        #保存旧的位置
        self.pos = copy.deepcopy(self.nextPos)
        self.dir = copy.deepcopy(self.nextDir)
        #更新下一步状态
        self.nextDir = algorithm(neighboursList, self)

        self.nextPos += self.nextDir * self.V * self.stepTime

        # 这里更新的位置也需要重新计算在周期边界的实际位置。
        self.nextPos[0] = self.nextPos[0] if (0 <= self.nextPos[0] < self.L) else \
            (self.nextPos[0] - self.L if (self.nextPos[0] >= self.L) else self.nextPos[0] + self.L)
        self.nextPos[1] = self.nextPos[1] if (0 <= self.nextPos[1] < self.L) else \
            (self.nextPos[1] - self.L if (self.nextPos[1] >= self.L) else self.nextPos[1] + self.L)
        self.isUpdate = True

    def outPutPos(self):
        return copy.deepcopy(self.nextPos)

    def __str__(self) -> str:
        return '{' + super(Agent, self).__str__() + ',' +\
               'num:' + str(self.num) + \
               ',pos:' + str(self.pos) + \
                ',dir:' + str(self.dir) + \
               ',nextPos:' + str(self.nextPos) + \
                ',nextDir:' + str(self.nextDir) + '}'





