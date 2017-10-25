from __future__ import print_function
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet, SequentialDataSet
from pybrain.supervised.trainers import BackpropTrainer

ds = SupervisedDataSet(2, 1)

ds.addSample((0.5, 0.4), (1.0))
ds.addSample((0.5, 0.7), (2.0))
ds.addSample((1.0, 0.8), (3.0))

data = [
    (1,2),
    (1,3),
    (10,2),
    (2,0),
    (2,9),
    (4,3),
    (1,2),
    (10,5)
]

ds = SequentialDataSet(2,2)
for sample, next_sample in zip(data, cycle(test_data[1:])):
   ds.addSample(sample, next_sample)

nn = buildNetwork(2, 4, 1, bias=True)

trainer = BackpropTrainer(nn, ds)

for i in range(2000):
    print(trainer.train())

print("Rock: 1 \nPunk: 2\nAxe: 3")

while True:
    a = float(raw_input("VAI: \n"))
    b = float(raw_input("VAI: \n"))

    z = nn.activate((a, b))

    print("FOI: ", z * 10)