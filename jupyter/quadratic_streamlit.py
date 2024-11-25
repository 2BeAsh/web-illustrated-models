# Imports
import streamlit as st
import numpy as np
import plotly.graph_objects as go


# Create frames for sine wave
x = np.linspace(0, 4 * np.pi, 100)
frames = []

for i in range(50):
    y = np.sin(x + (i * 0.1))
    frames.append(go.Frame(data=[go.Scatter(x=x, y=y)]))
    
# Define initial trace
initial_trace = go.Scatter(x=x, y=np.sin(x))

# Figure
fig = go.Figure(data=[initial_trace],
                frames=frames,
                layout=go.Layout(
                    updatemenus=[dict(type='buttons', showactive=False,
                                      buttons=[dict(label='Play',
                                                    method="animate",
                                                    args=[None])])]))


# Display animated figure
st.plotly_chart(fig)