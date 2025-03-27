import os
import zipfile
import pdfplumber
import pandas as pd
import logging
import traceback

#TESTE DE TRANSFORMAÇÃO DE DADOS

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
        return sorted(pdfs)  # Garantir ordem consistente

    def extrair_dados_pdf(self, pdf_path):
        """
        Extrai dados de tabelas do PDF com tratamento robusto
        Tenta múltiplas estratégias de extração
        """
        dados = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                logging.info(f"Processando PDF: {pdf_path}")
                logging.info(f"Número total de páginas: {len(pdf.pages)}")

                # Tentar extrair dados de todas as páginas
                for page_num, page in enumerate(pdf.pages, 1):
                    logging.info(f"Processando página {page_num}")
                    
                    # Tentar extrair texto completo da página
                    texto_pagina = page.extract_text() or ""
                    logging.info(f"Texto da página: {texto_pagina[:200]}...")

                    # Extrair tabela
                    tabela = page.extract_table()
                    
                    if tabela:
                        logging.info(f"Tabela encontrada na página {page_num}")
                        # Filtrar linhas não vazias
                        tabela_limpa = [
                            linha for linha in tabela 
                            if linha and any(str(cel).strip() for cel in linha)
                        ]
                        
                        if tabela_limpa:
                            # Se ainda não temos dados, usar o cabeçalho da primeira tabela
                            if not dados:
                                dados = tabela_limpa
                            else:
                                # Adicionar linhas subsequentes, ignorando cabeçalhos
                                dados.extend(tabela_limpa[1:])
                    else:
                        logging.warning(f"Nenhuma tabela encontrada na página {page_num}")

                logging.info(f"Total de linhas extraídas: {len(dados)}")
        
        except Exception as e:
            logging.error(f"Erro detalhado na extração de {pdf_path}:")
            logging.error(traceback.format_exc())
        
        return dados

    def processar_dados(self, dados):
        """Processa e limpa os dados"""
        # Verificar se há dados para processar
        if not dados or len(dados) < 2:
            logging.error("Nenhum dado encontrado para processamento")
            logging.error(f"Dados recebidos: {dados}")
            return pd.DataFrame()

        try:
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
        
        except Exception as e:
            logging.error(f"Erro no processamento de dados: {e}")
            logging.error(traceback.format_exc())
            return pd.DataFrame()

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
                        dados_consolidados = dados
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
            logging.error(traceback.format_exc())

def main():
    processor = PDFProcessor()
    processor.executar()

if __name__ == "__main__":
    main()