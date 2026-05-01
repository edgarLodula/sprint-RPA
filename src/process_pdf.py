import pdfplumber
import fitz
import pandas as pd
import re

COLUNAS = [
    "cv_kw",          
    "carcaca", 
    "conjugado_nominal_kgfm",
    "corrente_rotor_bloqueado_ip_in", 
    "conjugado_partida_cp_cn",
    "conjugado_maximo_cmax_cn", 
    "momento_inercia_kgm2",
    "tempo_rotor_bloqueado_s", 
    "massa_kg",
    "pressao_sonora_dba", 
    "rpm",
    "rend_50", "rend_75", "rend_100",
    "fp_50", "fp_75", "fp_100",
    "corrente_220v", "corrente_440v"
]

GRUPOS = {
    1: "II_polos",
    2: "II_polos_opcional",
    3: "IV_polos",
    4: "IV_polos_opcional",
    5: "VI_polos"
}

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
    df.columns = COLUNAS
    return df



def processa_pdf(PATH):
    textos = texto_pdf(PATH)
    tabelas = tabela_pdf(PATH)

    frames = []
    for idx, grupo in GRUPOS.items():
        t = tabelas[idx]
        df = pd.DataFrame(t, columns=COLUNAS)
        df["grupo_polos"] = grupo
        frames.append(df)

    df_final = pd.concat(frames, ignore_index=True)

    # Separa cv_kw em duas colunas
    # Separa cv_kw em duas colunas
    df_final[["cv", "kw"]] = df_final["cv_kw"].str.extract(r"(\d+[,.]?\d*)\s+(\d+[,.]?\d*)")
    df_final["cv"] = pd.to_numeric(df_final["cv"].str.replace(",", "."), errors="coerce")
    df_final["kw"] = pd.to_numeric(df_final["kw"].str.replace(",", "."), errors="coerce")
    df_final = df_final.drop(columns=["cv_kw"])

    # Limpa células com múltiplos valores colados por \n
    for col in df_final.columns:
        df_final[col] = df_final[col].apply(
            lambda x: x.split("\n")[0] if isinstance(x, str) else x
        )

    # Converte vírgula → ponto e cast numérico
    for col in df_final.columns:
        if col != "carcaca" and col != "grupo_polos" and col != "cv_kw":
            df_final[col] = pd.to_numeric(
                df_final[col].astype(str).str.replace(",", "."),
                errors="coerce"
            )

    return textos, df_final
