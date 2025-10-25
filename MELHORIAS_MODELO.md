# 🎯 Análise Crítica e Melhorias Propostas para o Modelo LSTM

## 📊 Diagnóstico do Problema Atual

### ❌ Sintomas Identificados:

1. **Previsões constantes (~0.27)** - O modelo está prevendo sempre a média
2. **Alta variabilidade não capturada** - Valores reais variam 0.1-0.4, previsões ficam em 0.26-0.28
3. **UNDERFITTING** - Não há overfitting, mas o modelo não aprende padrões complexos

### 🔍 Causas Prováveis:

1. **Janela temporal muito curta** (4 semanas) - Pouco contexto histórico
2. **Modelo muito simples** (50 neurônios) - Baixa capacidade de aprendizado
3. **Poucas amostras** (~50 semanas) - Dados insuficientes para treinamento robusto
4. **Features limitadas** (6 features) - Falta informação contextual

---

## 🛠️ Melhorias Propostas (Por Prioridade)

### ⭐ **Prioridade 1: Aumentar Janela Temporal**

**Atual:** 4 semanas → **Proposta:** 8-12 semanas

**Por quê:**
- Acidentes têm padrões sazonais e mensais
- Mais contexto = melhor compreensão de tendências
- **Risco de overfitting: BAIXO** (apenas mais contexto, não mais parâmetros)

**Mudança no código:**
```python
# ANTES:
n_passos_para_tras = 4  # 4 semanas de contexto

# DEPOIS:
n_passos_para_tras = 8  # 8 semanas de contexto
```

**Impacto esperado:** +15-20% de melhoria

---

### ⭐ **Prioridade 2: Adicionar Features de Lag (Histórico)**

**Atual:** 6 features → **Proposta:** 10-12 features

**Adicionar:**
```python
# Features de lag (histórico das últimas semanas)
weekly_df['prop_severos_lag1'] = weekly_df.groupby('uf')['prop_severos'].shift(1)
weekly_df['prop_severos_lag2'] = weekly_df.groupby('uf')['prop_severos'].shift(2)
weekly_df['prop_severos_lag3'] = weekly_df.groupby('uf')['prop_severos'].shift(3)

# Média móvel
weekly_df['prop_severos_ma3'] = weekly_df.groupby('uf')['prop_severos'].rolling(3).mean().reset_index(0, drop=True)

# Tendência
weekly_df['prop_severos_tendencia'] = weekly_df.groupby('uf')['prop_severos'].diff()

# Volatilidade
weekly_df['prop_severos_volatilidade'] = weekly_df.groupby('uf')['prop_severos'].rolling(3).std().reset_index(0, drop=True)
```

**Impacto esperado:** +20-25% de melhoria
**Risco de overfitting: BAIXO** (features derivadas dos dados reais)

---

### ⭐ **Prioridade 3: Aumentar Capacidade do Modelo**

**Atual:** 2 camadas LSTM (50, 50) → **Proposta:** 3 camadas LSTM (64, 32, 16)

```python
# MODELO MELHORADO
model = Sequential()

# Primeira camada LSTM (aumentar neurônios)
model.add(LSTM(units=64, return_sequences=True, input_shape=(n_passos_para_tras, n_features)))
model.add(Dropout(0.2))

# Segunda camada LSTM
model.add(LSTM(units=32, return_sequences=True))
model.add(Dropout(0.2))

# Terceira camada LSTM (adicional)
model.add(LSTM(units=16))
model.add(Dropout(0.2))

# Camada densa intermediária
model.add(Dense(units=8, activation='relu'))
model.add(Dropout(0.2))

# Camada de saída
model.add(Dense(units=1, activation='linear'))
```

**Impacto esperado:** +10-15% de melhoria
**Risco de overfitting: MÉDIO** (mais parâmetros, mas com Dropout adequado)

---

### 🔸 **Prioridade 4: Ajustar Hiperparâmetros**

