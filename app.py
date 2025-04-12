import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from AlgorithmImplementation import bb84_protocolo
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
import time
import io
from PIL import Image
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

st.set_page_config(layout="wide", page_title="BB84 Quantum Key Distribution Protocol")

st.markdown("<h1 class='main-header'>BB84 Quantum Key Distribution Protocol</h1>", unsafe_allow_html=True)

st.markdown("""
<div class='section'>
    <p>This interactive demonstration shows the BB84 protocol, a quantum key distribution method developed by Charles Bennett and Gilles Brassard in 1984. It allows two parties (Alice and Bob) to create a shared random secret key for secure communication, using quantum mechanics principles to detect any eavesdropping attempts.</p>
</div>
""", unsafe_allow_html=True)

# Protocol parameters sidebar
with st.sidebar:
    st.markdown("### Protocol Parameters")
    n_bits = st.slider("Number of qubits", min_value=10, max_value=1000, value=100, step=10)
    erro_canal = st.slider("Channel error rate", min_value=0.0, max_value=0.2, value=0.05, step=0.01)
    presenca_eve = st.checkbox("Simulate Eve (eavesdropper)", value=False)

    if st.button("Run Simulation", type="primary"):
        with st.spinner("Running simulation..."):
            resultado = bb84_protocolo(n_bits=n_bits, erro_canal=erro_canal, presenca_eve=presenca_eve)
            st.session_state.resultado = resultado
            st.session_state.simulation_run = True

    # Color options for the charts
    st.markdown("---")
    st.markdown("### Visualization Options")
    if 'color_theme' not in st.session_state:
        st.session_state.color_theme = "Black and White"

    color_theme = st.radio("Color scheme:",
                           ["Black and White", "Blue and Gray", "Red and Black"],
                           index=0)
    st.session_state.color_theme = color_theme

    # Setting colors based on the choice (keeping white backgrounds)
    if color_theme == "Black and White":
        st.session_state.primary_color = "#000000"
        st.session_state.secondary_color = "#333333"
        st.session_state.accent_color = "#555555"
        st.session_state.correct_color = "#008000"
        st.session_state.error_color = "#C00000"

        # Apply CSS variables
        st.markdown("""
        <style>
            :root {
                --primary-color: #000000;
                --secondary-color: #333333;
                --accent-color: #555555;
                --correct-color: #008000;
                --error-color: #C00000;
            }
            .stButton>button[data-baseweb="button"] {
                background-color: #000000 !important;
            }
        </style>
        """, unsafe_allow_html=True)

    elif color_theme == "Blue and Gray":
        st.session_state.primary_color = "#1E3A8A"
        st.session_state.secondary_color = "#2563EB"
        st.session_state.accent_color = "#93C5FD"
        st.session_state.correct_color = "#047857"
        st.session_state.error_color = "#DC2626"

        # Apply CSS variables
        st.markdown("""
        <style>
            :root {
                --primary-color: #1E3A8A;
                --secondary-color: #2563EB;
                --accent-color: #93C5FD;
                --correct-color: #047857;
                --error-color: #DC2626;
            }
            .stButton>button[data-baseweb="button"] {
                background-color: #1E3A8A !important;
            }
        </style>
        """, unsafe_allow_html=True)

    else:  # Red and Black
        st.session_state.primary_color = "#770000"
        st.session_state.secondary_color = "#AA0000"
        st.session_state.accent_color = "#FFAAAA"
        st.session_state.correct_color = "#008800"
        st.session_state.error_color = "#000000"

        # Apply CSS variables
        st.markdown("""
        <style>
            :root {
                --primary-color: #770000;
                --secondary-color: #AA0000;
                --accent-color: #FFAAAA;
                --correct-color: #008800;
                --error-color: #000000;
            }
            .stButton>button[data-baseweb="button"] {
                background-color: #770000 !important;
            }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Protocol Steps")
    step_options = ["1. Quantum Bit Generation",
                   "2. Basis Selection",
                   "3. Quantum Transmission",
                   "4. Basis Reconciliation",
                   "5. Key Sifting",
                   "6. Error Estimation"]
    selected_step = st.radio("Navigate to step:", step_options)

# Configure matplotlib style to match the theme
plt.style.use('default')  # Reset to default first
plt.rcParams['axes.edgecolor'] = st.session_state.get('primary_color', '#000000')
plt.rcParams['axes.labelcolor'] = st.session_state.get('primary_color', '#000000')
plt.rcParams['xtick.color'] = st.session_state.get('primary_color', '#000000')
plt.rcParams['ytick.color'] = st.session_state.get('primary_color', '#000000')
plt.rcParams['axes.titlecolor'] = st.session_state.get('primary_color', '#000000')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['lines.color'] = st.session_state.get('primary_color', '#000000')
plt.rcParams['patch.edgecolor'] = st.session_state.get('primary_color', '#000000')
plt.rcParams['grid.color'] = '#DDDDDD'

# Main content
tab1, tab2, tab3 = st.tabs(["Protocol Visualization", "Quantum Circuits", "Results Analysis"])

with tab1:
    # Protocol Visualization
    st.markdown("<h2 class='sub-header'>Protocol Visualization</h2>", unsafe_allow_html=True)

    # Determine which step is selected
    step_idx = step_options.index(selected_step) + 1

    # Display the appropriate step content
    if step_idx == 1:
        st.markdown("<div class='step-box'><h3>Step 1: Quantum Bit Generation</h3></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <p>Alice generates random classical bits that she wants to securely share with Bob.</p>
            <p>Each bit (0 or 1) will be encoded in a quantum state.</p>
            """, unsafe_allow_html=True)

        with col2:
            if 'simulation_run' in st.session_state and st.session_state.simulation_run:
                alice_bits = st.session_state.resultado['alice_bits']
                fig, ax = plt.subplots(figsize=(10, 2))
                ax.imshow([alice_bits[:20]], cmap='binary', aspect='auto')
                ax.set_yticks([])
                ax.set_xticks(range(20))
                ax.set_xticklabels(alice_bits[:20])
                ax.set_title("First 20 random bits from Alice")
                st.pyplot(fig)
            else:
                st.info("Run the simulation to view Alice's random bits")

    elif step_idx == 2:
        st.markdown("<div class='step-box'><h3>Step 2: Basis Selection</h3></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <p>Alice randomly chooses a basis (Computational or Hadamard) for each bit.</p>
            <p>Bob, independently, chooses random bases for his measurements.</p>
            <ul>
                <li>Computational basis (0): |0⟩ and |1⟩</li>
                <li>Hadamard basis (1): |+⟩ and |-⟩</li>
            </ul>
            """, unsafe_allow_html=True)

        with col2:
            if 'simulation_run' in st.session_state and st.session_state.simulation_run:
                alice_bases = np.random.randint(0, 2, n_bits)  # We're recreating this for visualization
                bob_bases = np.random.randint(0, 2, n_bits)

                # Use theme colors
                primary_color = st.session_state.get('primary_color', '#000000')
                secondary_color = st.session_state.get('secondary_color', '#333333')
                custom_cmap = plt.cm.colors.ListedColormap([primary_color, secondary_color])

                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 3))
                ax1.imshow([alice_bases[:20]], cmap=custom_cmap, aspect='auto', vmin=0, vmax=1)
                ax1.set_yticks([])
                ax1.set_xticks(range(20))
                ax1.set_xticklabels(['C' if b == 0 else 'H' for b in alice_bases[:20]])
                ax1.set_title("Alice's Bases (C = Computational, H = Hadamard)")

                ax2.imshow([bob_bases[:20]], cmap=custom_cmap, aspect='auto', vmin=0, vmax=1)
                ax2.set_yticks([])
                ax2.set_xticks(range(20))
                ax2.set_xticklabels(['C' if b == 0 else 'H' for b in bob_bases[:20]])
                ax2.set_title("Bob's Bases (C = Computational, H = Hadamard)")

                fig.tight_layout()
                st.pyplot(fig)
            else:
                st.info("Run the simulation to view the basis selection")

    elif step_idx == 3:
        st.markdown("<div class='step-box'><h3>Step 3: Quantum Transmission</h3></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <p>Alice prepares qubits according to her bits and chosen bases:</p>
            <ul>
                <li>Computational basis (0): |0⟩ for bit 0, |1⟩ for bit 1</li>
                <li>Hadamard basis (1): |+⟩ for bit 0, |-⟩ for bit 1</li>
            </ul>
            <p>The qubits are sent through the quantum channel to Bob.</p>
            <p>If Eve is present, she intercepts, measures, and resends the qubits.</p>
            """, unsafe_allow_html=True)

        with col2:
            if 'simulation_run' in st.session_state and st.session_state.simulation_run:
                # Animated quantum state transmission
                st.markdown("### Quantum Transmission Visualization")

                # Replace animation with a static visualization
                fig, ax = plt.subplots(figsize=(8, 4))

                # Use theme colors
                primary_color = st.session_state.get('primary_color', '#000000')
                secondary_color = st.session_state.get('secondary_color', '#333333')
                accent_color = st.session_state.get('accent_color', '#777777')

                if presenca_eve:
                    ax.plot([0, 1, 2], [0, 0, 0], 'ko', markersize=15, color=primary_color)
                    ax.text(0, 0.2, "Alice", fontsize=12, ha='center', color=primary_color)
                    ax.text(1, 0.2, "Eve", fontsize=12, ha='center', color=st.session_state.get('error_color', '#C00000'))
                    ax.text(2, 0.2, "Bob", fontsize=12, ha='center', color=primary_color)
                    ax.set_xlim(-0.5, 2.5)
                    ax.set_ylim(-0.5, 0.5)

                    # Qubits at different positions to simulate movement
                    ax.plot([0.3], [0], 'bo', markersize=10, alpha=0.6, color=secondary_color)
                    ax.plot([0.6], [0], 'bo', markersize=10, alpha=0.6, color=secondary_color)
                    ax.plot([1.3], [0], 'bo', markersize=10, alpha=0.6, color=secondary_color)
                    ax.plot([1.6], [0], 'bo', markersize=10, alpha=0.6, color=secondary_color)

                    # Add arrows to indicate flow
                    ax.annotate("", xy=(0.9, 0), xytext=(0.1, 0),
                                arrowprops=dict(arrowstyle="->", color=secondary_color))
                    ax.annotate("", xy=(1.9, 0), xytext=(1.1, 0),
                                arrowprops=dict(arrowstyle="->", color=secondary_color))
                else:
                    ax.plot([0, 1], [0, 0], 'ko', markersize=15, color=primary_color)
                    ax.text(0, 0.2, "Alice", fontsize=12, ha='center', color=primary_color)
                    ax.text(1, 0.2, "Bob", fontsize=12, ha='center', color=primary_color)
                    ax.set_xlim(-0.5, 1.5)
                    ax.set_ylim(-0.5, 0.5)

                    # Qubits at different positions to simulate movement
                    ax.plot([0.25], [0], 'bo', markersize=10, alpha=0.6, color=secondary_color)
                    ax.plot([0.5], [0], 'bo', markersize=10, alpha=0.6, color=secondary_color)
                    ax.plot([0.75], [0], 'bo', markersize=10, alpha=0.6, color=secondary_color)

                    # Add arrow to indicate flow
                    ax.annotate("", xy=(0.9, 0), xytext=(0.1, 0),
                               arrowprops=dict(arrowstyle="->", color=secondary_color))

                ax.set_title("Qubit Transmission")
                ax.axis('off')
                st.pyplot(fig)

                # Add explanation
                if presenca_eve:
                    st.markdown("""
                    <p>The figure shows how Eve intercepts the qubits sent by Alice, 
                    measures them, and sends new qubits to Bob. This intervention disturbs the 
                    quantum states and introduces errors.</p>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <p>The qubits travel directly from Alice to Bob without interference, 
                    preserving their quantum properties.</p>
                    """, unsafe_allow_html=True)
            else:
                st.info("Run the simulation to view the quantum transmission")

    elif step_idx == 4:
        st.markdown("<div class='step-box'><h3>Step 4: Basis Reconciliation</h3></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <p>Bob measures each qubit in his randomly chosen basis.</p>
            <p>Alice and Bob publicly share which bases they used (but not the bit values).</p>
            <p>They identify positions where they used the same basis.</p>
            """, unsafe_allow_html=True)

        with col2:
            if 'simulation_run' in st.session_state and st.session_state.simulation_run:
                alice_bases = np.random.randint(0, 2, n_bits)
                bob_bases = np.random.randint(0, 2, n_bits)
                mesma_base = alice_bases == bob_bases

                # Visualization of basis comparison
                fig, ax = plt.subplots(figsize=(10, 3))

                # Show first 20 bits
                display_len = 20
                # Use theme colors
                primary_color = st.session_state.get('primary_color', '#000000')
                accent_color = st.session_state.get('accent_color', '#777777')
                correct_color = st.session_state.get('correct_color', '#008000')
                error_color = st.session_state.get('error_color', '#C00000')

                cmap = plt.cm.colors.ListedColormap([accent_color, '#AAFFAA'])

                ax.imshow([mesma_base[:display_len]], cmap=cmap, aspect='auto', vmin=0, vmax=1)
                ax.set_yticks([])

                # Add Alice's and Bob's bases on top and bottom
                for i in range(display_len):
                    ax.text(i, -0.5, 'C' if alice_bases[i] == 0 else 'H',
                           ha='center', va='center', fontsize=9, color=primary_color)
                    ax.text(i, 1.5, 'C' if bob_bases[i] == 0 else 'H',
                           ha='center', va='center', fontsize=9, color=primary_color)

                    # Mark matches
                    if mesma_base[i]:
                        ax.text(i, 0, '✓', ha='center', va='center', color=correct_color, fontsize=12)
                    else:
                        ax.text(i, 0, '✗', ha='center', va='center', color=error_color, fontsize=12)

                ax.text(-1, -0.5, "Alice:", ha='right', va='center', fontsize=10, color=primary_color)
                ax.text(-1, 1.5, "Bob:", ha='right', va='center', fontsize=10, color=primary_color)
                ax.set_title("Basis Comparison (First 20 bits)")
                ax.set_xlim(-1.5, display_len-0.5)
                ax.set_ylim(-1, 2)

                st.pyplot(fig)

                # Display statistics
                match_rate = np.sum(mesma_base) / len(mesma_base) * 100
                st.markdown(f"<p>Basis match rate: <span class='highlight'>{match_rate:.1f}%</span> ({np.sum(mesma_base)} out of {len(mesma_base)} positions)</p>", unsafe_allow_html=True)
            else:
                st.info("Run the simulation to view the basis reconciliation")

    elif step_idx == 5:
        st.markdown("<div class='step-box'><h3>Step 5: Key Sifting</h3></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <p>Alice and Bob keep only the bits where they used the same basis.</p>
            <p>These bits form the <b>sifted key</b>.</p>
            <p>Without interference, when they use the same basis, Bob's measurements should match Alice's original bits.</p>
            """, unsafe_allow_html=True)

        with col2:
            if 'simulation_run' in st.session_state and st.session_state.simulation_run:
                # Get actual results from simulation
                alice_chave = st.session_state.resultado['alice_chave']
                bob_chave = st.session_state.resultado['bob_chave']

                # Visualization of sifted keys
                display_len = min(20, len(alice_chave))

                if display_len > 0:
                    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 2))

                    ax1.imshow([alice_chave[:display_len]], cmap='binary', aspect='auto')
                    ax1.set_yticks([])
                    ax1.set_xticks(range(display_len))
                    ax1.set_xticklabels(alice_chave[:display_len])
                    ax1.set_title("Alice's sifted key (first bits)")

                    ax2.imshow([bob_chave[:display_len]], cmap='binary', aspect='auto')
                    ax2.set_yticks([])
                    ax2.set_xticks(range(display_len))
                    ax2.set_xticklabels(bob_chave[:display_len])
                    ax2.set_title("Bob's sifted key (first bits)")

                    fig.tight_layout()
                    st.pyplot(fig)

                    # Display statistics
                    key_len = len(alice_chave)
                    st.markdown(f"<p>Sifted key length: <span class='highlight'>{key_len}</span> bits</p>", unsafe_allow_html=True)
                else:
                    st.warning("No matching bases were found in this simulation. Please run again.")
            else:
                st.info("Run the simulation to view the key sifting")

    elif step_idx == 6:
        st.markdown("<div class='step-box'><h3>Step 6: Error Estimation</h3></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <p>Alice and Bob compare a subset of their bits to estimate the error rate.</p>
            <p>A high error rate indicates possible eavesdropping (Eve's presence).</p>
            <p>Theoretical expectations:</p>
            <ul>
                <li>Without Eve: Error rate ≈ Channel error rate</li>
                <li>With Eve: Error rate ≈ 25% + Channel error rate</li>
            </ul>
            """, unsafe_allow_html=True)

        with col2:
            if 'simulation_run' in st.session_state and st.session_state.simulation_run:
                # Get actual results from simulation
                alice_chave = st.session_state.resultado['alice_chave']
                bob_chave = st.session_state.resultado['bob_chave']
                taxa_erro = st.session_state.resultado['taxa_erro']

                # Calculate expected error rates
                expected_error = erro_canal
                expected_with_eve = 0.25 + erro_canal - (0.25 * erro_canal)  # Adjusted for combined probabilities

                # Create error rate visualization
                fig, ax = plt.subplots(figsize=(8, 4))

                # Use theme colors
                primary_color = st.session_state.get('primary_color', '#000000')
                secondary_color = st.session_state.get('secondary_color', '#333333')
                accent_color = st.session_state.get('accent_color', '#777777')
                correct_color = st.session_state.get('correct_color', '#008000')
                error_color = st.session_state.get('error_color', '#C00000')

                bars = ax.bar(['Actual Error Rate', 'Expected (No Eve)', 'Expected (With Eve)'],
                       [taxa_erro, expected_error, expected_with_eve],
                       color=[primary_color, correct_color, error_color])

                # Threshold line for detecting Eve
                ax.axhline(y=0.15, color=error_color, linestyle='--', alpha=0.7)
                ax.text(2.5, 0.15, 'Threshold for detecting Eve', va='bottom', ha='right', color=error_color)

                ax.set_ylim(0, max(taxa_erro, expected_with_eve) * 1.2)
                ax.set_ylabel('Error Rate')
                ax.set_title('Error Rate Analysis')

                # Add actual values as text
                for bar in bars:
                    height = bar.get_height()
                    ax.annotate(f'{height:.3f}',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')

                st.pyplot(fig)

                # Determine if Eve is detected
                eve_detected = taxa_erro > 0.15

                if presenca_eve:
                    if eve_detected:
                        st.markdown("<p class='danger'>⚠️ High error rate detected! Eve's presence is confirmed.</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p>Eve is present, but was not detected due to insufficient error rate.</p>", unsafe_allow_html=True)
                else:
                    if eve_detected:
                        st.markdown("<p class='danger'>⚠️ High error rate detected! This may indicate channel noise or an undetected eavesdropper.</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p class='success'>✓ Low error rate: No eavesdropper detected. The key is likely secure.</p>", unsafe_allow_html=True)
            else:
                st.info("Run the simulation to analyze error rates")

with tab2:
    # Quantum Circuits Visualization
    st.markdown("<h2 class='sub-header'>Quantum Circuits</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='section'>
        <p>Below are examples of quantum circuits used in the BB84 protocol for different scenarios:</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Bit 0, Computational Basis")
        qc0 = QuantumCircuit(1, 1)
        qc0.measure(0, 0)
        # Fix the error by converting the figure to bytes
        fig = qc0.draw(output='mpl')
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        st.image(buf)

        st.markdown("### Bit 1, Computational Basis")
        qc1 = QuantumCircuit(1, 1)
        qc1.x(0)
        qc1.measure(0, 0)
        # Fix the error by converting the figure to bytes
        fig = qc1.draw(output='mpl')
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        st.image(buf)

    with col2:
        st.markdown("### Bit 0, Hadamard Basis")
        qc2 = QuantumCircuit(1, 1)
        qc2.h(0)
        qc2.measure(0, 0)
        # Fix the error by converting the figure to bytes
        fig = qc2.draw(output='mpl')
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        st.image(buf)

        st.markdown("### Bit 1, Hadamard Basis")
        qc3 = QuantumCircuit(1, 1)
        qc3.x(0)
        qc3.h(0)
        qc3.measure(0, 0)
        # Fix the error by converting the figure to bytes
        fig = qc3.draw(output='mpl')
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        st.image(buf)

    st.markdown("### Eve's Intervention Circuit")
    qc_eve = QuantumCircuit(1, 1)
    qc_eve.barrier()
    qc_eve.measure(0, 0)
    qc_eve.barrier()
    qc_eve.x(0)
    qc_eve.barrier()
    # Fix the error by converting the figure to bytes
    fig = qc_eve.draw(output='mpl')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    st.image(buf)

with tab3:
    # Results Analysis
    st.markdown("<h2 class='sub-header'>Results Analysis</h2>", unsafe_allow_html=True)

    if 'simulation_run' in st.session_state and st.session_state.simulation_run:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<h3>Key Statistics</h3>", unsafe_allow_html=True)

            resultado = st.session_state.resultado

            # Create a metrics display
            st.metric("Total bits transmitted", n_bits)
            st.metric("Sifted key size", resultado['tamanho_chave'])
            st.metric("Error rate", f"{resultado['taxa_erro']:.4f}")

            # Key Utilization Rate
            key_util = resultado['tamanho_chave'] / n_bits * 100
            st.metric("Key utilization rate", f"{key_util:.1f}%")

            # Calculate bit mismatch
            bit_agreement = np.mean(resultado['alice_chave'] == resultado['bob_chave']) * 100
            st.metric("Bit agreement", f"{bit_agreement:.1f}%")

        with col2:
            st.markdown("<h3>Security Analysis</h3>", unsafe_allow_html=True)

            # Cores contrastantes que funcionam bem com texto branco/preto
            green_color = '#10b981'  # Verde mais brilhante
            red_color = '#ef4444'  # Vermelho intenso

            # Create a pie chart with better readability
            fig = go.Figure(data=[go.Pie(
                labels=['Correct Bits', 'Error Bits'],
                values=[bit_agreement, 100 - bit_agreement],
                hole=.4,
                marker_colors=[green_color, red_color],
                textinfo='percent',  # Mostra apenas a porcentagem para evitar sobreposição
                textfont=dict(size=16, color='white', family='Arial Black'),
                textposition='inside',
                insidetextorientation='radial',
                pull=[0, 0.05],  # Destaca apenas a fatia de erros
                hoverinfo='label+percent+value',
                showlegend=True
            )])

            fig.update_layout(
                title={
                    'text': "Bit Agreement Analysis",
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': dict(size=20, color="#1e293b", family='Arial')
                },
                height=380,  # Altura um pouco maior
                font=dict(
                    family="Arial, sans-serif",
                    color="#1e293b",
                    size=16
                ),
                paper_bgcolor='rgba(255, 255, 255, 0.95)',
                plot_bgcolor='rgba(255, 255, 255, 0.95)',
                margin=dict(l=20, r=20, t=70, b=80),  # Mais espaço para legendas
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,  # Posicionado mais abaixo para evitar sobreposição
                    xanchor="center",
                    x=0.5,
                    bgcolor='rgba(255,255,255,0.95)',
                    font=dict(size=14, color="#000000")
                ),
                annotations=[
                    dict(
                        text="Security<br>Metric",
                        x=0.5,
                        y=0.5,
                        font=dict(size=14, color="#475569", family='Arial'),
                        showarrow=False
                    )
                ]
            )

            # Adiciona uma nota explicativa abaixo da legenda para dar contexto
            fig.add_annotation(
                xref="paper", yref="paper",
                x=0.5, y=-0.3,
                text=f"Total bits analyzed: {len(resultado['alice_chave'])}",
                showarrow=False,
                font=dict(size=14),
                align="center"
            )

            # Renderiza o gráfico
            st.plotly_chart(fig, use_container_width=True)

            # Security assessment
            if resultado['taxa_erro'] < 0.1:
                safety_level = "High Security"
                desc = "Low error rate indicates secure transmission."
                color = st.session_state.get('correct_color', '#008000')
            elif resultado['taxa_erro'] < 0.2:
                safety_level = "Medium Security"
                desc = "Moderate error rate - possible noise or minor interference."
                color = "orange"
            else:
                safety_level = "Low Security"
                desc = "High error rate indicates possible espionage!"
                color = st.session_state.get('error_color', '#C00000')

            st.markdown(f"<h4 style='color:{color}'>{safety_level}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p>{desc}</p>", unsafe_allow_html=True)

            if presenca_eve:
                st.markdown("<p class='danger'>⚠️ The simulation included a spy (Eve)</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='success'>✓ The simulation was run without a spy</p>", unsafe_allow_html=True)

        # Add comparison section
        st.markdown("<h3>Comparison: With vs. Without Eve</h3>", unsafe_allow_html=True)

        # Run both simulations for comparison if not already done
        if not hasattr(st.session_state, 'comparison_done'):
            resultado_sem_eve = bb84_protocolo(n_bits=n_bits, erro_canal=erro_canal, presenca_eve=False)
            resultado_com_eve = bb84_protocolo(n_bits=n_bits, erro_canal=erro_canal, presenca_eve=True)

            st.session_state.resultado_sem_eve = resultado_sem_eve
            st.session_state.resultado_com_eve = resultado_com_eve
            st.session_state.comparison_done = True

        # Create comparison charts with better colors
        fig = go.Figure()

        # Cores mais atraentes e contrastantes
        without_eve_color = '#3b82f6'  # Azul brilhante
        with_eve_color = '#f97316'  # Laranja
        grid_color = '#e2e8f0'  # Cinza claro para a grade

        # Dados para o gráfico
        metrics = ['Error Rate', 'Key Size Ratio', 'Bit Agreement']
        without_eve_values = [
            st.session_state.resultado_sem_eve['taxa_erro'],
            st.session_state.resultado_sem_eve['tamanho_chave'] / n_bits,
            1 - st.session_state.resultado_sem_eve['taxa_erro']
        ]
        with_eve_values = [
            st.session_state.resultado_com_eve['taxa_erro'],
            st.session_state.resultado_com_eve['tamanho_chave'] / n_bits,
            1 - st.session_state.resultado_com_eve['taxa_erro']
        ]

        # Adiciona barras com bordas e estilo mais moderno
        fig.add_trace(go.Bar(
            x=metrics,
            y=without_eve_values,
            name='Without Eve',  # Make sure the name is explicit here
            marker_color=without_eve_color,
            marker_line_color='#1d4ed8',
            marker_line_width=1.5,
            opacity=0.9,
            text=[f'{v:.2f}' for v in without_eve_values],
            textposition='outside',
            textfont=dict(color='#1e293b')
        ))

        fig.add_trace(go.Bar(
            x=metrics,
            y=with_eve_values,
            name='With Eve',  # Make sure the name is explicit here
            marker_color=with_eve_color,
            marker_line_color='#c2410c',
            marker_line_width=1.5,
            opacity=0.9,
            text=[f'{v:.2f}' for v in with_eve_values],
            textposition='outside',
            textfont=dict(color='#1e293b')
        ))

        # Configuração aprimorada do layout
        fig.update_layout(
            title={
                'text': 'Impact of Eve on BB84 Protocol',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20, color="#1e293b", family='Arial')
            },
            xaxis_title={
                'text': 'Protocol Metrics',
                'font': dict(size=16, color="#475569")
            },
            yaxis_title={
                'text': 'Value (normalized)',
                'font': dict(size=16, color="#475569")
            },
            barmode='group',
            bargap=0.3,
            bargroupgap=0.1,
            font=dict(
                family="Arial, sans-serif",
                color="#1e293b",
                size=14
            ),
            paper_bgcolor='rgba(255, 255, 255, 0.95)',
            plot_bgcolor='rgba(255, 255, 255, 0.95)',
            margin=dict(l=60, r=30, t=80, b=120),  # Increased bottom margin even more
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,  # Moved legend even more down
                xanchor="center",
                x=0.5,
                bgcolor='rgba(255,255,255,0.9)',
                bordercolor="#d1d5db",
                borderwidth=1,
                font=dict(size=14)  # Increased legend font size
            )
        )

        # Improve x-axis readability
        fig.update_xaxes(
            tickfont=dict(size=14, color="#1e293b"),  # Larger font for x-axis labels
            tickangle=0,  # Keep labels horizontal
            title_standoff=20  # More space for title
        )

        # Adiciona grade de fundo para facilitar leitura dos valores
        fig.update_yaxes(
            showgrid=True,
            gridwidth=1,
            gridcolor=grid_color,
            zeroline=True,
            zerolinewidth=1.5,
            zerolinecolor='#94a3b8',
            range=[0, max(max(without_eve_values), max(with_eve_values)) * 1.2]  # Ajusta escala
        )

        # Adiciona anotações explicativas com posicionamento melhorado
        fig.add_annotation(
            x='Error Rate',
            y=max(without_eve_values[0], with_eve_values[0]) * 1.15,
            text="Higher with Eve = Security risk",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowcolor="#64748b",
            ax=-40,
            ay=-40,
            font=dict(size=12, color="#1e293b")
        )

        fig.add_annotation(
            x='Bit Agreement',
            y=max(without_eve_values[2], with_eve_values[2]) * 1.15,
            text="Lower with Eve = Compromised key",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowcolor="#64748b",
            ax=40,
            ay=-40,
            font=dict(size=12, color="#1e293b")
        )

        # EXPLICITLY SET LEGEND ITEMS - this is the critical fix
        fig.data[0].name = "Without Eve"
        fig.data[1].name = "With Eve"

        # Completely remove any legend title that might be causing issues
        fig.update_layout(
            legend_title_text='',
            showlegend=True
        )

        # Renderiza o gráfico
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class='section'>
            <p>Key observations:</p>
            <ul>
                <li>Eve's presence significantly increases the error rate (theoretically by ~25%)</li>
                <li>The key size (after sifting) remains similar with or without Eve</li>
                <li>Bit agreement drops substantially when Eve intercepts the communication</li>
            </ul>
            <p>This demonstrates the main advantage of the BB84 protocol: the ability to <b>detect espionage</b> using quantum principles.</p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info("Run the simulation to see the results analysis")

st.markdown("""
<div class='section'>
    <h3>Fundamentals of the BB84 Protocol</h3>
    <p>The BB84 protocol is based on several fundamental principles of quantum mechanics:</p>
    <ul>
        <li><b>No-cloning theorem:</b> Quantum states cannot be perfectly copied</li>
        <li><b>Heisenberg's Uncertainty Principle:</b> Measuring a quantum system disturbs it</li>
        <li><b>Quantum superposition:</b> Qubits can exist in multiple states simultaneously</li>
    </ul>
    <p>These principles ensure that any espionage attempt will introduce detectable errors in the transmission.</p>
</div>
""", unsafe_allow_html=True)