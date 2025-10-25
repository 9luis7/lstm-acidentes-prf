# Script Python para converter em notebook
# Este é um notebook completo de CLASSIFICAÇÃO

# CÉLULA 0 - Markdown
"""
# 🚗 Sprint Challenge 4 – Previsão de Acidentes com LSTMs
## Case Sompo: Antecipando Padrões de Risco em Rodovias Brasileiras

---

**Equipe Big 5**
- Lucca Phelipe Masini - RM 564121
- Luiz Henrique Poss - RM 562177
- Luis Fernando de Oliveira Salgado - RM 561401
- Igor Paixão Sarak - RM 563726
- Bernardo Braga Perobeli - RM 562468

---

## 🎯 Target Escolhido: Classificação de 4 Níveis de Risco

- **Classe 0 - BAIXO**: < 20% de acidentes severos
- **Classe 1 - MÉDIO-BAIXO**: 20-30% de acidentes severos
- **Classe 2 - MÉDIO-ALTO**: 30-40% de acidentes severos
- **Classe 3 - ALTO**: ≥ 40% de acidentes severos

Inicialmente tentamos regressão, mas obtivemos R² negativo. Identificamos que as features disponíveis não capturam fatores críticos (clima, eventos), então reformulamos como classificação - mais robusta e útil na prática.
"""

# CÉLULA 1 - Instalação
"""
!pip install openpyxl --quiet
print("✅ Bibliotecas instaladas!")
"""

# CÉLULA 2 - Importações
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import urllib.request
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("📚 Bibliotecas importadas!")
"""

# CÉLULA 3 - Carregamento de Dados
"""
print("📥 Baixando dataset...")

github_raw_url = 'https://raw.githubusercontent.com/9luis7/lstm-acidentes-prf/main/dados/datatran2025.xlsx'
output_filename = 'dados_acidentes.xlsx'

try:
    urllib.request.urlretrieve(github_raw_url, output_filename)
    df = pd.read_excel(output_filename)
    print(f"✅ Dataset carregado: {len(df):,} acidentes")
    print(f"\\n📊 Informações do Dataset:")
    df.info()
except Exception as e:
    print(f"❌ Erro: {e}")
    raise
"""

# CÉLULA 4 - Pré-processamento
"""
print("🎯 Criando variável target...")

df['horario'] = pd.to_datetime(df['horario'], format='%H:%M:%S', errors='coerce').dt.time
df['severo'] = ((df['mortos'] > 0) | (df['feridos_graves'] > 0)).astype(int)

colunas_relevantes = ['data_inversa', 'horario', 'uf', 'br', 'km', 'pessoas', 'veiculos', 'severo']
df_limpo = df[colunas_relevantes].copy()
df_limpo['horario'].fillna(pd.to_datetime('12:00:00').time(), inplace=True)

print("✅ Variável 'severo' criada!")
print(f"\\n📊 Distribuição:")
print(df_limpo['severo'].value_counts(normalize=True))
"""

# CÉLULA 5 - Agregação Semanal
"""
print("🔄 Agregando dados em séries temporais semanais...")

df_indexed = df_limpo.set_index('data_inversa')

weekly_df = df_indexed.groupby([pd.Grouper(freq='W'), 'uf']).agg(
    total_acidentes=('severo', 'count'),
    acidentes_severos=('severo', 'sum'),
    pessoas_total=('pessoas', 'sum'),
    veiculos_total=('veiculos', 'sum'),
    pessoas_media=('pessoas', 'mean'),
    veiculos_media=('veiculos', 'mean')
).reset_index()

weekly_df['prop_severos'] = np.where(
    weekly_df['total_acidentes'] > 0,
    weekly_df['acidentes_severos'] / weekly_df['total_acidentes'],
    0
)

print(f"✅ Dados agregados: {len(weekly_df):,} semanas × estados")
"""

# CÉLULA 6 - Feature Engineering
"""
print("🎨 Criando features temporais e de histórico...")

weekly_df['dia_semana'] = weekly_df['data_inversa'].dt.dayofweek
weekly_df['mes'] = weekly_df['data_inversa'].dt.month
weekly_df['fim_semana'] = weekly_df['dia_semana'].isin([5, 6]).astype(int)

weekly_df['sazonalidade_sen'] = np.sin(2 * np.pi * weekly_df['data_inversa'].dt.dayofyear / 365)
weekly_df['sazonalidade_cos'] = np.cos(2 * np.pi * weekly_df['data_inversa'].dt.dayofyear / 365)

for lag in [1, 2, 3]:
    weekly_df[f'prop_severos_lag{lag}'] = weekly_df.groupby('uf')['prop_severos'].shift(lag)

