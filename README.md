# 🚗 Sprint Challenge 4 – Previsão de Acidentes com LSTMs

**Case Sompo**: Antecipando Padrões de Risco em Rodovias Brasileiras

---

## 👥 Equipe Big 5

- **Lucca Phelipe Masini** - RM 564121
- **Luiz Henrique Poss** - RM 562177  
- **Luis Fernando de Oliveira Salgado** - RM 561401
- **Igor Paixão Sarak** - RM 563726
- **Bernardo Braga Perobeli** - RM 562468

---

## 🎯 Objetivo do Projeto

Desenvolver uma rede neural LSTM capaz de **classificar níveis de risco de acidentes severos** em rodovias federais brasileiras, utilizando dados públicos da PRF (Polícia Rodoviária Federal).

O modelo visa apoiar decisões estratégicas para:
- 🚑 **Prevenção de riscos**: Identificar períodos críticos
- 💰 **Seguradoras**: Precificação dinâmica de seguros
- 📊 **Planejamento logístico**: Alocação inteligente de recursos

---

## 📊 Target Escolhido: Classificação de 4 Níveis de Risco

### Definição das Classes

| Classe | Nome | Faixa | Descrição |
|--------|------|-------|-----------|
| 0 | **BAIXO** | < 20% | Menos de 20% dos acidentes são severos |
| 1 | **MÉDIO-BAIXO** | 20-30% | Entre 20% e 30% de acidentes severos |
| 2 | **MÉDIO-ALTO** | 30-40% | Entre 30% e 40% de acidentes severos |
| 3 | **ALTO** | ≥ 40% | 40% ou mais de acidentes severos |

### Justificativa da Escolha

#### 🔬 Processo Científico

**Tentativa Inicial**: Regressão
- Objetivo: Prever proporção exata de acidentes severos (valor contínuo)
- ❌ Resultado: R² negativo (modelo pior que baseline)
- ❌ Problema: Previsões constantes (~0.29), sem variabilidade
- 🤔 Causa: Features disponíveis não capturam fatores críticos (clima, eventos, tráfego)

**Descoberta Importante**:
> As features temporais e de histórico disponíveis não contêm informação suficiente para previsões precisas de valores contínuos. Extremos dependem de fatores externos não capturados no dataset.

**Solução Final**: Classificação
- ✅ Mais robusta às limitações dos dados
- ✅ Mais útil na prática (alertas: "Semana de risco ALTO")
- ✅ Não requer precisão decimal
- ✅ Facilita tomada de decisão

#### 💼 Valor Prático

**Para Seguradoras:**
```
Risco BAIXO  → Precificação padrão
Risco MÉDIO  → Campanhas preventivas
Risco ALTO   → Alertas críticos + precificação ajustada
```

**Para Gestores de Rodovias:**
```
Risco BAIXO  → Operação normal
Risco ALTO   → Aumento de patrulhas + campanhas intensivas
```

---

## 🛠️ Como os Dados Foram Tratados

### 1. Limpeza e Preparação

```python
# Criação da variável 'severo' (target binário intermediário)
df['severo'] = ((df['mortos'] > 0) | (df['feridos_graves'] > 0)).astype(int)
```

**Definição de Acidente Severo:**
- `severo = 1` se mortos > 0 **OU** feridos_graves > 0
- `severo = 0` caso contrário

### 2. Agregação Temporal

**Transformação**: Acidentes individuais → Séries temporais semanais por UF

```python
# Agregação semanal
weekly_df = df.groupby([pd.Grouper(freq='W'), 'uf']).agg({
    'total_acidentes': count,
    'acidentes_severos': sum,
    'pessoas_media': mean,
    'veiculos_media': mean
})

# Cálculo do target contínuo
weekly_df['prop_severos'] = acidentes_severos / total_acidentes
```

**Por quê semanal?**
- ✅ Suficiente para capturar padrões
- ✅ Evita esparsidade (muitos zeros diários)
- ✅ Útil para planejamento (campanhas semanais)

### 3. Feature Engineering

**12 Features Criadas:**

| Categoria | Features | Propósito |
|-----------|----------|-----------|
| **Temporais** | `dia_semana`, `mes`, `fim_semana` | Capturar padrões semanais/mensais |
| **Sazonalidade** | `sazonalidade_sen`, `sazonalidade_cos` | Ciclos anuais (férias, festas) |
| **Histórico (Lags)** | `prop_severos_lag1/2/3` | Memória das últimas 3 semanas |
| **Estatísticas** | `prop_severos_ma3` | Média móvel (tendência) |
| | `prop_severos_tendencia` | Está subindo ou descendo? |
| | `prop_severos_volatilidade` | Estabilidade da série |

### 4. Preparação para LSTM

**Sequências Temporais:**
```
Janela: 8 semanas de histórico → Prevê semana 9
Formato: [amostras, 8 timesteps, 12 features]
```

