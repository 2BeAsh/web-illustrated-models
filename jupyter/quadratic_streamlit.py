# Imports
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Create sliders for parameters
st.sidebar.header("Adjust Model parameters")
a = st.sidebar.slider("a", -10, 10, 1, 1)
b = st.sidebar.slider("b", -20, 20, 0, 2)


# Function
def plot_quadratic(a, b):
    x = np.linspace(-10, 10, 100)
    y = a * x ** 2 + b 
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x, y)
    ax.set(xlabel="x", ylabel="y", title=fr"$y = {a}x^2 + {b}$",
           ylim=[-100, 100])
    ax.grid()
    return fig

# Display
st.pyplot(plot_quadratic(a, b))