import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

st.title("Friendship Network Visualization")

# Data
nodes = [
    "Alice", "Bob", "Charlie", "Diana", "Eve",
    "Frank", "Grace", "Hannah", "Ian", "Jack"
]

edges = [
    ("Alice", "Bob"),
    ("Alice", "Charlie"),
    ("Bob", "Charlie"),
    ("Charlie", "Diana"),
    ("Diana", "Eve"),
    ("Bob", "Diana"),
    ("Frank", "Eve"),
    ("Eve", "Ian"),
    ("Diana", "Ian"),
    ("Ian", "Grace"),
    ("Grace", "Hannah"),
    ("Hannah", "Jack"),
    ("Grace", "Jack"),
    ("Charlie", "Frank"),
    ("Alice", "Eve"),
    ("Bob", "Jack")
]

# Build Graph
G = nx.Graph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# Centrality calculations
betweenness = nx.betweenness_centrality(G)
most_influential = max(betweenness, key=betweenness.get)

# Community detection
from networkx.algorithms.community import greedy_modularity_communities
communities = list(greedy_modularity_communities(G))

# Assign a color to each community
palette = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
node_to_comm = {}

for c_index, comm in enumerate(communities):
    for node in comm:
        node_to_comm[node] = c_index

# Community colors for each node
community_colors = [palette[node_to_comm[n]] for n in G.nodes()]

# Highlight most influential
highlight_colors = []
for n in G.nodes():
    if n == most_influential:
        highlight_colors.append("red")
    else:
        highlight_colors.append(palette[node_to_comm[n]])

# Layout
pos = nx.spring_layout(G, seed=42)

# Draw Graph
fig, ax = plt.subplots(figsize=(8, 6))

nx.draw(
    G, pos,
    with_labels=True,
    node_color=highlight_colors,
    node_size=1800,
    edge_color="gray",
    font_size=10,
    font_weight="bold"
)

plt.title("Friendship Network (Communities + Most Influential Highlighted)")
st.pyplot(fig)

import pandas as pd

st.subheader("Centrality Metrics")

# Degree and centralities
degree = dict(G.degree())
degree_centrality = nx.degree_centrality(G)
closeness = nx.closeness_centrality(G)

# Build DataFrame
df_metrics = pd.DataFrame({
    "Node": list(G.nodes()),
    "Degree": [degree[n] for n in G.nodes()],
    "Degree Centrality": [degree_centrality[n] for n in G.nodes()],
    "Betweenness": [betweenness[n] for n in G.nodes()],
    "Closeness": [closeness[n] for n in G.nodes()],
    "Community": [node_to_comm[n] for n in G.nodes()]
})

# Sort by Degree
df_metrics = df_metrics.sort_values(["Degree", "Betweenness"], ascending=False)

st.dataframe(df_metrics, use_container_width=True)

st.subheader("Findings and Analysis")

st.markdown("""
### **1. Network Structure**
The friendship network forms several tightly connected groups with a few key individuals linking those groups together. 

---

### **2. Most Connected Individuals (Degree Analysis)**
The individuals with the highest number of direct friendships (**degree = 4**) are:

- **Bob**
- **Charlie**
- **Diana**
- **Eve**

---

### **3. Centrality Measures**

#### **Betweenness Centrality**
**Bob** has the highest betweenness score.  
He lies on the most shortest paths between students, which means:

- He connects separate friend groups  
- He plays the largest role in spreading information  
- He is the most structurally influential person in the class  

#### **Closeness Centrality**
Diana, Charlie, Bob, and Ian have relatively high closeness scores, meaning they can reach others efficiently.

#### **Degree Centrality**
Matches degree: Bob, Charlie, Diana, and Eve are the most directly connected.

---

### **4. Community Detection**
The algorithm found **three distinct friendship communities**, shown in different colors in the graph.

Each community represents a sub-group of students who interact more closely with each other.

---

### **5. Key Insight**
The most important pattern is the combination of:

- **Multiple hubs (Bob, Charlie, Diana, Eve)**  
- **One major bridge: Bob**  

Bob is uniquely positioned between communities, making him the central connector.

""")