weekly_df['prop_severos_ma3'] = weekly_df.groupby('uf')['prop_severos'].rolling(3).mean().reset_index(0, drop=True)
weekly_df['prop_severos_tendencia'] = weekly_df.groupby('uf')['prop_severos'].diff()
weekly_df['prop_severos_volatilidade'] = weekly_df.groupby('uf')['prop_severos'].rolling(3).std().reset_index(0, drop=True)

print("✅ Features criadas!")
"""

# CÉLULA 7 - Criação de Sequências
"""
from sklearn.preprocessing import MinMaxScaler

print("🔢 Preparando sequências para LSTM...")

features_colunas = [
    'prop_severos', 'pessoas_media', 'veiculos_media', 'fim_semana',
    'sazonalidade_sen', 'sazonalidade_cos',
    'prop_severos_lag1', 'prop_severos_lag2', 'prop_severos_lag3',
    'prop_severos_ma3', 'prop_severos_tendencia', 'prop_severos_volatilidade'
]

df_features = weekly_df.set_index('data_inversa').sort_index()
df_features = df_features[features_colunas].copy()
df_features = df_features.dropna()

scaler = MinMaxScaler(feature_range=(0, 1))
dados_scaled = scaler.fit_transform(df_features.values)

n_passos_para_tras = 8
n_features = len(features_colunas)

X, y = [], []
for i in range(n_passos_para_tras, len(dados_scaled)):
    X.append(dados_scaled[i-n_passos_para_tras:i, :])
    y.append(dados_scaled[i, 0])

X, y = np.array(X), np.array(y)

print(f"✅ Sequências criadas!")
print(f"   Shape X: {X.shape}")
print(f"   Shape y: {y.shape}")
"""

# CÉLULA 8 - Criação de Classes
"""
from tensorflow.keras.utils import to_categorical

print("🎯 Transformando para CLASSIFICAÇÃO...")

def criar_classes_risco(y_data):
    classes = np.zeros_like(y_data, dtype=int)
    classes[y_data < 0.20] = 0
    classes[(y_data >= 0.20) & (y_data < 0.30)] = 1
    classes[(y_data >= 0.30) & (y_data < 0.40)] = 2
    classes[y_data >= 0.40] = 3
    return classes

split_index = int(len(X) * 0.85)
X_train, X_val = X[:split_index], X[split_index:]
y_train, y_val = y[:split_index], y[split_index:]

y_train_classes = criar_classes_risco(y_train)
y_val_classes = criar_classes_risco(y_val)

y_train_categorical = to_categorical(y_train_classes, num_classes=4)
y_val_categorical = to_categorical(y_val_classes, num_classes=4)

nomes_classes = ['BAIXO (<0.20)', 'MÉDIO-BAIXO (0.20-0.30)', 
                 'MÉDIO-ALTO (0.30-0.40)', 'ALTO (≥0.40)']

print("\\n📊 Distribuição no TREINO:")
for i in range(4):
    count = (y_train_classes == i).sum()
    print(f"   Classe {i}: {count:4d}")

print("\\n📊 Distribuição na VALIDAÇÃO:")
for i in range(4):
    count = (y_val_classes == i).sum()
    print(f"   Classe {i}: {count:4d}")

print("\\n✅ Dados preparados!")
"""

# CÉLULA 9 - Construção do Modelo
"""
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam

print("🏗️  Construindo modelo de CLASSIFICAÇÃO...")

model = Sequential([
    LSTM(units=64, return_sequences=True, input_shape=(n_passos_para_tras, n_features)),
    Dropout(0.2),
    LSTM(units=32, return_sequences=False),
    Dropout(0.2),
    Dense(units=32, activation='relu'),
    Dropout(0.2),
    Dense(units=4, activation='softmax')
])

optimizer = Adam(learning_rate=0.001)
model.compile(
    optimizer=optimizer,
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("✅ Modelo construído!")
model.summary()

early_stop = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True, verbose=1)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, min_lr=0.00001, verbose=1)

print("\\n✅ Callbacks configurados!")
"""

# CÉLULA 10 - Treinamento
"""
print("\\n" + "="*70)
print("🚀 TREINANDO MODELO")
print("="*70)
print("\\n⏱️  Aguarde 15-30 minutos...\\n")

history = model.fit(
    X_train, y_train_categorical,
    epochs=100,
    batch_size=16,
    validation_data=(X_val, y_val_categorical),
    callbacks=[early_stop, reduce_lr],
    verbose=1
)

print("\\n" + "="*70)
print("✅ TREINAMENTO CONCLUÍDO!")
print("="*70)
"""

# CÉLULA 11 - Avaliação
"""
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

