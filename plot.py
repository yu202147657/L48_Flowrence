import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_metric_results(results_file):
    df = pd.read_csv(results_file)
    metric_name = df.columns[-1]
    results = df[metric_name]

    plt.style.use('ggplot')
    plt.rc('font', family='serif')
    plt.plot(np.arange(len(results)), results)
    plt.title(metric_name.capitalize())
    plt.savefig(f"plots/{'_'.join(metric_name.split(' '))}_n={len(results)}.png")
    plt.show()
