import pandas as pd
import threading
from apscheduler.schedulers.blocking import BlockingScheduler
from src.process_pdf import processa_pdf
from src.database import init_db, insere_motor, insere_leitura
from src.sensor_simulator import gera_leitura_sensor
from src.login import get_logger

log = get_logger("main")

MOTORES = [
    "WEG-W22-63-II_polos-0.12kw",
    "WEG-W22-80-II_polos-0.55kw",
    "WEG-W22-112M-IV_polos-3.0kw"
]

def inicia_agendador():
    sched = BlockingScheduler()

    @sched.scheduled_job("interval", seconds=10, id="coleta_sensores")
    def coleta_periodica():
        for mid in MOTORES:
            leitura = gera_leitura_sensor(mid)
            insere_leitura(leitura)
            log.info("Leitura | motor=%s | temp=%.1f°C | rpm=%d",
                     mid, leitura["temperatura_c"], leitura["rpm"])

    log.info("Agendador iniciado — coletando a cada 10s")
    sched.start()

def main():
    PATH = r"./data/pdf/sprint_data.pdf"

    log.info("Iniciando pipeline de ingestão")
    init_db()

    textos, df = processa_pdf(PATH)

    for _, row in df.iterrows():
        kw_str = f"{row['kw']}kw" if not pd.isna(row['kw']) else "desconhecido"
        dados = {
            "id": f"WEG-W22-{row['carcaca']}-{row['grupo_polos']}-{kw_str}",
            "cv": row["cv"],
            "kw": row["kw"],
            "carcaca": row["carcaca"],
            "rpm": row["rpm"],
            "massa_kg": row["massa_kg"]
        }
        insere_motor(dados)

    log.info(f"Pipeline concluído — {len(df)} registros inseridos")

    # Inicia agendador em thread separada para não bloquear
    t = threading.Thread(target=inicia_agendador, daemon=True)
    t.start()
    log.info("Pressione Ctrl+C para encerrar")
    t.join()

if __name__ == "__main__":
    main()