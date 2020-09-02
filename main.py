from agent import *
from agentProxy import *
from agentsInit import *
from plotShow.agentsPlot import AgentPlot
import datetime
from getData.dataAnalysis import *
from excel.operateExcel import *
import time
from Env.env import agentParams, resMap
import matplotlib.pyplot as plt

class Main:

    def __init__(self,
                 configName):
        """
        初始化类
        :param configName: 选取一个配置名
        """
        self.mainConfig = {}
        self.agentConfig = {}
        self.configName = configName
        self.agents = []
        self.getConfig()

        self.L = self.agentConfig['L']
        #重新确定N
        self.N = self.agentConfig['N']
        self.density = self.mainConfig['simulation']['density']
        if self.density != 0:
            self.N = self.L**2*self.density
        self.agentConfig['N'] = self.N
        #初始化粒子初始状态
        self.ai = AgentInit(self.mainConfig)
        #初始化数据采集
        self.dal = DataAnalysis(self.mainConfig)
        agentParams['N'] = self.agentConfig['N']
        agentParams['noise'] = self.agentConfig['noise']

        print(self.mainConfig)
        print(self.agentConfig)
        self.blockLength = self.mainConfig['simulation']['blockLength']
        self.sideN = int(self.L/self.blockLength)
        self.agentsList = [ \
                           [[] for _ in range(self.sideN)] \
                           for _ in range(self.sideN)]

    def getConfig(self,
                  path="config/config.yml"):
        """
        读取配置文件内容
        """
        f = open(path, 'r', encoding='utf-8')
        content = f.read()
        config = yaml.load(content, Loader=yaml.FullLoader)
        self.mainConfig = config[self.configName]

        self.agentConfig = self.mainConfig['agentParams']


    def putAgentToBlock(self,
                        inputAgent):
        """
        将粒子分区，这里强调分区存储的是粒子本身而不是代理对象
        :param inputAgent: 被分区的粒子
        :return:
        """
        agentPos = inputAgent.nextPos
        xIndex = int(agentPos[0]/self.blockLength)
        yIndex = int(agentPos[1]/self.blockLength)
        self.agentsList[xIndex][yIndex].append(inputAgent)


    def initAgents(self,
                   index):
        """
        初始化所有的粒子
        """

        agentsPos, agentsDir, agentsVel = self.ai.getAgentInitWithIndex(index)
        #初始化N个粒子
        self.agents = []
        self.agentsList = [ \
            [[] for _ in range(self.sideN)] \
            for _ in range(self.sideN)]
        for i in range(self.N):
            realAgent = Agent(self.agentConfig,
                                i,
                                agentsDir[i],
                                agentsPos[i])
            agentProxy = AgentProxy(realAgent, self.mainConfig['simulation'])
            self.agents.append(agentProxy)
            self.putAgentToBlock(realAgent)


    def run(self,
            index
            ):
        """
        开始运行算法
        """
        count = 0
        dataMap = {}
        #print(self.agents[1])
        self.initAgents(index)
        ap = AgentPlot(self.mainConfig)
        syncRate = 0
        entropy = 0
        localSyncRate = 0
        while count < 2000:
            startTime = datetime.datetime.now()
            # 画图
            # if simulation['plotShow']:
            ap.agentShow(self.agents)
            # 保存之前的粒子分区表
            preAgentsList = self.agentsList
            # 清空表，存放新的粒子分区。
            self.agentsList = [ \
                [[] for _ in range(self.sideN)] \
                for _ in range(self.sideN)]
            for agentProxy in self.agents:
                # 返回一个跟新过状态的粒子
                realAgent = agentProxy.agentRun(preAgentsList)
                self.putAgentToBlock(realAgent)
                self.dal.dealAllData(realAgent)

            syncRate = self.dal.getAllAnalysis('syncRate')
            print('syncRate', syncRate)

            entropy = self.dal.getAllAnalysis('entropy')
            print('entropy', entropy)

            # localSyncRate = self.dal.getAllAnalysis('localSyncRate')
            # print('localSyncRate', localSyncRate)
            # 统计时间
            endTime = datetime.datetime.now()
            print((endTime - startTime))
            count += 1
            print('count:', count)
        # dataMap['localSyncRate'] = localSyncRate
        dataMap['syncRate'] = syncRate
        dataMap['entropy'] = entropy
        return dataMap

    def run_noise(self,
            index
            ):
        """
        开始运行算法
        """
        count = 0
        dataMap = {}
        #print(self.agents[1])
        self.initAgents(index)
        ap = AgentPlot(self.mainConfig)
        syncRate_list = []
        entropy_list = []
        while count < 2000:
            startTime = datetime.datetime.now()
            # 画图
            # if simulation['plotShow']:
            ap.agentShow(self.agents)
            # 保存之前的粒子分区表
            preAgentsList = self.agentsList
            # 清空表，存放新的粒子分区。
            self.agentsList = [ \
                [[] for _ in range(self.sideN)] \
                for _ in range(self.sideN)]
            for agentProxy in self.agents:
                # 返回一个跟新过状态的粒子
                realAgent = agentProxy.agentRun(preAgentsList)
                self.putAgentToBlock(realAgent)
                self.dal.dealAllData(realAgent)

            syncRate = self.dal.getAllAnalysis('syncRate')
            syncRate_list.append(syncRate)
            print('syncRate', syncRate)

            entropy = self.dal.getAllAnalysis('entropy')
            entropy_list.append(entropy)
            print('entropy', entropy)

            # localSyncRate = self.dal.getAllAnalysis('localSyncRate')
            # dataMap['localSyncRate'] = localSyncRate
            # print('localSyncRate', localSyncRate)
            # 统计时间
            endTime = datetime.datetime.now()
            print((endTime - startTime))
            count += 1
            print('count:', count)
        dataMap['syncRate_list'] = syncRate_list
        dataMap['entropy_list'] = entropy_list
        return dataMap

    def run_time(self,
            index
            ):
        """
        开始运行算法
        """
        count = 0
        dataMap = {}
        #print(self.agents[1])
        self.initAgents(index)
        ap = AgentPlot(self.mainConfig)
        syncRate = 0
        entropy = 0
        while syncRate < 0.95 and count < 10000:
            startTime = datetime.datetime.now()
            # 画图
            # if simulation['plotShow']:
            ap.agentShow(self.agents)
            # 保存之前的粒子分区表
            preAgentsList = self.agentsList
            # 清空表，存放新的粒子分区。
            self.agentsList = [ \
                [[] for _ in range(self.sideN)] \
                for _ in range(self.sideN)]
            for agentProxy in self.agents:
                # 返回一个跟新过状态的粒子
                realAgent = agentProxy.agentRun(preAgentsList)
                self.putAgentToBlock(realAgent)
                self.dal.dealAllData(realAgent)

            syncRate = self.dal.getAllAnalysis('syncRate')
            print('syncRate', syncRate)

            entropy = self.dal.getAllAnalysis('entropy')
            print('entropy', entropy)

            # localSyncRate = self.dal.getAllAnalysis('localSyncRate')
            # print('localSyncRate', localSyncRate)
            # 统计时间
            endTime = datetime.datetime.now()
            print((endTime - startTime))
            count += 1
            print('count:', count)
        # dataMap['localSyncRate'] = localSyncRate
        dataMap['entropy'] = entropy
        dataMap['count'] = count
        return dataMap

    def run_step(self,
            index
            ):
        """
         开始运行算法
         """
        count = 0
        dataMap = {}
        # print(self.agents[1])
        self.initAgents(index)
        ap = AgentPlot(self.mainConfig)
        syncRate_list = []
        entropy_list = []
        while count < 1000:
            startTime = datetime.datetime.now()
            # 画图
            # if simulation['plotShow']:
            ap.agentShow(self.agents)
            # 保存之前的粒子分区表
            preAgentsList = self.agentsList
            # 清空表，存放新的粒子分区。
            self.agentsList = [ \
                [[] for _ in range(self.sideN)] \
                for _ in range(self.sideN)]
            for agentProxy in self.agents:
                # 返回一个跟新过状态的粒子
                realAgent = agentProxy.agentRun(preAgentsList)
                self.putAgentToBlock(realAgent)
                self.dal.dealAllData(realAgent)

            syncRate = self.dal.getAllAnalysis('syncRate')
            syncRate_list.append(syncRate)
            print('syncRate', syncRate)

            entropy = self.dal.getAllAnalysis('entropy')
            entropy_list.append(entropy)
            print('entropy', entropy)

            # localSyncRate = self.dal.getAllAnalysis('localSyncRate')
            # dataMap['localSyncRate'] = localSyncRate
            # print('localSyncRate', localSyncRate)
            # 统计时间
            endTime = datetime.datetime.now()
            print((endTime - startTime))
            count += 1
            print('count:', count)
        dataMap['syncRate_list'] = syncRate_list
        dataMap['entropy_list'] = entropy_list
        return dataMap

