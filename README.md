# 🚗 Sprint Challenge 4 – Previsão de Acidentes com LSTMs

**Case Sompo**: Antecipando Volume de Acidentes em Rodovias Brasileiras

## 🎥 Apresentação do Projeto

📺 **[Assista à apresentação completa do projeto no YouTube](https://youtu.be/Gxeuqourrzk)**

---

## 👥 Equipe Big 5

- **Lucca Phelipe Masini** - RM 564121
- **Luiz Henrique Poss** - RM 562177  
- **Luis Fernando de Oliveira Salgado** - RM 561401
- **Igor Paixão Sarak** - RM 563726
- **Bernardo Braga Perobeli** - RM 562468

---

## 🎯 Objetivo do Projeto

Desenvolver uma rede neural LSTM capaz de **prever o número total de acidentes** em rodovias federais brasileiras, utilizando dados públicos da PRF (Polícia Rodoviária Federal).

O modelo visa apoiar decisões estratégicas para:
- 🚑 **Prevenção de riscos**: Antecipar períodos de alta incidência
- 💰 **Seguradoras**: Precificação dinâmica baseada em volume
- 📊 **Planejamento logístico**: Alocação inteligente de recursos

---

## 📊 Target Escolhido: Previsão de Número Total de Acidentes

### Definição do Target

**Objetivo**: Prever o número total de acidentes por semana em cada estado brasileiro.

**Tipo**: Regressão (valor contínuo)
- **Input**: Sequências de 8 semanas de histórico
- **Output**: Número previsto de acidentes na semana seguinte

### Justificativa da Escolha

#### 🔬 Processo Científico

**Tentativas Anteriores**:
1. **Classificação de Risco**: Modelo sempre predizia a classe majoritária
2. **Regressão de Proporção**: R² negativo, previsões constantes
3. **Descoberta**: Features temporais não capturam fatores críticos para proporções

**Solução Final**: Previsão de Volume Total
- ✅ **Dados mais informativos**: Lags de contagem são altamente preditivos
- ✅ **Padrões temporais claros**: Volume de acidentes tem sazonalidade
- ✅ **Aplicação prática**: Gestores precisam saber "quantos acidentes esperar"
- ✅ **Métricas interpretáveis**: MAE, RMSE, R² são intuitivos

#### 💼 Valor Prático

**Para Gestores de Rodovias:**
```
Previsão: 80 acidentes → Alocar mais patrulhas
Previsão: 20 acidentes → Operação normal
```

**Para Seguradoras:**
```
Volume alto → Ajustar precificação
Volume baixo → Campanhas promocionais
```

**Para Planejamento:**
```
Previsão semanal → Planejamento de recursos
Tendência → Estratégias de longo prazo
```

---

## 🛠️ Como os Dados Foram Tratados

### 1. Limpeza e Preparação

```python
# Agregação semanal por estado
weekly_df = df.groupby([pd.Grouper(freq='W'), 'uf']).agg({
    'total_acidentes': 'count',
    'pessoas_media': 'mean',
    'veiculos_media': 'mean'
})
```

**Definição de Acidente**: Qualquer registro no dataset PRF

### 2. Feature Engineering

**12 Features Criadas:**

| Categoria | Features | Propósito |
|-----------|----------|-----------|
| **Temporais** | `dia_semana`, `mes`, `fim_semana` | Padrões semanais/mensais |
| **Sazonalidade** | `sazonalidade_sen`, `sazonalidade_cos` | Ciclos anuais |
| **Histórico (Lags)** | `acidentes_lag1/2/3` | Memória das últimas 3 semanas |
| **Estatísticas** | `acidentes_ma3` | Média móvel (tendência) |
| | `acidentes_tendencia` | Está subindo ou descendo? |
| | `acidentes_volatilidade` | Estabilidade da série |

### 3. Preparação para LSTM

**Sequências Temporais:**
```
Janela: 8 semanas de histórico → Prevê semana 9
Formato: [amostras, 8 timesteps, 12 features]
```

**Normalização:**
- MinMaxScaler (0-1) para features e target
- Essencial para convergência da LSTM

**Divisão Temporal:**
- 85% treino, 15% validação
- ⚠️ **SEM shuffle** (respeita ordem temporal)

---

## 🧠 Arquitetura do Modelo LSTM

### Diagrama da Rede

```
Input: (8 timesteps, 12 features)
    ↓
┌─────────────────────────────┐
│  LSTM Layer 1 (128 units)    │  ← Captura padrões temporais complexos
│  return_sequences=True       │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Dropout (0.2)               │  ← Previne overfitting
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  LSTM Layer 2 (64 units)     │  ← Refina os padrões
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Dropout (0.2)               │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Dense (32 units, ReLU)       │  ← Processamento não-linear
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Dropout (0.2)               │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Dense (16 units, ReLU)      │  ← Camada intermediária
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Dense (1 unit, Linear)      │  ← Saída: número de acidentes
└─────────────────────────────┘
```

### Hiperparâmetros

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| **Loss Function** | `mean_absolute_error` | Adequada para regressão |
| **Optimizer** | `Adam` (lr=0.001) | Adaptativo, converge bem |
| **Batch Size** | 32 | Balanceio entre velocidade e estabilidade |
| **Epochs** | 100 | Com EarlyStopping |
| **Dropout** | 0.2 | Regularização moderada |

### Callbacks

**EarlyStopping:**
```python
patience=15, restore_best_weights=True
```
- Para se não houver melhoria em 15 épocas
- Restaura pesos da melhor época

**ReduceLROnPlateau:**
```python
factor=0.5, patience=7
```
- Reduz learning rate pela metade se estagnado
- Ajuda a escapar de platôs

---

## 📈 Métricas de Avaliação

### Métricas Utilizadas

Para regressão, utilizamos:

| Métrica | Descrição | Objetivo |
|---------|-----------|----------|
| **MAE** | Erro absoluto médio | Interpretável (acidentes) |
| **RMSE** | Raiz do erro quadrático médio | Penaliza erros grandes |
| **R² Score** | Coeficiente de determinação | % da variância explicada |
| **MAPE** | Erro percentual absoluto médio | Erro relativo |

### Baselines para Comparação

- 📊 **Média Histórica**: Sempre prever a média (55.5 acidentes)
- 🎯 **Nosso Objetivo**: R² > 0.70, MAE < 15 acidentes

---

## 🚀 Instruções de Execução

### Opção 1: Google Colab (Recomendado) ⭐

**Clique no badge abaixo para abrir diretamente no Colab:**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/9luis7/lstm-acidentes-prf/blob/main/Sprint_Challenge_4_LSTM_Acidentes.ipynb)

