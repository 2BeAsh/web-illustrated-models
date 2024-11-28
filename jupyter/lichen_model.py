import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class LichenModel:
    def __init__(self):
        self.node_positions = None  # To store fixed positions of nodes
    
    
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
        """Create an LxL grid keeping track of the Lichen species. Initially, 5 species are present. 
        Also create the interaction network between the species.
        """
        # self.lichen = np.random.randint(low=0, high=3, size=(self.L, self.L))  # Pick 3 random species initially
        self.lichen = np.zeros(shape=(self.L, self.L), dtype=int)
        self.lichen[:5, :5] = 1
        self.lichen[-5:, -5:] = 2
        self.interaction_network = nx.erdos_renyi_graph(n=self._number_of_species(), p=self.gamma, directed=True)
        self.node_positions = nx.spring_layout(self.interaction_network)  # Initialize node positions
    
        
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
            
            # Update positions to include the new node
            self.node_positions = nx.spring_layout(self.interaction_network, pos=self.node_positions, fixed=self.node_positions.keys())
    
    
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
        """In each time step, pick a random site and a neighbour. If the chosen site can invade the neighbour, it does so.
        Also pick a random site with probability alpha * gamma / N to create a new species on.
        """
        self._invade()
        self._new_species()
        
        
    def _identify_active_interactions(self):
        """An interaction between two species is active if they are adjacent in the grid, and inactive if they are not.
        Find all species which border another species, which are potentials for an active interaction. 
        Then go through all edges and see if they are in the set of active edges.
        """

        # Step 1: Prepare to find neighboring pairs
        active_edges = set()
        
        # Step 2: Find neighbors for all cells using Numpy slicing
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            rolled_grid = np.roll(self.lichen, shift=dx, axis=0)
            rolled_grid = np.roll(rolled_grid, shift=dy, axis=1)

            # Mask to find cells where neighboring species are different
            neighbor_mask = (self.lichen != rolled_grid)

            # Find locations where species are different and add the pairs as active edges
            unique_pairs = set(zip(self.lichen[neighbor_mask].flatten(), rolled_grid[neighbor_mask].flatten()))

            # Ensure the species value pair (a, b) is ordered to prevent duplicate representation (b, a)
            for pair in unique_pairs:
                active_edges.add(tuple(sorted(pair)))
        
        # Step 3: Identify active and inactive interactions in the network
        active_in_network = []
        inactive_in_network = []

        # Loop through all edges in the network and classify as active or inactive
        for u, v in self.interaction_network.edges():
            interaction = tuple(sorted((u, v)))
            if interaction in active_edges:
                active_in_network.append((u, v))
            else:
                inactive_in_network.append((u, v))

        return active_in_network, inactive_in_network
        
    
    def _initial_image(self):
        self.plot_placeholder = st.empty()

        # Display initial grid state
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(12, 6))
        self.img = self.ax1.imshow(self.lichen, cmap='tab10', interpolation='nearest')
        self.ax1.set_xticks([])
        self.ax1.set_yticks([])
        self.ax1.set_title("Initial State", fontsize=10)
        
        # Initial network visualization
        self._update_network_plot()
        self.plot_placeholder.pyplot(self.fig)
        
    
    def _update_network_plot(self):
        self.ax2.clear()
        
        # Use fixed positions for nodes
        pos = self.node_positions
        
        # Draw nodes, with size representing population size
        species_sizes = [np.sum(self.lichen == node) * 20 for node in self.interaction_network.nodes()]
        nx.draw_networkx_nodes(self.interaction_network, pos, ax=self.ax2, node_size=species_sizes, node_color='blue')
        
        # Draw active (green) and potential (grey) interactions
        active_edges = []
        potential_edges = []
        for u, v in self.interaction_network.edges():
            if np.any((self.lichen == u) & (np.roll(self.lichen, 1, axis=0) == v)) or \
               np.any((self.lichen == u) & (np.roll(self.lichen, -1, axis=0) == v)) or \
               np.any((self.lichen == u) & (np.roll(self.lichen, 1, axis=1) == v)) or \
               np.any((self.lichen == u) & (np.roll(self.lichen, -1, axis=1) == v)):
                active_edges.append((u, v))
            else:
                potential_edges.append((u, v))
        
        nx.draw_networkx_edges(self.interaction_network, pos, ax=self.ax2, edgelist=active_edges, edge_color='green', width=2)
        nx.draw_networkx_edges(self.interaction_network, pos, ax=self.ax2, edgelist=potential_edges, edge_color='grey', style='dashed')
        
        self.ax2.set_title("Interaction Network", fontsize=10)
    
    
    def _append_fig(self, step):
        # Update the grid state
        self.img.set_data(self.lichen)
        self.ax1.set_title(f"Step {step + 1}", fontsize=10)
        
        # Update the network state
        self._update_network_plot()
        
        self.plot_placeholder.pyplot(self.fig)
        
    
    def animate(self):
        self._streamlit_setup()
        self._initialize_grid()
        self._initial_image()
        
        if st.button("Play"):
            for step in range(self.time_steps):
                self._lichen_step()
                self._append_fig(step)
