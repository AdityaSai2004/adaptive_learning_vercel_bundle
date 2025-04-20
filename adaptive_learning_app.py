
import streamlit as st
import json
import networkx as nx
import matplotlib.pyplot as plt

# Load concept map
with open("KnowledgeGraph_ColdChain.json") as f:
    data = json.load(f)

concepts = data["concepts"]

# Create a directed graph
G = nx.DiGraph()
for concept in concepts:
    G.add_node(concept["id"], label=concept["name"])
    for prereq in concept["prerequisites"]:
        G.add_edge(prereq, concept["id"])

# Streamlit UI
st.title("Adaptive Learning Platform: Cold Chain Monitoring")

selected_concept = st.selectbox("Select a Concept", [c["name"] for c in concepts])
concept_data = next(c for c in concepts if c["name"] == selected_concept)

st.subheader("Learning Objectives")
for obj in concept_data["learning_objectives"]:
    st.markdown(f"- {obj}")

st.subheader("Expected Outcomes")
for out in concept_data["outcomes"]:
    st.markdown(f"- {out}")

# Draw concept map
st.subheader("Knowledge Graph")
fig, ax = plt.subplots()
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, arrows=True, node_color='skyblue', node_size=3000, font_size=10, font_weight='bold', ax=ax)
st.pyplot(fig)
