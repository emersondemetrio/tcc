from __future__ import print_function
from pybrain.datasets import SequentialDataSet
from itertools import cycle



asb = [-690.553405762, 155.242446899, -14.5201539993, 41.0483360291, 7.07259941101, 11.0448350906, 5.05975961685, -0.987285614014, -1.29114532471, 2.80567622185, 0.498306363821, 0.0166814476252, -6.32610750198]

data_set = []

for i in range(3):
    data_set.append(asb)


ds = SequentialDataSet(1, 1)

#for data in data_set:
    #print(data)


for sample, next_sample in zip(asb, cycle(asb[1:])):
    ds.addSample(sample, next_sample)

print(ds)

# https://www.google.com.br/search?biw=1366&bih=702&q=pybrain+example+SequentialDataSet&oq=pybrain+example+SequentialDataSet&gs_l=psy-ab.3...51257.53595.0.53804.12.10.2.0.0.0.545.1027.0j2j1j5-1.4.0....0...1.1.64.psy-ab..7.1.127...0i8i13i30k1.0.dQ3VO5jLSEk
# https://stackoverflow.com/questions/25967922/pybrain-time-series-prediction-using-lstm-recurrent-nets
# https://www.youtube.com/watch?v=0ZsXYytmiVs
# http://pybrain.org/docs/tutorial/datasets.html
# https://stackoverflow.com/questions/8139822/how-to-load-training-data-in-pybrain
