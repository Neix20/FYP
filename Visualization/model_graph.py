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
            'xanchor': 'center'
        },
        xaxis_title=x_label,
        yaxis_title=y_label,
        legend_title="Legend",
    )
    fig.update_yaxes(range=[0, 1])
    fig.show("notebook")
    
def prc_roc_graph(model_arr, X, Y, x_cor, title, x_title, y_title, func):
    # Empty Plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_cor, line=dict(dash='dash'), name="", showlegend=False))
    
    for name, model in model_arr:
        yhat = model.predict_proba(X)
        yhat = yhat[:, 1]
        a, b, c = func(Y, yhat)
        if x_cor == [1, 0]:
            x_val, y_val = b, a
        else:
            x_val, y_val = a, b
        fig.add_trace(
            go.Scatter(
                x = x_val, 
                y = y_val, 
                name = name,
                mode='lines'
            )
        )
        
    fig.update_layout(
        title = {
            'text': title,
            'x': 0.5,
            "y": 0.85,
            'xanchor': 'center'
        },
        xaxis_title = x_title,
        yaxis_title = y_title,
        legend_title = "Legend",
    )
    
    fig.update_xaxes(range=[0,1])
    fig.update_yaxes(range=[0,1])
    fig.show("notebook")
    
def acc_graph(acc_arr, title, x_title, y_title):
    # Empty Plots
    fig = go.Figure()
    
    for name, acc in acc_arr:
        fig.add_trace(
            go.Bar(
                x = [acc], 
                y = [name],
                name = name,
                orientation = 'h'
            )
        )
        
    fig.update_traces(
        texttemplate='%{value:.2f}%', 
        textposition='outside'
    )
    
    fig.update_layout(
        title = {
            'text': title,
            'x': 0.5,
            'y': 0.85,
            'xanchor': 'center'
        },
        xaxis_title = x_title,
        yaxis_title = y_title,
        legend_title = "Legend",
    )
    fig.update_xaxes(range=[0,100])
    fig.show("notebook")