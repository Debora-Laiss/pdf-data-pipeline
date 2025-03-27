# 📊 PDF Data Processing and Web Scraping

Este projeto contém dois scripts principais que realizam operações de **transformação de dados** e **web scraping** para manipulação de arquivos **PDF**.

---

## 📝 Descrição

### **1. Web Scraping (`webscraping.py`)**
Este script realiza o download de arquivos **PDF** de URLs específicas e extrai o conteúdo desses PDFs, salvando-o como texto em arquivos **.txt**. Os PDFs e os arquivos de texto são então compactados em um arquivo **ZIP**.

### **2. Data Transformation (`dataTransformation.py`)**
Este script processa arquivos **PDF**, extraindo tabelas de dados, realizando a transformação e limpeza dessas informações e, finalmente, salvando os dados em um arquivo **CSV**. Além disso, o script compacta os arquivos originais e o **CSV** em um arquivo **ZIP** para facilitar o armazenamento e a distribuição.

---

## ⚙️ Funcionalidades

### **Web Scraping**
- **📥 Download de PDFs**: O script baixa arquivos **PDF** de URLs fornecidas.
- **📖 Leitura de PDFs**: O conteúdo dos PDFs baixados é extraído e salvo em arquivos **.txt**.
- **📦 Compactação**: O script compacta os PDFs e os arquivos **.txt** em um arquivo **ZIP** para facilitar o compartilhamento.


### **Data Transformation**
- **🔍 Listar PDFs**: O script verifica um diretório local para arquivos **PDF**.
- **📄 Extrair Dados de Tabelas**: Utilizando a biblioteca `pdfplumber`, as tabelas dos PDFs são extraídas e transformadas.
- **🔧 Processamento de Dados**: O script limpa e organiza os dados extraídos, substituindo abreviações, e converte os dados em um **DataFrame** do **pandas**.
- **💾 Salvar Dados**: Os dados processados são salvos em um arquivo **CSV**.
- **📦 Compactação**: O **CSV** e os arquivos **PDF** originais são compactados em um arquivo **ZIP**.


---
