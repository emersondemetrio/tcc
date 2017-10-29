from __future__ import print_function
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

data_set = SupervisedDataSet(1, 3)

data_set.addSample((0.120,), [0, 0, 1])
data_set.addSample((0.80,), [0, 1, 0])
data_set.addSample((0.70,), [1, 0, 0])

neural_network = buildNetwork(1, 4, 3, bias=True)

trainer = BackpropTrainer(neural_network, data_set)

for i in range(2000):
    print(trainer.train())

while True:
    param_1 = float(raw_input("Param 1: \n"))

    resp = neural_network.activate(
        (param_1, )
    )

    print("FOI: ", resp)
