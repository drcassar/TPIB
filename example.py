import sys
import os
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from TPIB import transformationPeakIterativeBaseline


# Loading example data
examplepath = os.path.join(sys.path[0], 'example.csv')
data = pd.read_csv(examplepath)
x_raw, y_raw = data['x'].values, data['y'].values

# Original data plot
fig, axe = plt.subplots(1, 1, figsize=(5, 5))
axe.set_xlabel('X')
axe.set_ylabel('Y')
axe.set_title('Raw data')
axe.plot(x_raw, y_raw)
plt.show(fig)

# Using the TPIB algorithm
x_left = [765, 820]
x_right = [1000, 1150]
x, y, fun = transformationPeakIterativeBaseline(x_raw, y_raw, x_left, x_right,
                                                numOfIteractions=10,
                                                peakIsPointingDown=True,
                                                normalizePeakArea=True)
xrange = np.linspace(min(x), max(x))
fig2, axe2 = plt.subplots(1, 1, figsize=(5, 5))
axe2.axhline(0, ls='--', c='red')
axe2.plot(xrange, fun(xrange), ls='', marker='o', markersize=3,
          label='Interpolated peak function')
axe2.plot(x, y, label='Discrete peak data')
axe2.set_xlabel('X')
axe2.set_ylabel('Y')
axe2.set_title('Peak')
axe2.legend(loc=0)
plt.show(fig2)
