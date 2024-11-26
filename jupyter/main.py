# Import libraries
import streamlit as st
# Import model scripts
from ising_model import IsingModel
from sine_wave_model import SineWaveModel


# Model selection
st.sidebar.header("Select Model")  
model = st.sidebar.selectbox("Choose a model", ["Sine wave", "Ising"])


if model == "Sine wave":
    ising_model = IsingModel()
    ising_model.animate()
    
elif model == "Ising":
    sinewave_model = SineWaveModel()
    sinewave_model.animate()
    