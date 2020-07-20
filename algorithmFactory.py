from algorithms import *

class AlgorithmFactory:

    def __init__(self):
        self.algorithmContext = {'Vicsek': Vicseck,
                                 'syncControlDistance':syncControlDistance}

    def createAlgorithm(self,
                        name):
        return self.algorithmContext[name]

if __name__ == '__main__':
    af = AlgorithmFactory()
    algorithm = af.createAlgorithm("Vicseck")
    res = algorithm([np.array([1.0,2.0]), np.array([2.0,3.0])], np.array([1.0,1.0]))
    print(res)