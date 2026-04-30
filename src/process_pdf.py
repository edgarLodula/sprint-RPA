import pdfplumber
import fitz
import pandas as pd
import re

def tabela_pdf(PDF):
    with pdfplumber.open(PDF) as pdf:
        pagina = pdf.pages[5]
        tabelas = pagina.extract_tables()
    
    print("="*60)
    print("✅ Tabelas extraidas com sucesso")
    print(f"   Total de tabelas na página 6: {len(tabelas)}")
    print("="*60)
    return tabelas

def texto_pdf(PDF):
    doc = fitz.open(PDF)
    textos = {}
    for i, pagina in enumerate(doc):
        textos[f"pagina_{i+1}"] = pagina.get_text()
    doc.close()
    
    print("="*60)
    print("✅ Texto extraido com sucesso")
    print(f"   Total de páginas extraídas: {len(textos)}")
    print("="*60)
    return textos

def limpa_header(df):
    colunas = [
        "cv", "kw", "carcaca", "conjugado_nominal",
        "corrente_rotor_bloqueado", "conjugado_partida",
        "conjugado_maximo", "momento_inercia",
        "tempo_rotor_bloqueado", "massa_kg",
        "pressao_sonora_dba", "rpm",
        "rend_50", "rend_75", "rend_100",
        "fp_50", "fp_75", "fp_100",
        "corrente_220v", "corrente_440v"
    ]

    df.columns = colunas
    return df



def processa_pdf(PATH):
    textos = texto_pdf(PATH)
    tabelas = tabela_pdf(PATH)

    df=pd.DataFrame(tabelas)
    #df_header=limpa_header(df)
    #print(df)
    #print(df_header)
    print(len(df.columns))
    print(df.columns)
    
    return textos, tabelas