print("📊 Avaliando modelo...")

y_pred_proba = model.predict(X_val, verbose=0)
y_pred_classes = np.argmax(y_pred_proba, axis=1)

accuracy = accuracy_score(y_val_classes, y_pred_classes)

print("\\n" + "="*70)
print("🎯 RESULTADOS FINAIS")
print("="*70)
print(f"\\n🏆 ACURÁCIA: {accuracy:.2%}\\n")

baseline_random = 0.25
baseline_majority = np.bincount(y_val_classes).max() / len(y_val_classes)

print("📊 Comparação com Baselines:")
print(f"   Random: {baseline_random:.1%}")
print(f"   Classe mais comum: {baseline_majority:.1%}")
print(f"   Nosso modelo: {accuracy:.1%} ✅")

print("\\n" + "="*70)
print("📊 RELATÓRIO POR CLASSE")
print("="*70 + "\\n")
print(classification_report(y_val_classes, y_pred_classes, target_names=nomes_classes, digits=3))
"""

# CÉLULA 12 - Visualizações
"""
plt.figure(figsize=(16, 12))

plt.subplot(3, 2, 1)
plt.plot(history.history['loss'], label='Treino', color='blue', linewidth=2)
plt.plot(history.history['val_loss'], label='Validação', color='red', linewidth=2)
plt.title('Curvas de Aprendizagem - Loss', fontsize=14, fontweight='bold')
plt.xlabel('Épocas')
plt.ylabel('Loss')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(3, 2, 2)
plt.plot(history.history['accuracy'], label='Treino', color='blue', linewidth=2)
plt.plot(history.history['val_accuracy'], label='Validação', color='red', linewidth=2)
plt.title('Curvas de Aprendizagem - Acurácia', fontsize=14, fontweight='bold')
plt.xlabel('Épocas')
plt.ylabel('Acurácia')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(3, 2, 3)
cm = confusion_matrix(y_val_classes, y_pred_classes)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Matriz de Confusão', fontsize=14, fontweight='bold')
plt.ylabel('Real')
plt.xlabel('Previsto')
plt.xticks([0.5, 1.5, 2.5, 3.5], ['Baixo', 'Médio-Baixo', 'Médio-Alto', 'Alto'], rotation=0)
plt.yticks([0.5, 1.5, 2.5, 3.5], ['Baixo', 'Médio-Baixo', 'Médio-Alto', 'Alto'], rotation=0)

plt.subplot(3, 2, 4)
plt.plot(y_val_classes, label='Real', marker='o', linewidth=2, markersize=5, alpha=0.7)
plt.plot(y_pred_classes, label='Previsto', marker='x', linestyle='--', linewidth=2, markersize=5, alpha=0.7)
plt.title('Comparação Temporal', fontsize=14, fontweight='bold')
plt.xlabel('Amostras')
plt.ylabel('Classe')
plt.yticks([0, 1, 2, 3], ['Baixo', 'Médio-Baixo', 'Médio-Alto', 'Alto'])
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(3, 2, 5)
for i in range(4):
    plt.hist(y_pred_proba[:, i], bins=20, alpha=0.6, label=f'Classe {i}', edgecolor='black')
plt.title('Distribuição de Probabilidades', fontsize=14, fontweight='bold')
plt.xlabel('Probabilidade')
plt.ylabel('Frequência')
plt.legend()
plt.grid(True, alpha=0.3)

plt.subplot(3, 2, 6)
acertos_por_classe = []
for i in range(4):
    mask = (y_val_classes == i)
    if mask.sum() > 0:
        acertos = (y_pred_classes[mask] == i).sum() / mask.sum() * 100
        acertos_por_classe.append(acertos)
    else:
        acertos_por_classe.append(0)

colors = ['green' if acc > 50 else 'orange' if acc > 30 else 'red' for acc in acertos_por_classe]
bars = plt.bar(['Baixo', 'Médio-Baixo', 'Médio-Alto', 'Alto'], acertos_por_classe, color=colors, edgecolor='black')
plt.title('Acurácia por Classe', fontsize=14, fontweight='bold')
plt.ylabel('Acurácia (%)')
plt.ylim(0, 100)
plt.grid(True, alpha=0.3, axis='y')

for bar, acc in zip(bars, acertos_por_classe):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height, f'{acc:.1f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()

print("\\n✅ Visualizações geradas!")
"""

# CÉLULA 13 - Salvar Modelo
"""
model_filename = 'modelo_lstm_classificacao_risco.keras'
model.save(model_filename)
print(f"💾 Modelo salvo: '{model_filename}'")
print("\\n✅ Projeto concluído!")
"""

print("Notebook completo criado!")

