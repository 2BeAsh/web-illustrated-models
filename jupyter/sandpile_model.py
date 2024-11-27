import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

class SandpileModel:
    def __init__(self):
        self.critical_height = 4
        self.fig = None
        self.ax = None
        self.cax = None
        self.plot_placeholder = None
    
    
    def _streamlit_setup(self):
        # Streamlit setup
        st.title("Sandpile Model Simulation")
        st.sidebar.header("Parameters")

        # Model parameters
        self.N = st.sidebar.slider("Grid Size (N)", min_value=10, max_value=100, value=50, step=10)
        self.critical_height = 4
        self.time_steps = st.sidebar.number_input("Number of Time Steps", min_value=1, max_value=1000, value=100, step=10)
        self.add_location = st.sidebar.selectbox("Grain Addition Location", ("Center", "Random"))
    
        
    def _initial_grid(self):
        self.grid = np.random.randint(low=0, high=self.critical_height + 1, size=(self.N, self.N), dtype=int)
    

    def _add_grain(self, x, y):
        self.grid[x, y] += 1
        self._topple()


    def _topple(self):
        self.avalanche_size = 0

        while np.any(self.grid >= self.critical_height):
            unstable_sites = np.argwhere(self.grid >= self.critical_height)
            for x, y in unstable_sites:
                self.avalanche_size += 1
                self.grid[x, y] -= 4
                if x > 0:
                    self.grid[x - 1, y] += 1
                if x < self.N - 1:
                    self.grid[x + 1, y] += 1
                if y > 0:
                    self.grid[x, y - 1] += 1
                if y < self.N - 1:
                    self.grid[x, y + 1] += 1

                # Update the data in the image after each topple
                self.cax.set_data(self.grid)
                self.ax.set_title(f"Step {self.step + 1}, Avalanche size = {self.avalanche_size}")
                self.plot_placeholder.pyplot(self.fig)
                time.sleep(0.01)


    def animate(self):
        # Initialize
        self._streamlit_setup()
        self._initial_grid()
        
        # Initial image and figure setup
        self.plot_placeholder = st.empty()
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        cmap = plt.cm.colors.ListedColormap(['black', 'red', 'orange', 'yellow', 'white'])
        self.cax = self.ax.imshow(self.grid, cmap=cmap, interpolation="nearest")
        cbar = self.fig.colorbar(self.cax, ax=self.ax, boundaries=np.arange(-0.5, self.critical_height + 1, 1), ticks=range(self.critical_height + 1))
        cbar.ax.set_yticklabels([str(i) for i in range(self.critical_height + 1)])
        cbar.set_label('Height')
        self.plot_placeholder.pyplot(self.fig)
      
        # Run simulation if button is pressed
        if st.button("Play"):
            for self.step in range(self.time_steps):
                # Add grain
                if self.add_location == "Center":
                    self._add_grain(self.N // 2, self.N // 2)
                elif self.add_location == "Random":
                    x, y = np.random.randint(0, self.N, size=2)
                    self._add_grain(x, y)

                # Update the data in the image instead of calling imshow
                self.cax.set_data(self.grid)
                self.ax.set_title(f"Step {self.step + 1}, Avalanche size = {self.avalanche_size}")
                self.plot_placeholder.pyplot(self.fig)
                time.sleep(0.01)  # Small delay to visualize the simulation