**Passos:**
1. Clique no badge acima
2. No Colab: `Ambiente de execução` → `Executar tudo`
3. ☕ Aguarde ~15-30 minutos
4. Visualize os resultados!

**Sem configurações necessárias!** Tudo é automático:
- ✅ Instalação de dependências
- ✅ Carregamento do dataset
- ✅ Treinamento do modelo
- ✅ Geração de gráficos

### Opção 2: Execução Local

**Requisitos:**
- Python 3.8+
- pip

**Passos:**

```bash
# 1. Clone o repositório
git clone https://github.com/9luis7/lstm-acidentes-prf.git
cd lstm-acidentes-prf

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o notebook
jupyter notebook Sprint_Challenge_4_LSTM_Acidentes.ipynb
```

---

## 📦 Estrutura do Repositório

```
lstm-acidentes-prf/
│
├── 📓 Sprint_Challenge_4_LSTM_Acidentes.ipynb   # Notebook principal
│
├── 📊 dados/
│   └── datatran2025.xlsx                         # Dataset PRF
│
├── 📄 README.md                                  # Este arquivo
│
└── 📋 requirements.txt                           # Dependências Python
```

---

## 🎓 Resultados e Conclusões

### Resultados Obtidos

**Métricas Finais:**
- 🎯 **R² Score**: 0.8114 (81.1% da variância explicada)
- 📊 **MAE**: 11.47 acidentes (erro médio)
- 📈 **RMSE**: 22.09 acidentes
- 📊 **MAPE**: 34.60%
- 🏆 **Melhoria vs Baseline**: 70.9%

**Qualidade das Predições:**
- 70.2% das predições têm erro < 10 acidentes
- Mediana do erro: 5.91 acidentes
- 75% das predições têm erro ≤ 11 acidentes

### Descobertas Importantes

#### 🔬 Processo Científico

