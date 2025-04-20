import streamlit as st
import json
import networkx as nx
import matplotlib.pyplot as plt

# Load concept map
with open("KnowledgeGraph_ColdChain.json") as f:
    data = json.load(f)

concepts = data["concepts"]
id_to_name = {c["id"]: c["name"] for c in concepts}

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

# Draw concept map with labels
st.subheader("Knowledge Graph")
fig, ax = plt.subplots()
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, labels=id_to_name, arrows=True,
        node_color='skyblue', node_size=3000, font_size=10, font_weight='bold', ax=ax)

# Add hover-like annotations manually (as real hover isn't supported in matplotlib directly)
for node_id, (x, y) in pos.items():
    ax.text(x, y + 0.05, id_to_name[node_id], fontsize=9, ha='center', bbox=dict(facecolor='white', alpha=0.6, edgecolor='gray'))

st.pyplot(fig)
