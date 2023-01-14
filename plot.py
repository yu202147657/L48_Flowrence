import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_metric_results(df, file_name, minimisation=True):
    metric_name = df.columns[-1]
    results = df[metric_name]
    
    if minimisation:
        cuma = results.cummin()
    else:
        cuma = results.cummax()

    plt.figure()
    plt.style.use('ggplot')
    plt.rc('font', family='serif')
    plt.plot(np.arange(len(results)), results)
    plt.plot(np.arange(len(results)), cuma)
    plt.legend(['actual', 'cumulative'])
    plt.title(metric_name.capitalize())
    plt.savefig(file_name)

    return plt

def plot_sensitivity(main_effects, total_effects, file_name):

    params = main_effects.columns
    main_effects = main_effects.values.tolist()[0]
    total_effects = total_effects.values.tolist()[0]

    plt.figure()
    plt.style.use('ggplot')
    plt.rc('font', family='serif')

    X_axis = np.arange(len(params))

    plt.bar(X_axis - 0.2, main_effects, 0.4, label='Main Effects')
    plt.bar(X_axis + 0.2, total_effects, 0.4, label='Total Effects')

    plt.xticks(X_axis, params)
    plt.ylabel('Sensitivity')

    title = file_name[6:-4]
    plt.title(title)

    plt.savefig(file_name)

    return plt
