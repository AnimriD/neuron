import streamlit as st
from neuron import h
from neuron.units import ms, mV, µm
import matplotlib.pyplot as plt

# Streamlit interface
st.title('NEURON Simulation with Streamlit')

# Function to run the NEURON simulation
def run_simulation(voltage):
    # Load standard run library
    h.load_file("stdrun.hoc")

    # Create soma section
    soma = h.Section(name='soma')
    soma.L = 20  # microns
    soma.diam = 20  # microns

    # Simulation parameters
    h.dt = 0.025  # time step (ms)
    h.tstop = 100  # simulation stop time (ms)

    # Record membrane potential at the center of the soma
    v_soma = h.Vector().record(soma(0.5)._ref_v)
    t = h.Vector().record(h._ref_t)

    # Define a simple mechanism (e.g., Hodgkin-Huxley)
    soma.insert('hh')

    # Run the simulation
    h.finitialize(voltage * mV)
    h.run()

    return t, v_soma

# Function to plot the results
def plot_results(t, v_soma):
    plt.figure(figsize=(8, 4))
    plt.plot(t, v_soma)
    plt.xlabel('Time (ms)')
    plt.ylabel('Membrane Potential (mV)')
    plt.title('Membrane Potential vs. Time in Soma')
    st.pyplot(plt)

# Slider for selecting the initial voltage
voltage = st.slider("Choose the voltage with which to run the simulation", min_value=-80, max_value=-55, value=-65)

# Run the simulation when the button is pressed
if st.button('Run Simulation'):
    st.write('Running simulation...')
    t, v_soma = run_simulation(voltage)
    st.write('Simulation completed.')
    plot_results(t, v_soma)
