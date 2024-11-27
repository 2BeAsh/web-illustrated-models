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
        self.time_steps = st.sidebar.number_input("Time steps", min_value=1, max_value=1000, value=100, step=10)
        self.grain_add_location = st.sidebar.radio("Where are grains added?", ["Random", "Center", "Top left corner"])
        

    def _initial_image(self):
        self.plot_placeholder = st.empty()
        
        # Display initial network state
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.img = self.ax.matshow(self.grid, cmap="hot")
        self.ax.set_title("Initial State", fontsize=10)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Add colorbar to show the height of each color
        cbar = self.fig.colorbar(self.img, ax=self.ax, orientation='vertical')
        cbar.set_label('Height', fontsize=10)
        
        self.plot_placeholder.pyplot(self.fig)
        
        

    
    def _initialize_grid(self):
        self.grid = np.random.randint(low=0, high=3, size=(self.N, self.N))
    
    
    def _add_grain_random(self, step):    
        """Add grain randomly"""
        self.grid[np.random.randint(0, self.N), np.random.randint(0, self.N)] += 1
        self._append_fig(step)
    
    
    def add_grain_center(self, step):
        """Add grain to the center of the grid"""
        self.grid[self.N // 2, self.N // 2] += 1
        self._append_fig(step)
    
    
    def add_grain_top_left_corner(self, step):
        """Add grain to the top left corner of the grid"""
        self.grid[0, 0] += 1
        self._append_fig(step)
    
    
    def _determine_add_grain_function(self):
        if self.grain_add_location == "Random":
            self._add_grain = self._add_grain_random
        elif self.grain_add_location == "Center":
            self._add_grain = self.add_grain_center
        elif self.grain_add_location == "Top left corner":
            self._add_grain = self.add_grain_top_left_corner
    
    
    def _topple(self, step):
        """Topple the grid if any site has more grains than the critical height"""
        avalanche_size = 0
            
        
        while np.any(self.grid >= 4):
            unstable_sites = np.argwhere(self.grid >= 4)
            
            for x, y in unstable_sites:
                self.grid[x, y] -= 4
                if x > 0:
                    self.grid[x - 1, y] += 1
                if x < self.N - 1:
                    self.grid[x + 1, y] += 1
                if y > 0:
                    self.grid[x, y - 1] += 1
                if y < self.N - 1:
                    self.grid[x, y + 1] += 1
                
                avalanche_size += 1
            
            # Append current grid to list of figures
            self._append_fig(step, avalanche_size)
            time.sleep(0.05)
    
    
    def _append_fig(self, step, avalanche_size=0):
        self.img.set_data(self.grid)
        self.ax.set_title(f"Step {step + 1}, Avalanche size = {avalanche_size}", fontsize=10)
        self.plot_placeholder.pyplot(self.fig)   
        time.sleep(0.05)
    
            
    def animate(self):        
        self._streamlit_setup()
        self._initialize_grid()
        self._initial_image()
        self._determine_add_grain_function()

        if st.button("Play"):
            for step in range(self.time_steps):
                self._add_grain(step)
                self._topple(step)
                
    
    