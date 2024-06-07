import streamlit as st
from neuron import h
import numpy as np
import matplotlib.pyplot as plt



# Initialize NEURON
soma = h.Section(name='soma')
soma.L = 20
soma.diam = 20

h.dt = 0.025
h.tstop = 100

v_soma = h.Vector()
v_soma.record(soma(0.5)._ref_v)

# Run the simulation
h.finitialize(-65)
h.continuerun(h.tstop)

# Retrieve and plot the data
v_soma_array = np.array(v_soma)

fig, ax = plt.subplots()
ax.plot(np.arange(0, h.tstop + h.dt, h.dt), v_soma_array)
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Membrane Potential (mV)')
ax.set_title('Membrane Potential vs. Time')

# Display the plot in Streamlit
st.pyplot(fig)
