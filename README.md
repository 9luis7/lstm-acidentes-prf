# LSTM - Previsão de Acidentes PRF

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue?style=flat-square&logo=github)](https://github.com/9luis7/lstm-acidentes-prf)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-orange?style=flat-square&logo=tensorflow)](https://tensorflow.org)
[![License](https://img.shields.io/badge/License-Academic-green?style=flat-square)](LICENSE)

**Sprint Challenge 4 – Previsão de Acidentes com LSTMs (Case Sompo)**

## 📑 Sumário

- [📋 Sobre o Projeto](#-sobre-o-projeto)
- [👥 Integrantes](#-integrantes)
- [🎯 Objetivo](#-objetivo)
- [🚀 Instalação e Execução](#-instalação-e-execução)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [🧠 Arquitetura do Modelo](#-arquitetura-do-modelo)
- [📊 Resultados Principais](#-resultados-principais)
- [🔧 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [📈 Como Interpretar os Resultados](#-como-interpretar-os-resultados)
- [🚨 Solução de Problemas](#-solução-de-problemas)
- [📝 Notas Técnicas](#-notas-técnicas)
- [📞 Suporte](#-suporte)
- [🤝 Contribuição](#-contribuição)
- [📄 Licença](#-licença)

## 📋 Sobre o Projeto

Este projeto desenvolve uma Rede Neural Recorrente (LSTM) para prever padrões de acidentes nas rodovias federais brasileiras, utilizando dados públicos da PRF (Polícia Rodoviária Federal). O modelo visa apoiar decisões estratégicas de prevenção e análise de riscos.

### 🎯 Características Principais

- **Modelo LSTM Avançado** com 3 camadas e regularização
- **6 Features Enriquecidas** incluindo sazonalidade e componentes temporais
- **Múltiplos Estados** (10 estados brasileiros) para maior robustez
- **Janela Temporal de 8 semanas** para contexto histórico adequado
- **Avaliação Completa** com múltiplas métricas e visualizações

## 👥 Integrantes

- **Lucca Phelipe Masini** - RM 564121
- **Luiz Henrique Poss** - RM 562177  
- **Luis Fernando de Oliveira Salgado** - RM 561401
- **Igor Paixão Sarak** - RM 563726
- **Bernardo Braga Perobeli** - RM 562468

## 🎯 Objetivo

Desenvolver e treinar uma Rede Neural Recorrente (LSTM) para prever a **proporção de acidentes severos** (envolvendo mortos ou feridos graves) nas rodovias federais, utilizando dados históricos e features temporais enriquecidas.

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.8 ou superior
- Google Colab (recomendado) ou Jupyter Notebook
- Conexão com internet para download dos dados

### Instalação das Dependências

```bash
# Clone o repositório
git clone https://github.com/9luis7/lstm-acidentes-prf.git
cd lstm-acidentes-prf

# Instale as dependências
pip install -r requirements.txt
```

### Execução no Google Colab

1. **Abra o notebook:** [`SPRINT_RNNs_LSTM.ipynb`](SPRINT_RNNs_LSTM.ipynb)
2. **Execute todas as células** em sequência (Runtime → Run All)
3. **Aguarde o download** dos dados (primeira execução)
4. **Visualize os resultados** nas células finais

### Execução Local

```bash
# Inicie o Jupyter Notebook
jupyter notebook

# Abra o arquivo SPRINT_RNNs_LSTM.ipynb
# Execute todas as células
```

## 📁 Estrutura do Projeto

```
lstm-acidentes-prf/
├── README.md                          # Este arquivo
├── SPRINT_RNNs_LSTM.ipynb            # Notebook principal
├── requirements.txt                   # Dependências Python
├── .gitignore                        # Arquivos ignorados pelo Git
├── dados/                            # Pasta para dados (vazia)
│   └── .gitkeep                      
├── modelos/                          # Pasta para modelos salvos
│   └── .gitkeep                      
└── resultados/                       # Resultados e relatórios
    ├── graficos/                     # Gráficos PNG salvos
    └── relatorio_tecnico.html       # Relatório técnico
```

## 🧠 Arquitetura do Modelo

### Características Técnicas

- **Tipo:** Rede Neural Recorrente (LSTM)
- **Camadas:** 3 camadas LSTM (100, 100, 50 neurônios)
- **Regularização:** BatchNormalization + Dropout
- **Otimizador:** Adam (learning rate: 0.001)
- **Callbacks:** EarlyStopping + ReduceLROnPlateau

### Features Utilizadas

1. **Proporção de Acidentes Severos** (target)
2. **Média de Pessoas por Acidente**
3. **Média de Veículos por Acidente**
4. **Identificação de Fim de Semana**
5. **Sazonalidade Seno** (padrões anuais)
6. **Sazonalidade Cosseno** (padrões anuais)

### Dados

- **Estados:** SP, MG, RJ, PR, RS, BA, CE, GO, PE, SC
- **Período:** Dados históricos agregados semanalmente
- **Janela Temporal:** 8 semanas para prever a próxima semana
- **Total de Sequências:** Centenas de amostras de treinamento

## 📊 Resultados Principais

### Métricas de Avaliação

- **MAE (Mean Absolute Error):** Erro médio absoluto
- **MSE (Mean Squared Error):** Erro quadrático médio  
- **RMSE (Root Mean Squared Error):** Raiz do erro quadrático médio
- **R² (Coeficiente de Determinação):** Proporção da variância explicada

### Visualizações

O modelo gera 4 gráficos de análise:

1. **Curvas de Aprendizagem - Loss (MSE)**
2. **Curvas de Aprendizagem - MAE**
3. **Comparação: Valores Reais vs. Previsões**
4. **Gráfico de Resíduos**

> 📊 **Nota:** Os gráficos são salvos automaticamente em `resultados/graficos/` ao executar o notebook.

## 🔧 Tecnologias Utilizadas

- **Python 3.8+**
- **TensorFlow/Keras** - Deep Learning
- **Pandas** - Manipulação de dados
- **NumPy** - Computação numérica
- **Matplotlib/Seaborn** - Visualização
- **Scikit-learn** - Pré-processamento
- **Google Colab** - Ambiente de execução

## 📈 Como Interpretar os Resultados

### Gráficos de Treinamento
- **Loss decrescente:** Modelo está aprendendo
- **Gap treino/validação:** Indica capacidade de generalização
- **Estabilização:** Modelo convergiu

### Previsões vs Real
- **Linha laranja próxima à azul:** Boa precisão
- **Captura de picos/vales:** Modelo aprendeu padrões
- **Suavização excessiva:** Pode indicar underfitting

### Resíduos
- **Dispersão aleatória:** Bom sinal
- **Padrões sistemáticos:** Indica problemas no modelo

## 🚨 Solução de Problemas

### Erro de Download
```python
# Se o download falhar, execute:
!pip install gdown --upgrade
```

### Erro de Memória
- Reduza o batch_size na célula de treinamento
- Use menos estados na filtragem inicial

### Gráficos não Aparecem
- Execute a célula de visualização novamente
- Verifique se matplotlib está instalado

## 📝 Notas Técnicas

### Pré-processamento
- Dados normalizados com MinMaxScaler (0-1)
- Divisão temporal: 85% treino, 15% validação
- Agregação semanal por estado

### Treinamento
- Máximo 200 épocas com early stopping
- Paciência de 15 épocas para early stopping
- Learning rate adaptativo com redução automática

### Salvamento
- Modelo salvo como `modelo_lstm_acidentes.keras`
- Gráficos salvos automaticamente em `resultados/graficos/`

## 📞 Suporte

Para dúvidas ou problemas:

1. **Verifique os logs** de erro no notebook
2. **Consulte a documentação** das bibliotecas utilizadas
3. **Execute as células** em sequência correta
4. **Verifique a conexão** com internet para download

## 🤝 Contribuição

Este é um projeto acadêmico desenvolvido para o Sprint Challenge 4. Para contribuições:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto foi desenvolvido para fins acadêmicos no contexto do Sprint Challenge 4.

---

**Desenvolvido com ❤️ pela equipe Big 5**

[![GitHub](https://img.shields.io/badge/GitHub-9luis7-blue?style=flat-square&logo=github)](https://github.com/9luis7)
[![Repository](https://img.shields.io/badge/Repository-lstm--acidentes--prf-green?style=flat-square)](https://github.com/9luis7/lstm-acidentes-prf)