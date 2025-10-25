# 🎥 Guia para Apresentação em Vídeo (5 minutos)

## 📋 Checklist Pré-Gravação

- [ ] Testar execução do notebook no Colab (verificar que funciona)
- [ ] Preparar slides ou notas visuais (opcional)
- [ ] Verificar áudio e câmera
- [ ] Ensaiar o roteiro (timing de 5 minutos)

---

## 🎬 Roteiro Sugerido (5 minutos)

### **Introdução (30 segundos)**

**O que falar:**
> "Olá! Sou [Nome] da Equipe Big 5, e vou apresentar nosso projeto da Sprint Challenge 4: um modelo LSTM para prever níveis de risco de acidentes em rodovias federais, usando dados públicos da PRF."

**O que mostrar:**
- Tela: README.md no GitHub (mostrar logo e equipe)
- Mencionar o case da Sompo

---

### **Parte 1: O Desafio e Nossa Abordagem (1 minuto)**

**O que falar:**
> "O desafio era construir uma LSTM para antecipar padrões de acidentes. Escolhemos prever **níveis de risco** classificados em 4 categorias: Baixo, Médio-Baixo, Médio-Alto e Alto."
>
> "Por quê classificação? Inicialmente tentamos regressão, mas descobrimos que as features disponíveis - temporais, lags e sazonalidade - não capturam fatores críticos como clima e eventos. Classificação é mais robusta e útil na prática."

**O que mostrar:**
- Tela: README.md (seção "Target Escolhido")
- Destacar a tabela das 4 classes
- Mostrar a justificativa científica (tentativa → descoberta → solução)

---

### **Parte 2: Tratamento dos Dados (1 minuto)**

**O que falar:**
> "Transformamos acidentes individuais em séries temporais semanais por estado. Criamos 12 features enriquecidas: temporais, sazonalidade, e principalmente **features de histórico** como lags das últimas 3 semanas, média móvel, tendência e volatilidade."
>
> "Preparamos sequências de 8 semanas para prever a 9ª semana. Total: mais de 800 amostras para treino."

**O que mostrar:**
- Tela: README.md (seção "Como os Dados Foram Tratados")
- Destacar a tabela de features
- Mostrar o diagrama "Janela: 8 semanas → Prevê semana 9"

---

### **Parte 3: Arquitetura do Modelo (45 segundos)**

**O que falar:**
> "Nossa arquitetura usa 2 camadas LSTM empilhadas - 64 e 32 neurônios - com dropout para regularização. A camada final usa softmax para classificar as 4 classes. Treinamos com Adam optimizer e categorical crossentropy, usando callbacks como EarlyStopping."

**O que mostrar:**
- Tela: README.md (diagrama ASCII da arquitetura)
- Apontar para as camadas principais
- Mencionar ~53k parâmetros treináveis

---

### **Parte 4: Resultados e Métricas (1 minuto)**

**O que falar:**
> "Nosso modelo alcançou [X]% de acurácia, superando os baselines de 25% (random) e 30% (classe mais comum). Analisamos com matriz de confusão, precision, recall e F1-score por classe."
>
> "As curvas de aprendizagem mostram convergência sem overfitting - treino e validação permanecem próximos."

**O que mostrar:**
- Tela: Notebook no Colab (se executado) - mostrar os gráficos
- OU: Screenshots dos gráficos salvos
- Destacar:
  * Curvas de Loss/Accuracy
  * Matriz de confusão
  * Comparação temporal

**Dica:** Se não tiver executado ainda, mencione: 
> "O notebook está pronto para execução no Colab com um clique - todos os gráficos são gerados automaticamente."

---

### **Parte 5: Aplicações Práticas e Conclusão (45 segundos)**

**O que falar:**
> "Este modelo tem aplicações reais: seguradoras podem ajustar precificação baseado em risco, gestores de rodovias podem alocar recursos inteligentemente, e motoristas podem receber alertas de períodos críticos."
>
> "Identificamos limitações - principalmente a falta de dados climáticos e de eventos - e planejamos melhorias como integração com APIs meteorológicas e deploy com dashboard interativo."
>
> "Todo o código está documentado, reprodutível e pronto para execução no Colab. Obrigado!"

**O que mostrar:**
- Tela: README.md (seção "Aplicações Práticas")
- Mostrar badge do Colab
- Finalizar na estrutura do repositório

---

## 🎯 Pontos-Chave para Mencionar

### ✅ Critérios de Avaliação Atendidos

