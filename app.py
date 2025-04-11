import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from main import bb84_protocolo
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
import time
import io
from PIL import Image
import matplotlib.animation as animation
from matplotlib.animation import FuncAnimation

st.set_page_config(layout="wide", page_title="Protocolo de Distribuição de Chaves Quânticas BB84")

# Custom CSS
st.markdown("""
<style>
    /* Alterar o tema do Streamlit padrão para cinza claro */
    .stApp {
        background-color: #F8F8F8;
    }
    /* Cabeçalho e rodapé do Streamlit */
    header[data-testid="stHeader"], footer[data-testid="stFooter"] {
        background-color: #F8F8F8 !important;
    }
    /* Botão de menu hamburguer */
    .st-bq {
        background-color: #F8F8F8 !important;
    }
    /* Botões e interações */
    .st-bv, .st-bx, .st-by, .st-bz, .st-cf, .st-cx, .st-cy, .st-cz {
        background-color: #F8F8F8 !important;
    }
    /* Links e textos que normalmente são azuis */
    a, a:hover, a:focus, a:active, .st-cp, .st-co, .st-cn {
        color: #555555 !important;
    }
    /* Seletores e dropdown */
    .st-c0, .st-bv, .st-bw {
        border-color: #DDDDDD !important;
    }
    /* Botão de expansão de widgets */
    .st-ch {
        background-color: #F8F8F8 !important;
    }
    /* Controles da sidebar */
    [data-testid="stSidebar"] [data-testid="stImage"] {
        background-color: #F8F8F8 !important;
    }
    /* Elementos de foco */
    .st-c4:focus, .st-c4:focus-visible, .st-c5:focus, .st-c5:focus-visible {
        outline-color: #999999 !important;
    }
    /* Menu dropdown */
    .st-c0, .st-c3 {
        background-color: #F8F8F8 !important;
    }
    /* Barra de progresso */
    .stProgress > div > div > div {
        background-image: linear-gradient(to right, #DDDDDD, #999999) !important;
    }
    /* Elementos de toggle */
    .st-db, .st-dc, .st-dd, .st-de {
        background-color: #F8F8F8 !important;
    }
    /* Remover a borda azul ao selecionar */
    *:focus {
        outline-color: #999999 !important;
    }
    /* Alterar cores nas abas */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #F8F8F8 !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #555555 !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #EEEEEE !important;
        color: #333333 !important;
    }
    /* Menu expansível */
    [data-testid="stExpander"] [data-testid="stWidgetLabel"] {
        color: #333333 !important;
    }
    /* Cabeçalho da dataframe */
    .dataframe thead th {
        background-color: #EEEEEE !important;
        color: #333333 !important;
    }
    /* Caixa de texto de entrada */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-color: #DDDDDD !important;
        color: #333333 !important;
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #999999 !important;
        box-shadow: 0 0 0 0.2rem rgba(153, 153, 153, 0.25) !important;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #000000;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #111111;
        margin-top: 2rem;
    }
    .section {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #FFFFFF;
        border: 1px solid #EEEEEE;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        color: #111111;
    }
    .highlight {
        background-color: #F8F8F8;
        padding: 0.5rem;
        border-radius: 5px;
        font-weight: 500;
        color: #000000;
        border-left: 3px solid #000000;
    }
    .step-box {
        background-color: #FFFFFF;
        border-left: 5px solid #000000;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0 5px 5px 0;
        color: #000000;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    .success {
        color: #008000;
        font-weight: 500;
    }
    .danger {
        color: #C00000;
        font-weight: 500;
    }
    /* Regras adicionais para melhorar o contraste em fundos brancos */
    p, li, h3, h4 {
        color: #000000;
    }
    /* Estilo para o texto em seções com fundo branco */
    div.stMarkdown p, div.stMarkdown li {
        color: #000000;
    }
    /* Melhor contraste para rótulos e títulos */
    label, .stRadio label span p, .stCheckbox label span p {
        color: #000000 !important;
        font-weight: 500;
    }
    /* Estilo para métricas e valores */
    .metric-container p, .metric-container div {
        color: #000000 !important;
    }
    /* Ajuste para títulos em gráficos */
    .js-plotly-plot .plotly .gtitle {
        fill: #000000 !important;
    }
    
    /* Novas regras para melhorar o contraste em fundos brancos */
    /* Botões primários e elementos com fundo colorido */
    .stButton>button[data-baseweb="button"] {
        color: white !important;
        border-color: var(--accent-color) !important;
    }
    /* Tabs selecionadas e elementos de navegação */
    .stTabs [aria-selected="true"] {
        color: var(--primary-color) !important;
        border-bottom-color: var(--primary-color) !important;
    }
    .stTabs [role="tab"] {
        color: #666666 !important;
    }
    .stTabs [role="tab"]:hover {
        color: var(--primary-color) !important;
    }
    /* Sidebar - tema claro */
    .css-1d391kg, .css-12oz5g7, [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
    }
    /* Texto em elementos da sidebar */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] div {
        color: #000000 !important;
    }
    /* Sliders e controles */
    .stSlider [role="slider"] {
        background-color: var(--primary-color) !important;
    }
    .stSlider [data-baseweb="slider"] {
        background-color: #EEEEEE !important;
    }
    /* Checkbox */
    .stCheckbox input:checked ~ div {
        background-color: var(--primary-color) !important;
        border-color: var(--primary-color) !important;
    }
    /* Radio button */
    .stRadio input:checked ~ div {
        border-color: var(--primary-color) !important;
    }
    .stRadio input:checked ~ div::before {
        background-color: var(--primary-color) !important;
    }
    /* Melhor visualização para elementos interativos */
    .element-container button {
        color: white !important;
    }
    /* Ajuste para a visualização de texto em gráficos */
    .js-plotly-plot text {
        fill: currentColor !important;
    }
    /* Ajuste para títulos e rótulos */
    h1, h2, h3, h4 {
        color: #000000;
    }
    /* Corrigir conflito em gráficos */
    .js-plotly-plot .plotly .gtitle {
        fill: #000000 !important;
    }
    /* Garantir cor adequada para textos em elementos do Streamlit */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #000000;
    }
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #000000;
    }
    /* Melhorar contraste em componentes específicos */
    .stButton button span {
        color: white !important;
    }
    /* Sidebar - fundo claro */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
    }
    /* Corrige títulos de gráficos e legendas */
    g.legend text {
        fill: #000000 !important;
    }
    /* Rótulos eixos de gráficos */
    g.ytitle text, g.xtitle text {
        fill: #000000 !important;
    }
    /* Barras de progresso */
    .stProgress > div > div {
        background-color: var(--primary-color) !important;
    }
    /* Botão de colapso da sidebar */
    button[kind="headerButton"] {
        color: #000000 !important;
    }
    /* Adicionar estilo para dividers */
    hr {
        border-color: #EEEEEE !important;
    }
    /* Fundo principal */
    .main .block-container {
        background-color: #FFFFFF;
    }
    /* Cores primárias para elementos e temas */
    :root {
        --primary-color: #555555;
        --secondary-color: #777777;
        --accent-color: #999999;
        --correct-color: #008000;
        --error-color: #C00000;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Protocolo de Distribuição de Chaves Quânticas BB84</h1>", unsafe_allow_html=True)

st.markdown("""
<div class='section'>
    <p>Esta demonstração interativa mostra o protocolo BB84, um método de distribuição de chaves quânticas desenvolvido por Charles Bennett e Gilles Brassard em 1984. Ele permite que duas partes (Alice e Bob) criem uma chave secreta aleatória compartilhada para comunicação segura, usando os princípios da mecânica quântica para detectar qualquer tentativa de espionagem.</p>
</div>
""", unsafe_allow_html=True)

# Protocol parameters sidebar
with st.sidebar:
    st.markdown("### Parâmetros do Protocolo")
    n_bits = st.slider("Número de qubits", min_value=10, max_value=1000, value=100, step=10)
    erro_canal = st.slider("Taxa de erro do canal", min_value=0.0, max_value=0.2, value=0.05, step=0.01)
    presenca_eve = st.checkbox("Simular Eve (espião)", value=False)
    
    if st.button("Executar Simulação", type="primary"):
        with st.spinner("Executando simulação..."):
            resultado = bb84_protocolo(n_bits=n_bits, erro_canal=erro_canal, presenca_eve=presenca_eve)
            st.session_state.resultado = resultado
            st.session_state.simulation_run = True
    
    # Opções de cores para os gráficos        
    st.markdown("---")
    st.markdown("### Opções de Visualização")
    if 'color_theme' not in st.session_state:
        st.session_state.color_theme = "Preto e Branco"
    
    color_theme = st.radio("Esquema de cores:", 
                           ["Preto e Branco", "Azul e Cinza", "Vermelho e Preto"],
                           index=0)
    st.session_state.color_theme = color_theme
    
    # Definindo as cores com base na escolha (mantendo fundos brancos)
    if color_theme == "Preto e Branco":
        st.session_state.primary_color = "#000000"
        st.session_state.secondary_color = "#333333"
        st.session_state.accent_color = "#555555"
        st.session_state.correct_color = "#008000"
        st.session_state.error_color = "#C00000"
        
        # Aplicar variáveis CSS
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
        
    elif color_theme == "Azul e Cinza":
        st.session_state.primary_color = "#1E3A8A"
        st.session_state.secondary_color = "#2563EB"
        st.session_state.accent_color = "#93C5FD"
        st.session_state.correct_color = "#047857"
        st.session_state.error_color = "#DC2626"
        
        # Aplicar variáveis CSS
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
        
    else:  # Vermelho e Preto
        st.session_state.primary_color = "#770000"
        st.session_state.secondary_color = "#AA0000"
        st.session_state.accent_color = "#FFAAAA"
        st.session_state.correct_color = "#008800"
        st.session_state.error_color = "#000000"
        
        # Aplicar variáveis CSS
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
    st.markdown("### Etapas do Protocolo")
    step_options = ["1. Geração de Bits Quânticos",
                   "2. Seleção de Bases",
                   "3. Transmissão Quântica",
                   "4. Reconciliação de Bases",
                   "5. Peneiramento da Chave",
                   "6. Estimativa de Erro"]
    selected_step = st.radio("Navegar para etapa:", step_options)

# Configurar o estilo do matplotlib para combinar com o tema
plt.style.use('default')  # Resetar para o padrão primeiro
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
tab1, tab2, tab3 = st.tabs(["Visualização do Protocolo", "Circuitos Quânticos", "Análise de Resultados"])

with tab1:
    # Protocol Visualization
    st.markdown("<h2 class='sub-header'>Visualização do Protocolo</h2>", unsafe_allow_html=True)
    
    # Determine which step is selected
    step_idx = step_options.index(selected_step) + 1
    
    # Display the appropriate step content
    if step_idx == 1:
        st.markdown("<div class='step-box'><h3>Etapa 1: Geração de Bits Quânticos</h3></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <p>Alice gera bits clássicos aleatórios que deseja compartilhar com segurança com Bob.</p>
            <p>Cada bit (0 ou 1) será codificado em um estado quântico.</p>
            """, unsafe_allow_html=True)
            
        with col2:
            if 'simulation_run' in st.session_state and st.session_state.simulation_run:
                alice_bits = st.session_state.resultado['alice_bits']
                fig, ax = plt.subplots(figsize=(10, 2))
                ax.imshow([alice_bits[:20]], cmap='binary', aspect='auto')
                ax.set_yticks([])
                ax.set_xticks(range(20))
                ax.set_xticklabels(alice_bits[:20])
                ax.set_title("Primeiros 20 bits aleatórios de Alice")
                st.pyplot(fig)
            else:
                st.info("Execute a simulação para visualizar os bits aleatórios de Alice")
    
    elif step_idx == 2:
        st.markdown("<div class='step-box'><h3>Etapa 2: Seleção de Bases</h3></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <p>Alice escolhe aleatoriamente uma base (Computacional ou Hadamard) para cada bit.</p>
            <p>Bob, independentemente, escolhe bases aleatórias para suas medições.</p>
            <ul>
                <li>Base computacional (0): |0⟩ e |1⟩</li>
                <li>Base Hadamard (1): |+⟩ e |-⟩</li>
            </ul>
            """, unsafe_allow_html=True)
            
        with col2:
            if 'simulation_run' in st.session_state and st.session_state.simulation_run:
                alice_bases = np.random.randint(0, 2, n_bits)  # We're recreating this for visualization
                bob_bases = np.random.randint(0, 2, n_bits)
                
                # Usar cores do tema
                primary_color = st.session_state.get('primary_color', '#000000')
                secondary_color = st.session_state.get('secondary_color', '#333333')
                custom_cmap = plt.cm.colors.ListedColormap([primary_color, secondary_color])
                
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 3))
                ax1.imshow([alice_bases[:20]], cmap=custom_cmap, aspect='auto', vmin=0, vmax=1)
                ax1.set_yticks([])
                ax1.set_xticks(range(20))
                ax1.set_xticklabels(['C' if b == 0 else 'H' for b in alice_bases[:20]])
                ax1.set_title("Bases de Alice (C = Computacional, H = Hadamard)")
                
                ax2.imshow([bob_bases[:20]], cmap=custom_cmap, aspect='auto', vmin=0, vmax=1)
                ax2.set_yticks([])
                ax2.set_xticks(range(20))
                ax2.set_xticklabels(['C' if b == 0 else 'H' for b in bob_bases[:20]])
                ax2.set_title("Bases de Bob (C = Computacional, H = Hadamard)")
                
                fig.tight_layout()
                st.pyplot(fig)
            else:
                st.info("Execute a simulação para visualizar a seleção de bases")
    
    elif step_idx == 3:
        st.markdown("<div class='step-box'><h3>Etapa 3: Transmissão Quântica</h3></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <p>Alice prepara qubits de acordo com seus bits e bases escolhidas:</p>
            <ul>
                <li>Base computacional (0): |0⟩ para bit 0, |1⟩ para bit 1</li>
                <li>Base Hadamard (1): |+⟩ para bit 0, |-⟩ para bit 1</li>
            </ul>
            <p>Os qubits são enviados pelo canal quântico para Bob.</p>
            <p>Se Eve estiver presente, ela intercepta, mede e reenvia os qubits.</p>
            """, unsafe_allow_html=True)
            
        with col2:
            if 'simulation_run' in st.session_state and st.session_state.simulation_run:
                # Animated quantum state transmission
                st.markdown("### Visualização da Transmissão Quântica")
                
                # Substituir a animação por uma visualização estática
                fig, ax = plt.subplots(figsize=(8, 4))
                
                # Usar cores do tema
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
                    
                    # Qubits em diferentes posições para simular o movimento
                    ax.plot([0.3], [0], 'bo', markersize=10, alpha=0.6, color=secondary_color)
                    ax.plot([0.6], [0], 'bo', markersize=10, alpha=0.6, color=secondary_color)
                    ax.plot([1.3], [0], 'bo', markersize=10, alpha=0.6, color=secondary_color)
                    ax.plot([1.6], [0], 'bo', markersize=10, alpha=0.6, color=secondary_color)
                    
                    # Adicionar setas para indicar o fluxo
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
                    
                    # Qubits em diferentes posições para simular o movimento
                    ax.plot([0.25], [0], 'bo', markersize=10, alpha=0.6, color=secondary_color)
                    ax.plot([0.5], [0], 'bo', markersize=10, alpha=0.6, color=secondary_color)
                    ax.plot([0.75], [0], 'bo', markersize=10, alpha=0.6, color=secondary_color)
                    
                    # Adicionar seta para indicar o fluxo
                    ax.annotate("", xy=(0.9, 0), xytext=(0.1, 0), 
                               arrowprops=dict(arrowstyle="->", color=secondary_color))
                
                ax.set_title("Transmissão de qubits")
                ax.axis('off')
                st.pyplot(fig)
                
                # Adicionar explicação
                if presenca_eve:
                    st.markdown("""
                    <p>A figura mostra como Eve intercepta os qubits enviados por Alice, 
                    mede-os e envia novos qubits para Bob. Esta intervenção perturba os 
                    estados quânticos e introduz erros.</p>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <p>Os qubits viajam diretamente de Alice para Bob sem interferência, 
                    preservando suas propriedades quânticas.</p>
                    """, unsafe_allow_html=True)
            else:
                st.info("Execute a simulação para visualizar a transmissão quântica")
    
    elif step_idx == 4:
        st.markdown("<div class='step-box'><h3>Etapa 4: Reconciliação de Bases</h3></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <p>Bob mede cada qubit em sua base aleatoriamente escolhida.</p>
            <p>Alice e Bob compartilham publicamente quais bases usaram (mas não os valores dos bits).</p>
            <p>Eles identificam posições onde usaram a mesma base.</p>
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
                # Usar cores do tema
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
                ax.set_title("Comparação de Bases (Primeiros 20 bits)")
                ax.set_xlim(-1.5, display_len-0.5)
                ax.set_ylim(-1, 2)
                
                st.pyplot(fig)
                
                # Display statistics
                match_rate = np.sum(mesma_base) / len(mesma_base) * 100
                st.markdown(f"<p>Taxa de correspondência de bases: <span class='highlight'>{match_rate:.1f}%</span> ({np.sum(mesma_base)} de {len(mesma_base)} posições)</p>", unsafe_allow_html=True)
            else:
                st.info("Execute a simulação para visualizar a reconciliação de bases")
    
    elif step_idx == 5:
        st.markdown("<div class='step-box'><h3>Etapa 5: Peneiramento da Chave</h3></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <p>Alice e Bob mantêm apenas os bits onde usaram a mesma base.</p>
            <p>Esses bits formam a <b>chave peneirada</b>.</p>
            <p>Sem interferência, quando usam a mesma base, as medições de Bob devem corresponder aos bits originais de Alice.</p>
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
                    ax1.set_title("Chave peneirada de Alice (primeiros bits)")
                    
                    ax2.imshow([bob_chave[:display_len]], cmap='binary', aspect='auto')
                    ax2.set_yticks([])
                    ax2.set_xticks(range(display_len))
                    ax2.set_xticklabels(bob_chave[:display_len])
                    ax2.set_title("Chave peneirada de Bob (primeiros bits)")
                    
                    fig.tight_layout()
                    st.pyplot(fig)
                    
                    # Display statistics
                    key_len = len(alice_chave)
                    st.markdown(f"<p>Tamanho da chave peneirada: <span class='highlight'>{key_len}</span> bits</p>", unsafe_allow_html=True)
                else:
                    st.warning("Nenhuma base correspondente foi encontrada nesta simulação. Por favor, execute novamente.")
            else:
                st.info("Execute a simulação para visualizar o peneiramento da chave")
    
    elif step_idx == 6:
        st.markdown("<div class='step-box'><h3>Etapa 6: Estimativa de Erro</h3></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <p>Alice e Bob comparam um subconjunto de seus bits para estimar a taxa de erro.</p>
            <p>Uma alta taxa de erro indica possível espionagem (presença de Eve).</p>
            <p>Expectativas teóricas:</p>
            <ul>
                <li>Sem Eve: Taxa de erro ≈ Taxa de erro do canal</li>
                <li>Com Eve: Taxa de erro ≈ 25% + Taxa de erro do canal</li>
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
                
                # Usar cores do tema
                primary_color = st.session_state.get('primary_color', '#000000')
                secondary_color = st.session_state.get('secondary_color', '#333333')
                accent_color = st.session_state.get('accent_color', '#777777')
                correct_color = st.session_state.get('correct_color', '#008000')
                error_color = st.session_state.get('error_color', '#C00000')
                
                bars = ax.bar(['Taxa de Erro Real', 'Esperada (Sem Eve)', 'Esperada (Com Eve)'], 
                       [taxa_erro, expected_error, expected_with_eve],
                       color=[primary_color, correct_color, error_color])
                
                # Threshold line for detecting Eve
                ax.axhline(y=0.15, color=error_color, linestyle='--', alpha=0.7)
                ax.text(2.5, 0.15, 'Limiar para detectar Eve', va='bottom', ha='right', color=error_color)
                
                ax.set_ylim(0, max(taxa_erro, expected_with_eve) * 1.2)
                ax.set_ylabel('Taxa de Erro')
                ax.set_title('Análise da Taxa de Erro')
                
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
                        st.markdown("<p class='danger'>⚠️ Alta taxa de erro detectada! A presença de Eve está confirmada.</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p>Eve está presente, mas não foi detectada devido à taxa de erro insuficiente.</p>", unsafe_allow_html=True)
                else:
                    if eve_detected:
                        st.markdown("<p class='danger'>⚠️ Alta taxa de erro detectada! Isso pode indicar ruído no canal ou um espião não detectado.</p>", unsafe_allow_html=True)
                    else:
                        st.markdown("<p class='success'>✓ Baixa taxa de erro: Nenhum espião detectado. A chave provavelmente está segura.</p>", unsafe_allow_html=True)
            else:
                st.info("Execute a simulação para analisar as taxas de erro")

with tab2:
    # Quantum Circuits Visualization
    st.markdown("<h2 class='sub-header'>Circuitos Quânticos</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='section'>
        <p>Abaixo estão exemplos dos circuitos quânticos usados no protocolo BB84 para diferentes cenários:</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Bit 0, Base Computacional")
        qc0 = QuantumCircuit(1, 1)
        qc0.measure(0, 0)
        # Corrige o erro convertendo a figura para bytes
        fig = qc0.draw(output='mpl')
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        st.image(buf)
        
        st.markdown("### Bit 1, Base Computacional")
        qc1 = QuantumCircuit(1, 1)
        qc1.x(0)
        qc1.measure(0, 0)
        # Corrige o erro convertendo a figura para bytes
        fig = qc1.draw(output='mpl')
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        st.image(buf)
    
    with col2:
        st.markdown("### Bit 0, Base Hadamard")
        qc2 = QuantumCircuit(1, 1)
        qc2.h(0)
        qc2.measure(0, 0)
        # Corrige o erro convertendo a figura para bytes
        fig = qc2.draw(output='mpl')
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        st.image(buf)
        
        st.markdown("### Bit 1, Base Hadamard")
        qc3 = QuantumCircuit(1, 1)
        qc3.x(0)
        qc3.h(0)
        qc3.measure(0, 0)
        # Corrige o erro convertendo a figura para bytes
        fig = qc3.draw(output='mpl')
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        st.image(buf)
    
    st.markdown("### Circuito de Intervenção de Eve")
    qc_eve = QuantumCircuit(1, 1)
    qc_eve.barrier()
    qc_eve.measure(0, 0)
    qc_eve.barrier()
    qc_eve.x(0)
    qc_eve.barrier()
    # Corrige o erro convertendo a figura para bytes
    fig = qc_eve.draw(output='mpl')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    st.image(buf)

with tab3:
    # Results Analysis
    st.markdown("<h2 class='sub-header'>Análise de Resultados</h2>", unsafe_allow_html=True)
    
    if 'simulation_run' in st.session_state and st.session_state.simulation_run:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h3>Estatísticas da Chave</h3>", unsafe_allow_html=True)
            
            resultado = st.session_state.resultado
            
            # Create a metrics display
            st.metric("Total de bits transmitidos", n_bits)
            st.metric("Tamanho da chave peneirada", resultado['tamanho_chave'])
            st.metric("Taxa de erro", f"{resultado['taxa_erro']:.4f}")
            
            # Key Utilization Rate
            key_util = resultado['tamanho_chave'] / n_bits * 100
            st.metric("Taxa de utilização da chave", f"{key_util:.1f}%")
            
            # Calculate bit mismatch
            bit_agreement = np.mean(resultado['alice_chave'] == resultado['bob_chave']) * 100
            st.metric("Concordância de bits", f"{bit_agreement:.1f}%")
            
        with col2:
            st.markdown("<h3>Análise de Segurança</h3>", unsafe_allow_html=True)
            
            # Create a pie chart showing correct vs incorrect bits
            fig = go.Figure(data=[go.Pie(
                labels=['Bits Corretos', 'Bits com Erro'],
                values=[bit_agreement, 100-bit_agreement],
                hole=.4,
                marker_colors=[st.session_state.get('correct_color', '#008000'), 
                               st.session_state.get('error_color', '#C00000')]
            )])
            
            fig.update_layout(
                title="Análise de Concordância de Bits",
                height=300,
                font=dict(color=st.session_state.get('primary_color', '#000000')),
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Security assessment
            if resultado['taxa_erro'] < 0.1:
                safety_level = "Alta Segurança"
                desc = "Baixa taxa de erro indica transmissão segura."
                color = st.session_state.get('correct_color', '#008000')
            elif resultado['taxa_erro'] < 0.2:
                safety_level = "Segurança Média"
                desc = "Taxa de erro moderada - possível ruído ou interferência menor."
                color = "orange"
            else:
                safety_level = "Baixa Segurança"
                desc = "Alta taxa de erro indica possível espionagem!"
                color = st.session_state.get('error_color', '#C00000')
                
            st.markdown(f"<h4 style='color:{color}'>{safety_level}</h4>", unsafe_allow_html=True)
            st.markdown(f"<p>{desc}</p>", unsafe_allow_html=True)
            
            if presenca_eve:
                st.markdown("<p class='danger'>⚠️ A simulação incluiu um espião (Eve)</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p class='success'>✓ A simulação foi executada sem espião</p>", unsafe_allow_html=True)
        
        # Add comparison section
        st.markdown("<h3>Comparação: Com vs. Sem Eve</h3>", unsafe_allow_html=True)
        
        # Run both simulations for comparison if not already done
        if not hasattr(st.session_state, 'comparison_done'):
            resultado_sem_eve = bb84_protocolo(n_bits=n_bits, erro_canal=erro_canal, presenca_eve=False)
            resultado_com_eve = bb84_protocolo(n_bits=n_bits, erro_canal=erro_canal, presenca_eve=True)
            
            st.session_state.resultado_sem_eve = resultado_sem_eve
            st.session_state.resultado_com_eve = resultado_com_eve
            st.session_state.comparison_done = True
        
        # Create comparison charts
        fig = go.Figure()
        
        # Cores do tema
        primary_color = st.session_state.get('primary_color', '#000000')
        secondary_color = st.session_state.get('secondary_color', '#333333')
        
        fig.add_trace(go.Bar(
            x=['Taxa de Erro', 'Tamanho da Chave', 'Concordância de Bits'],
            y=[st.session_state.resultado_sem_eve['taxa_erro'], 
               st.session_state.resultado_sem_eve['tamanho_chave']/n_bits, 
               1 - st.session_state.resultado_sem_eve['taxa_erro']],
            name='Sem Eve',
            marker_color=primary_color
        ))
        
        fig.add_trace(go.Bar(
            x=['Taxa de Erro', 'Tamanho da Chave', 'Concordância de Bits'],
            y=[st.session_state.resultado_com_eve['taxa_erro'], 
               st.session_state.resultado_com_eve['tamanho_chave']/n_bits, 
               1 - st.session_state.resultado_com_eve['taxa_erro']],
            name='Com Eve',
            marker_color=secondary_color
        ))
        
        fig.update_layout(
            title='Impacto de Eve no Protocolo BB84',
            xaxis_title='Métricas',
            yaxis_title='Valor (normalizado)',
            barmode='group',
            bargap=0.15,
            bargroupgap=0.1,
            font=dict(color=primary_color),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class='section'>
            <p>Observações principais:</p>
            <ul>
                <li>A presença de Eve aumenta significativamente a taxa de erro (teoricamente em ~25%)</li>
                <li>O tamanho da chave (após peneiramento) permanece semelhante com ou sem Eve</li>
                <li>A concordância de bits cai substancialmente quando Eve intercepta a comunicação</li>
            </ul>
            <p>Isso demonstra a principal vantagem do protocolo BB84: a capacidade de <b>detectar espionagem</b> usando princípios quânticos.</p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.info("Execute a simulação para ver a análise de resultados")

st.markdown("""
<div class='section'>
    <h3>Fundamentos do Protocolo BB84</h3>
    <p>O protocolo BB84 se baseia em vários princípios fundamentais da mecânica quântica:</p>
    <ul>
        <li><b>Teorema da não-clonagem:</b> Estados quânticos não podem ser perfeitamente copiados</li>
        <li><b>Princípio da Incerteza de Heisenberg:</b> Medir um sistema quântico o perturba</li>
        <li><b>Superposição quântica:</b> Qubits podem existir em múltiplos estados simultaneamente</li>
    </ul>
    <p>Esses princípios garantem que qualquer tentativa de espionagem introduzirá erros detectáveis na transmissão.</p>
</div>
""", unsafe_allow_html=True) 