import streamlit as st
from neuron import h, gui
from neuron.units import ms, mV

# Initialize the NEURON environment
h.load_file("stdrun.hoc")

# Create the soma section
soma = h.Section(name='soma')
soma.L = 20  # length in microns
soma.diam = 20  # diameter in microns

# Insert passive properties (hh mechanism)
soma.insert('hh')

# Set up the current clamp stimulus
stim = h.IClamp(soma(0.5))
stim.delay = 5  # ms
stim.dur = 1  # ms
stim.amp = 0.1  # nA, initial amplitude

# Function to run the simulation
def run_simulation(stim_amp):
    # Update the stimulus amplitude
    stim.amp = stim_amp

    # Record the membrane potential
    v_soma = h.Vector().record(soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    # Run the simulation
    h.finitialize(-65 * mV)
    h.continuerun(25 * ms)

    return t, v_soma

# Streamlit UI components
st.title('NEURON Simulation with Streamlit')

stim_amp = st.slider('Stimulus Amplitude (nA)', 0.0, 1.0, 0.1, 0.01)
st.write(f'Stimulus amplitude set to: {stim_amp} nA')

# Run the simulation with the selected stimulus amplitude
t, v_soma = run_simulation(stim_amp)

# Plot the results
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(t, v_soma, label='Membrane Potential (mV)')
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Voltage (mV)')
ax.set_title('Membrane Potential vs. Time')
ax.legend()

st.pyplot(fig)
