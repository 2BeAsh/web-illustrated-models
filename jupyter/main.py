# Import libraries
import streamlit as st
# Import model scripts
from ising_model import IsingModel
from network import ErdosRenyiNetworkModel
from sandpile_model import SandpileModel
from lichen_model import LichenModel

# Model selection
st.sidebar.header("Select Model")  
model = st.sidebar.selectbox(label="Choose a model", options=["Ising", "Erdos-Renyi Network", "Sandpile", "Lichen"])


if model == "Ising":
    ising_model = IsingModel()
    ising_model.animate()
    
# elif model == "Sine wave":
#     sinewave_model = SineWaveModel()
#     sinewave_model.animate()

elif model == "Erdos-Renyi Network":
    network_model = ErdosRenyiNetworkModel()
    network_model.animate()
    
elif model == "Sandpile":
    sandpile = SandpileModel()
    sandpile.animate()
    
elif model == "Lichen":
    lichen = LichenModel()
    lichen.animate()   