# Configuração do GitHub para Sprint_4_LSTM_Grupo_BIG5

## ⚙️ Passos para Configurar o Notebook com Seu Repositório

### 1. Criar Repositório no GitHub

```bash
# Se ainda não criou o repositório:
# Acesse: https://github.com/new
# Nome: fiap-sprint4-lstm
# Descrição: Sprint Challenge 4 - LSTM para Previsão de Acidentes
# Selecione: Public
# Clique: Create repository
```

### 2. Clonar e Fazer Push do Projeto

```bash
# No seu computador/terminal:
cd C:\Users\Luis\Downloads\Development\lstm-acidentes-prf

# Inicializar git (se ainda não estiver)
git init
git add .
git commit -m "Sprint 4 LSTM - Previsão de Acidentes com Dados do GitHub"

# Adicionar repositório remoto (substitua pelo seu)
git remote add origin https://github.com/SEU_USUARIO/fiap-sprint4-lstm.git

# Fazer push
git branch -M main
git push -u origin main
```

### 3. Atualizar o Link no Notebook

No notebook `Sprint_4_LSTM_Grupo_BIG5.ipynb`, na **Célula 2**, atualize esta linha:

```python
github_raw_url = 'https://raw.githubusercontent.com/SEU_USUARIO/fiap-sprint4-lstm/main/dados/datatran2025.xlsx'
```

Substituindo:
- `SEU_USUARIO` → Seu username do GitHub
- `fiap-sprint4-lstm` → Nome do seu repositório

### 4. Verificar se o Link está Correto

1. Acesse seu repositório no GitHub
2. Navegue até: `dados/datatran2025.xlsx`
3. Clique em **"Raw"**
4. Copie a URL completa
5. Cole no notebook

**Formato esperado:**
```
https://raw.githubusercontent.com/seu_usuario/seu_repositorio/main/dados/datatran2025.xlsx
```

### 5. Testar no Google Colab

1. Abra: https://colab.research.google.com/
2. Clique em **Arquivo > Fazer upload do notebook**
3. Selecione `Sprint_4_LSTM_Grupo_BIG5.ipynb`
4. Execute a Célula 2 para verificar se os dados carregam corretamente do GitHub
5. Se tudo funcionar, execute o notebook completo

---

## 📋 Checklist Final

- [ ] Repositório criado no GitHub
- [ ] Arquivos foram feitos push
- [ ] Link do GitHub adicionado ao notebook
- [ ] Dados carregam corretamente no Colab
- [ ] Notebook executa sem erros

---

## 🔗 Links Úteis

- GitHub: https://github.com/
- Google Colab: https://colab.research.google.com/
- Git Docs: https://git-scm.com/doc

---

**Desenvolvido pela equipe Big 5**
