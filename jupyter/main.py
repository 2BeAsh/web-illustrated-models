# Import libraries
import streamlit as st
# Import model scripts
from ising_model import IsingModel
from sine_wave_model import SineWaveModel


# Model selection
st.sidebar.header("Select Model")  
model = st.sidebar.selectbox(label=None, options=["Sine wave", "Ising"])


if model == "Ising":
    ising_model = IsingModel()
    ising_model.animate()
    
elif model == "Sine wave":
    sinewave_model = SineWaveModel()
    sinewave_model.animate()
    