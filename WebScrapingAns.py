import os
import zipfile
import pdfplumber
import pandas as pd
import logging

# Configurações de logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s: %(message)s')

class PDFProcessor:
    def __init__(self, download_dir='downloads'):
        self.download_dir = download_dir
        
        # Verificar se o diretório existe
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def listar_pdfs(self):
        """Lista todos os PDFs no diretório de downloads"""
        pdfs = [
            os.path.join(self.download_dir, arquivo) 
            for arquivo in os.listdir(self.download_dir) 
            if arquivo.lower().endswith('.pdf')
        ]
        return pdfs

    def extrair_dados_pdf(self, pdf_path):
        """Extrai dados de tabelas do PDF com tratamento robusto"""
        dados = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    tabela = page.extract_table()
                    if tabela:
                        # Remover linhas vazias e cabeçalhos
                        tabela = [linha for linha in tabela[1:] if any(linha)]
                        dados.extend(tabela)
            logging.info(f"Dados extraídos de {pdf_path}")
        except Exception as e:
            logging.error(f"Erro na extração de {pdf_path}: {e}")
        
        return dados

    def processar_dados(self, dados):
        """Processa e limpa os dados"""
        # Verificar se há dados para processar
        if not dados or len(dados) < 2:
            logging.error("Nenhum dado encontrado para processamento")
            return pd.DataFrame()

        # Usar a primeira linha como cabeçalho
        df = pd.DataFrame(dados[1:], columns=dados[0])
        
        # Substituir abreviações
        abreviacoes = {
            'OD': 'Odontológico',
            'AMB': 'Ambulatorial'
        }
        
        for coluna, desc in abreviacoes.items():
            if coluna in df.columns:
                df[coluna] = df[coluna].apply(
                    lambda x: desc if str(x).upper() == coluna.upper() else x
                )
        
        return df

    def executar(self):
        """Método principal de execução"""
        try:
            # Listar PDFs
            pdfs = self.listar_pdfs()
            
            if not pdfs:
                logging.error("Nenhum PDF encontrado no diretório!")
                return
            
            logging.info(f"PDFs encontrados: {pdfs}")
            
            # Consolidar dados de todos os PDFs
            dados_consolidados = []
            for pdf in pdfs:
                dados = self.extrair_dados_pdf(pdf)
                if dados:
                    # Se for o primeiro PDF, incluir o cabeçalho
                    if not dados_consolidados:
                        dados_consolidados = [dados[0]] + dados[1:]
                    else:
                        # Para PDFs subsequentes, adicionar apenas as linhas de dados
                        dados_consolidados.extend(dados[1:])
            
            # Processar dados
            df = self.processar_dados(dados_consolidados)
            
            # Verificar se o DataFrame não está vazio
            if df.empty:
                logging.error("Não foi possível processar os dados")
                return
            
            # Salvar CSV
            csv_path = os.path.join(self.download_dir, 'Teste_DeboraLais.csv')
            df.to_csv(csv_path, index=False, encoding='utf-8')
            logging.info(f"CSV salvo: {csv_path}")
            
            # Compactar arquivos
            zip_path = os.path.join(self.download_dir, 'Teste_DeboraLais.zip')
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for arquivo in pdfs + [csv_path]:
                    zipf.write(arquivo, os.path.basename(arquivo))
            
            logging.info(f"Arquivo ZIP criado: {zip_path}")
        
        except Exception as e:
            logging.error(f"Erro no processamento: {e}")

def main():
    processor = PDFProcessor()
    processor.executar()

if __name__ == "__main__":
    main()