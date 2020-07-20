import matplotlib.pyplot as plt
import random
import math
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import sys
import scipy.io as scio


class AgentPlot:
    def __init__(self,
                 mainConfig):
        self.L = mainConfig['agentParams']['L']
        self.N = mainConfig['agentParams']['N']
        self.plotShow = mainConfig['simulation']['plotShow']
        if self.plotShow:
            self.agentsShowList = []
            self.fig = plt.figure()  # 制作图表fig
            self.ax = []
            self.ax.append(self.fig.add_subplot(111))
            self.ax[0].set_xlabel('x')  # 坐标轴加标签
            self.ax[0].set_ylabel('y')
            self.ax[0].set_ylim(0, self.L)
            self.ax[0].set_xlim(0, self.L)

    def show(self,
             agents):
        self.agentsShowList = []
        for realAgent in agents:
            realAgent.agent.isUpdate = False
            agentPos = realAgent.agent.nextPos
            agentDir = realAgent.agent.nextDir
            agentPlot = self.ax[0].arrow(agentPos[0],
                                         agentPos[1],
                                         agentDir[0] * 0.5,
                                         agentDir[1] * 0.5,
                                         width=0.01,
                                         length_includes_head=True,  # 增加的长度包含箭头部分
                                         head_width=0.5 * 0.2,
                                         head_length=1 * 0.2,
                                         fc='royalblue',
                                         ec='royalblue',
                                         alpha=0.8)
            self.agentsShowList.append(agentPlot)
            #print(realAgent)
    def clearPlot (self):
        for agentsShow in self.agentsShowList:
            agentsShow.remove()

    @staticmethod
    def pause (time=0.01):
        plt.pause(time)

    def agentShow(self,
                  agents,
                  time=0.01):
        if self.plotShow:
            self.clearPlot()
            self.show(agents)
            self.pause(time)
        else:
            for realAgent in agents:
                realAgent.agent.isUpdate = False
