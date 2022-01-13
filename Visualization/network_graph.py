import numpy as np
import pandas as pd
import networkx as nx

import plotly.express as px
import plotly.graph_objects as go

def create_graph(corr_matrix):
    corr_matrix.columns = ["asset_1", "asset_2", "correlation"]
    
    # create a new graph from edge list
    Gx = nx.from_pandas_edgelist(corr_matrix, "asset_1", "asset_2", edge_attr=["correlation"])

    # Remove Nodes that are isolated
    Gx.remove_nodes_from(list(nx.isolates(Gx)))

    # Remove Smaller Tree Graph
    cmp_len_arr = list(map(lambda x : len(x), nx.connected_components(Gx)))

    for component in list(nx.connected_components(Gx)):
        if len(component) < max(cmp_len_arr):
            for node in component:
                Gx.remove_node(node)
                
    return Gx

def assign_colour(correlation):
    return "#ffa09b" if correlation <= 0 else "#9eccb7"

def assign_thickness(correlation, benchmark_thickness = 2, scaling_factor = 3):
    return benchmark_thickness * abs(correlation) ** scaling_factor

def assign_node_size(degree, scaling_factor=50):
    return degree * scaling_factor

def get_edge_width(Gx):
    edge_witdth = []
    
    for key, value in nx.get_edge_attributes(Gx, "correlation").items():
        edge_width.append(assign_thickness(value))
    
    return edge_width

def get_edge_color(Gx):
    # assign edge colours
    edge_colours = []
    
    for key, value in nx.get_edge_attributes(Gx, "correlation").items():
        edge_colours.append(assign_colour(value))
        
    return edge_colours
        
def get_node_size(Gx):
    # assign node size depending on number of connections (degree)
    node_size = []
    
    for key, value in dict(Gx.degree).items():
        node_size.append(assign_node_size(value))
        
    return node_size

def get_coordinates(Gx):
    """Returns the positions of nodes and edges in a format
    for Plotly to draw the network
    """
    # get list of node positions
    pos = nx.fruchterman_reingold_layout(Gx)

    Xnodes = [pos[n][0] for n in Gx.nodes()]
    Ynodes = [pos[n][1] for n in Gx.nodes()]

    Xedges = []
    Yedges = []
    for e in Gx.edges():
        # x coordinates of the nodes defining the edge e
        Xedges.extend([pos[e[0]][0], pos[e[1]][0], None])
        Yedges.extend([pos[e[0]][1], pos[e[1]][1], None])

    return Xnodes, Ynodes, Xedges, Yedges

def network_graph(corr_matrix, title):
    # Create Basic Graph from Correlation Matrix
    Gx = create_graph(corr_matrix)
    
    # Make Graph into Minimum Spanning Tree
    mst = nx.minimum_spanning_tree(Gx)
    
    # Get Edge Colours
    edge_colours = get_edge_color(mst)
    
    # Get Edge Width
    edge_widths = get_edge_width(mst)
    
    # Get Node Size
    node_sizes = get_node_size(mst)
    
    # Get Node Labels
    node_label = list(mst.nodes())
    
    # edges
    tracer = go.Scatter(
        x = Xedges,
        y = Yedges,
        mode="lines",
        line=dict(color="#DCDCDC", width=1),
        hoverinfo="none",
        showlegend=False,
    )

    # nodes
    tracer_marker = go.Scatter(
        x=Xnodes,
        y=Ynodes,
        mode="markers+text",
        textposition="top center",
        marker=dict(size=node_size, line=dict(width=1), color=edge_colours),
        text=node_label,
        textfont=dict(size=7),
        showlegend=False,
    )

    axis_style = dict(
        title="",
        titlefont=dict(size=20),
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks="",
        showticklabels=False,
    )

    layout = dict(
        title=title,
        width=800,
        height=800,
        autosize=False,
        showlegend=False,
        xaxis=axis_style,
        yaxis=axis_style,
        hovermode="closest",
        plot_bgcolor="#fff",
    )

    fig = go.Figure()
    fig.add_trace(tracer)
    fig.add_trace(tracer_marker)
    fig.update_layout(layout)

    fig.show()
    