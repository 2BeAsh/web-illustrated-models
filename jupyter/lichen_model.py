import numpy as np
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt


class LichenModel:
    def __init__(self):
        pass
    
    
    def _streamlit_setup(self):
        st.header("Lichen Model")
        st.sidebar.header("Lichen Model Parameters")
        
        self.L = st.sidebar.slider("Grid Size (L)", min_value=10, max_value=100, value=50, step=10)
        self.alpha = st.sidebar.slider("Evolve rate", min_value=0.0, max_value=1.0, value=0.1, step=0.025)
        self.gamma = st.sidebar.slider("Interaction probability", min_value=0.0, max_value=1.0, value=0.1, step=0.025)
        self.time_steps = st.sidebar.number_input("Time steps", min_value=1, max_value=1000, value=100, step=10)
        
    
    def _number_of_species(self):
        return np.unique(self.lichen).size
    
    
    def _initialize_grid(self):
        """Create an LxL grid keeping track of the Lichen species. Initially, 10 species are present. 
        Also create the interaction network between the species.
        """
        self.lichen = np.random.randint(low=0, high=10, size=(self.L, self.L))  # Pick 10 random species initially
        self.interaction_network = nx.erdos_renyi_graph(n=self._number_of_species(), p=self.gamma, directed=True)
    
    
    def _new_species(self):
        """With probability alpha * gamma / L**2, choose a random point on the grid.
        The point is given a value of the number of species, to ensure it is not equal to existing species' values.
        Then create a new node in the interaction network and potentially connect it to existing nodes, and all existing nodes to it.
        Always connect it to the node of the species that was at the site before it spawned.            
        """
        if np.random.uniform() < self.alpha * self.gamma / self.L**2:
            # Find the site to spawn the new species on, and its value
            x, y = np.random.randint(low=0, high=self.L, size=2)
            new_species_value = self._number_of_species()

            # Add the new species to the interaction network and connect it to the species that was at the site before it spawned
            self.interaction_network.add_node(new_species_value)            
            self.interaction_network.add_edge(self.lichen[x, y], new_species_value)
            
            # Update the grid to contain the new species
            self.lichen[x, y] = new_species_value
            
            # For each other species, check if both the new species can invade that species and vice versa
            for node in self.interaction_network.nodes():
                if np.random.uniform() < self.gamma:
                    self.interaction_network.add_edge(new_species_value, node)
                if np.random.uniform() < self.gamma:
                    self.interaction_network.add_edge(node, new_species_value)
    
    
    def _get_neighbors(self, x, y):
        neighbors = []
        if x > 0:
            neighbors.append((x - 1, y))
        if x < self.L - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < self.L - 1:
            neighbors.append((x, y + 1))
        return neighbors
    
    
    def _invade(self):
        # Pick random site and one of its neighbours.
        idx_picked = np.random.randint(low=0, high=self.L, size=2)
        x, y = idx_picked
        # The neighbour must take closed boundary conditions into account
        possible_nbors = self._get_neighbors(x, y)
        x_nbor, y_nbor = possible_nbors[np.random.randint(low=0, high=len(possible_nbors))]
        
        # Check if the picked site can invade the neighbour from interaction_network
        if self.interaction_network.has_edge(self.lichen[x, y], self.lichen[x_nbor, y_nbor]):
            self.lichen[x_nbor, y_nbor] = self.lichen[x, y]
                
    
    def _lichen_step(self):
        """In each time step, pick a random site and a neighbour. If the chosen site kan invade the neighbour, it does so.
        Also pick a random site with probability alpha * gamma / N to create a new species on.
        """
        self._invade()
        self._new_species()
        
        
    def _initial_image(self):
        self.plot_placeholder = st.empty()

        # Display initial grid state
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.img = self.ax.imshow(self.lichen, cmap='tab10', interpolation='nearest')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_title("Initial State", fontsize=10)
        self.plot_placeholder.pyplot(self.fig)
        
    
    def _append_fig(self, step):
        self.img.set_data(self.lichen)
        self.ax.set_title(f"Step {step + 1}", fontsize=10)
        self.plot_placeholder.pyplot(self.fig)
        plt.pause(0.05)
        
        
    def animate(self):
        self._streamlit_setup()
        self._initialize_grid()
        self._initial_image()
        
        if st.button("Play"):
            for step in range(self.time_steps):
                self._lichen_step()
                self._append_fig(step)