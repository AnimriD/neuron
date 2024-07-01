import streamlit as st
from neuron import h, gui
import matplotlib.pyplot as plt
import numpy as np

st.title("NEURON Simulation with Streamlit")


st.sidebar.header("Neuron Parameters")
soma_diameter = st.sidebar.slider("Soma Diameter (µm)", min_value=10, max_value=50, value=20)
soma_length = st.sidebar.slider("Soma Length (µm)", min_value=10, max_value=50, value=20)
stim_current = st.sidebar.slider("Stimulus Current (nA)", min_value=0.1, max_value=10.0, value=0.5)

soma = h.Section(name='soma')
soma.L = soma_length
soma.diam = soma_diameter
soma.insert('hh') 


stim = h.IClamp(soma(0.5))
stim.delay = 5  
stim.dur = 1  
stim.amp = stim_current 


t = h.Vector().record(h._ref_t)
v = h.Vector().record(soma(0.5)._ref_v)


h.tstop = 40.0  
h.run()


fig, ax = plt.subplots()
ax.plot(t, v)
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Voltage (mV)')
ax.set_title('Membrane Potential')

st.pyplot(fig)
