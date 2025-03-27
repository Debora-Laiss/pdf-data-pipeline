import os
import requests
import fitz 
import zipfile

#TESTE DE WEB SCRAPING

def baixar_arquivo(url, endereco):
    """Baixa um arquivo e salva localmente."""
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        
        os.makedirs(os.path.dirname(endereco), exist_ok=True)
        
        with open(endereco, 'wb') as novo_arquivo:
            novo_arquivo.write(resposta.content)
        
        print(f"✅ Download finalizado: {endereco}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao baixar {endereco}: {e}")

def ler_pdf(caminho_pdf):
    """Lê e retorna o texto de um arquivo PDF."""
    try:
        with fitz.open(caminho_pdf) as pdf:
            texto = "\n".join([pagina.get_text() for pagina in pdf])
        return texto
    except Exception as e:
        return f"Erro ao ler o PDF: {e}"

def main():
    # Links dos anexos PDF
    links = [
        'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf',
        'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf'
    ]
    
    OUTPUT_DIR = 'downloads'
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for i, url in enumerate(links, 1):
        nome_arquivo = os.path.join(OUTPUT_DIR, f'anexo_{i}.pdf')
        baixar_arquivo(url, nome_arquivo)

        # Lendo e exibindo o conteúdo do PDF
        conteudo = ler_pdf(nome_arquivo)
        txt_path = os.path.join(OUTPUT_DIR, f'anexo_{i}.txt')
        
        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(conteudo)
        
        print(f"📖 Texto salvo em: {txt_path}")

    # Compactar os arquivos PDF e TXT
    with zipfile.ZipFile(os.path.join(OUTPUT_DIR, 'anexos.zip'), 'w') as zipf:
        for i in range(1, len(links) + 1):
            zipf.write(os.path.join(OUTPUT_DIR, f'anexo_{i}.pdf'), arcname=f'anexo_{i}.pdf')
           

    print("📦 Todos os anexos pdf foram compactados em downloads/anexos.zip")

if __name__ == "__main__":
    main()
