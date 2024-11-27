# Import libraries
import streamlit as st
# Import model scripts
from ising_model import IsingModel
from sine_wave_model import SineWaveModel
from network import ErdosRenyiNetworkModel
from sandpile_model import SandpileModel

# Model selection
st.sidebar.header("Select Model")  
model = st.sidebar.selectbox(label="Choose a model", options=["Sine wave", "Ising", "Erdos-Renyi Network", "Sandpile"])


if model == "Ising":
    ising_model = IsingModel()
    ising_model.animate()
    
elif model == "Sine wave":
    sinewave_model = SineWaveModel()
    sinewave_model.animate()

elif model == "Erdos-Renyi Network":
    network_model = ErdosRenyiNetworkModel()
    network_model.animate()
    
elif model == "Sandpile":
    if 'sandpile' not in st.session_state:
        st.session_state.sandpile = SandpileModel()

    sandpile = st.session_state.sandpile
    sandpile.animate()