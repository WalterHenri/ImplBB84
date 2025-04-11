# Visualização do Protocolo de Distribuição de Chaves Quânticas BB84

Esta aplicação interativa fornece uma visualização dinâmica e educativa do Protocolo de Distribuição de Chaves Quânticas BB84. Ela permite que os usuários compreendam os princípios fundamentais da criptografia quântica através de uma interface envolvente e visual.

## Recursos

- **Simulação Interativa do Protocolo**: Ajuste parâmetros como quantidade de bits, taxa de erro do canal e presença de espião
- **Visualização Passo a Passo**: Percorra cada etapa do protocolo BB84 com explicações claras
- **Exibição de Circuitos Quânticos**: Veja os circuitos quânticos reais usados em diferentes cenários
- **Análise de Resultados em Tempo Real**: Analise métricas de segurança e compare cenários com/sem espionagem
- **Conteúdo Educativo**: Aprenda sobre princípios de criptografia quântica enquanto interage com a simulação

## Instalação

1. Clone este repositório:
```bash
git clone <url-do-repositório>
cd <diretório-do-repositório>
```

2. Instale as dependências necessárias:
```bash
pip install -r requirements.txt
```

## Uso

1. Execute a aplicação Streamlit:
```bash
streamlit run app.py
```

2. Abra seu navegador e acesse o endereço mostrado no terminal (normalmente http://localhost:8501)

3. Use a barra lateral para definir parâmetros e executar simulações

4. Navegue pelas diferentes abas e etapas para explorar o protocolo BB84

## Requisitos

- Python 3.8 ou superior
- Veja requirements.txt para todas as dependências

## Como Funciona

A aplicação simula o protocolo BB84, introduzido por Charles Bennett e Gilles Brassard em 1984. Este protocolo permite que duas partes (Alice e Bob) gerem uma chave secreta aleatória compartilhada que pode ser usada para comunicação segura. A simulação demonstra:

1. Como propriedades quânticas permitem a distribuição segura de chaves
2. Como tentativas de espionagem podem ser detectadas através dos princípios da mecânica quântica
3. Os efeitos do ruído do canal na segurança do protocolo

## Para Apresentações Acadêmicas

Esta ferramenta é projetada especificamente para apresentações acadêmicas, com visualizações claras e controles intuitivos que facilitam a demonstração de conceitos de criptografia quântica para públicos com diferentes níveis de conhecimento.

## Licença

[Licença MIT](LICENSE) 