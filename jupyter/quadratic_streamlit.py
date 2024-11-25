import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time


def initialize_grid(N):
    # Create an NxN grid with spins randomly set to +1 or -1
    return np.random.choice([-1, 1], size=(N, N))

def metropolis_step(grid, beta):
    # Perform one step of the Metropolis algorithm
    N = grid.shape[0]
    for _ in range(N * N):  # Loop over all spins in the grid
        i, j = np.random.randint(0, N, size=2)  # Choose a random spin
        delta_E = 2 * grid[i, j] * (
            grid[(i + 1) % N, j] + grid[(i - 1) % N, j] +
            grid[i, (j + 1) % N] + grid[i, (j - 1) % N]
        )
        # Apply Metropolis criterion
        if delta_E < 0 or np.random.uniform() < np.exp(-beta * delta_E):
            grid[i, j] *= -1  # Flip the spin
    return grid


# Sidebar controls
st.sidebar.header("Ising Model")
N = st.sidebar.slider('Grid Size (N)', min_value=10, max_value=100, value=50, step=10)
temperature = st.sidebar.slider('Temperature (T)', min_value=0.1, max_value=5.0, value=2.0, step=0.1)
steps = st.sidebar.number_input('Number of Steps', min_value=1, max_value=1000, value=100, step=10)

# Beta is inverse of temperature
beta = 1.0 / temperature

# Initialize the grid
grid = initialize_grid(N)

# Create a placeholder for the plot
plot_placeholder = st.empty()

# Perform Metropolis steps and update the plot
for step in range(steps):
    # Perform one Metropolis step
    grid = metropolis_step(grid, beta)

    # Create the plot
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(grid, cmap='coolwarm', interpolation='nearest')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Step {step + 1}")

    # Display the plot in Streamlit
    plot_placeholder.pyplot(fig)

    # Add a small delay to make the animation visible
    time.sleep(0.1)