from __future__ import print_function
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

data_set = SupervisedDataSet(2, 1)

data_set.addSample((0.8, 0.4), (0.7))
data_set.addSample((0.5, 0.7), (0.5))
data_set.addSample((1.0, 0.8), (0.95))

neural_network = buildNetwork(2, 4, 1, bias=True)

trainer = BackpropTrainer(neural_network, data_set)

for i in range(2000):
    print(trainer.train())

while True:
    param_1 = float(raw_input("Param 1: \n"))
    param_2 = float(raw_input("Param 2: \n"))

    resp = neural_network.activate(
        (param_1, param_2)
    )

    print("FOI: ", resp * 10)
