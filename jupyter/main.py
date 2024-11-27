# Import libraries
import streamlit as st
# Import model scripts
from ising_model import IsingModel
from sine_wave_model import SineWaveModel
from network import ErdosRenyiNetworkModel

# Model selection
st.sidebar.header("Select Model")  
model = st.sidebar.selectbox(label="", options=["Sine wave", "Ising", "Erdos-Renyi Network"])


if model == "Ising":
    ising_model = IsingModel()
    ising_model.animate()
    
elif model == "Sine wave":
    sinewave_model = SineWaveModel()
    sinewave_model.animate()

elif model == "Erdos-Renyi Network":
    network_model = ErdosRenyiNetworkModel()
    network_model.animate()