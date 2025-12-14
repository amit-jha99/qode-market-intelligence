# Streaming plots

import matplotlib.pyplot as plt


def streaming_plot(data):
    plt.plot(data[-500:]) # sampling
    plt.show()