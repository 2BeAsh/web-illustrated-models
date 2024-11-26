# Imports
import streamlit as st
import numpy as np
import plotly.graph_objects as go


class SineWaveModel:
    def __init(self):
        pass


    def _streamlit_setup(self):
        # Sidebar sliders for parameters
        st.header('Sinusoidal Animation')
        st.sidebar.header('Sine Wave Parameters')
        self.frequency = st.sidebar.slider("Frequency", min_value=0.1, max_value=5.0, value=1.0, step=0.1)


    def _frames(self):
        # Create frames for sine wave
        x = np.linspace(0, 2 * np.pi, 200)
        self.frames = []

        for i in range(500):
            y = np.sin(self.frequency * (x + i*0.05))
            self.frames.append(go.Frame(data=[go.Scatter(x=x, y=y)]))
            
        self.initial_trace = go.Scatter(x=x, y=np.sin(self.frequency*x))


    def _animated_figure(self):
        self.fig = go.Figure(
            data=[self.initial_trace],
            frames=self.frames,
            layout=go.Layout(
                updatemenus=[
                    dict(type='buttons', 
                        showactive=False,
                        buttons=[
                            dict(label='Play',
                                method="animate",
                                args=[None, {"frame": {"duration": 20, "redraw": True}, "fromcurrent": True, "mode": "immediate"}],
                        )])]))
        st.plotly_chart(self.fig)


    def animate(self):
        self._streamlit_setup()
        self._frames()
        self._animated_figure()
        
        

