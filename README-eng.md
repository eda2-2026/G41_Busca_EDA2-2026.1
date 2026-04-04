🇺🇸 **English** | [🇧🇷 Português](README.md)
<H1> Search Algorithm Project - Library System (LS) 📚 </H1>

<p align="center">
<img src="https://img.shields.io/badge/Status-Completed-green?style=flat-square" alt="Status">
<img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Search-BST%20%2F%20Fuzzy-orange?style=flat-square" alt="Search">
</p>

<p align="center">
<img src="https://i.postimg.cc/YCsvxJLN/Captura-de-Tela-2026-04-04-a-s-02-39-39.png" width="500">
</p>

---
## 📝 Description 
**The Library System (LS)** is a Python application designed to be fast and user-friendly. Featuring a modern dark mode interface, it was engineered to ensure a fluid experience without lags or unnecessary wait times.
In this new version, the system evolves from a simple search tool into a comprehensive solution. It is built upon three core concepts: **Binary Search Trees (BST)**, which organize book codes for agile record retrieval; **Inverted Indexes**, which help locate keywords without scanning the entire database; and **Fuzzy Search**, which understands user intent even with typos or incomplete names.
Ultimately, the system handles large volumes of books without losing performance, maintaining a balance between technical efficiency and a simple, pleasant daily user experience.

## 💡 Technical Highlights
The main feature of this update is the Advanced Search Module, which employs different strategies based on user input:
- **Binary Search Tree (BST):** Implemented from scratch for exact numerical searches and range queries;
- **Inverted Index:** A technique used by major search engines like Google to find keywords in titles and authors instantaneously, without traversing the entire list;
- **Fuzzy Search (Levenshtein):** A string similarity algorithm that finds results even if the user misspells the book title.

## 🎯 Features
- **Collection Management:** Detailed book registration including title, author, genre, and stock with automatic indexing for instant searches;
- **Student Records:** Centralized user control, storing IDs and contact data securely;
- **Dynamic Editing:** Allows updating information for books and students already in the system, keeping the database current;
- **Loan Management:** Agile checkout process, linking students to books and documenting withdrawal dates;
- **Returns Management:** Automatic processing of returns with immediate updates to collection availability;
- **Queries and Reports:** Organized visualization of all registered data, facilitating audits of students, books, and transactions.

---

## 💻 Prerequisites
Before running the program, ensure you have the following requirements installed:

**1. Python 3.10 or higher..**

**2. Dependencies:**
  * PySide6;
  * qdarktheme;
  * rapidfuzz.

**3.Operating System: Windows, macOS, or Linux**

 ---
 
## 🚀 Running the Project
**1. Instalar o python**

Check if you have Python 3.10 or higher installed. To do this, follow these steps:

Open the Terminal (on Windows, use Command Prompt or PowerShell).

Type the following command to check the version:

```bash
python --version
```
**Or**

```bash
python3 --version
```
If you don't have Python 3.10, you can download it [here](https://www.python.org/downloads/).

**2. Clone the Repository**

First, clone the project repository to your machine. Open the terminal and run:

```bash
git clone https://github.com/eda2-2026/G41_Busca_EDA2-2026.1.git
```
**3. Install Dependencies:**

Navigate to the project directory in the terminal and run the following command to install all dependencies:

```bash
pip install -r requirements.txt
```
If the **requirements.txt** file is not present, you can install the dependencies manually:* **Install Pyside6**

```bash
pip install pyside6 
```
* **Install qdarktheme**

```bash
pip install qdarktheme
```
* **Install rapidfuzz**

```bash
pip install rapidfuzz
```

**4. Run the Program**

With the environment configured and dependencies installed, you can now run the system:

```bash
python biblioteca.py
```
**Or**

```bash
python3 biblioteca.py
```
**⚠️ Note:**
If the code presents any error during execution, verify if all necessary files are present (especially the .json files in the db_files directory).

---
## 🫂 Contributors:

| <span style="color:black;">[Camila Cavalcante](https://github.com/CamilaSilvaC)</span> | <span style="color:black;">[Luísa Ferreira](https://github.com/luisa12ll)</span> |
| :---: | :---: |
| <div align="center"><img src="https://github.com/CamilaSilvaC.png" alt="camila" width="400"></div> | <div align="center"><img src="https://github.com/luisa12ll.png" alt="luisa" width="400"></div> |


