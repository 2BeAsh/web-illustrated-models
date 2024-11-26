import streamlit as st
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time


class ErdosRenyiNetworkModel():
    def __init__(self):
        """Illustration of a simple Erdos-Renyi network model where at each time step, one edge is deleted and another is added.
        """
        pass
    
    
    def _streamlit_setup(self):
        st.header("Erdos-Renyi Network Model")
        st.sidebar.header("Erdos-Renyi Network Parameters")
        
        self.N = st.sidebar.slider("Number of nodes (N)", min_value=10, max_value=100, value=50, step=10)
        self.p = st.sidebar.slider("Edge probability (p)", min_value=0.1, max_value=1.0, value=0.5, step=0.1)
        self.time_steps = st.sidebar.number_input("Time steps", min_value=1, max_value=1000, value=100, step=10)
        
        
    def _initialize_network(self):
        self.G = nx.erdos_renyi_graph(self.N, self.p)
        
    
    def _network_step(self):
        """Delete a random edge and add a random edge"""
        edges = list(self.G.edges)
        remove_edge = edges[np.random.randint(0, len(edges))]
        self.G.remove_edge(*remove_edge)
        
        add_edge = (np.random.randint(0, self.N), np.random.randint(0, self.N))
        self.G.add_edge(*add_edge)
        

    def _initial_image(self):
        self.plot_placeholder = st.empty()
        
        # Display initial network state
        fig, ax = plt.subplots(figsize=(8, 8))
        nx.draw(self.G, ax=ax, with_labels=True)
        ax.set_title("Initial State", fontsize=10)
        self.plot_placeholder.pyplot(fig)
    
    
    def _append_fig(self, step):
        fig, ax = plt.subplots(figsize=(8, 8))
        nx.draw(self.G, ax=ax, with_labels=True)
        ax.set_title(f"Step {step + 1}", fontsize=10)
        self.plot_placeholder.pyplot(fig)   
        time.sleep(0.1)
    
    
    def animate(self):
        self._streamlit_setup()
        self._initialize_network()
        self._initial_image()
        
        if st.button("Play"):
            for i in range(self.time_steps):
                self._network_step()
                self._append_fig(i)