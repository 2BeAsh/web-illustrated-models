import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

class SandpileModel:
    def __init__(self):
        self.critical_height = 4
    
    
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
        self.grid = np.random.randint(low=0, high=self.critical_height+1, size=(self.N, self.N), dtype=int)
        self.avalanche_grid = np.zeros((self.N, self.N), dtype=int)  # Initialize avalanche grid
    

    def _add_grain(self, x, y):
        self.grid[x, y] += 1
        self._topple()


    def _topple(self):
        self.avalanche_size = 0
        self.avalanche_grid[:] = 0  # Reset avalanche grid
        while np.any(self.grid >= self.critical_height):
            unstable_sites = np.argwhere(self.grid >= self.critical_height)
            for x, y in unstable_sites:
                self.avalanche_size += 1
                self.avalanche_grid[x, y] += 1  # Track toppling events
                self.grid[x, y] -= 4
                if x > 0:
                    self.grid[x - 1, y] += 1
                if x < self.N - 1:
                    self.grid[x + 1, y] += 1
                if y > 0:
                    self.grid[x, y - 1] += 1
                if y < self.N - 1:
                    self.grid[x, y + 1] += 1

    
    def _step(self):
        if self.add_location == "Center":
            self._add_grain(self.N // 2, self.N // 2)
        elif self.add_location == "Random":
            x, y = np.random.randint(0, self.N, size=2)
            self._add_grain(x, y)


    def animate(self):
        # Initialize
        self._streamlit_setup()
        self._initial_grid()
        
        # Initial image and figure setup
        plot_placeholder = st.empty()
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        # Grid state plot
        ax1.set(xticks=[], yticks=[])
        ax1.set_title("Initial state", fontsize=10)
        cmap = plt.cm.colors.ListedColormap(['black', 'red', 'orange', 'yellow', 'white'])
        cax1 = ax1.imshow(self.grid, cmap=cmap, interpolation="nearest", vmin=0, vmax=self.critical_height)
        cbar1 = fig.colorbar(cax1, ax=ax1, boundaries=np.arange(-0.5, self.critical_height + 1, 1), ticks=range(self.critical_height + 1))
        cbar1.ax.set_yticklabels([str(i) for i in range(self.critical_height + 1)])
        cbar1.set_label('Height')
        
        # Avalanche size heatmap plot
        ax2.set(xticks=[], yticks=[])
        ax2.set_title("Avalanche Size Heatmap", fontsize=10)
        cax2 = ax2.imshow(self.avalanche_grid, cmap="magma", interpolation="nearest", vmin=0, vmax=5)
        cbar2 = fig.colorbar(cax2, ax=ax2)
        cbar2.set_label('Number of Topplings')
        
        plot_placeholder.pyplot(fig)
      
        # Run simulation if button is pressed
        if st.button("Play"):
            for step in range(self.time_steps):
                self._step()    
                
                # Update the data in the images
                cax1.set_data(self.grid)
                ax1.set_title(f"Step {step + 1}", fontsize=10)
                cax2.set_data(self.avalanche_grid)
                
                plot_placeholder.pyplot(fig)
                
                time.sleep(0.1)  # Small delay to visualize the simulation