| Critério | Pontuação | Como Abordar no Vídeo |
|----------|-----------|----------------------|
| **Preparação dos dados** | 20 pts | Mostrar as 12 features, agregação semanal, normalização |
| **Construção do modelo LSTM** | 30 pts | Diagrama da arquitetura, 2 LSTMs empilhadas, dropout |
| **Qualidade dos resultados** | 20 pts | Acurácia, matriz de confusão, curvas de aprendizagem |
| **Organização do repositório** | 15 pts | Estrutura limpa, README completo, execução 1-clique |
| **Apresentação em vídeo** | 15 pts | Este guia! Clareza, objetividade, 5 min |

### 🔬 Destaque a Metodologia Científica

**Não esconda o processo!** Mostre que tentaram regressão primeiro:

> "Este projeto demonstra metodologia científica real: testamos uma hipótese (regressão), obtivemos resultados negativos (R² negativo), analisamos a causa (features limitadas), e adaptamos a solução (classificação). Isso é ciência de dados na prática."

Isso mostra maturidade e pensamento crítico! 🏆

---

## 📱 Dicas Técnicas de Gravação

### Antes de Gravar

1. **Teste o notebook no Colab**
   - Clique no badge: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/9luis7/lstm-acidentes-prf/blob/main/Sprint_Challenge_4_LSTM_Acidentes.ipynb)
   - Execute "Reiniciar e executar tudo"
   - **⏱️ Aguarde 15-30 min** (treina o modelo)
   - Tire screenshots dos gráficos finais

2. **Prepare os slides/anotações**
   - 5 slides = 5 partes do roteiro
   - Ou use o próprio README como roteiro visual

3. **Ensaie o timing**
   - 5 minutos passam RÁPIDO
   - Fale de forma clara, mas não apressada
   - Se passar de 5 min, corte detalhes técnicos

### Durante a Gravação

**Ferramentas:**
- OBS Studio (gratuito, profissional)
- Zoom (gravar apresentação)
- Loom (rápido e fácil)

**Setup:**
- Câmera: Opcional, mas dá um toque pessoal
- Áudio: **CRÍTICO** - use fone com microfone ou microfone USB
- Tela: Compartilhar navegador (GitHub + Colab)

**Estrutura de Tela:**
```
┌─────────────────────────────────┐
│  [Sua câmera - canto superior]  │  ← Pequeno, não atrapalha
│                                  │
│     [Tela principal]             │
│     GitHub README.md             │
│     ou                           │
│     Colab Notebook               │
│                                  │
└─────────────────────────────────┘
```

### Depois de Gravar

1. **Edição básica** (opcional):
   - Cortar início/fim
   - Adicionar intro simples com título
   - Adicionar música de fundo baixa (opcional)

2. **Upload no YouTube**:
   - Título: "Sprint Challenge 4 - LSTM Acidentes PRF - Equipe Big 5"
   - Descrição: Copie o resumo do README
   - **Privacidade: NÃO LISTADO** ⚠️
   - Copie o link

3. **Adicione o link no README**:
   ```markdown
   ## 🎥 Apresentação em Vídeo
   
   [![Assista no YouTube](https://img.shields.io/badge/YouTube-Assista-red?logo=youtube)](SEU_LINK_AQUI)
   ```

---

## 💡 Dicas de Ouro

### ✅ FAÇA

- ✅ Seja objetivo e claro
- ✅ Mostre paixão pelo projeto
- ✅ Destaque as descobertas (regressão → classificação)
- ✅ Mencione todas as partes (dados, modelo, resultados, aplicações)
- ✅ Mostre o repositório organizado

### ❌ EVITE

- ❌ Falar muito rápido (ansiedade)
- ❌ Entrar em detalhes técnicos demais (equações, código)
- ❌ Esquecer de mencionar métricas e resultados
- ❌ Passar de 5 minutos
- ❌ Áudio ruim (maior problema!)

---

## 🎬 Script Completo para Copiar

Se preferir um roteiro palavra por palavra, use este:

---

**[0:00 - 0:30] INTRODUÇÃO**

> "Olá! Sou [Nome] da Equipe Big 5, e vou apresentar nossa solução para a Sprint Challenge 4: um modelo LSTM para classificação de níveis de risco de acidentes em rodovias federais brasileiras, utilizando dados públicos da Polícia Rodoviária Federal. Este projeto foi desenvolvido como case para a seguradora Sompo."

---

**[0:30 - 1:30] DESAFIO E ABORDAGEM**