1. **Experimento Inicial**: Classificação (sempre predizia classe majoritária)
2. **Segunda Tentativa**: Regressão de proporção (R² negativo)
3. **Descoberta**: Features temporais são mais preditivas para volume que para proporção
4. **Solução Final**: Regressão de volume total (sucesso!)

#### 💡 Insights sobre os Dados

- **Lags são cruciais**: Histórico de 3 semanas é altamente preditivo
- **Sazonalidade existe**: Componentes seno/cosseno ajudam
- **Volume é mais previsível**: Que proporção de severidade

### Limitações Identificadas

| Limitação | Impacto | Solução Futura |
|-----------|---------|----------------|
| **Features ausentes** (clima, eventos) | Dificulta previsão de extremos | Integrar APIs (OpenWeather, feriados) |
| **Outliers extremos** | Alguns picos não são capturados | Detecção de anomalias + tratamento |
| **Janela fixa (8 semanas)** | Pode perder padrões de longo prazo | Testar janelas variáveis |

### Aplicações Práticas

#### Para Seguradoras (Sompo)

**Sistema de Alertas:**
```
📗 Volume BAIXO  → "Período normal - sem ações especiais"
📙 Volume MÉDIO  → "Atenção - campanhas preventivas recomendadas"
📕 Volume ALTO   → "ALERTA - intensificar fiscalização"
```

**Precificação Dinâmica:**
- Ajustar prêmios baseado no volume previsto
- Oferecer descontos em períodos de baixo volume
- Alertar segurados em períodos críticos

#### Para Gestores de Rodovias

**Alocação de Recursos:**
- Priorizar patrulhas em semanas de alto volume
- Planejar campanhas de conscientização
- Antecipar necessidade de ambulâncias

#### Para Motoristas

**Informação e Conscientização:**
- App com alertas semanais de volume
- Dicas de segurança personalizadas
- Recomendações de horários mais seguros

---

## 🚀 Próximos Passos

### Melhorias de Curto Prazo

- [ ] Integrar dados climáticos (API OpenWeather)
- [ ] Adicionar calendário de feriados
- [ ] Implementar detecção de outliers
- [ ] Testar janelas temporais variáveis (4, 12, 16 semanas)

### Melhorias de Médio Prazo

- [ ] Explorar Attention mechanisms
- [ ] Testar modelos híbridos (CNN+LSTM)
- [ ] Implementar ensemble com XGBoost
- [ ] Validação cruzada temporal (walk-forward)

### Deploy e Produção

- [ ] API REST com FastAPI
- [ ] Dashboard interativo (Streamlit)
- [ ] Sistema de alertas automático (email/SMS)
- [ ] Retreinamento periódico (MLOps)

---

## 📚 Tecnologias Utilizadas

### Core

- **Python** 3.8+
- **TensorFlow/Keras** 2.x - Deep Learning
- **Pandas** - Manipulação de dados
- **NumPy** - Operações numéricas

### Visualização

- **Matplotlib** - Gráficos
- **Seaborn** - Visualizações estatísticas

### Machine Learning

- **Scikit-learn** - Pré-processamento e métricas
- **LSTM** - Redes neurais recorrentes

---

## 📖 Referências

1. **Dataset**: [PRF - Dados Abertos](https://www.gov.br/prf/pt-br/acesso-a-informacao/dados-abertos)
2. **Keras Documentation**: [https://keras.io](https://keras.io)
3. **Understanding LSTM Networks**: [Colah's Blog](https://colah.github.io/posts/2015-08-Understanding-LSTMs/)
4. **Time Series Forecasting with Deep Learning**: [TensorFlow Tutorials](https://www.tensorflow.org/tutorials/structured_data/time_series)

---

## 📄 Licença

Este projeto é licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- **PRF**: Por disponibilizar os dados públicos
- **FIAP**: Pela oportunidade e desafio
- **Sompo**: Pela inspiração do case real

---

## 📧 Contato

**Equipe Big 5**
- 🐙 GitHub: [https://github.com/9luis7/lstm-acidentes-prf](https://github.com/9luis7/lstm-acidentes-prf)

---

<div align="center">

### 🏆 Sprint Challenge 4 - FIAP 2025

**Desenvolvido com ❤️ pela Equipe Big 5**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/9luis7/lstm-acidentes-prf/blob/main/Sprint_Challenge_4_LSTM_Acidentes.ipynb)

</div>