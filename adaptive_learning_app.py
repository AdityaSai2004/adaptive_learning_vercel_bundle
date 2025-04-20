
import streamlit as st
import json
import networkx as nx
import plotly.graph_objects as go

# Load concept map
with open("KnowledgeGraph_ColdChain.json") as f:
    data = json.load(f)

concepts = data["concepts"]
id_to_name = {c["id"]: c["name"] for c in concepts}

# Create a directed graph
G = nx.DiGraph()
for concept in concepts:
    G.add_node(concept["id"], name=concept["name"])
    for prereq in concept["prerequisites"]:
        G.add_edge(prereq, concept["id"])

# Streamlit UI
st.set_page_config(layout="wide")
st.title("Adaptive Learning Platform: Cold Chain Monitoring")

selected_concept = st.selectbox("Select a Concept", [c["name"] for c in concepts])
concept_data = next(c for c in concepts if c["name"] == selected_concept)

st.subheader("Learning Objectives")
for obj in concept_data["learning_objectives"]:
    st.markdown(f"- {obj}")

st.subheader("Expected Outcomes")
for out in concept_data["outcomes"]:
    st.markdown(f"- {out}")

# Generate node positions
pos = nx.spring_layout(G, seed=42, k=0.8)

# Create edge traces
edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=1, color='#888'),
    hoverinfo='none',
    mode='lines')

# Create node traces with hover text
node_x = []
node_y = []
hover_text = []
labels = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)
    hover_text.append(id_to_name[node])
    labels.append(node)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    text=labels,
    textposition="bottom center",
    hovertext=hover_text,
    hoverinfo='text',
    marker=dict(
        showscale=False,
        color='skyblue',
        size=30,
        line_width=2))

# Create figure
fig = go.Figure(data=[edge_trace, node_trace],
         layout=go.Layout(
            title='Knowledge Graph',
            titlefont_size=20,
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
        )

st.plotly_chart(fig, use_container_width=True)
