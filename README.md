# Artigo: Visualização Interativa do Protocolo BB84 para Ensino de Criptografia Quântica

**Autores:** Walter H.A. Santos, Kauã O. S. Menezes, Lucas W. Santos, Marcos V. S. Morais, Antônio J. A. Neto (Universidade Federal de Sergipe - UFS)

**Artigo Associado:** Visualização Interativa do Protocolo BB84 para Ensino de Criptografia Quântica (SBSeg'25)
*   **Link/DOI do Artigo:** [!-- LINK PARA O ARTIGO --]

---

## 📜 Visão Geral (Overview)

Este repositório contém o artefato associado ao artigo "Visualização Interativa do Protocolo BB84 para Ensino de Criptografia Quântica", submetido ao SBSeg'25.

O artigo apresenta uma visualização interativa do protocolo de distribuição de chaves quânticas BB84, implementada com Python, Qiskit e Streamlit. O objetivo é fornecer uma ferramenta didática para o ensino de criptografia quântica, permitindo a simulação do protocolo, incluindo a presença de um espião, e a observação do impacto na Taxa de Erro Quântico (QBER). O artefato associado permite a replicação dos resultados experimentais apresentados, contribuindo para a compreensão prática da segurança em QKD.

O artefato consiste em uma implementação do protocolo de distribuição de chaves quânticas (QKD) BB84, utilizando Python com as bibliotecas Qiskit para simulação quântica e Streamlit para criar uma interface de visualização interativa.

**Objetivo Principal do Artefato:**

*   Fornecer uma ferramenta didática e interativa para o ensino e compreensão do protocolo BB84.
*   Permitir a simulação do protocolo, incluindo a possibilidade de simular a presença de um espião (Eve).
*   Demonstrar visualmente como a presença de um espião afeta a Taxa de Erro Quântico (QBER), um indicador chave da segurança do protocolo.
*   Permitir a replicação dos resultados apresentados na Tabela 1 do artigo associado.

**Para instruções detalhadas sobre como replicar os resultados experimentais do artigo (Tabela 1), consulte o arquivo:**
➡️ **[`ARTEFATO.md`](ARTEFATO.md)** ⬅️

---

## 🚀 Começando

Siga estes passos para configurar e executar a visualização interativa:

1.  **Clone o Repositório:**
    ```bash
    git clone https://github.com/WalterHenri/ImplBB84.git
    cd ImplBB84
    ```

2.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *Isso instalará Qiskit, Streamlit, NumPy e outras bibliotecas necessárias.*

3.  **Execute a Aplicação Interativa:**
    ```bash
    streamlit run app.py
    ```
    *Isso abrirá a interface da aplicação no seu navegador web padrão.*

---

## 🔧 Requisitos 

### Hardware
*   Computador pessoal padrão.
*   Mínimo de 4GB de RAM recomendado (simulações maiores podem exigir mais).
*   Acesso à Internet (para clonar o repositório e instalar dependências via pip).

### Software
*   **Sistema Operacional:**
    *   Testado em: Windows 10 e 11.
*   **Python:** Versão 3.13.x ou superior.
*   **Gerenciador de Pacotes:** `pip` (geralmente incluído com Python).
*   **Dependências Principais (veja `requirements.txt` para a lista completa e versões exatas):**
    *   `qiskit`: Framework para computação quântica.
    *   `qiskit-aer`: Simulador de alto desempenho para Qiskit.
    *   `streamlit`: Framework para criação de aplicações web interativas com Python.
    *   `numpy`: Biblioteca para computação numérica.
    *   `matplotlib`: Biblioteca para geração de gráficos (usada internamente pelo Qiskit/Streamlit).

---

## 📈 Workflow de Avaliação e Reprodução de Resultados

A aplicação `streamlit run app.py` permite a exploração interativa do protocolo BB84. Você pode:

1.  Definir o número de qubits a serem transmitidos.
2.  Ativar ou desativar a simulação de um espião (Eve).
3.  Observar as bases escolhidas por Alice e Bob.
4.  Visualizar os qubits enviados e medidos.
5.  Verificar a chave peneirada resultante.
6.  Analisar a Taxa de Erro Quântico (QBER) calculada.

**Para reproduzir especificamente os resultados da Tabela 1 do nosso artigo (QBER e tamanho médio da chave com/sem espião), siga as instruções passo a passo detalhadas em:**
➡️ **[`ARTEFATO.md`](ARTEFATO.md)** ⬅️

Este arquivo contém os scripts ou comandos exatos e os parâmetros necessários para gerar os dados que fundamentam as conclusões do artigo.

---

## 📁 Estrutura do Repositório
ImplBB84/ </br>
├── LICENSE </br>
├── README.md  </br>
├── app.py </br>
├── main.py  </br>
└── requirements.txt </br>

---

## 📄 Licença (License)

Este projeto é licenciado sob os termos da **Licença MIT**. Veja o arquivo [`LICENSE`](LICENSE) para mais detalhes.

