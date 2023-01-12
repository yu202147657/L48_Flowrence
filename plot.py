import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_metric_results(df, file_name):
    metric_name = df.columns[-1]
    results = df[metric_name]
    cummin = results.cummin()

    plt.style.use('ggplot')
    plt.rc('font', family='serif')
    plt.plot(np.arange(len(results)), results)
    plt.plot(np.arange(len(results)), cummin)
    plt.legend(['actual', 'cumulative'])
    plt.title(metric_name.capitalize())
    plt.savefig(file_name)

    return plt
