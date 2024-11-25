# Imports
import streamlit as st
import numpy as np
import plotly.graph_objects as go


# Sidebar sliders for parameters
st.sidebar.title('Sinusoidal Animation')
frequency = st.sidebar.slider("Frequency", min_value=0.1, max_value=5.0, value=1.0, step=0.1)

# Create frames for sine wave
x = np.linspace(0, 4 * np.pi, 1000)
frames = []

for i in range(50):
    y = np.sin(frequency * (x + (i * 0.1)))
    frames.append(go.Frame(data=[go.Scatter(x=x, y=y)]))
    
# Define initial trace
initial_trace = go.Scatter(x=x, y=np.sin(frequency*x))

# Figure
fig = go.Figure(
    data=[initial_trace],
    frames=frames,
    layout=go.Layout(
        updatemenus=[
            dict(type='buttons', showactive=False,
                 buttons=[dict(label='Play',
                 method="animate",
                 args=[None]
                 )])]))


# Display animated figure
st.plotly_chart(fig)