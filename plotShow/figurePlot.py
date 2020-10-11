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

# plt.figure(figsize=[15,8])
# plt.scatter(X, Y, label = 'RealValue')
# plt.plot(X, func(X, a, b), 'red', label = 'CurveLine')
# plt.title(station, fontdict={'family' : 'Times New Roman', 'size'   : 16})
# plt.ylabel('Clocks($\mu S$)', fontdict={'family' : 'Times New Roman', 'size'   : 16})
# plt.xlabel('Time', fontdict={'family' : 'Times New Roman', 'size'   : 16})
# plt.yticks(fontproperties = 'Times New Roman', size = 14)
# plt.xticks(fontproperties = 'Times New Roman', size = 14)
# plt.legend(prop={'family' : 'Times New Roman', 'size'   : 16})
# plt.savefig('./stationClocks/' + station + '.ps', dpi = 200)
# plt.show()

font = {'family' : 'Times New Roman',
        # 'color'  : 'black',
        # 'weight' : 'normal',
        # 'size'   : 20,
        }
fig = plt.figure()          #制作图表fig
class FigurePlot(object):
    def __init__(self,
                 figureName='',
                 xlabel='k',
                 ylabel=r'$\phi$',
                 k=111):
        self.title = figureName           #图标标题
        self.fig = fig
        self.ax = {}
        self.ax = self.fig.add_subplot(k)  #当前画布切成1行1列，本图占1块ax1
        self.ax.set_xlabel(xlabel,font)           #坐标轴加标签
        self.ax.set_ylabel(ylabel,font)
        plt.yticks(fontproperties='Times New Roman')
        plt.xticks(fontproperties='Times New Roman')
        plt.title(self.title)                    #加上标题
        plt.rcParams["font.family"] = 'Times New Roman'
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
        elif  n == 1:
            return data


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

    def noise_plot_syncRate(self,
                            N, L, R, V, k1,
                            c, m,
                            label,
                            name=''
                            ):
        fileName = '../resData/' + self.simulation['algorithmName'] + \
                   '_' + str(N) + \
                   '_' + str(L) + \
                   '_' + str(R) + \
                   '_' + str(V) + \
                   '_' + str(k1) + \
                   '_noise' + \
                   '.xlsx'

        re = readExcel(fileName)
        y = []
        for i in range(30):
            r = re.readRows(i, name)
            y.append(sum(r[1501:])/500)
        x = [i*0.05 for i in range(30)]
        plt.scatter(x, y, c=c, marker=m, label=label)
        yy = self.NiHe(y, 1)
        xx = [i * 0.05 for i in range(len(yy))]
        plt.plot(xx, yy, c=c)
        self.ax.legend()

    def sync_speed_step(self,
                        N, L, R, V, k1,
                        c, m,
                        label,
                        name=''
                        ):
        fileName = '../resData/' + self.simulation['algorithmName'] + \
                   '_' + str(N) + \
                   '_' + str(L) + \
                   '_' + str(R) + \
                   '_' + str(V) + \
                   '_' + str(k1) + \
                   '_step' + \
                   '.xlsx'
        re = readExcel(fileName)
        y = np.array([])
        for i in range(50):
            r = re.readRows(i, name)
            if len(y) == 0:
                y = np.array(r)
            else:
                y += np.array(r)
        y /= 50
        x = [i+1  for i in range(2000)]
        plt.plot(x, y, c=c, label=label)
        plt.legend()

def test_figure_entropy():
    fp = FigurePlot('', 111)
    fp.k_entropy(400, 20, 1, 1, 'g', '>', 'N=400,L=20', 'entropy')
    # fp = FigurePlot('', 111)
    fp.k_entropy(900, 30, 1, 1, 'b', 'v', 'N=900,L=30', 'entropy')
    # fp = FigurePlot('', 111)
    fp.k_entropy(1600, 40, 1, 1, 'r', '^', 'N=1600,L=40', 'entropy')
    plt.show()

