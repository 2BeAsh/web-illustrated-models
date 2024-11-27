import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time


class SandpileModel():
    def __init__(self):
        pass
    
    
    def _streamlit_setup(self):
        st.header("Sandpile Model")
        st.sidebar.header("Sandpile Model Parameters")
        
        self.N = st.sidebar.slider("Grid size (N)", min_value=5, max_value=100, value=50, step=5)
        self.critical_height = st.sidebar.slider("Critical height", min_value=1, max_value=10, value=4, step=1)
        self.time_steps = st.sidebar.number_input("Time steps", min_value=1, max_value=1000, value=100, step=10)
        

    def _initial_image(self):
        self.plot_placeholder = st.empty()
        
        # Create custom colormap with distinct colors for each height
        cmap = plt.cm.get_cmap("hot", self.critical_height)
        
        # Display initial network state
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.matshow(self.grid, cmap="hot")
        ax.set_title("Initial State", fontsize=10)
        self.plot_placeholder.pyplot(fig)

    
    def _initialize_grid(self):
        self.grid = np.random.randint(low=0, high=self.critical_height-1, size=(self.N, self.N))
    
    
    def _add_grain(self, step):    
        # Add grain randomly
        self.grid[np.random.randint(0, self.N), np.random.randint(0, self.N)] += 1
        self._append_fig(step)
    
    
    def _topple(self, step):
        """Topple the grid if any site has more grains than the critical height"""
        while np.any(self.grid >= self.critical_height):
            # Find the site with more grains than the critical height
            x, y = np.where(self.grid >= self.critical_height)
            
            # Topple the site taking boundary conditions into account
            # Boundary conditions: Ignore any grains that would fall off the grid
            x_minus_one = x[x - 1 > 0]
            x_plus_one = x[x + 1 < self.N]
            y_minus_one = y[y - 1 > 0]
            y_plus_one = y[y + 1 < self.N]

            self.grid[x, y] -= 4
            self.grid[x_minus_one, y] += 1
            self.grid[x_plus_one, y] += 1
            self.grid[x, y_minus_one] += 1
            self.grid[x, y_plus_one] += 1
            
            # Append current grid to list of figures
            self._append_fig(step)
    
    
    def _append_fig(self, step):
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.matshow(self.grid, cmap="hot")
        ax.set_title(f"Step {step + 1}", fontsize=10)
        self.plot_placeholder.pyplot(fig)   
        time.sleep(0.1)
    
            
    def animate(self):
        self._streamlit_setup()
        self._initialize_grid()
        self._initial_image()
        
        for step in range(self.time_steps):
            self._add_grain(step)
            self._topple(step)
            
    
    