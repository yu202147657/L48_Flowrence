import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_metric_results(df, file_id, minimisation=True):
    metric_name = df.columns[-1]
    results = df[metric_name]

    file_name = f'plots/{file_id}.png'
    
    if minimisation:
        cuma = results.cummin()
    else:
        cuma = results.cummax()

    plt.figure()
    plt.style.use('ggplot')
    plt.rc('font', family='serif')
    plt.plot(np.arange(len(results)), results,)
    # plt.plot(np.arange(len(results)), cuma)
    plt.legend(['actual', 'cumulative'])
    # plt.title(file_id)
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
    plt.bar(X_axis + 0.2, [-x/2 if x < 0 else x for x in total_effects], 0.4, label='Total Effects')

    # plt.xticks(X_axis, params)
    plt.ylabel('Sensitivity')

    plt.savefig(file_name, bbox_inches='tight', pad_inches=0.2)

    return plt
