import numpy as np
from math import *
from copy import deepcopy
import yaml
import random
from Env.env import agentParams, resMap



def addNoise(realDir):
    noise = agentParams['noise']
    noiseDir = np.array([0.0, 0.0])
    if noise != 0:
        noiseAngle = random.uniform(-noise, noise)
        noiseDir[0] = realDir[0] * cos(noiseAngle) \
                 - realDir[1] * sin(noiseAngle)
        noiseDir[1] = realDir[0] * sin(noiseAngle) \
                 + realDir[1] * cos(noiseAngle)
    else:
        noiseDir = realDir
    return noiseDir

def getConfig(path="config/config.yml"):
    """
    读取配置文件内容
    """
    f = open(path, 'r', encoding='utf-8')
    content = f.read()
    config = yaml.load(content, Loader=yaml.FullLoader)
    return config['algorithmParams']

algorithmParams = getConfig()

def Vicseck(neighboursList,
            centerAgent):
    """
    Vicsek模型算法
    :param neighboursList:
    :param centerAgent:
    :return:
    """
    dirSum = np.array([0.0, 0.0])
    #print(neighboursList)
    for neighbour in neighboursList:
        d = neighbour.dir if (neighbour.isUpdate == True) else neighbour.nextDir
        dirSum += d
    realDir = dirSum / sqrt(dirSum[0] ** 2 + dirSum[1] ** 2)
    return addNoise(realDir)

def syncControlDistance(neighboursList,
                        centerAgent):
    """
    方向同步控制距离
    :param neighboursList:
    :param centerAgent:
    :return:
    """
    V = centerAgent.V
    stepTime = centerAgent.stepTime
    R = centerAgent.R
    L = centerAgent.L
    dirSum = np.array([0.0, 0.0])
    for neighbour in neighboursList:
        neighborDir = neighbour.dir if (neighbour.isUpdate == True) else neighbour.nextDir
        neighborPos = neighbour.pos if (neighbour.isUpdate == True) else neighbour.nextPos
        #重新复制一份
        neighborPos = deepcopy(neighborPos)

        centerAgentPos = centerAgent.nextPos
        centerAgentDir = centerAgent.nextDir
        #换算相对位置修改坐标
        if neighborPos[0] - centerAgentPos[0] > R:
            neighborPos[0] -= L
        elif centerAgentPos[0] - neighborPos[0] > R:
            neighborPos[0] += L

        if neighborPos[1] - centerAgentPos[1] > R:
            neighborPos[1] -= L
        elif centerAgentPos[1] - neighborPos[1] > R:
            neighborPos[1] += L

        #估计下一步为位置
        CenterAgentNewPos = centerAgentPos + centerAgentDir * V * stepTime
        neighborNewPose = neighborPos + neighborDir * V * stepTime

        dNow = centerAgentPos - neighborPos
        dPre = CenterAgentNewPos - neighborNewPose
        dd = sqrt(dNow[0]**2 + dNow[1]**2) - sqrt(dPre[0]**2 + dPre[1]**2)
        #print(dd)
        k1 = algorithmParams['syncControlDistance']['k1']
        dirSum += exp(k1 * dd)*neighborDir

    realDir = dirSum / sqrt(dirSum[0] ** 2 + dirSum[1] ** 2)
    return addNoise(realDir)


