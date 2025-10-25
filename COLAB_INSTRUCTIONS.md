# 🚀 Como Executar o Notebook no Google Colab

## Link Direto (Recomendado)

Clique no link abaixo para abrir o notebook diretamente no Google Colab:

👉 **[Abrir no Google Colab](https://colab.research.google.com/github/9luis7/lstm-acidentes-prf/blob/main/Sprint_4_LSTM_Grupo_BIG5.ipynb)**

---

## Passos Alternativos (Se o link acima não funcionar)

### 1️⃣ Acessar o Google Colab
- Abra: https://colab.research.google.com/

### 2️⃣ Fazer Upload do Notebook
- Clique em **"Arquivo"** → **"Fazer upload do notebook"**
- Selecione o arquivo `Sprint_4_LSTM_Grupo_BIG5.ipynb`

### 3️⃣ Executar o Notebook
- Clique em **"Ambiente de execução"** → **"Reiniciar e executar tudo"**
- **OU** execute célula por célula com Ctrl+Enter

---

## ✅ Verificação

### O notebook carregará corretamente se:
- ✅ A Célula 2 executar sem erro
- ✅ Ver mensagem: `✅ Arquivo 'dados_acidentes.xlsx' baixado com sucesso do GitHub!`
- ✅ Os dados forem exibidos corretamente

### Se receber erro 404:
1. Verifique se o repositório é **público** no GitHub
2. Verifique se o arquivo existe em: `dados/datatran2025.xlsx`
3. Atualize a variável `github_raw_url` na Célula 2 com o link correto

---

## 📊 O que Esperar

Após executar completamente, você terá:

1. **Dados carregados** - 47.192 registros de acidentes
2. **Variáveis processadas** - Limpeza e engenharia de features
3. **Séries temporais** - Agregação semanal por estado
4. **Sequências LSTM** - Janelas de 4 semanas
5. **Modelo treinado** - LSTM com 2 camadas
6. **Gráficos de avaliação:**
   - Curvas de Loss (treino vs validação)
   - Curvas de MAE (treino vs validação)
   - Previsões vs Valores Reais
   - Gráfico de Resíduos

7. **Modelo salvo** - `modelo_lstm_acidentes_sp.keras`

---

## 💾 Download dos Arquivos

Após treinar, faça download:

1. **Modelo:**
   - Clique no ícone de pasta à esquerda
   - Encontre `modelo_lstm_acidentes_sp.keras`
   - Clique com botão direito → "Fazer download"

2. **Notebook:**
   - "Arquivo" → "Fazer download" → "Fazer download do .ipynb"

---

## ⏱️ Tempo de Execução

- **Total:** ~15-30 minutos (dependendo do GPU disponível)
- Carregamento de dados: ~2 min
- Pré-processamento: ~2 min
- Agregação: ~1 min
- Sequências: ~1 min
- **Treinamento do modelo: ~8-20 min** (varia com GPU)
- Avaliação: ~2 min

---

## 🆘 Troubleshooting

### Erro: "HTTP Error 404: Not Found"
**Solução:** Atualize o link `github_raw_url` na Célula 2 com o link Raw correto do seu repositório

### Erro: "ModuleNotFoundError"
**Solução:** As bibliotecas serão instaladas automaticamente na Célula 1 com `!pip install`

### Erro: "MemoryError"
**Solução:** O dataset é grande. Se ocorrer erro de memória:
- Clique em "Ambiente de execução" → "Alterar tipo de ambiente"
- Selecione "GPU" para melhor performance

### Erro: Arquivo não carrega
**Solução:** Verifique:
1. O repositório é público?
2. O arquivo existe em `dados/datatran2025.xlsx`?
3. O link está correto?

---

## 📚 Estrutura do Notebook (14 Células)

| Célula | Tipo | Descrição |
|--------|------|-----------|
| 0 | Markdown | Cabeçalho e Objetivo |
| 1 | Markdown | Documentação Passo 1 |
| 2 | Código | **Carregamento de Dados (GitHub)** |
| 3 | Markdown | Documentação Passo 2 |
| 4 | Código | Pré-processamento |
| 5 | Markdown | Documentação Passo 3 |
| 6 | Código | Agregação Semanal |
| 7 | Markdown | Documentação Passo 4 |
| 8 | Código | Criação de Sequências |
| 9 | Markdown | Documentação Passo 5 |
| 10 | Código | Construção e Treinamento |
| 11 | Markdown | Documentação Passo 6 |
| 12 | Código | Avaliação e Salvamento |
| 13 | Markdown | Conclusão e Próximos Passos |

---

## 🎯 Resultado Esperado

Após a execução completa:
- **MAE:** ~0.22 (22% de erro médio)
- **Modelo salvo:** `modelo_lstm_acidentes_sp.keras`
- **Gráficos:** 4 gráficos de avaliação
- **Dados:** Processados de 47k registros para séries temporais

---

**Desenvolvido com ❤️ pela equipe Big 5**

Para dúvidas, consulte o `README.md` ou `CONFIGURACAO_GITHUB.md`
