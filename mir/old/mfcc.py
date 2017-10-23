import sys

import essentia
from pylab import plot, show, figure, imshow
from essentia.standard import *
import essentia.streaming

# let's have a look at what is in there


# Essentia has a selection of audio loaders:
#
#  - AudioLoader: the basic one, returns the audio samples, sampling rate and number of channels
#  - MonoLoader: which returns audio, down-mixed and resampled to a given sampling rate
#  - EasyLoader: a MonoLoader which can optionally trim start/end slices and rescale according
#                to a ReplayGain value
#  - EqloudLoader: an EasyLoader that applies an equal-loudness filtering on the audio
#

audiofile = sys.argv[1]

# we start by instantiating the audio loader:

loader = essentia.standard.MonoLoader(filename = audiofile)

# and then we actually perform the loading:
audio = loader()


w = Windowing(type = 'hann')
spectrum = Spectrum()
mfcc = MFCC()

"""
mfccs = []

for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
    mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
    mfccs.append(mfcc_coeffs)

mfccs = essentia.array(mfccs).T

imshow(mfccs[1:,:], aspect = 'auto')
show()

"""

pool = essentia.Pool()

for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
    mfcc_bands, mfcc_coeffs = mfcc(spectrum(w(frame)))
    pool.add('lowlevel.mfcc', mfcc_coeffs)
    pool.add('lowlevel.mfcc_bands', mfcc_bands)

imshow(pool['lowlevel.mfcc'].T[1:,:], aspect = 'auto')
#show() # unnecessary if you started "ipython --pylab"
#figure()
#imshow(pool['lowlevel.mfcc_bands'].T, aspect = 'auto', interpolation = 'nearest')

YamlOutput(filename = 'mfcc.json', format='json')(pool)

#http://essentia.upf.edu/documentation/essentia_python_tutorial.html