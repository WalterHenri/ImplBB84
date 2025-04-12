import qiskit_aer
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np

def bb84_protocolo(n_bits=100, erro_canal=0.05, presenca_eve=False):
    """
    Simula o protocolo BB84 para Distribuição de Chaves Quânticas

    Args:
        n_bits (int): Número de qubits a serem transmitidos
        erro_canal (float): Taxa de erro do canal quântico
        presenca_eve (bool): Se True, simula a presença de um espião

    Returns:
        dict: Dicionário com resultados e estatísticas
    """
    # Alice gera bits aleatórios para a mensagem e escolha de bases
    alice_bits = np.random.randint(0, 2, n_bits)
    alice_bases = np.random.randint(0, 2, n_bits)

    # Bob escolhe bases aleatórias para medição
    bob_bases = np.random.randint(0, 2, n_bits)

    # Lista para armazenar os resultados da medição de Bob
    bob_resultados = []

    # Simulador quântico
    simulator = AerSimulator()

    # Para cada bit, Alice prepara um qubit e Bob mede
    for i in range(n_bits):
        qc = QuantumCircuit(1, 1)

        # Alice codifica seu bit
        if alice_bits[i] == 1:
            qc.x(0)  # Aplica porta X se o bit for 1

        # Se Alice usar a base Hadamard
        if alice_bases[i] == 1:
            qc.h(0)  # Aplica porta Hadamard

        # Simulação de espião (Eve)
        if presenca_eve:
            # Eve mede em uma base aleatória e reenvia
            eve_base = np.random.randint(0, 2)
            eve_qc = qc.copy()  # Cria uma cópia do circuito para medição de Eve

            # Eve aplica H gate se sua base for 1 (Hadamard)
            if eve_base == 1:
                eve_qc.h(0)

            # Eve mede o circuito
            eve_qc.measure(0, 0)
            resultado = simulator.run(eve_qc, shots=1).result().get_counts(eve_qc)
            bit_medido = int(list(resultado.keys())[0])

            # Eve prepara um novo circuito baseado no que mediu
            new_qc = QuantumCircuit(1, 1)
            if bit_medido == 1:
                new_qc.x(0)

            # Se Eve usou base Hadamard, aplica H gate novamente
            if eve_base == 1:
                new_qc.h(0)

            qc = new_qc  # Substitui o circuito original pelo novo preparado por Eve

        # Simulação de erro no canal
        if np.random.random() < erro_canal:
            qc.x(0)  # Bit flip com probabilidade erro_canal

        # Bob mede na sua base escolhida
        if bob_bases[i] == 1:  # Base Hadamard
            qc.h(0)

        qc.measure(0, 0)

        # Executa o circuito e obtém resultados
        resultado = simulator.run(qc, shots=1).result().get_counts(qc)

        # Armazena o resultado de Bob
        bit_medido = int(list(resultado.keys())[0])
        bob_resultados.append(bit_medido)

    # Converte para numpy array para facilitar operações
    bob_resultados = np.array(bob_resultados)

    # Determina quais bits mantêm (onde as bases coincidem)
    mesma_base = alice_bases == bob_bases

    # Bits da chave peneirada (sifted key)
    alice_chave = alice_bits[mesma_base]
    bob_chave = bob_resultados[mesma_base]

    # Verifica taxa de erro
    taxa_erro = np.sum(alice_chave != bob_chave) / len(alice_chave) if len(alice_chave) > 0 else 0

    return {
        'alice_bits': alice_bits,
        'bob_resultados': bob_resultados,
        'alice_chave': alice_chave,
        'bob_chave': bob_chave,
        'taxa_erro': taxa_erro,
        'tamanho_chave': len(alice_chave)
    }

# Executa simulação sem espião
resultado_sem_eve = bb84_protocolo(n_bits=1000, erro_canal=0.05, presenca_eve=False)
print(f"Sem espião: Taxa de erro: {resultado_sem_eve['taxa_erro']:.4f}, Tamanho da chave: {resultado_sem_eve['tamanho_chave']}")

# Executa simulação com espião
resultado_com_eve = bb84_protocolo(n_bits=1000, erro_canal=0.05, presenca_eve=True)
print(f"Com espião: Taxa de erro: {resultado_com_eve['taxa_erro']:.4f}, Tamanho da chave: {resultado_com_eve['tamanho_chave']}")