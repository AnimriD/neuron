import streamlit as st
from neuron import h, gui
from neuron.units import mV, ms

# Initialize the NEURON environment
h.load_file("stdrun.hoc")

# Create the soma section
soma = h.Section(name='soma')
soma.L = 20  # length in microns
soma.diam = 20  # diameter in microns

# Insert passive properties (hh mechanism)
soma.insert('hh')

# Set up the voltage clamp stimulus
vclamp = h.VClamp(soma(0.5))
vclamp.dur[0] = 5  # duration of the first clamp level in ms
vclamp.amp[0] = -65  # initial clamp level in mV

# Function to run the simulation
def run_simulation(clamp_voltage):
    # Update the clamp voltage
    vclamp.amp[0] = clamp_voltage

    # Record the membrane potential
    v_soma = h.Vector().record(soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    # Run the simulation
    h.finitialize(-65 * mV)
    h.continuerun(5 * ms)

    return t, v_soma

# Streamlit UI components
st.title('NEURON Simulation with Streamlit')

clamp_voltage = st.slider('Clamp Voltage (mV)', -100.0, 100.0, -65.0, 1.0)
st.write(f'Clamp voltage set to: {clamp_voltage} mV')

# Run the simulation with the selected clamp voltage
t, v_soma = run_simulation(clamp_voltage)

# Plot the results
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(t, v_soma, label='Membrane Potential (mV)')
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Voltage (mV)')
ax.set_title('Membrane Potential vs. Time')
ax.legend()

st.pyplot(fig)