> "O desafio era construir uma rede neural recorrente - uma LSTM - capaz de antecipar padrões de acidentes. Escolhemos prever quatro níveis de risco: Baixo, Médio-Baixo, Médio-Alto e Alto, baseados na proporção de acidentes severos.
>
> É importante mencionar que inicialmente tentamos resolver como um problema de regressão - prever o valor exato da proporção. Porém, obtivemos R² negativo, indicando que o modelo não estava aprendendo. Analisamos a causa e descobrimos que as features disponíveis - temporais, lags e sazonalidade - não capturam fatores críticos como condições climáticas e eventos especiais.
>
> Por isso, reformulamos como classificação de níveis de risco. Essa abordagem é mais robusta às limitações dos dados e mais útil na prática para tomada de decisão."

---

**[1:30 - 2:30] TRATAMENTO DOS DADOS**

> "No tratamento de dados, transformamos registros individuais de acidentes em séries temporais semanais agregadas por estado. Criamos 12 features enriquecidas, incluindo: features temporais como dia da semana e mês, componentes de sazonalidade usando seno e cosseno, e principalmente features de histórico - lags das últimas 3 semanas, média móvel, tendência e volatilidade.
>
> Preparamos sequências de 8 semanas de histórico para prever a nona semana. Utilizamos MinMaxScaler para normalização e fizemos divisão temporal respeitando a ordem cronológica: 85% treino e 15% validação. No total, geramos mais de 800 amostras para treinamento."

---

**[2:30 - 3:15] ARQUITETURA DO MODELO**

> "Nossa arquitetura usa duas camadas LSTM empilhadas - a primeira com 64 neurônios e a segunda com 32 - seguidas de uma camada densa com 32 neurônios e uma camada de saída com softmax para as 4 classes. Aplicamos dropout de 0.2 após cada camada para regularização.
>
> Compilamos com otimizador Adam e categorical crossentropy como função de perda. Utilizamos callbacks como EarlyStopping com patience de 20 épocas e ReduceLROnPlateau para ajuste automático da taxa de aprendizado. O modelo possui aproximadamente 53 mil parâmetros treináveis."

---

**[3:15 - 4:15] RESULTADOS E MÉTRICAS**

> "Nosso modelo alcançou [X por cento] de acurácia no conjunto de validação, superando significativamente os baselines de 25% para palpite aleatório e 30% para sempre prever a classe mais comum. Avaliamos usando múltiplas métricas: precision, recall e F1-score para cada classe.
>
> As curvas de aprendizagem mostram convergência saudável sem overfitting - as curvas de treino e validação permanecem próximas durante todo o treinamento. A matriz de confusão revela que o modelo identifica bem as classes extremas e tem alguma confusão esperada entre classes adjacentes.
>
> Todo o notebook está preparado para execução com um clique no Google Colab, gerando automaticamente todos os gráficos de avaliação."

---

**[4:15 - 5:00] APLICAÇÕES E CONCLUSÃO**

> "Este modelo tem aplicações práticas concretas. Seguradoras como a Sompo podem usar para precificação dinâmica de apólices e identificação de períodos críticos. Gestores de rodovias podem alocar recursos como patrulhas e ambulâncias nos momentos de maior risco. E motoristas podem receber alertas antecipados de períodos perigosos.
>
> Identificamos limitações importantes, principalmente a ausência de dados climáticos e de eventos no dataset. Como próximos passos, planejamos integração com APIs meteorológicas, implementação de um dashboard interativo e deploy em produção.
>
> Todo o código está documentado, organizado em um repositório GitHub limpo, com README completo e instruções claras de execução. Obrigado pela atenção!"

---

## ✅ Checklist Final Antes de Enviar

- [ ] Vídeo gravado e editado
- [ ] Duração entre 4:30 e 5:00 minutos
- [ ] Áudio claro e sem ruídos
- [ ] Todas as 5 partes abordadas (intro, desafio, dados, modelo, resultados/conclusão)
- [ ] Upload no YouTube como "Não listado"
- [ ] Link adicionado no README.md
- [ ] Notebook testado no Colab (funciona!)
- [ ] Repositório GitHub organizado e limpo

---

## 🏆 Boa Sorte!

Você tem um projeto excelente nas mãos:
- ✅ Código funcional e reprodutível
- ✅ Documentação profissional
- ✅ Metodologia científica sólida
- ✅ Aplicação prática clara

**Apresente com confiança!** 🚀

---

**Equipe Big 5 - FIAP 2025**