**Learning Rate mais baixo:**
```python
# ANTES:
optimizer = Adam(learning_rate=0.001)

# DEPOIS:
optimizer = Adam(learning_rate=0.0005)  # Mais conservador
```

**Early Stopping menos restritivo:**
```python
# ANTES:
early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# DEPOIS:
early_stop = EarlyStopping(
    monitor='val_loss', 
    patience=15,  # Mais paciência
    min_delta=0.001,  # Mudança mínima significativa
    restore_best_weights=True
)
```

**Mais épocas:**
```python
# ANTES:
history = model.fit(..., epochs=100, ...)

# DEPOIS:
history = model.fit(..., epochs=150, ...)  # Mais tempo para aprender
```

**Impacto esperado:** +5-10% de melhoria
**Risco de overfitting: BAIXO** (com early stopping adequado)

---

### 🔸 **Prioridade 5: Usar Todos os Dados (Não Filtrar Estados)**

**Atual:** Filtra 10 estados → **Proposta:** Usar TODOS os estados

```python
# REMOVER esta linha:
# df_multi_estados = weekly_df[weekly_df['uf'].isin(estados_principais)].copy()

# USAR:
df_multi_estados = weekly_df.copy()  # Todos os estados
```

**Por quê:**
- Mais amostras = melhor generalização
- Diversidade geográfica = padrões mais ricos

**Impacto esperado:** +10-15% de melhoria
**Risco de overfitting: BAIXO** (mais dados é sempre melhor)

---

## 📈 Plano de Implementação Gradual

### Fase 1: Mudanças Seguras (Baixo Risco)
1. ✅ Aumentar janela temporal para 8 semanas
2. ✅ Adicionar features de lag
3. ✅ Usar todos os estados

**Resultado esperado:** MAE de ~0.12 → ~0.08 (33% de melhoria)

### Fase 2: Ajustes de Modelo (Risco Controlado)
4. ✅ Aumentar capacidade do modelo (3 camadas)
5. ✅ Ajustar hiperparâmetros

**Resultado esperado:** MAE de ~0.08 → ~0.06 (50% de melhoria total)

---

## ⚠️ Sinais de Alerta para Overfitting

Monitore estes indicadores:

### ❌ OVERFITTING se:
- Loss de validação **SOBE** enquanto loss de treino continua caindo
- Gap entre loss de treino e validação **AUMENTA** (>50%)
- MAE de validação >> MAE de treino

### ✅ BOA PERFORMANCE se:
- Loss de treino e validação caem juntos
- Gap pequeno (<20%)
- Previsões capturam variabilidade dos dados reais

---

## 🎯 Métricas Alvo

| Métrica | Atual | Meta Realista | Meta Otimista |
|---------|-------|---------------|---------------|
| MAE | 0.12-0.13 | 0.08-0.09 | 0.06-0.07 |
| R² | ~0.10-0.20 | 0.50-0.60 | 0.70-0.80 |
| Variabilidade Capturada | 10-15% | 50-60% | 70-80% |

---

## 🔄 Próximos Passos

1. **Implementar melhorias da Fase 1** (seguras)
2. **Treinar e avaliar**
3. **Se resultados melhorarem:** Implementar Fase 2
4. **Se overfitting aparecer:** Reverter mudanças

---

## 📝 Notas Importantes

### Por que NÃO é overfitting atual:
- Loss de treino e validação estão **próximos**
- MAE de treino e validação são **similares**
- Problema é **underfitting** (modelo muito simples)

### Como evitar overfitting ao melhorar:
- ✅ Manter Dropout (0.2-0.3)
- ✅ Usar Early Stopping
- ✅ Mais dados (todos os estados)
- ✅ Validação adequada (85/15 split temporal)
- ✅ Monitorar Loss de validação

---

**Desenvolvido pela equipe Big 5**

*Última atualização: 25/10/2025*

