# Sprint Challenge 4 – Previsão de Acidentes com LSTMs (Case Sompo)

**Integrantes Big 5:**
- Lucca Phelipe Masini RM 564121
- Luiz Henrique Poss RM562177
- Luis Fernando de Oliveira Salgado RM 561401
- Igor Paixão Sarak RM 563726
- Bernardo Braga Perobeli RM 562468

---

## 1. Objetivo do Projeto
Desenvolver e treinar uma Rede Neural Recorrente (LSTM) para prever padrões de acidentes nas rodovias federais, utilizando a base de dados pública da PRF. O modelo visa apoiar decisões estratégicas de prevenção e análise de riscos.

---

## 2. Instruções Claras de Execução

A forma mais simples de executar este projeto é através do Google Colab:

1.  **[Clique aqui para abrir o Notebook no Google Colab](https://colab.research.google.com/github/SEU_USUARIO/SEU_REPO/blob/main/Sprint_4_LSTM_Grupo_BIG5.ipynb)** *(**Atenção:** Substitua `SEU_USUARIO/SEU_REPO` pela URL do seu repositório)*

2.  Com o notebook aberto, clique no menu **"Ambiente de execução"**.
3.  Clique em **"Executar tudo"**.

O notebook irá instalar as dependências, baixar o dataset do Google Drive, tratar os dados, treinar o modelo e gerar os gráficos de avaliação automaticamente.

---

## 3. Relatório Curto do Projeto

### Qual foi o target escolhido e por quê?

O target escolhido foi uma variável binária chamada `severo`. 
-   Ela recebe o valor `1` se o acidente envolveu `mortos > 0` ou `feridos_graves > 0`.
-   Ela recebe o valor `0` para todos os outros casos (apenas feridos leves ou ilesos).

A justificativa é focar os esforços de previsão nos acidentes de maior impacto humano e social, que são o principal ponto de preocupação para estratégias de prevenção e para o mercado de seguros.

### Como os dados foram tratados?

O tratamento foi feito em 3 etapas principais:
1.  **Limpeza:** Carregamos o dataset (`.xlsx`), ajustamos tipos de dados (como `horario`) e criamos a coluna alvo `severo`.
2.  **Agregação:** Transformamos os dados de registros individuais em uma série temporal. Agrupamos os acidentes por **semana** e por **estado (UF)**, calculando a `prop_severos` (proporção de acidentes severos) para cada período.
3.  **Sequenciamento:** Para a LSTM, filtramos os dados para os estados principais (SP, MG, RJ, PR, RS, BA, CE, GO, PE, SC) e criamos "janelas" de dados. O modelo usa os dados de 4 semanas (`X`) para prever a proporção da semana seguinte (`y`).

### Arquitetura do modelo LSTM

Utilizamos uma arquitetura de LSTM "empilhada" (stacked), ideal para capturar padrões temporais:
1.  **Camada LSTM** (`units=50`, `return_sequences=True`) - Lê a sequência de entrada.
2.  **Dropout** (`0.2`) - Regularização para evitar overfitting.
3.  **Camada LSTM** (`units=50`) - Processa a sequência da camada anterior.
4.  **Dropout** (`0.2`) - Mais regularização.
5.  **Camada Densa** (`units=1`) - A camada de saída, que prevê o valor final (a proporção de 0 a 1).

O modelo foi compilado com o otimizador `adam` (learning rate 0.001) e a função de perda `mean_squared_error`.

### Métricas utilizadas para avaliação

Utilizamos duas métricas principais para avaliar o modelo nos dados de validação:
1.  **Loss (Mean Squared Error):** Usada pelo modelo durante o treino. O gráfico de Loss vs. Val_Loss mostrou que o modelo aprendeu e o `EarlyStopping` funcionou corretamente.
2.  **Erro Médio Absoluto (MAE):** Métrica principal para interpretação humana. O modelo obteve um **MAE** que indica a precisão das previsões em pontos percentuais.

Isso significa que, em média, a previsão do modelo sobre a proporção de acidentes severos tem um erro baixo, demonstrando boa capacidade de generalização.

### Features Utilizadas

O modelo utiliza 6 features principais:
1. **Proporção de Acidentes Severos** (target)
2. **Média de Pessoas por Acidente**
3. **Média de Veículos por Acidente**
4. **Identificação de Fim de Semana** (binária)
5. **Sazonalidade Seno** (padrões anuais)
6. **Sazonalidade Cosseno** (padrões anuais)

### Estados Incluídos

O modelo foi treinado com dados de 10 estados brasileiros:
- SP, MG, RJ, PR, RS, BA, CE, GO, PE, SC

Essa diversidade geográfica garante que o modelo possa generalizar bem para diferentes regiões do país.

### Janela Temporal

Utilizamos uma janela de **4 semanas** para prever a semana seguinte. Isso fornece contexto histórico suficiente para capturar padrões temporais sem tornar o modelo excessivamente complexo.

---

## 4. Tecnologias Utilizadas

- **Python 3.8+**
- **TensorFlow/Keras** - Deep Learning
- **Pandas** - Manipulação de dados
- **NumPy** - Computação numérica
- **Matplotlib/Seaborn** - Visualização
- **Scikit-learn** - Pré-processamento e métricas
- **Google Colab** - Ambiente de execução

---

## 5. Estrutura do Projeto

```
├── Sprint_4_LSTM_Grupo_BIG5.ipynb  # Notebook principal
├── modelo_lstm_acidentes_sp.keras   # Modelo treinado (gerado após execução)
├── README.md                        # Este arquivo
├── INSTRUCOES_FINAL.md             # Instruções detalhadas
├── requirements.txt                 # Dependências
└── dados/
    └── datatran2025.xlsx           # Dataset original
```

---

## 6. Próximos Passos

1. **Expandir o Dataset:** Incorporar mais estados e períodos históricos
2. **Features Adicionais:** Adicionar condições climáticas, dados de tráfego
3. **Otimização:** Grid search para encontrar melhores hiperparâmetros
4. **Deploy:** Implementar em produção para uso em tempo real
5. **Monitoramento:** Sistema de monitoramento contínuo da performance

---

**Desenvolvido com ❤️ pela equipe Big 5**

*Sprint Challenge 4 - Previsão de Acidentes com LSTMs (Case Sompo)*
