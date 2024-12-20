import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

class IsingModel():
    def __init__(self):
        pass
    
    
    def _streamlit_setup(self):
        # Header and parameter sidebar controls
        st.header("2D Ising Model")
        st.sidebar.header("2D Ising Model Parameters")
        
        self.N = st.sidebar.slider("Grid Size (N)", min_value=10, max_value=100, value=50, step=10)
        self.temperature = st.sidebar.slider("Temperature (T)", min_value=0.1, max_value=5.0, value=2.0, step=0.1)
        self.time_steps = st.sidebar.number_input("Time steps", min_value=1, max_value=1000, value=100, step=10)

        self.beta = 1. / self.temperature
    
    
    def _initialize_grid(self):
        # Create an NxN grid with spins randomly set to +1 or -1
        self.grid = np.random.choice([-1, 1], size=(self.N, self.N))

    
    def _ising_step(self):
        for _ in range(self.N * self.N):
            i, j = np.random.randint(0, self.N, size=2)
            delta_E = 2 * self.grid[i, j] * (
                self.grid[(i + 1) % self.N, j] + self.grid[(i - 1) % self.N, j] +
                self.grid[i, (j + 1) % self.N] + self.grid[i, (j - 1) % self.N]
            )
            
            if delta_E < 0 or np.random.rand() < np.exp(-self.beta * delta_E):
                self.grid[i, j] *= -1
        
        
    def _initial_image(self):
        self.plot_placeholder = st.empty()

        # Display initial grid state
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.img = self.ax.imshow(self.grid, cmap='coolwarm', interpolation='nearest')
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_title("Initial State", fontsize=10)
        self.plot_placeholder.pyplot(self.fig)
                
                
    def _append_fig(self, step):
        self.img.set_data(self.grid)
        self.ax.set_title(f"Step {step + 1}", fontsize=10)
        self.plot_placeholder.pyplot(self.fig)
        time.sleep(0.05)
        
        
    def animate(self):
        self._streamlit_setup()
        self._initialize_grid()
        self._initial_image()
        
        # Create animation
        if st.button("Play"):
            for i in range(self.time_steps):
                self._ising_step()
                self._append_fig(i)