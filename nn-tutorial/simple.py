from __future__ import print_function
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

ds = SupervisedDataSet(13, 1)

ds.addSample((
    -885.995056152,
    216.85345459,
    52.4779205322,
    -10.1295471191,
    -26.842590332,
    -23.118478775,
    -17.0884284973,
    -9.46554756165,
    -7.79739236832,
    -6.47718429565,
    -4.50396442413,
    -2.63221335411,
    0.0336214564741),
    (0.7)
)

nn = buildNetwork(2, 4, 1, bias=True)

trainer = BackpropTrainer(nn, ds)

for i in range(2000):
    print(trainer.train())

while True:
    a = float(raw_input("VAI: \n"))
    b = float(raw_input("VAI: \n"))

    z = nn.activate((a, b))

    print("FOI: ", z * 10)