🇧🇷 **Português** | 🇺🇸 [English](README-eng.md)
<H1> Trabalho de Algoritmo de Busca - Sistema de Biblioteca (SB) 📚 </H1>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Concluido-green?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Busca-BST%20%2F%20Fuzzy-orange?style=flat-square" alt="Busca">
</p>

<p align="center">
  <img src="https://i.postimg.cc/YCsvxJLN/Captura-de-Tela-2026-04-04-a-s-02-39-39.png" width="500">
</p>

---

## 📝 Descrição

O ***Sistema de Biblioteca (SB)*** é uma aplicação em Python pensada para ser rápida e fácil de usar. Com uma interface moderna em modo escuro, ele foi projetado para que tudo aconteça de forma fluida, sem travamentos ou esperas desnecessárias.
Nessa nova versão, o sistema deixa de ser apenas um buscador simples e passa a funcionar como uma solução mais completa. Onde se baseia em três ideias principais: as **árvores binárias de busca**, que organizam os códigos dos livros e permitem encontrar registros de forma muito ágil; os ***índices invertidos**, que ajudam a localizar palavras-chave sem precisar percorrer toda a base; e a **busca aproximada***, que consegue entender o que o usuário quis dizer mesmo com erros de digitação ou nomes incompletos.
No fim, o sistema consegue lidar com grandes quantidades de livros sem perder desempenho, mantendo um equilíbrio entre eficiência técnica e uma experiência de uso simples e agradável no dia a dia.

## 💡 Diferenciais Técnicos

O grande destaque desta atualização é o Módulo de Busca Avançada, que utiliza diferentes estratégias dependendo da entrada do usuário:

- ***Árvore Binária de Busca (BST):*** Implementada do zero para buscas exatas por numeração e buscas por intervalo;
- ***Índice Invertido:*** Técnica utilizada por grandes buscadores, como Google para encontrar palavras-chave em títulos e autores instantaneamente, sem percorrer a lista inteira; e
- ***Busca Fuzzy (Levenshtein):*** Algoritmo de similaridade de strings que encontra resultados mesmo se o usuário digitar o nome do livro com erros ortográficos.

## 🎯 Funcionalidades

- ***Gestão de Acervo:*** Cadastro detalhado de livros, com título, autor, gênero e estoque com indexação automática para buscas instantâneas;
- ***Registro de Alunos:*** Controle centralizado de usuários, armazenando matrículas e dados de contato de forma segura;
- ***Edição Dinâmica:*** Permite alterar informações de livros e alunos já cadastrados, mantendo a base de dados sempre atualizada;
- ***Controle de Empréstimos:*** Registro ágil de saídas, associando o aluno ao livro e documentando a data de retirada;
- ***Gestão de Devoluções:*** Baixa automática de empréstimos com atualização imediata da disponibilidade no acervo; e
- ***Consultas e Listagens:*** Visualização organizada de todos os dados cadastrados, facilitando a auditoria de alunos, livros e movimentações.

---

## 💻 Pré-requisitos

Antes de executar o programa, certifique-se de que você possui os seguintes requisitos instalados:

**1. Python 3.10 ou superior.**

**2. Dependências:**

- PySide6;
- qdarktheme; e
- rapidfuzz.

**3.Sistema Operacional: Windows, macOS ou Linux.**

 ---

## 🚀 Executando

**1. Instalar o python**

Verifique se você possui o **Python 3.10 ou superior** instalado em seu sistema. Para isso, siga as instruções abaixo:

Abra o Terminal (no Windows, você pode abrir o Prompt de Comando ou PowerShell).

Digite o seguinte comando para verificar a versão do Python:

```bash
python --version
```

**Ou**

```bash
python3 --version
```

Se não tiver o Python 3.10, você pode baixá-lo [aqui](https://www.python.org/downloads/).

**2. Clonar o Repositório**

Primeiro, clone o repositório do projeto para a sua máquina. Para isso, abra o terminal (ou prompt de comando no Windows) e execute o comando abaixo:

```bash
git clone https://github.com/eda2-2026/G41_Busca_EDA2-2026.1.git
```

**3. Instale as dependências:**

No terminal, navegue até o diretório onde o projeto foi baixado e execute o seguinte comando para instalar todas as dependências:

```bash
pip install -r requirements.txt
```

Se o arquivo **requirements.txt** não existir, você pode instalar as dependências manualmente.
- **Instalar o Pyside6**

```bash
pip install pyside6 
```

* **Instalar o qdarktheme**

```bash
pip install qdarktheme
```

* **Instalar o rapidfuzz**

```bash
pip install rapidfuzz
```

**4. Executar o programa**

Com o ambiente configurado e as dependências instaladas, agora você pode rodar o sistema.

```bash
python biblioteca.py
```

Ou

```bash
python3 biblioteca.py
```

**⚠️ Observação:**
Caso o código apresente algum erro durante a execução, verifique se todos os arquivos necessários estão presentes (principalmente os arquivos .json no diretório db_files).

---

## 🫂 Colaboradores

| <span style="color:black;">[Camila Cavalcante - 232013944](https://github.com/CamilaSilvaC)</span> | <span style="color:black;">[Luísa Ferreira - 232014807](https://github.com/luisa12ll)</span> |
| :---: | :---: |
| <div align="center"><img src="https://github.com/CamilaSilvaC.png" alt="camila" width="400"></div> | <div align="center"><img src="https://github.com/luisa12ll.png" alt="luisa" width="400"></div> |
