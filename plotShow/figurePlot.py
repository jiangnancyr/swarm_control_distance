import matplotlib.pyplot as plt
import random
import math
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import sys
import scipy.io as scio

import xlrd
import xlwt
import openpyxl
# from pygame import color
from excel.operateExcel import *
from Env.env import *

"""
　　八种内建默认颜色缩写
　　b: blue
　　g: green
　　r: red
　　c: cyan
　　m: magenta
　　y: yellow
　　k: black
　　w: white
"""
colors = {  0:'b',
            1:'k',
            2:'r',
            3:'m',
            4:'c',
            5:'y',
            6:'g',
            7:'#005566',
            8:'#445566',
            9:'#445500',
            10:'#440066',}

lineStyle = {0:'-',
             1:'--',
             2:'-.',
             3:':',
             4:' '}

pointStyle = {0:'.',
              1:'x',
              2:'*',
              3:'v',
              4:'^',
              5:'s',
              6:'p',
              7:'+',
              8:'D',
              9:'d',
              10:''}


font = {'family' : 'Times New Roman',
        'color'  : 'black',
        'weight' : 'normal',
        'size'   : 20,
        }
fig = plt.figure()          #制作图表fig
class FigurePlot(object):
    def __init__(self,
                 figureName,
                 k=111):
        self.title = figureName           #图标标题
        self.fig = fig
        self.ax = {}
        self.ax = self.fig.add_subplot(k)  #当前画布切成1行1列，本图占1块ax1
        self.ax.set_xlabel('k')           #坐标轴加标签
        self.ax.set_ylabel(r'$\phi$')
        plt.title(self.title)                    #加上标题
        self.simulation = Env_mainConfig['simulation']
        self.agentConfig = Env_mainConfig['agentParams']

    def NiHe(self,
             data,
             n):
        if n == 2:
            res = [(data[i] + data[i + 1])/2 for i in range(len(data) - 2)]
            return res
        elif n == 3:
            res = [(data[i] + data[i + 1] + data[i + 2]) / 3 for i in range(len(data) - 3)]
            return res


    def k_entropy(self,
                  N, L, R, V,
                  c, m,
                  label,
                  name=''):
        fileName = '../resData/' + self.simulation['algorithmName'] + \
                   '_' + str(N) + \
                   '_' + str(L) + \
                   '_' + str(R) + \
                   '_' + str(V) + \
                   '_k1' + \
                   '.xlsx'

        re = readExcel(fileName)
        y = re.readRows(0,name)
        x = np.array([-100 + i*2 for i in range(len(y))])
        plt.scatter(x, y, c=c, marker=m, label=label)
        yy = self.NiHe(y,3)
        xx = [-100 + i * 2 for i in range(len(yy))]
        plt.plot(xx, yy, c=c)
        self.ax.legend()

def figure_entropy():
    fp = FigurePlot('', 111)
    fp.k_entropy(400, 20, 1, 1, 'g', '>', 'N=400,L=20', 'entropy')
    # fp = FigurePlot('', 111)
    fp.k_entropy(900, 30, 1, 1, 'b', 'v', 'N=900,L=30', 'entropy')
    # fp = FigurePlot('', 111)
    fp.k_entropy(1600, 40, 1, 1, 'r', '^', 'N=1600,L=40', 'entropy')
    plt.show()

def figure_syncRate():
    fp = FigurePlot('', 111)
    fp.k_entropy(400, 20, 1, 1, 'g', '>', 'N=400,L=20', 'syncRate')
    # fp = FigurePlot('', 111)
    fp.k_entropy(900, 30, 1, 1, 'b', 'v', 'N=900,L=30', 'syncRate')
    # fp = FigurePlot('', 111)
    fp.k_entropy(1600, 40, 1, 1, 'r', '^', 'N=1600,L=40', 'syncRate')
    plt.show()


if __name__=='__main__':
    figure_syncRate()



