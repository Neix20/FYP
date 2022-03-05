# importing the sys module
import sys
import time
import numpy as np
import pandas as pd
import plotly.express as px
import scipy.stats as stats
import plotly.graph_objects as go

from plotly.subplots import make_subplots

from scipy.stats import pearsonr, spearmanr, kendalltau, pointbiserialr, chi2, chi2_contingency

sys.path.append('D:\\Github\\FYP')

from Utilities.corr_matrix import *
from Visualization.network_graph import *

filename = sys.argv[1]

# Read File
df = pd.read_csv(f"..\\Dataset\\{filename}")

# Generate UTAUT Factor Dataframe
utaut_fac_df = pd.DataFrame()

column_arr = df.iloc[:, 28:].columns
column_arr = [col.split(": ")[0] for col in column_arr]

for (ind, col_name) in enumerate(column_arr):
    utaut_fac_df[col_name] = df.iloc[:, 28 + ind]
    utaut_fac_df[col_name] = utaut_fac_df[col_name].map(lambda x : x - 1)
    
# Change Data Type to int
utaut_fac_df = utaut_fac_df.astype(int)

# Output Pearson

# Create Correlation Matrix
corr_df = create_corr_matrix(utaut_fac_df, pearsonr)

# Circular Layout
cirFig = network_graph(corr_df, "Important Features - Circular Layout", nx.circular_layout, 0.75)
layout = dict(
    width = 800,
    height = 800,
    hovermode = "closest",
    plot_bgcolor = "#fff",
)
cirFig.update_layout(layout)
cirFig.write_image("..\\public\\img\\Pearson-CirFig.jpeg")

# Fruchterman Reingold Layout
fruFig = network_graph(corr_df, "Important Features - Fruchterman Reingold Layout", nx.fruchterman_reingold_layout, 0.75)
layout = dict(
    width = 800,
    height = 800,
    hovermode = "closest",
    plot_bgcolor = "#fff",
)
fruFig.update_layout(layout)
fruFig.write_image("..\\public\\img\\Pearson-FruFig.jpeg")

# Output Spearman

# Create Correlation Matrix
corr_df = create_corr_matrix(utaut_fac_df, spearmanr)

# Circular Layout
cirFig = network_graph(corr_df, "Important Features - Circular Layout", nx.circular_layout, 0.75)
layout = dict(
    width = 800,
    height = 800,
    hovermode = "closest",
    plot_bgcolor = "#fff",
)
cirFig.update_layout(layout)
cirFig.write_image("..\\public\\img\\Spearman-CirFig.jpeg")

# Fruchterman Reingold Layout
fruFig = network_graph(corr_df, "Important Features - Fruchterman Reingold Layout", nx.fruchterman_reingold_layout, 0.75)
layout = dict(
    width = 800,
    height = 800,
    hovermode = "closest",
    plot_bgcolor = "#fff",
)
fruFig.update_layout(layout)
fruFig.write_image("..\\public\\img\\Spearman-FruFig.jpeg")