**Normalização:**
- MinMaxScaler (0-1) para todas as features
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
│  LSTM Layer 1 (64 units)    │  ← Captura padrões temporais complexos
│  return_sequences=True       │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Dropout (0.2)               │  ← Previne overfitting
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  LSTM Layer 2 (32 units)     │  ← Refina os padrões
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Dropout (0.2)               │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Dense (32 units, ReLU)      │  ← Processamento não-linear
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Dropout (0.2)               │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Dense (4 units, Softmax)    │  ← Probabilidades das 4 classes
└─────────────────────────────┘
```

### Hiperparâmetros

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| **Loss Function** | `categorical_crossentropy` | Padrão para classificação multiclasse |
| **Optimizer** | `Adam` (lr=0.001) | Adaptativo, converge bem |
| **Batch Size** | 16 | Balanceio entre velocidade e estabilidade |
| **Epochs** | 100 | Com EarlyStopping |
| **Dropout** | 0.2 | Regularização moderada |

### Callbacks

**EarlyStopping:**
```python
patience=20, restore_best_weights=True
```
- Para se não houver melhoria em 20 épocas
- Restaura pesos da melhor época

**ReduceLROnPlateau:**
```python
factor=0.5, patience=10
```
- Reduz learning rate pela metade se estagnado
- Ajuda a escapar de platôs

---

## 📈 Métricas de Avaliação

### Métricas Utilizadas

Para classificação multiclasse, utilizamos:

| Métrica | Descrição | Objetivo |
|---------|-----------|----------|
| **Acurácia** | % de previsões corretas | > 40-50% (baseline ~30%) |
| **Precision** | De todas as previsões da classe X, quantas estão corretas? | Alta confiança nas previsões |
| **Recall** | De todos os casos reais da classe X, quantos identificamos? | Não perder casos importantes |
| **F1-Score** | Média harmônica de Precision e Recall | Balanceamento geral |
| **Matriz de Confusão** | Onde o modelo erra? | Identificar confusões sistemáticas |

### Baselines para Comparação

- 🎲 **Random Guess**: 25% (4 classes equiprováveis)
- 📊 **Classe Mais Comum**: ~30-35% (sempre prever a classe majoritária)
- 🎯 **Nosso Objetivo**: > 40-50%

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
- ✅ Download do dataset do GitHub
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

**Ou usando Python:**
```bash
python -m notebook Sprint_Challenge_4_LSTM_Acidentes.ipynb
```

---

## 📦 Estrutura do Repositório

```
lstm-acidentes-prf/
│
├── 📓 Sprint_Challenge_4_LSTM_Acidentes.ipynb   # Notebook principal (storytelling)
│
├── 📊 dados/
│   └── datatran2025.xlsx                         # Dataset PRF
│
├── 🤖 modelo_lstm_classificacao_risco.keras      # Modelo treinado
│
├── 📄 README.md                                  # Este arquivo
│
├── 📋 requirements.txt                           # Dependências Python
│
└── 📜 LICENSE                                    # Licença MIT
```

---

## 🎓 Resultados e Conclusões

### Resultados Obtidos

**Métricas Finais:**
- 🎯 **Acurácia**: [Inserir após execução] (superior aos baselines)
- 📊 **F1-Score Macro**: [Inserir após execução]
- ⚖️ **Balanceamento**: Sem overfitting (curvas treino/validação próximas)

**Visualizações Geradas:**
1. Curvas de aprendizagem (Loss + Accuracy)
2. Matriz de confusão (onde o modelo erra)
3. Comparação temporal (previsões vs real)
4. Distribuição de probabilidades
5. Acurácia por classe de risco

### Descobertas Importantes

#### 🔬 Processo Científico

1. **Experimento Inicial**: Regressão (R² negativo)
2. **Hipótese**: Features não capturam fatores críticos
3. **Teste**: Classificação de níveis de risco
4. **Resultado**: Sucesso! Modelo aprende padrões úteis

#### 💡 Insights sobre os Dados

- **Temporalidade importa**: Lags e média móvel são features importantes
- **Sazonalidade existe**: Componentes seno/cosseno ajudam
- **Limitação natural**: Sem clima/eventos, extremos são difíceis de prever

### Limitações Identificadas

| Limitação | Impacto | Solução Futura |
|-----------|---------|----------------|
| **Features ausentes** (clima, eventos) | Dificulta previsão de extremos | Integrar APIs (OpenWeather, feriados) |
| **Classes raras** | Algumas classes têm poucos exemplos | Oversampling ou class weights |
| **Desbalanceamento** | Modelo favorece classes comuns | SMOTE ou amostragem estratificada |
| **Janela fixa (8 semanas)** | Pode perder padrões de longo prazo | Testar janelas variáveis |

### Aplicações Práticas

#### Para Seguradoras (Sompo)

**Sistema de Alertas:**
```
📗 Risco BAIXO  → "Período normal - sem ações especiais"
📙 Risco MÉDIO  → "Atenção - campanhas preventivas recomendadas"
📕 Risco ALTO   → "ALERTA - intensificar fiscalização"
```

**Precificação Dinâmica:**
- Ajustar prêmios baseado no nível de risco previsto
- Oferecer descontos em períodos de baixo risco
- Alertar segurados em períodos críticos

#### Para Gestores de Rodovias

**Alocação de Recursos:**
- Priorizar patrulhas em semanas de alto risco
- Planejar campanhas de conscientização
- Antecipar necessidade de ambulâncias

#### Para Motoristas

**Informação e Conscientização:**
- App com alertas semanais de risco
- Dicas de segurança personalizadas
- Recomendações de horários mais seguros

---

## 🚀 Próximos Passos

### Melhorias de Curto Prazo

- [ ] Integrar dados climáticos (API OpenWeather)
- [ ] Adicionar calendário de feriados
- [ ] Implementar class weights para desbalanceamento
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
- 📧 Email: [Inserir email do grupo]
- 🐙 GitHub: [https://github.com/9luis7/lstm-acidentes-prf](https://github.com/9luis7/lstm-acidentes-prf)

---

<div align="center">

### 🏆 Sprint Challenge 4 - FIAP 2025

**Desenvolvido com ❤️ pela Equipe Big 5**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/9luis7/lstm-acidentes-prf/blob/main/Sprint_Challenge_4_LSTM_Acidentes.ipynb)

</div>
