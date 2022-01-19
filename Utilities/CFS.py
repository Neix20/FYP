import math
import numpy as np
import pandas as pd

from Utilities.HeapQueue import *

# Calculate Merit
def merit_calculation(X, Y, func):
    k = X.shape[1]
    
    # average feature-class correlation
    rcf_all = [func(X.iloc[:, i], Y) for i in range(k)]
    rcf_all = list(map(lambda x : abs(x[0]), rcf_all))
    rcf = np.mean(rcf_all)

    # average feature-feature correlation
    corr = X.corr()
    if corr.shape != (1, 1):
        corr.values[np.tril_indices_from(corr.values)] = np.nan
    corr = abs(corr)
    rff = corr.unstack().mean()

    return (k * rcf) / math.sqrt(k + k * (k-1) * rff)

# Get Feature With Best Merit Value
def get_best_feature_val(X, Y, func):
    # Initialize default value
    best_value, best_feature = -1, ''
    
    # 1. Get (Corr, P_Val) for Every Feature
    rcf_all = [func(X.iloc[:, i], Y) for i in range(X.shape[1])]
    
    # 2. Get only Correlation Coefficient
    rcf_all = map(lambda x: abs(x[0]),rcf_all)
    
    # 3. Convert Python List to Series
    rcf_all = pd.Series(rcf_all)
    
    # 4. Complete
    best_feature, best_value = rcf_all.idxmax(), rcf_all[rcf_all.idxmax()]
    
    return (best_feature, best_value)

# Correlation Feature Selection
def CFS(X, Y, func, n_selected_features = 10):
    # initialize Heap
    queue = HeapQueue()
    
    # Calculate Best Feature and Best Value
    best_feature, best_value = get_best_feature_val(X, Y, func)
    
    # push first best_subset, merit
    queue.push([best_feature], best_value)

    # list for visited nodes
    visited = []
    
    # counter for backtracks, limit of backtracks
    max_backtrack, n_backtrack = 25, 0
    
    # repeat until queue is empty
    # or the maximum number of backtracks is reached
    while not queue.isEmpty():
        # get element of queue with highest merit
        subset, merit = queue.pop()
    
        # check whether the merit of this subset
        # is higher than the current best subset
        if merit >= best_value:
            best_value = merit
            best_subset = subset
        else:
            n_backtrack += 1

        # goal condition
        if len(best_subset) == n_selected_features + 1 or n_backtrack == max_backtrack:
            break
    
        # iterate through all features and look of one can
        # increase the merit
        for idx in range(X.shape[1]):
            temp_subset = subset + [idx]
        
            temp_subset = sorted(list(set(temp_subset)))
        
            if not temp_subset in visited:
                visited.append(temp_subset)
                merit = merit_calculation(X.iloc[:, temp_subset], Y, func)
                queue.push(temp_subset, merit)
                
    # Sort Feature Set
    best_subset = sorted(best_subset)
    
    # Get Feature from X.Columns
    best_subset = list(map(lambda x: X.columns[x], best_subset))
    
    return best_subset