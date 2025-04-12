# BB84 Quantum Key Distribution Protocol Visualization

This interactive application provides a dynamic and educational visualization of the BB84 Quantum Key Distribution Protocol. It allows users to understand the fundamental principles of quantum cryptography through an engaging and visual interface.

## Features

- **Interactive Protocol Simulation**: Adjust parameters such as bit quantity, channel error rate, and presence of an eavesdropper
- **Step-by-Step Visualization**: Walk through each stage of the BB84 protocol with clear explanations
- **Quantum Circuit Display**: View actual quantum circuits used in different scenarios
- **Real-Time Result Analysis**: Analyze security metrics and compare scenarios with/without eavesdropping
- **Educational Content**: Learn about quantum cryptography principles while interacting with the simulation

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the Streamlit application:
```bash
python -m streamlit run app.py 
```
2. If Streamlit prompts for an email to receive updates, you can leave it blank and press `enter`

3. Open your browser and go to the address shown in the terminal (usually http://localhost:8501)

4. Use the sidebar to set parameters and run simulations

5. Navigate through the different tabs and steps to explore the BB84 protocol

## Requirements

- Python 3.8 or higher
- See requirements.txt for all dependencies

## How It Works

The application simulates the BB84 protocol, introduced by Charles Bennett and Gilles Brassard in 1984. This protocol allows two parties (Alice and Bob) to generate a shared random secret key that can be used for secure communication. The simulation demonstrates:

1. How quantum properties enable secure key distribution
2. How eavesdropping attempts can be detected through quantum mechanics principles
3. The effects of channel noise on protocol security

## For Academic Presentations

This tool is specifically designed for academic presentations, with clear visualizations and intuitive controls that make it easy to demonstrate quantum cryptography concepts to audiences with different levels of knowledge.

## License

[MIT License](LICENSE)
