"""
The package requirements do not enforce matplotlib as a requirement so this
package is optional. However, it's useful.
"""
import numpy as np
import matplotlib.pyplot as plt


def plot_pivots(X, pivots, ax=None):
    if ax is None:
        ax = plt.subplots(1, 1)[1]

    ax.set_xlim(0, len(X))
    ax.set_ylim(X.min()*0.99, X.max()*1.01)
    ax.plot(np.arange(len(X)), X, 'k:', alpha=0.5)
    ax.plot(np.arange(len(X))[pivots != 0], X[pivots != 0], 'k-')
    ax.scatter(np.arange(len(X))[pivots == 1], X[pivots == 1], color='g')
    ax.scatter(np.arange(len(X))[pivots == -1], X[pivots == -1], color='r')