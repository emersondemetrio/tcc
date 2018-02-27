# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt


# The slices will be ordered and plotted counter-clockwise.
labels = [
	r'Rayos X (88.4 %)',
	r'RMN en solucion (10.6 %)',
	r'Microscopia electronica (0.7 %)',
	r'Otros (0.3 %)'
]

sizes = [88.4, 10.6, 0.7, 0.3]

colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']

patches, texts = plt.pie(sizes, colors=None, startangle=90)

plt.legend(patches, labels, loc="best")
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.tight_layout()
plt.show()
