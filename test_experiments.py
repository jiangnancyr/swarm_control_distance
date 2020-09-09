from test_main import *



class experiment1(test_base):
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

def test_experiment1():
    experiment = experiment1()
    experiment.test_k1()




class experiment2(test_base):

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

def test_experiment2():
    experiment = experiment2()
    experiment.test_noise()

class experiment3(test_base):
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

def test_experiment3():
    experiment = experiment3()
    experiment.test_noises()

class experiment4(test_base):
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

def test_experiment4():
    experiment = experiment4()
    experiment.test_time_entropy()

class experiment5(test_base):
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

def test_experiment5():
    experiment = experiment5()
    experiment.test_step()