def test_figure_syncRate():
    fp = FigurePlot('', 111)
    fp.k_entropy(400, 20, 1, 1, 'g', '>', 'N=400,L=20', 'syncRate')
    # fp = FigurePlot('', 111)
    fp.k_entropy(900, 30, 1, 1, 'b', 'v', 'N=900,L=30', 'syncRate')
    # fp = FigurePlot('', 111)
    fp.k_entropy(1600, 40, 1, 1, 'r', '^', 'N=1600,L=40', 'syncRate')
    plt.show()

def figure_noise_plot_syncRate():
    fp = FigurePlot('', xlabel=r'$\eta$', ylabel=r'$\phi$', k=111)
    fp.noise_plot_syncRate(400, 20, 1, 1, -75, 'r', '>','k=-75',name='syncRate_list')
    fp.noise_plot_syncRate(400, 20, 1, 1, -50, 'g', 'D', 'k=-50', name='syncRate_list')
    fp.noise_plot_syncRate(400, 20, 1, 1, -25, 'b', '.', 'k=-25', name='syncRate_list')
    fp.noise_plot_syncRate(400, 20, 1, 1, -15, 'y', 'v', 'k=-15', name='syncRate_list')
    fp.noise_plot_syncRate(400, 20, 1, 1, 0, 'c', 's', 'k=0', name='syncRate_list')
    fp.noise_plot_syncRate(400, 20, 1, 1, 25, 'm', 'd', 'k=20', name='syncRate_list')
    fp.noise_plot_syncRate(400, 20, 1, 1, 50, 'k', '^', 'k=50', name='syncRate_list')
    plt.show()

def figure_noise_plot_entropy():
    fp = FigurePlot('', xlabel=r'$\eta$', ylabel=r'$S$',k=111)
    fp.noise_plot_syncRate(400, 20, 1, 1, -75, 'r', '>', 'k=-75', name='entropy_list')
    fp.noise_plot_syncRate(400, 20, 1, 1, -50, 'g', 'D', 'k=-50', name='entropy_list')
    fp.noise_plot_syncRate(400, 20, 1, 1, -25, 'b', '.', 'k=-25', name='entropy_list')
    fp.noise_plot_syncRate(400, 20, 1, 1, -15, 'y', 'v', 'k=-15', name='entropy_list')
    fp.noise_plot_syncRate(400, 20, 1, 1, 0, 'c', 's', 'k=0', name='entropy_list')
    fp.noise_plot_syncRate(400, 20, 1, 1, 25, 'm', 'd', 'k=25', name='entropy_list')
    fp.noise_plot_syncRate(400, 20, 1, 1, 50, 'k', '^', 'k=50', name='entropy_list')
    plt.show()

def figure_sync_speed_step():
    fp = FigurePlot('', xlabel='t', ylabel=r'$\phi$', k=111)
    fp.sync_speed_step(900, 30, 1, 1, 0, 'r', '>', 'k=0', name='syncRate_list')
    fp.sync_speed_step(900, 30, 1, 1, 15, 'g', '>', 'k=15', name='syncRate_list')
    fp.sync_speed_step(900, 30, 1, 1, 25, 'b', '>', 'k=25', name='syncRate_list')
    fp.sync_speed_step(900, 30, 1, 1, 30, 'm', '>', 'k=30', name='syncRate_list')
    plt.show()
def figure_entropy_step():
    fp = FigurePlot('', xlabel='t', ylabel=r'$S$', k=111)
    fp.sync_speed_step(900, 30, 1, 1, 0, 'r', '>', 'k=0', name='entropy_list')
    fp.sync_speed_step(900, 30, 1, 1, 15, 'g', '>', 'k=15', name='entropy_list')
    fp.sync_speed_step(900, 30, 1, 1, 25, 'b', '>', 'k=25', name='entropy_list')
    fp.sync_speed_step(900, 30, 1, 1, 30, 'm', '>', 'k=30', name='entropy_list')
    plt.show()



