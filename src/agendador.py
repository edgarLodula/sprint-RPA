from apscheduler.schedulers.blocking import BlockingScheduler
from src.sensor_simulator import gera_leitura_sensor
from src.database import insere_leitura
from src.login import get_logger

log = get_logger("agendador")
sched = BlockingScheduler()

MOTORES = [
    "WEG-W22-63-II_polos-0.12kw",
    "WEG-W22-80-II_polos-0.55kw",
    "WEG-W22-112M-IV_polos-3.0kw"
]

@sched.scheduled_job("interval", seconds=10, id="coleta_sensores")
def coleta_periodica():
    for mid in MOTORES:
        leitura = gera_leitura_sensor(mid)
        insere_leitura(leitura)
        log.info("Leitura registrada | motor=%s | temp=%.1f°C | rpm=%d",
                 mid, leitura["temperatura_c"], leitura["rpm"])

if __name__ == "__main__":
    log.info("Agendador iniciado — coletando a cada 10s")
    sched.start()