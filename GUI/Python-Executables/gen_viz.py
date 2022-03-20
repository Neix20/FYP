import sys
import numpy as np
import pandas as pd

import plotly.express as px
from Visualization.model_graph import *

selected_feature = sys.argv[1]
targeted_feature = sys.argv[2]

# Read Dataset
df = pd.read_csv("Dataset/res_processed.csv")

# Construct Bar Graph that shows relationship between the two features
tmp_df = df.loc[:, [targeted_feature, selected_feature]]
unique_arr = tmp_df[targeted_feature].unique().tolist()

tmp_df = pd.crosstab(tmp_df.iloc[:, 1], tmp_df.iloc[:, 0])

tmp_df = tmp_df[unique_arr]

fig = show_bar_graph(tmp_df, selected_feature, targeted_feature, "Legend", "Count")
fig.write_image("public\\img\\filter-target-graph.jpeg")

print("Successfully output filter-target-graph.jpeg!")

sys.stdout.flush()