class testClass:
    def __init__(self):
        self.main = Main('mainConfig')
        self.mainConfig = self.main.mainConfig
        self.agentConfig = self.main.agentConfig
        # 从algorithms中得到
        self.algorithmParams = algorithmParams

    def test_k1(self):

        simulation = self.mainConfig['simulation']
        fileName = './resData/' + simulation['algorithmName'] + \
                                 '_' + str(self.agentConfig['N']) + \
                                 '_' + str(self.agentConfig['L']) + \
                                 '_' + str(self.agentConfig['R']) + \
                                 '_' + str(self.agentConfig['V']) + \
                                 '_k1' + \
                                 '.xlsx'
        print(fileName)

        row = 0
        for k1 in range(-50, 0, 2):
            self.algorithmParams['syncControlDistance']['k1'] = k1
            dataMap = self.main.run(row)
            while True:
                try:
                    we = writeExcel(fileName=fileName)
                    we.writeCell(row + 1, int((k1 + 100) / 2) + 1, dataMap['syncRate'], 'syncRate')
                    we.writeCell(row + 1, int((k1 + 100) / 2) + 1, dataMap['entropy'], 'entropy')
                    we.writeCell(row + 1, int((k1 + 100) / 2) + 1, dataMap['localSyncRate'], 'localSyncRate')
                    we.saveExcel()
                    break
                except PermissionError:
                    time.sleep(1)

    def test_noise(self):

        simulation = self.mainConfig['simulation']
        fileName = './resData/' + simulation['algorithmName'] + \
                                 '_' + str(self.agentConfig['N']) + \
                                 '_' + str(self.agentConfig['L']) + \
                                 '_' + str(self.agentConfig['R']) + \
                                 '_' + str(self.agentConfig['V']) + \
                                 '_noise' + \
                                 '.xlsx'
        print(fileName)

        row = 0
        for k1 in range(-20, 20, 2):
            self.algorithmParams['syncControlDistance']['k1'] = k1
            dataMap = self.main.run(row)
            while True:
                try:
                    we = writeExcel(fileName=fileName)
                    we.writeCell(row + 1, int((k1 + 100) / 2) + 1, dataMap['syncRate'], 'syncRate')
                    we.writeCell(row + 1, int((k1 + 100) / 2) + 1, dataMap['entropy'], 'entropy')
                    we.writeCell(row + 1, int((k1 + 100) / 2) + 1, dataMap['localSyncRate'], 'localSyncRate')
                    we.saveExcel()
                    break
                except PermissionError:
                    time.sleep(1)

    def catch_figure(self):
        row = 0
        self.main.run(row)
        while True:
            plt.pause(0.1)

    def test_noises(self):
        simulation = self.mainConfig['simulation']
        k1 = self.algorithmParams['syncControlDistance']['k1']
        fileName = './resData/' + simulation['algorithmName'] + \
                                 '_' + str(self.agentConfig['N']) + \
                                 '_' + str(self.agentConfig['L']) + \
                                 '_' + str(self.agentConfig['R']) + \
                                 '_' + str(self.agentConfig['V']) + \
                                 '_' + str(k1) + \
                                 '_noise' + \
                                 '.xlsx'
        print(fileName)
        row = 0
        for k1 in range(0, 30):
            agentParams['noise'] = k1*0.05
            dataMap = self.main.run_noise(row)
            while True:
                try:
                    we = writeExcel(fileName=fileName)
                    we.writeRows(int(k1) + 1, dataMap['syncRate_list'], 'syncRate_list')
                    we.writeRows(int(k1) + 1, dataMap['entropy_list'], 'entropy_list')
                    # we.writeCell(row + 1, int((k1 + 100) / 2) + 1, dataMap['localSyncRate'], 'localSyncRate')
                    we.saveExcel()
                    break
                except PermissionError:
                    time.sleep(1)

    def test_time_entropy(self):
        simulation = self.mainConfig['simulation']
        fileName = './resData/' + simulation['algorithmName'] + \
                                 '_' + str(self.agentConfig['N']) + \
                                 '_' + str(self.agentConfig['L']) + \
                                 '_' + str(self.agentConfig['R']) + \
                                 '_' + str(self.agentConfig['V']) + \
                                 '_time_entropy' + \
                                 '.xlsx'
        print(fileName)
        row = 0
        for k1 in range(0, 100):
            dataMap = self.main.run_time(row)
            while True:
                try:
                    we = writeExcel(fileName=fileName)
                    we.writeCell(row + 1, k1 + 1, dataMap['entropy'], 'entropy')
                    we.writeCell(row + 1, k1 + 1, dataMap['count'], 'count')
                    # we.writeCell(row + 1, int((k1 + 100) / 2) + 1, dataMap['localSyncRate'], 'localSyncRate')
                    we.saveExcel()
                    break
                except PermissionError:
                    time.sleep(1)

    def test_step(self):
        simulation = self.mainConfig['simulation']
        k1 = self.algorithmParams['syncControlDistance']['k1']
        fileName = './resData/' + simulation['algorithmName'] + \
                                 '_' + str(self.agentConfig['N']) + \
                                 '_' + str(self.agentConfig['L']) + \
                                 '_' + str(self.agentConfig['R']) + \
                                 '_' + str(self.agentConfig['V']) + \
                                 '_' + str(k1) + \
                                 '_step' + \
                                 '.xlsx'
        print(fileName)
        for row in range(0, 100):
            dataMap = self.main.run_step(row)
            while True:
                try:
                    we = writeExcel(fileName=fileName)
                    we.writeRows(int(k1) + 1, dataMap['syncRate_list'], 'syncRate_list')
                    we.writeRows(int(k1) + 1, dataMap['entropy_list'], 'entropy_list')
                    # we.writeCell(row + 1, int((k1 + 100) / 2) + 1, dataMap['localSyncRate'], 'localSyncRate')
                    we.saveExcel()
                    break
                except PermissionError:
                    time.sleep(1)

if __name__ == '__main__':
    # main = Main('mainConfig')
    # main.run(0)
    test = testClass()
    test.test_noises()

