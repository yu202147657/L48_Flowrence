import pandas
import os
import re

def mean_best(files, metric):

    data = {'RBF': [], 'RQ': [], 'M52': []}
    
    assert not len(files) % len(data)
    
    files_per_kernel = (len(files) / len(data))
    
    for f in files:
        df = pandas.read_csv('csv_files/'+f, index_col=0)

        if metric == 'WT':
            best = df['average steps waiting'].min()
        else:
            best = df['completed journeys'].max()

        if 'RBF' in f:
            data['RBF'] += [best]
        elif 'RQ' in f:
            data['RQ'] += [best]
        elif 'M52' in f:
            data['M52'] += [best]
    
    return(data)


def convergence(files, metric, eps, N):

    data = {'RBF': [], 'RQ': [], 'M52': []}
    
    assert not len(files) % len(data)
    
    files_per_kernel = (len(files) / len(data))
    
    for f in files:
        df = pandas.read_csv('csv_files/'+f, index_col=0)

        converged = False
        prev = None
        count = 0

        for i, row in df.iterrows():

            if metric == 'WT':
                current = row['average steps waiting']
            else:
                current = row['completed journeys']
            #print('curr', current)
            #print('prev', prev)

            if prev is not None:

                diff = abs(current - prev)

                if diff < eps:
                    count += 1
                    #print('diff', diff)
                    #print('count', count)
                    #breakpoint()
                else:
                    count = 0

            if count >= N:
                if 'RBF' in f:
                    data['RBF'] += [i]
                elif 'RQ' in f:
                    data['RQ'] += [i]
                elif 'M52' in f:
                    data['M52'] += [i]

                converged = True
                break

            prev = current

        if not converged: 
            if 'RBF' in f:
                data['RBF'] += ['DNC']
            elif 'RQ' in f:
                data['RQ'] += ['DNC']
            elif 'M52' in f:
                data['M52'] += ['DNC']

    return(data)


csv_files = sorted(os.listdir('csv_files/'))

DL2_files = [f for f in csv_files if 'DL2' in f]
DB2_files = [f for f in csv_files if 'DB2' in f]

DL2_CJ_files = [f for f in DL2_files if 'CJ' in f]
DB2_CJ_files = [f for f in DB2_files if 'CJ' in f]

DL2_WT_files = [f for f in DL2_files if 'WT' in f]
DB2_WT_files = [f for f in DB2_files if 'WT' in f]

print('DL2 CJ', convergence(DL2_CJ_files, 'CJ', 3, 3))
print('DB2 CJ', convergence(DB2_CJ_files, 'CJ', 3, 3))
print('DL2 WT', convergence(DL2_WT_files, 'WT', 0.2, 3))
print('DB2 WT', convergence(DB2_WT_files, 'WT', 1, 3))

print()

print('DL2 CJ', mean_best(DL2_CJ_files, 'CJ'))
print('DB2 CJ', mean_best(DB2_CJ_files, 'CJ'))
print('DL2 WT', mean_best(DL2_WT_files, 'WT'))
print('DB2 WT', mean_best(DB2_WT_files, 'WT'))
breakpoint()

