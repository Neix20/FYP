import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

def get_df_type(clf_report_arr, col_name):
    df = pd.DataFrame()

    for name, clf_report in clf_report_arr:
        df[name] = clf_report[col_name.lower()][:-3]
    
    # Replace NA value with 0
    df.fillna(0, inplace=True)
    return df

def pfr_graph(df, x_label, y_label, title):
    fig = px.bar(df.T, x=df.columns, y=df.index, barmode="group")
    fig.update_traces(texttemplate='%{value:.4f}', textposition='outside')
    fig.update_layout(
        title = {
            'text': title,
            'x':0.5,
            "y": 0.85,
            'xanchor': 'center'
        },
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend_title="Legend",
    )
    fig.update_yaxes(range=[0, 1])
    fig.show("notebook")