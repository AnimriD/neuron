import streamlit as st
from neuron import h, gui
import matplotlib.pyplot as plt
import numpy as np

st.title("NEURON Simulation with Streamlit")

# Define a basic neuron model
st.sidebar.header("Neuron Parameters")
soma_diameter = st.sidebar.slider("Soma Diameter (µm)", min_value=10, max_value=50, value=20)
soma_length = st.sidebar.slider("Soma Length (µm)", min_value=10, max_value=50, value=20)
stim_current = st.sidebar.slider("Stimulus Current (nA)", min_value=0.1, max_value=10.0, value=0.5)

# Create the soma
soma = h.Section(name='soma')
soma.L = soma_length
soma.diam = soma_diameter
soma.insert('hh')  # Insert Hodgkin-Huxley channels

# Create a stimulus
stim = h.IClamp(soma(0.5))
stim.delay = 5  # ms
stim.dur = 1  # ms
stim.amp = stim_current  # nA

# Record time and voltage
t = h.Vector().record(h._ref_t)
v = h.Vector().record(soma(0.5)._ref_v)

# Run the simulation
h.tstop = 40.0  # ms
h.run()

# Plot the results
fig, ax = plt.subplots()
ax.plot(t, v)
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Voltage (mV)')
ax.set_title('Membrane Potential')

st.pyplot(fig)
