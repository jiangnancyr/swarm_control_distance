from algorithmFactory import *


class AgentProxy:

    def __init__(self,
                 agent,
                 simulation):
        self.agent = agent
        self.algorithm = AlgorithmFactory()\
            .createAlgorithm(simulation['algorithmName'])


    def agentRun(self,
                 agentsList):
        """
        代理负责执行一次粒子的运行
        :param agentsList: 粒子列表
        :return: 返回新的位置
        """
        #获取邻居
        neighboursList = self.agent.getNeighbors(agentsList)
        #更新粒子信息
        self.agent.updateAgent(neighboursList, self.algorithm)
        # self.agent.LocalSyncRate(neighboursList)
        #返回新的位置
        return  self.agent

    def __str__(self) -> str:
        return self.agent.__str__()

